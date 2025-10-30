import reflex as rx
import os
import json
import logging
import re
from typing import Any, TypedDict, cast, ForwardRef
from openai import AsyncOpenAI
from pypdf import PdfReader
import io
import anthropic
import mistralai
from mistralai.client import MistralClient as MistralAsyncClient


class TreeNode(TypedDict):
    name: str
    path: str
    type: str
    children: list["TreeNode"]


JsonValue = str | int | float | bool | list["JsonValue"] | dict[str, "JsonValue"]


class MainState(rx.State):
    """Manages the complete application state for the Hydrogen site builder."""

    brief_text: str = ""
    brand_guidelines: str = ""
    shopify_domain: str = ""
    storefront_token: str = ""
    private_token: str = ""
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    openrouter_api_key: str = ""
    mistralai_api_key: str = ""
    spec_json: dict[str, JsonValue] = {}
    file_plan: dict[str, JsonValue] = {}
    generated_files: dict[str, str] = {}
    is_generating_spec: bool = False
    is_generating_plan: bool = False
    is_generating_files: bool = False
    is_testing_openai: bool = False
    is_testing_anthropic: bool = False
    is_testing_openrouter: bool = False
    is_testing_mistralai: bool = False
    is_validating: bool = False
    is_fixing_files: bool = False
    files_being_fixed: set[str] = set()
    validation_results: dict[str, list[dict]] = {}
    current_progress: int = 0
    progress_message: str = "Awaiting brief submission."
    error_message: str = ""
    selected_file: str = ""
    selected_file_content: str = ""

    @rx.event(background=True)
    async def test_openai_connection(self):
        async with self:
            self.is_testing_openai = True
            yield
        try:
            if not self.openai_api_key:
                raise ValueError("OpenAI API Key is not set.")
            client = AsyncOpenAI(api_key=self.openai_api_key)
            await client.models.list()
            async with self:
                self.is_testing_openai = False
                yield rx.toast.success("OpenAI connection successful!")
        except Exception as e:
            logging.exception(f"OpenAI connection test failed: {e}")
            async with self:
                self.is_testing_openai = False
                yield rx.toast.error(f"OpenAI connection failed: {e}")

    @rx.event(background=True)
    async def test_anthropic_connection(self):
        async with self:
            self.is_testing_anthropic = True
            yield
        try:
            if not self.anthropic_api_key:
                raise ValueError("Anthropic API Key is not set.")
            client = anthropic.AsyncAnthropic(api_key=self.anthropic_api_key)
            await client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1,
                messages=[{"role": "user", "content": "test"}],
            )
            async with self:
                self.is_testing_anthropic = False
                yield rx.toast.success("Anthropic connection successful!")
        except Exception as e:
            logging.exception(f"Anthropic connection test failed: {e}")
            async with self:
                self.is_testing_anthropic = False
                yield rx.toast.error(f"Anthropic connection failed: {e}")

    @rx.event(background=True)
    async def test_openrouter_connection(self):
        async with self:
            self.is_testing_openrouter = True
            yield
        try:
            if not self.openrouter_api_key:
                raise ValueError("OpenRouter API Key is not set.")
            client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_api_key,
                default_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Hydrogen Builder",
                },
            )
            await client.chat.completions.create(
                model="openrouter/auto",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=20,
            )
            async with self:
                self.is_testing_openrouter = False
                yield rx.toast.success("OpenRouter connection successful!")
        except Exception as e:
            logging.exception(f"OpenRouter connection test failed: {e}")
            async with self:
                self.is_testing_openrouter = False
                yield rx.toast.error(f"OpenRouter connection failed: {e}")

    @rx.event(background=True)
    async def test_mistralai_connection(self):
        async with self:
            self.is_testing_mistralai = True
            yield
        try:
            if not self.mistralai_api_key:
                raise ValueError("MistralAI API Key is not set.")
            client = MistralAsyncClient(api_key=self.mistralai_api_key)
            await client.models.list()
            async with self:
                self.is_testing_mistralai = False
                yield rx.toast.success("MistralAI connection successful!")
        except Exception as e:
            logging.exception(f"MistralAI connection test failed: {e}")
            async with self:
                self.is_testing_mistralai = False
                yield rx.toast.error(f"MistralAI connection failed: {e}")

    @rx.var
    def validation_passed(self) -> bool:
        """Check if all files passed validation."""
        if not self.validation_results:
            return False
        return not any(self.validation_results.values())

    @rx.event(background=True)
    async def validate_all_files(self):
        """Validate all generated files for common issues."""
        from app.validation.validator import CodeValidator

        validator = CodeValidator()
        async with self:
            self.is_validating = True
            self.progress_message = "Validating generated files..."
            self.current_progress = 92
            self.validation_results = {}
            yield
        results = {}
        for path, content in self.generated_files.items():
            issues = validator.validate_file(path, content)
            if issues:
                results[path] = issues
        async with self:
            self.validation_results = results
            self.is_validating = False
            if not results:
                self.progress_message = "Validation passed!"
                yield rx.toast.success("All files passed validation.")
            else:
                self.progress_message = f"Validation failed for {len(results)} files."
                yield rx.toast.warning("Validation issues found.")

    def _strip_markdown_code(self, content: str | None) -> str:
        """Strips markdown code fences and extracts the first valid JSON object from a string."""
        if not content:
            return ""
        content = content.strip()
        match = re.search(
            "(?:json|typescript|javascript)?\\s*\\n(.*?)\\n", content, re.DOTALL
        )
        if match:
            extracted = match.group(1).strip()
            try:
                json.loads(extracted)
                return extracted
            except json.JSONDecodeError as e:
                logging.exception(
                    f"Failed to parse extracted content as JSON, falling back: {e}"
                )
        start = content.find("{")
        if start != -1:
            brace_count = 0
            in_string = False
            escape_next = False
            for i in range(start, len(content)):
                char = content[i]
                if escape_next:
                    escape_next = False
                    continue
                if char == "\\":
                    escape_next = True
                    continue
                if char == '"' and (not escape_next):
                    in_string = not in_string
                    continue
                if not in_string:
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            return content[start : i + 1].strip()
        return content

    @rx.var
    def spec_json_string(self) -> str:
        """The spec JSON as a formatted string."""
        return json.dumps(self.spec_json, indent=2) if self.spec_json else ""

    @rx.event
    async def handle_guidelines_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of a brand guidelines PDF."""
        if not files:
            return
        try:
            upload_data = await files[0].read()
            pdf_file = io.BytesIO(upload_data)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            self.brand_guidelines = text
            yield rx.toast.success("Brand guidelines extracted from PDF.")
        except Exception as e:
            logging.exception(f"Error parsing PDF: {e}")
            self.error_message = f"Failed to parse PDF: {e}"
            yield rx.toast.error(self.error_message)

    def _build_tree(self, path_list: list[str]) -> list[TreeNode]:
        tree_map: dict[str, TreeNode] = {}
        tree: list[TreeNode] = []
        for path in sorted(path_list):
            parts = path.split("/")
            for i in range(len(parts)):
                current_path = "/".join(parts[: i + 1])
                if current_path not in tree_map:
                    is_file = i == len(parts) - 1
                    node: TreeNode = {
                        "name": parts[i],
                        "path": path if is_file else current_path,
                        "type": "file" if is_file else "folder",
                        "children": [],
                    }
                    tree_map[current_path] = node
                    if i == 0:
                        tree.append(node)
                    else:
                        parent_path = "/".join(parts[:i])
                        if parent_path in tree_map:
                            tree_map[parent_path]["children"].append(node)
        return tree

    @rx.var
    def file_tree(self) -> list[TreeNode]:
        """The file plan as a tree structure for the file explorer."""
        if not self.file_plan:
            return []
        return self._build_tree(list(self.file_plan.keys()))

    @rx.event
    def view_file(self, path: str):
        """Sets the selected file for viewing."""
        self.selected_file = path
        self.selected_file_content = self.generated_files.get(
            path, "File content not found."
        )

    @rx.event
    def on_files_page_load(self):
        """Selects the first file when the files page loads."""
        if not self.selected_file and self.file_plan:
            first_file = next(iter(self.file_plan.keys()), None)
            if first_file:
                self.view_file(first_file)

    @rx.event(background=True)
    async def generate_specification(self):
        """Generate the project specification from the brief using an LLM."""
        async with self:
            if not self.brief_text:
                self.error_message = "Project brief cannot be empty."
                yield rx.toast.error(self.error_message)
                return
            self.is_generating_spec = True
            self.current_progress = 25
            self.progress_message = "Generating specification..."
            self.error_message = ""
            yield
        full_schema = {
            "store": {
                "domain": "your-store.myshopify.com",
                "storefrontApiVersion": "2025-07",
            },
            "brand": {
                "name": "",
                "logo": {"src": "brand/logo.svg", "alt": ""},
                "colors": {
                    "primary": "#1E2A39",
                    "accent": "#97E3FF",
                    "bg": "#FFFFFF",
                    "surface": "#F7F9FB",
                },
                "typography": {
                    "heading": {"font": "Inter", "weight": 700},
                    "body": {"font": "Inter", "weight": 400},
                },
            },
            "nav": [],
            "catalog": {
                "collections": ["all"],
                "pdp": {
                    "mediaGallery": True,
                    "badges": ["in_stock"],
                    "buybox": {"quantitySelector": True, "variantPicker": "dropdown"},
                },
                "search": {"provider": "storefront", "filters": ["price"]},
            },
            "i18n": {"locales": ["en"], "defaultLocale": "en"},
            "seo": {"titleTemplate": "%s | Store", "metaDescription": ""},
            "features": {"markets": False, "b2b": False, "subscriptions": False},
            "a11y": {"contrastMin": 4.5, "focusVisible": True},
            "analytics": {"lighthouseBudget": 85},
            "environments": {"preview": True, "production": True},
        }
        try:
            client, model = await self._get_client_and_model("spec")
            prompt = f"You are a Shopify Hydrogen expert. Convert the user's brief into a structured JSON object that strictly follows the provided schema. Fill in all fields.\n\nUSER BRIEF:\n{self.brief_text}\n\nBRAND GUIDELINES:\n{self.brand_guidelines}\n\nCRITICAL INSTRUCTIONS:\n1.  Return ONLY valid JSON.\n2.  You MUST include ALL fields from this schema template:\n    {json.dumps(full_schema, indent=2)}\n3.  Fill in values from the brief where provided.\n4.  For the `nav` field, create an array of objects, where each object has a `label` (the nav item name) and an `href` (a slugified, lowercase path, e.g., '/about-us').\n5.  Keep default values for fields not mentioned in the brief.\n6.  Ensure the JSON is complete, valid, and matches the full schema structure.\n\nReturn the complete JSON now:"
            spec_string = ""
            if isinstance(client, AsyncOpenAI):
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a Shopify Hydrogen expert specializing in creating structured JSON specs from natural language. You must respond with only a valid JSON object.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                spec_string = response.choices[0].message.content
            elif isinstance(client, anthropic.AsyncAnthropic):
                response = await client.messages.create(
                    model=model,
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a Shopify Hydrogen expert specializing in creating structured JSON specs from natural language. You must respond with only a valid JSON object.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.2,
                )
                spec_string = response.content[0].text
            elif isinstance(client, MistralAsyncClient):
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a Shopify Hydrogen expert specializing in creating structured JSON specs from natural language. You must respond with only a valid JSON object.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                )
                spec_string = response.choices[0].message.content
            async with self:
                if not spec_string:
                    raise ValueError("Received empty response from AI.")
                self.spec_json = json.loads(self._strip_markdown_code(spec_string))
                if self.shopify_domain:
                    self.spec_json.setdefault("store", {})["domain"] = (
                        self.shopify_domain
                    )
                self.is_generating_spec = False
                self.current_progress = 50
                self.progress_message = "Specification generated."
                yield rx.toast.success("Specification generated successfully!")
                yield rx.redirect("/specs")
        except Exception as e:
            logging.exception(f"Error generating specification: {e}")
            async with self:
                self.error_message = f"Failed to generate specification: {e}"
                self.is_generating_spec = False
                self.progress_message = "Specification generation failed."
                yield rx.toast.error(self.error_message)

    @rx.event(background=True)
    async def generate_file_plan(self):
        """Generate the file plan from the specification."""
        async with self:
            if not self.spec_json:
                self.error_message = "Specification must be generated first."
                yield rx.toast.error(self.error_message)
                return
            self.is_generating_plan = True
            self.current_progress = 50
            self.progress_message = "Generating file plan..."
            self.error_message = ""
        try:
            client, model = await self._get_client_and_model("plan")
            prompt = f"""You are a Shopify Hydrogen expert. Based on the provided Store Spec JSON, generate a file plan for a new Hydrogen project. The file plan should be a JSON object where keys are file paths and values are a brief description of the file's purpose (the 'intent').\n\nStore Spec:\n{self.spec_json_string}\n\nCRITICAL INSTRUCTIONS:\n1.  Return ONLY a valid JSON object representing the file plan.\n2.  Include all necessary files for a basic Hydrogen project: routes, components, styles, and configuration.\n3.  Create routes based on the `nav` and `catalog` sections of the spec.\n4.  Create components for header, footer, product cards, etc.\n5.  Structure the file paths correctly (e.g., `app/routes/_index.tsx`, `app/components/Header.tsx`).\n6.  The output must be a single JSON object with file paths as keys and string descriptions as values.\n\nExample Output Format:\n{{\n  "app/root.tsx": "React Router root, theme provider, and global layout.",\n  "app/routes/_index.tsx": "The home page component.",\n  "app/components/Header.tsx": "Site header with navigation derived from spec."\n}}\n\nGenerate the complete file plan now."""
            file_plan_str = ""
            if isinstance(client, AsyncOpenAI):
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a Shopify Hydrogen expert that generates file plans from JSON specifications. You must respond with only a valid JSON object.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                )
                file_plan_str = response.choices[0].message.content
            elif isinstance(client, anthropic.AsyncAnthropic):
                response = await client.messages.create(
                    model=model,
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a Shopify Hydrogen expert that generates file plans from JSON specifications. You must respond with only a valid JSON object.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,
                )
                file_plan_str = response.content[0].text
            elif isinstance(client, MistralAsyncClient):
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a Shopify Hydrogen expert that generates file plans from JSON specifications. You must respond with only a valid JSON object.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                )
                file_plan_str = response.choices[0].message.content
            async with self:
                if not file_plan_str:
                    raise ValueError("Received empty response from AI for file plan.")
                self.file_plan = json.loads(self._strip_markdown_code(file_plan_str))
                self.is_generating_plan = False
                self.current_progress = 75
                self.progress_message = "File plan generated. Now generating files..."
                yield rx.toast.success("File plan generated successfully!")
                yield MainState.generate_all_files
        except Exception as e:
            logging.exception(f"Error generating file plan: {e}")
            async with self:
                self.error_message = f"Failed to generate file plan: {e}"
                self.is_generating_plan = False
                self.progress_message = "File plan generation failed."
                yield rx.toast.error(self.error_message)

    @rx.event(background=True)
    async def generate_all_files(self):
        """Generate code for all files in the file plan."""
        async with self:
            if not self.file_plan:
                self.error_message = "File plan must be generated first."
                yield rx.toast.error(self.error_message)
                return
            self.is_generating_files = True
            self.progress_message = "Generating files..."
            self.generated_files = {}
        try:
            client, model = await self._get_client_and_model("code")
            file_items = list(self.file_plan.items())
            total_files = len(file_items)
            for i, (path, intent) in enumerate(file_items):
                async with self:
                    self.progress_message = (
                        f"Generating file {i + 1}/{total_files}: {path}"
                    )
                    self.current_progress = 75 + int(i / total_files * 25)
                prompt = f"You are an expert Shopify Hydrogen developer. Generate the full, production-ready code for the file at `{path}`.\n\nFile Intent: {intent}\n\nProject Specification:\n{self.spec_json_string}\n\nCRITICAL INSTRUCTIONS:\n1. Return ONLY the raw code for the file - no explanations, no markdown code fences, no extra text.\n2. Use modern TypeScript, React, and TailwindCSS.\n3. For route files (`app/routes/**/*.tsx`), you MUST export a `loader` function for data fetching and a `meta` function for SEO, even if they are empty.\n4. Use `@shopify/hydrogen-react` components like `Money` for prices and `Image` for media.\n5. Use the Storefront API client via `context.storefront.query()` inside loaders.\n6. Follow Remix conventions for routing and data loading.\n\nGenerate the raw code for `{path}` now - nothing else:"
                raw_code = ""
                if isinstance(client, AsyncOpenAI):
                    response = await client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You generate raw TypeScript/React code files for Shopify Hydrogen. You return ONLY code, no markdown or explanations.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.1,
                    )
                    raw_code = response.choices[0].message.content
                elif isinstance(client, anthropic.AsyncAnthropic):
                    response = await client.messages.create(
                        model=model,
                        max_tokens=4096,
                        messages=[
                            {
                                "role": "system",
                                "content": "You generate raw TypeScript/React code files for Shopify Hydrogen. You return ONLY code, no markdown or explanations.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.1,
                    )
                    raw_code = response.content[0].text
                elif isinstance(client, MistralAsyncClient):
                    response = await client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You generate raw TypeScript/React code files for Shopify Hydrogen. You return ONLY code, no markdown or explanations.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.1,
                    )
                    raw_code = response.choices[0].message.content
                if raw_code:
                    async with self:
                        cleaned_code = self._strip_markdown_code(raw_code)
                        self.generated_files[path] = cleaned_code
            async with self:
                self.is_generating_files = False
                self.current_progress = 100
                self.progress_message = "All files generated successfully."
                yield rx.toast.success("File generation complete!")
                if not self.selected_file and self.generated_files:
                    first_file = next(iter(self.generated_files.keys()), None)
                    if first_file:
                        self.selected_file = first_file
                        self.selected_file_content = self.generated_files.get(
                            first_file, "File content not found."
                        )
                yield rx.redirect("/files")
        except Exception as e:
            logging.exception(f"Error generating files: {e}")
            async with self:
                self.error_message = f"Failed to generate files: {e}"
                self.is_generating_files = False
                self.progress_message = "File generation failed."
                yield rx.toast.error(self.error_message)

    async def _get_client_and_model(
        self, task: str
    ) -> tuple[AsyncOpenAI | anthropic.AsyncAnthropic | MistralAsyncClient, str]:
        """Gets the best available AI client and model, checking env vars."""
        openrouter_key = (
            os.getenv("OPENROUTER_API_KEY") or self.openrouter_api_key or None
        )
        mistral_key = os.getenv("MISTRALAI_API_KEY") or self.mistralai_api_key or None
        openai_key = os.getenv("OPENAI_API_KEY") or self.openai_api_key or None
        anthropic_key = os.getenv("ANTHROPIC_API_KEY") or self.anthropic_api_key or None
        if openrouter_key:
            try:
                logging.info("Attempting to use OpenRouter...")
                client = AsyncOpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=openrouter_key,
                    default_headers={
                        "HTTP-Referer": "http://localhost:3000",
                        "X-Title": "Hydrogen Builder",
                    },
                )
                model_to_test = (
                    "deepseek/deepseek-chat-v3.1:free"
                    if task in ("spec", "plan")
                    else "minimax/minimax-m2"
                )
                model = model_to_test
                await client.chat.completions.create(
                    model=model_to_test,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=20,
                )
                model = model_to_test
                logging.info(
                    f"Successfully connected to OpenRouter. Using model: {model}"
                )
                return (client, model)
            except Exception as e:
                logging.exception(f"OpenRouter connection failed: {e}. Falling back.")
        if mistral_key:
            try:
                logging.info("Attempting to use MistralAI...")
                client = MistralAsyncClient(api_key=mistral_key)
                await client.models.list()
                model = (
                    "mistral-small-latest"
                    if task in ("spec", "plan")
                    else "open-devstral-small-1-1-25-07"
                )
                logging.info(
                    f"Successfully connected to MistralAI. Using model: {model}"
                )
                return (client, model)
            except Exception as e:
                logging.exception(f"MistralAI connection failed: {e}. Falling back.")
        if openai_key:
            try:
                logging.info("Attempting to use OpenAI...")
                client = AsyncOpenAI(api_key=openai_key)
                await client.models.list()
                model = "gpt-4o-mini"
                logging.info(f"Successfully connected to OpenAI. Using model: {model}")
                return (client, model)
            except Exception as e:
                logging.exception(f"OpenAI connection failed: {e}. Falling back.")
        if anthropic_key:
            try:
                logging.info("Attempting to use Anthropic...")
                client = anthropic.AsyncAnthropic(api_key=anthropic_key)
                model = (
                    "claude-haiku-4-5-20251001"
                    if task in ("spec", "plan")
                    else "claude-sonnet-4-5-20250929"
                )
                await client.messages.create(
                    model=model,
                    max_tokens=1,
                    messages=[{"role": "user", "content": "test"}],
                )
                logging.info(
                    f"Successfully connected to Anthropic. Using model: {model}"
                )
                return (client, model)
            except Exception as e:
                logging.exception(
                    f"Anthropic connection failed: {e}. No providers left."
                )
        raise ValueError(
            "No valid API key or connection available for any provider. Checked OpenRouter, Mistral, OpenAI, and Anthropic."
        )

    @rx.event
    def handle_brief_submit(self, form_data: dict[str, str]):
        """Handle the submission of the brief form."""
        self.brief_text = form_data.get("brief_text", "")
        self.brand_guidelines = form_data.get("brand_guidelines", "")
        self.shopify_domain = form_data.get("shopify_domain", "")
        self.storefront_token = form_data.get("storefront_token", "")
        self.private_token = form_data.get("private_token", "")
        yield MainState.generate_specification

    @rx.event(background=True)
    async def fix_file_issue(self, path: str, issue: dict):
        """Uses an LLM to fix a single validation issue in a file."""
        from app.validation.validator import CodeValidator

        async with self:
            self.files_being_fixed.add(path)
            yield
        try:
            client, model = await self._get_client_and_model("code")
            original_code = self.generated_files.get(path, "")
            if not original_code:
                raise ValueError("Original code not found.")
            prompt = f"You are an expert Shopify Hydrogen developer specializing in fixing code errors. Your task is to fix a specific issue in the provided file. Only return the corrected code, without any explanations or markdown fences.\n\nFile Path: {path}\n\nIssue to Fix:\nLine {issue['line']}: {issue['message']}\n\nOriginal Code:\ntypescript\n{original_code}\n\n\nCRITICAL INSTRUCTIONS:\n1.  Address ONLY the specified issue. Do not refactor or change other parts of the code.\n2.  Return ONLY the complete, corrected code for the entire file.\n3.  Do NOT include any markdown fences () or explanatory text in your response.\n\nReturn the full, corrected code now:"
            fixed_code = ""
            if isinstance(client, AsyncOpenAI):
                response = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )
                fixed_code = response.choices[0].message.content
            elif isinstance(client, anthropic.AsyncAnthropic):
                response = await client.messages.create(
                    model=model,
                    max_tokens=4096,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )
                fixed_code = response.content[0].text
            elif isinstance(client, MistralAsyncClient):
                response = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )
                fixed_code = response.choices[0].message.content
            if not fixed_code:
                raise ValueError("LLM returned an empty response.")
            cleaned_fixed_code = self._strip_markdown_code(fixed_code)
            validator = CodeValidator()
            new_issues = validator.validate_file(path, cleaned_fixed_code)
            async with self:
                self.generated_files[path] = cleaned_fixed_code
                if path == self.selected_file:
                    self.selected_file_content = cleaned_fixed_code
                if not new_issues:
                    if path in self.validation_results:
                        del self.validation_results[path]
                    yield rx.toast.success(f"Fixed issues in {path}")
                else:
                    self.validation_results[path] = new_issues
                    yield rx.toast.warning(
                        f"Attempted to fix {path}, but issues remain."
                    )
        except Exception as e:
            logging.exception(f"Error fixing file {path}: {e}")
            async with self:
                yield rx.toast.error(f"Failed to fix {path}: {e}")
        finally:
            async with self:
                self.files_being_fixed.remove(path)