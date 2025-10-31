import reflex as rx
from typing import TypedDict
import datetime


class Project(TypedDict):
    id: str
    name: str
    description: str
    brand_guidelines: str
    shopify_domain: str
    shopify_token: str
    spec_json: str
    status: str
    created_at: str


class AppState(rx.State):
    projects: list[Project] = []
    current_page: str = "Dashboard"
    current_project_id: str | None = None

    @rx.var
    def current_project(self) -> Project | None:
        if not self.current_project_id:
            return None
        for project in self.projects:
            if project["id"] == self.current_project_id:
                return project
        return None

    @rx.event
    def set_current_page(self, page_name: str):
        self.current_page = page_name
        self.current_project_id = None

    @rx.event
    def view_project(self, project_id: str):
        self.current_project_id = project_id
        self.current_page = "Project Details"

    @rx.event
    async def add_project_and_start_spec_extraction(self, form_data: dict):
        """Adds a new project and immediately triggers the spec extraction workflow."""
        import json
        from app.states.agent_state import AgentState

        project_id = f"proj_{len(self.projects) + 1}"
        spec = {
            "store": {
                "domain": form_data.get("shopify_domain", ""),
                "storefrontApiVersion": "2025-07",
            },
            "brand": {
                "name": form_data.get("project_name", ""),
                "logo": {
                    "src": "brand/logo.svg",
                    "alt": form_data.get("project_name", ""),
                },
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
            "nav": [
                {"label": "Home", "href": "/"},
                {"label": "Shop", "href": "/collections/all"},
                {"label": "About", "href": "/about"},
                {"label": "Contact", "href": "/contact"},
            ],
            "catalog": {
                "collections": ["all", "new", "sale"],
                "pdp": {
                    "mediaGallery": True,
                    "badges": ["in_stock", "low_stock", "sale"],
                    "buybox": {"quantitySelector": True, "variantPicker": "dropdown"},
                },
                "search": {
                    "provider": "storefront",
                    "filters": ["price", "vendor", "productType"],
                },
            },
            "i18n": {"locales": ["en"], "defaultLocale": "en"},
            "seo": {
                "titleTemplate": f"%s | {form_data.get('project_name', '')}",
                "metaDescription": form_data.get("store_description", ""),
            },
            "features": {"markets": False, "b2b": False, "subscriptions": False},
            "a11y": {"contrastMin": 4.5, "focusVisible": True},
            "analytics": {"lighthouseBudget": 85},
            "environments": {"preview": True, "production": True},
        }
        new_project = Project(
            id=project_id,
            name=form_data.get("project_name", ""),
            description=form_data.get("store_description", ""),
            brand_guidelines=form_data.get("brand_guidelines", ""),
            shopify_domain=form_data.get("shopify_domain", ""),
            shopify_token=form_data.get("shopify_token", ""),
            spec_json=json.dumps(spec, indent=2),
            status="Draft",
            created_at=datetime.datetime.now().isoformat(),
        )
        self.projects.append(new_project)
        self.current_project_id = project_id
        self.current_page = "Project Details"
        agent_state = await self.get_state(AgentState)
        yield agent_state.start_spec_extraction(project_id)

    @rx.event
    def add_project(self, form_data: dict):
        import json

        project_id = f"proj_{len(self.projects) + 1}"
        spec = {
            "store": {
                "domain": form_data.get("shopify_domain", ""),
                "storefrontApiVersion": "2025-07",
            },
            "brand": {
                "name": form_data.get("project_name", ""),
                "logo": {
                    "src": "brand/logo.svg",
                    "alt": form_data.get("project_name", ""),
                },
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
            "nav": [
                {"label": "Home", "href": "/"},
                {"label": "Shop", "href": "/collections/all"},
                {"label": "About", "href": "/about"},
                {"label": "Contact", "href": "/contact"},
            ],
            "catalog": {
                "collections": ["all", "new", "sale"],
                "pdp": {
                    "mediaGallery": True,
                    "badges": ["in_stock", "low_stock", "sale"],
                    "buybox": {"quantitySelector": True, "variantPicker": "dropdown"},
                },
                "search": {
                    "provider": "storefront",
                    "filters": ["price", "vendor", "productType"],
                },
            },
            "i18n": {"locales": ["en"], "defaultLocale": "en"},
            "seo": {
                "titleTemplate": f"%s | {form_data.get('project_name', '')}",
                "metaDescription": form_data.get("store_description", ""),
            },
            "features": {"markets": False, "b2b": False, "subscriptions": False},
            "a11y": {"contrastMin": 4.5, "focusVisible": True},
            "analytics": {"lighthouseBudget": 85},
            "environments": {"preview": True, "production": True},
        }
        new_project = Project(
            id=project_id,
            name=form_data.get("project_name", ""),
            description=form_data.get("store_description", ""),
            brand_guidelines=form_data.get("brand_guidelines", ""),
            shopify_domain=form_data.get("shopify_domain", ""),
            shopify_token=form_data.get("shopify_token", ""),
            spec_json=json.dumps(spec, indent=2),
            status="Draft",
            created_at=datetime.datetime.now().isoformat(),
        )
        self.projects.append(new_project)
        self.current_page = "Projects"