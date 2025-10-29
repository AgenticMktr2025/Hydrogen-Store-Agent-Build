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
    spec_json: dict[str, JsonValue] = {}
    file_plan: dict[str, JsonValue] = {}
    generated_files: dict[str, str] = {}
    is_generating_spec: bool = False
    is_generating_plan: bool = False
    is_generating_files: bool = False
    current_progress: int = 25
    progress_message: str = "Brief waiting to be submitted."
    error_message: str = ""
    selected_file: str = ""
    selected_file_content: str = ""

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
        tree: list[TreeNode] = []
        for path in path_list:
            parts = path.split("/")
            current_level = tree
            for i, part in enumerate(parts):
                existing_node = next(
                    (node for node in current_level if node["name"] == part), None
                )
                is_file = i == len(parts) - 1
                if not existing_node:
                    new_node: TreeNode = {
                        "name": part,
                        "path": path if is_file else "/".join(parts[: i + 1]),
                        "type": "file" if is_file else "folder",
                        "children": [],
                    }
                    current_level.append(new_node)
                    if not is_file:
                        current_level = new_node["children"]
                elif not is_file:
                    current_level = existing_node["children"]
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
        try:
            client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            prompt = f"Extract details from this brief to create a Shopify Hydrogen store spec.\n\nBrief: {self.brief_text}\nGuidelines: {self.brand_guidelines}\nDomain: {self.shopify_domain}"
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Shopify Hydrogen expert. Convert the user's brief into a structured JSON object that strictly follows the provided schema. Fill in all fields.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            spec_string = response.choices[0].message.content
            async with self:
                if not spec_string:
                    raise ValueError("Received empty response from AI.")
                self.spec_json = json.loads(spec_string)
                if self.shopify_domain and "store" in self.spec_json:
                    self.spec_json["store"]["domain"] = self.shopify_domain
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

    @rx.event
    @rx.event(background=True)
    async def generate_file_plan(self):
        """Generate the file plan from the specification."""
        async with self:
            self.is_generating_plan = True
            self.current_progress = 50
            self.progress_message = "Generating file plan..."
            self.error_message = ""
        try:
            time.sleep(2)
            async with self:
                self.file_plan = {
                    "app/root.tsx": "React Router root; theme provider",
                    "app/routes/_index.tsx": "Home page component",
                    "app/routes/products.$handle.tsx": "Product detail page",
                    "app/components/Header.tsx": "Site header component",
                    "app/components/Footer.tsx": "Site footer component",
                    "app/styles/global.css": "Global CSS styles",
                }
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

    @rx.event
    def handle_brief_submit(self, form_data: dict[str, Any]):
        """Handle the submission of the brief form."""
        self.brief_text = form_data.get("brief_text", "")
        self.brand_guidelines = form_data.get("brand_guidelines", "")
        self.shopify_domain = form_data.get("shopify_domain", "")
        self.storefront_token = form_data.get("storefront_token", "")
        self.private_token = form_data.get("private_token", "")
        yield MainState.generate_specification