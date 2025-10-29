import reflex as rx
import os
import json
import time
import logging
from typing import Any, TypedDict, cast
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
    current_progress: int = 0
    progress_message: str = ""
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

    @rx.event
    def handle_brief_submit(self, form_data: dict[str, Any]):
        """Handle the submission of the brief form."""
        self.brief_text = form_data.get("brief_text", "")
        self.brand_guidelines = form_data.get("brand_guidelines", "")
        self.shopify_domain = form_data.get("shopify_domain", "")
        self.storefront_token = form_data.get("storefront_token", "")
        self.private_token = form_data.get("private_token", "")