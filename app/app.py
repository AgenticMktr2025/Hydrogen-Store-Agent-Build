import reflex as rx
from app.states.main_state import MainState
from app.components.sidebar import sidebar


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Project Brief", class_name="text-2xl font-bold"),
                rx.el.p(
                    "Provide the details for your Shopify Hydrogen project.",
                    class_name="text-gray-500",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Project Brief",
                            html_for="brief_text",
                            class_name="font-semibold",
                        ),
                        rx.el.textarea(
                            id="brief_text",
                            name="brief_text",
                            placeholder="Describe your project requirements...",
                            default_value=MainState.brief_text,
                            class_name="w-full min-h-[150px] p-2 border rounded-md mt-1",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Brand Guidelines",
                            html_for="brand_guidelines",
                            class_name="font-semibold",
                        ),
                        rx.el.textarea(
                            id="brand_guidelines",
                            name="brand_guidelines",
                            placeholder="Enter your brand colors, fonts, etc...",
                            default_value=MainState.brand_guidelines,
                            class_name="w-full min-h-[100px] p-2 border rounded-md mt-1",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Shopify Credentials", class_name="text-lg font-semibold"
                        ),
                        rx.el.div(
                            rx.el.input(
                                placeholder="Shopify Domain (e.g., your-store.myshopify.com)",
                                name="shopify_domain",
                                default_value=MainState.shopify_domain,
                                class_name="w-full p-2 border rounded-md",
                            ),
                            rx.el.input(
                                placeholder="Storefront API Token",
                                name="storefront_token",
                                type="password",
                                default_value=MainState.storefront_token,
                                class_name="w-full p-2 border rounded-md",
                            ),
                            rx.el.input(
                                placeholder="Private Storefront API Token",
                                name="private_token",
                                type="password",
                                default_value=MainState.private_token,
                                class_name="w-full p-2 border rounded-md",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Generate Specification",
                        type="submit",
                        class_name="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700",
                    ),
                    on_submit=MainState.handle_brief_submit,
                    reset_on_submit=False,
                    class_name="mt-6",
                ),
                class_name="p-8",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50/50",
    )


def specs() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Specification", class_name="text-2xl font-bold"),
                rx.el.p(
                    "Review the generated project specification below.",
                    class_name="text-gray-500",
                ),
                rx.el.pre(
                    rx.el.code(MainState.spec_json_string, class_name="language-json"),
                    class_name="w-full bg-gray-100 p-4 rounded-lg mt-4 text-sm overflow-auto",
                ),
                class_name="p-8",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50/50",
    )


def files() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Generated Files", class_name="text-2xl font-bold"),
                rx.el.p(
                    "Browse the generated project files.", class_name="text-gray-500"
                ),
                class_name="p-8",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50/50",
    )


def review() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Review & Deploy", class_name="text-2xl font-bold"),
                rx.el.p(
                    "Review the changes and deploy to production.",
                    class_name="text-gray-500",
                ),
                class_name="p-8",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50/50",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, route="/")
app.add_page(specs, route="/specs")
app.add_page(files, route="/files")
app.add_page(review, route="/review")