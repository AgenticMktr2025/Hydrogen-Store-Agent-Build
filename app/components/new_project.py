import reflex as rx
from app.states.state import AppState
from app.states.agent_state import AgentState, WorkflowStage


def _form_field(
    label: str, placeholder: str, name: str, field_type: str = "input"
) -> rx.Component:
    if field_type == "textarea":
        control = rx.el.textarea(
            name=name,
            placeholder=placeholder,
            class_name="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[120px]",
        )
    else:
        control = rx.el.input(
            name=name,
            placeholder=placeholder,
            class_name="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
        )
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        control,
        class_name="w-full",
    )


def new_project_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Create New Project", class_name="text-3xl font-bold text-gray-800 mb-6"
        ),
        rx.el.form(
            rx.el.div(
                _form_field(
                    "Project Name", "e.g., Acme Apparel Fall Collection", "project_name"
                ),
                _form_field(
                    "Store Description",
                    "A brief description of the store's purpose and target audience.",
                    "store_description",
                    field_type="textarea",
                ),
                _form_field(
                    "Brand Guidelines",
                    "Describe colors, typography, and overall brand voice.",
                    "brand_guidelines",
                    field_type="textarea",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Shopify Credentials",
                        class_name="text-lg font-semibold text-gray-800 mb-4",
                    ),
                    _form_field(
                        "Shopify Domain", "your-store.myshopify.com", "shopify_domain"
                    ),
                    _form_field(
                        "Storefront API Token",
                        "Enter your public storefront API token",
                        "shopify_token",
                    ),
                    class_name="space-y-4 p-4 border rounded-lg bg-gray-50",
                ),
                rx.el.button(
                    "Create Project and Extract Spec",
                    type="submit",
                    class_name="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium self-end",
                ),
                class_name="flex flex-col gap-6",
            ),
            on_submit=AppState.add_project_and_start_spec_extraction,
            reset_on_submit=True,
            class_name="w-full max-w-2xl mx-auto",
        ),
        class_name="p-6",
    )