import reflex as rx
from app.states.state import AppState


def spec_viewer(spec_json: str) -> rx.Component:
    return rx.el.div(
        rx.el.h3("Store Specification (JSON)", class_name="font-semibold text-lg mb-2"),
        rx.el.pre(
            rx.el.code(spec_json, class_name="language-json"),
            class_name="bg-gray-800 text-white p-4 rounded-lg overflow-x-auto text-sm",
        ),
        class_name="mt-6",
    )


def project_details_page() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AppState.current_project,
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        AppState.current_project.get("name", ""),
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    rx.el.div(
                        AppState.current_project.get("status", ""),
                        class_name="px-3 py-1 text-sm font-medium rounded-full bg-blue-100 text-blue-800 w-fit",
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.p(
                    AppState.current_project.get("description", ""),
                    class_name="text-gray-600",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Brand Guidelines", class_name="font-semibold text-lg"
                        ),
                        rx.el.p(
                            AppState.current_project.get("brand_guidelines", ""),
                            class_name="text-sm text-gray-600 mt-1 whitespace-pre-wrap",
                        ),
                        class_name="p-4 bg-white border rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.h3("Shopify Info", class_name="font-semibold text-lg"),
                        rx.el.p(
                            f"Domain: {AppState.current_project.get('shopify_domain', '')}",
                            class_name="text-sm text-gray-600 mt-1",
                        ),
                        class_name="p-4 bg-white border rounded-lg",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6",
                ),
                spec_viewer(AppState.current_project.get("spec_json", "{}")),
                class_name="p-6",
            ),
            rx.el.div(
                rx.el.p("No project selected or found.", class_name="text-gray-500"),
                class_name="p-6 text-center",
            ),
        )
    )