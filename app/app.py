import reflex as rx
from app.states.main_state import MainState
from app.components.sidebar import sidebar
from app.files import files


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
                        rx.el.div(
                            rx.upload.root(
                                rx.el.div(
                                    rx.icon(
                                        "cloud_upload",
                                        class_name="h-8 w-8 text-gray-400",
                                    ),
                                    rx.el.p(
                                        "Drag & drop a PDF or paste text below",
                                        class_name="text-sm text-gray-500",
                                    ),
                                    class_name="flex flex-col items-center justify-center p-4 border-2 border-dashed rounded-t-lg",
                                ),
                                id="guidelines_upload",
                                accept={"application/pdf": [".pdf"]},
                                multiple=False,
                                on_drop=MainState.handle_guidelines_upload(
                                    rx.upload_files(upload_id="guidelines_upload")
                                ),
                                class_name="w-full cursor-pointer bg-gray-50 hover:bg-gray-100",
                            ),
                            rx.el.textarea(
                                id="brand_guidelines",
                                name="brand_guidelines",
                                placeholder="Enter your brand colors, fonts, etc... or drop a PDF above",
                                default_value=MainState.brand_guidelines,
                                on_change=MainState.set_brand_guidelines,
                                class_name="w-full min-h-[100px] p-2 border border-t-0 rounded-b-md mt-0 focus:ring-0",
                            ),
                            class_name="mt-1",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Shopify Credentials",
                                class_name="text-lg font-semibold",
                            ),
                            rx.el.p(
                                "Optional. You can provide these later in the 'Review & Deploy' step.",
                                class_name="text-sm text-gray-500",
                            ),
                            class_name="mb-2",
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
                        rx.cond(
                            MainState.is_generating_spec,
                            rx.spinner(class_name="mr-2"),
                            None,
                        ),
                        rx.cond(
                            MainState.is_generating_spec,
                            "Generating...",
                            "Generate Specification",
                        ),
                        type="submit",
                        class_name="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center",
                        disabled=MainState.is_generating_spec,
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
                rx.el.div(
                    rx.el.a(
                        "< Back to Brief",
                        href="/",
                        class_name="text-gray-600 hover:text-gray-900",
                    ),
                    rx.el.button(
                        rx.cond(
                            MainState.is_generating_plan,
                            rx.spinner(class_name="mr-2"),
                            None,
                        ),
                        rx.cond(
                            MainState.is_generating_plan,
                            "Generating Plan...",
                            "Generate File Plan ->",
                        ),
                        on_click=MainState.generate_file_plan,
                        class_name="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center",
                        disabled=MainState.is_generating_plan,
                    ),
                    class_name="mt-6 flex justify-between items-center",
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
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3("Generated Files", class_name="font-semibold"),
                            rx.icon("folder-git-2", class_name="h-5 w-5 text-gray-500"),
                            class_name="flex items-center justify-between pb-2 border-b",
                        ),
                        rx.el.div(
                            rx.el.p("Total Files", class_name="text-sm text-gray-600"),
                            rx.el.p(
                                MainState.file_plan.keys().length().to_string(),
                                class_name="font-semibold text-lg",
                            ),
                            class_name="flex items-center justify-between pt-4",
                        ),
                        class_name="bg-white p-4 rounded-lg border shadow-sm",
                    ),
                    class_name="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mt-6",
                ),
                rx.el.div(
                    rx.el.a(
                        "< Back to Files",
                        href="/files",
                        class_name="text-gray-600 hover:text-gray-900",
                    ),
                    rx.el.button(
                        "Deploy to Oxygen",
                        class_name="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700",
                    ),
                    class_name="mt-6 flex justify-between items-center",
                ),
                class_name="p-8",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full bg-gray-50/50",
    )


def settings() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1("Settings", class_name="text-2xl font-bold"),
                rx.el.p(
                    "Manage your API keys and other settings.",
                    class_name="text-gray-500",
                ),
                rx.el.div(
                    rx.el.h3("API Keys", class_name="text-lg font-semibold mt-6 mb-2"),
                    rx.el.div(
                        rx.el.label("Mistral API Key", class_name="font-medium"),
                        rx.el.div(
                            rx.el.input(
                                placeholder="Enter your Mistral API Key",
                                name="mistral_api_key",
                                default_value=MainState.mistral_api_key,
                                on_change=MainState.set_mistral_api_key,
                                class_name="w-full p-2 border rounded-md",
                                type="password",
                            ),
                            rx.el.button(
                                rx.cond(
                                    MainState.is_testing_mistral,
                                    rx.spinner(class_name="h-4 w-4"),
                                    rx.icon("plug-zap", class_name="h-4 w-4"),
                                ),
                                on_click=MainState.test_mistral_connection,
                                disabled=MainState.is_testing_mistral,
                                class_name="px-4 py-2 border rounded-md bg-gray-50 hover:bg-gray-100",
                            ),
                            class_name="flex items-center gap-2 mt-1",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label("OpenRouter API Key", class_name="font-medium"),
                        rx.el.div(
                            rx.el.input(
                                placeholder="Enter your OpenRouter API Key",
                                name="openrouter_api_key",
                                default_value=MainState.openrouter_api_key,
                                on_change=MainState.set_openrouter_api_key,
                                class_name="w-full p-2 border rounded-md",
                                type="password",
                            ),
                            rx.el.button(
                                rx.cond(
                                    MainState.is_testing_openrouter,
                                    rx.spinner(class_name="h-4 w-4"),
                                    rx.icon("plug-zap", class_name="h-4 w-4"),
                                ),
                                on_click=MainState.test_openrouter_connection,
                                disabled=MainState.is_testing_openrouter,
                                class_name="px-4 py-2 border rounded-md bg-gray-50 hover:bg-gray-100",
                            ),
                            class_name="flex items-center gap-2 mt-1",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label("OpenAI API Key", class_name="font-medium"),
                        rx.el.div(
                            rx.el.input(
                                placeholder="Enter your OpenAI API Key",
                                name="openai_api_key",
                                default_value=MainState.openai_api_key,
                                on_change=MainState.set_openai_api_key,
                                class_name="w-full p-2 border rounded-md",
                                type="password",
                            ),
                            rx.el.button(
                                rx.cond(
                                    MainState.is_testing_openai,
                                    rx.spinner(class_name="h-4 w-4"),
                                    rx.icon("plug-zap", class_name="h-4 w-4"),
                                ),
                                on_click=MainState.test_openai_connection,
                                disabled=MainState.is_testing_openai,
                                class_name="px-4 py-2 border rounded-md bg-gray-50 hover:bg-gray-100",
                            ),
                            class_name="flex items-center gap-2 mt-1",
                        ),
                        class_name="mb-4",
                    ),
                    class_name="mt-6 bg-white p-6 rounded-lg border shadow-sm",
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
app.add_page(settings, route="/settings")