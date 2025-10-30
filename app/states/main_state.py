import reflex as rx
import os
import json
import time
import logging
from typing import Any, TypedDict, cast
from openai import AsyncOpenAI
from pypdf import PdfReader
import io


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
    mistral_api_key: str = ""
    openrouter_api_key: str = ""
    openai_api_key: str = ""
    spec_json: dict[str, JsonValue] = {}
    file_plan: dict[str, JsonValue] = {}
    generated_files: dict[str, str] = {}
    is_generating_spec: bool = False
    is_generating_plan: bool = False
    is_generating_files: bool = False
    is_testing_mistral: bool = False
    is_testing_openrouter: bool = False
    is_testing_openai: bool = False
    current_progress: int = 0
    progress_message: str = "Awaiting brief submission."
    error_message: str = ""
    selected_file: str = ""
    selected_file_content: str = ""

    def _strip_markdown_code(self, content: str | None) -> str:
        """Strips markdown code fences from a string."""
        if not content:
            return ""
        content = content.strip()
        if content.startswith("") and content.endswith(""):
            lines = content.splitlines()
            if lines:
                start_index = 0
                for i, line in enumerate(lines):
                    if not line.strip().startswith(""):
                        start_index = i
                        break
                end_index = len(lines)
                for i in range(len(lines) - 1, -1, -1):
                    if not lines[i].strip().startswith(""):
                        end_index = i + 1
                        break
                return """
""".join(lines[start_index:end_index])
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
            api_key = os.environ.get("MISTRAL_API_KEY")
            base_url = "https://api.mistral.ai/v1"
            model = "mistral-tiny"
            if not api_key:
                api_key = os.environ.get("OPENROUTER_API_KEY")
                base_url = "https://openrouter.ai/api/v1"
                model = "mistralai/mistral-7b-instruct:free"
            if not api_key:
                api_key = os.environ.get("OPENAI_API_KEY")
                base_url = None
                model = "gpt-4o-mini"
            client = AsyncOpenAI(api_key=api_key, base_url=base_url)
            prompt = f"You are a Shopify Hydrogen expert. Convert the user's brief into a structured JSON object that strictly follows the provided schema. Fill in all fields.\n\nUSER BRIEF:\n{self.brief_text}\n\nBRAND GUIDELINES:\n{self.brand_guidelines}\n\nCRITICAL INSTRUCTIONS:\n1.  Return ONLY valid JSON.\n2.  You MUST include ALL fields from this schema template:\n    {json.dumps(full_schema, indent=2)}\n3.  Fill in values from the brief where provided.\n4.  For the `nav` field, create an array of objects, where each object has a `label` (the nav item name) and an `href` (a slugified, lowercase path, e.g., '/about-us').\n5.  Keep default values for fields not mentioned in the brief.\n6.  Ensure the JSON is complete, valid, and matches the full schema structure.\n\nReturn the complete JSON now:"
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Shopify Hydrogen expert specializing in creating structured JSON specs from natural language.",
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
                self.spec_json = json.loads(spec_string)
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
            api_key = os.environ.get("MISTRAL_API_KEY")
            base_url = "https://api.mistral.ai/v1"
            model = "mistral-tiny"
            if not api_key:
                api_key = os.environ.get("OPENROUTER_API_KEY")
                base_url = "https://openrouter.ai/api/v1"
                model = "mistralai/mistral-7b-instruct:free"
            if not api_key:
                api_key = os.environ.get("OPENAI_API_KEY")
                base_url = None
                model = "gpt-4o-mini"
            client = AsyncOpenAI(api_key=api_key, base_url=base_url)
            prompt = f"""You are a Shopify Hydrogen expert. Based on the provided Store Spec JSON, generate a file plan for a new Hydrogen project. The file plan should be a JSON object where keys are file paths and values are a brief description of the file's purpose (the 'intent').\n\nStore Spec:\n{self.spec_json_string}\n\nCRITICAL INSTRUCTIONS:\n1.  Return ONLY a valid JSON object representing the file plan.\n2.  Include all necessary files for a basic Hydrogen project: routes, components, styles, and configuration.\n3.  Create routes based on the `nav` and `catalog` sections of the spec.\n4.  Create components for header, footer, product cards, etc.\n5.  Structure the file paths correctly (e.g., `app/routes/_index.tsx`, `app/components/Header.tsx`).\n6.  The output must be a single JSON object with file paths as keys and string descriptions as values.\n\nExample Output Format:\n{{\n  "app/root.tsx": "React Router root, theme provider, and global layout.",\n  "app/routes/_index.tsx": "The home page component.",\n  "app/components/Header.tsx": "Site header with navigation derived from spec."\n}}\n\nGenerate the complete file plan now."""
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Shopify Hydrogen expert that generates file plans from JSON specifications.",
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
                self.file_plan = json.loads(file_plan_str)
                self.is_generating_plan = False
                self.current_progress = 75
                self.progress_message = "File plan generated."
                yield rx.toast.success("File plan generated successfully!")
                yield rx.redirect("/files")
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
            api_key = os.environ.get("MISTRAL_API_KEY")
            base_url = "https://api.mistral.ai/v1"
            model = "mistral-large-latest"
            if not api_key:
                api_key = os.environ.get("OPENROUTER_API_KEY")
                base_url = "https://openrouter.ai/api/v1"
                model = "deepseek/deepseek-chat"
            if not api_key:
                api_key = os.environ.get("OPENAI_API_KEY")
                base_url = None
                model = "gpt-4o-mini"
            client = AsyncOpenAI(api_key=api_key, base_url=base_url)
            file_items = list(self.file_plan.items())
            total_files = len(file_items)
            for i, (path, intent) in enumerate(file_items):
                async with self:
                    self.progress_message = (
                        f"Generating file {i + 1}/{total_files}: {path}"
                    )
                    self.current_progress = 75 + int(i / total_files * 25)
                prompt = f"You are an expert Shopify Hydrogen developer. Generate the full, production-ready code for the file at `{path}`.\n\nFile Intent: {intent}\n\nProject Specification:\n{self.spec_json_string}\n\nCRITICAL INSTRUCTIONS:\n1. Return ONLY the raw code for the file - no explanations, no markdown code fences, no extra text.\n2. Use modern TypeScript, React, and TailwindCSS.\n3. For route files (`app/routes/**/*.tsx`), you MUST export a `loader` function for data fetching and a `meta` function for SEO, even if they are empty.\n4. Use `@shopify/hydrogen-react` components like `Money` for prices and `Image` for media.\n5. Use the Storefront API client via `context.storefront.query()` inside loaders.\n6. Follow Remix conventions for routing and data loading.\n\nGenerate the raw code for `{path}` now - nothing else:"
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
                cleaned_code = self._strip_markdown_code(raw_code)
                if cleaned_code:
                    async with self:
                        self.generated_files[path] = cleaned_code
            async with self:
                self.is_generating_files = False
                self.current_progress = 100
                self.progress_message = "All files generated successfully."
                yield rx.toast.success("File generation complete!")
                if not self.selected_file and self.generated_files:
                    first_file = next(iter(self.generated_files.keys()), None)
                    if first_file:
                        self.view_file(first_file)
                yield rx.redirect("/files")
        except Exception as e:
            logging.exception(f"Error generating files: {e}")
            async with self:
                self.error_message = f"Failed to generate files: {e}"
                self.is_generating_files = False
                self.progress_message = "File generation failed."
                yield rx.toast.error(self.error_message)

    @rx.event(background=True)
    async def test_mistral_connection(self):
        """Test the connection to the Mistral API."""
        async with self:
            self.is_testing_mistral = True
            yield
        try:
            if not self.mistral_api_key:
                raise ValueError("Mistral API Key is not set.")
            client = AsyncOpenAI(
                api_key=self.mistral_api_key, base_url="https://api.mistral.ai/v1"
            )
            await client.models.list()
            yield rx.toast.success("Mistral connection successful!")
        except Exception as e:
            logging.exception(f"Mistral connection failed: {e}")
            yield rx.toast.error(f"Mistral Error: {e}")
        finally:
            async with self:
                self.is_testing_mistral = False

    @rx.event(background=True)
    async def test_openrouter_connection(self):
        """Test the connection to the OpenRouter API."""
        async with self:
            self.is_testing_openrouter = True
            yield
        try:
            if not self.openrouter_api_key:
                raise ValueError("OpenRouter API Key is not set.")
            client = AsyncOpenAI(
                api_key=self.openrouter_api_key, base_url="https://openrouter.ai/api/v1"
            )
            await client.models.list()
            yield rx.toast.success("OpenRouter connection successful!")
        except Exception as e:
            logging.exception(f"OpenRouter connection failed: {e}")
            yield rx.toast.error(f"OpenRouter Error: {e}")
        finally:
            async with self:
                self.is_testing_openrouter = False

    @rx.event(background=True)
    async def test_openai_connection(self):
        """Test the connection to the OpenAI API."""
        async with self:
            self.is_testing_openai = True
            yield
        try:
            if not self.openai_api_key:
                raise ValueError("OpenAI API Key is not set.")
            client = AsyncOpenAI(api_key=self.openai_api_key)
            await client.models.list()
            yield rx.toast.success("OpenAI connection successful!")
        except Exception as e:
            logging.exception(f"OpenAI connection failed: {e}")
            yield rx.toast.error(f"OpenAI Error: {e}")
        finally:
            async with self:
                self.is_testing_openai = False

    @rx.event
    def handle_brief_submit(self, form_data: dict[str, Any]):
        """Handle the submission of the brief form."""
        self.brief_text = form_data.get("brief_text", "")
        self.brand_guidelines = form_data.get("brand_guidelines", "")
        self.shopify_domain = form_data.get("shopify_domain", "")
        self.storefront_token = form_data.get("storefront_token", "")
        self.private_token = form_data.get("private_token", "")
        yield MainState.generate_specification