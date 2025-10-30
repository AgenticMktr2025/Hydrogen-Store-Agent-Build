import reflex as rx
from app.states.main_state import MainState
from app.components.sidebar import sidebar


def file_list_item(path: str) -> rx.Component:
    """A single file item in the flat list."""
    return rx.el.button(
        rx.icon("file-code", class_name="h-4 w-4 mr-2 flex-shrink-0"),
        rx.el.span(path, class_name="truncate"),
        on_click=MainState.view_file(path),
        class_name=rx.cond(
            MainState.selected_file == path,
            "flex items-center w-full text-left px-2 py-1.5 rounded-md bg-blue-100 text-blue-700 text-sm",
            "flex items-center w-full text-left px-2 py-1.5 rounded-md hover:bg-gray-100 text-sm",
        ),
        width="100%",
    )


def files() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Generated Files", class_name="text-2xl font-bold"),
                    rx.el.p(
                        "Browse the generated project files.",
                        class_name="text-gray-500 mb-4",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "< Back to Specification",
                            href="/specs",
                            class_name="text-gray-600 hover:text-gray-900",
                        ),
                        rx.el.button(
                            rx.cond(
                                MainState.is_generating_files,
                                rx.spinner(class_name="mr-2"),
                                None,
                            ),
                            rx.cond(
                                MainState.is_generating_files,
                                "Generating...",
                                "Regenerate Files",
                            ),
                            on_click=MainState.generate_all_files,
                            disabled=MainState.is_generating_files,
                            class_name="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 flex items-center",
                        ),
                        rx.el.a(
                            "Validate Files ->",
                            href="/validate",
                            class_name="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700",
                        ),
                        class_name="flex justify-between items-center w-full mb-6",
                    ),
                    class_name="border-b pb-4 mb-6",
                ),
                rx.cond(
                    MainState.file_plan.keys().length() > 0,
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Files",
                                class_name="font-semibold mb-2 text-gray-700 px-4",
                            ),
                            rx.el.div(
                                rx.foreach(MainState.file_plan.keys(), file_list_item),
                                class_name="space-y-1 p-2",
                            ),
                            class_name="w-80 p-2 bg-white border-r overflow-y-auto h-[calc(100vh-200px)] rounded-l-lg",
                        ),
                        rx.el.div(
                            rx.cond(
                                MainState.selected_file != "",
                                rx.el.div(
                                    rx.el.div(
                                        rx.icon("file-code", class_name="h-4 w-4 mr-2"),
                                        MainState.selected_file,
                                        class_name="flex items-center text-sm font-medium text-gray-700 mb-4 border-b pb-2",
                                    ),
                                    rx.el.pre(
                                        rx.el.code(
                                            MainState.selected_file_content,
                                            class_name="text-sm",
                                        ),
                                        class_name="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-auto h-[calc(100vh-280px)] font-mono text-sm",
                                    ),
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.icon(
                                            "file",
                                            class_name="h-12 w-12 text-gray-400 mb-4",
                                        ),
                                        rx.el.p(
                                            "Select a file to view its content",
                                            class_name="text-gray-500",
                                        ),
                                        class_name="flex flex-col items-center justify-center h-full",
                                    )
                                ),
                            ),
                            class_name="flex-1 p-4 bg-white rounded-r-lg",
                        ),
                        class_name="flex flex-1 overflow-hidden bg-gray-50 rounded-lg shadow-sm border",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "folder", class_name="h-16 w-16 text-gray-400 mb-4"
                            ),
                            rx.el.h3(
                                "No Files Generated Yet",
                                class_name="text-xl font-semibold text-gray-700 mb-2",
                            ),
                            rx.el.p(
                                "Generate a specification first, then create files to see them here.",
                                class_name="text-gray-500",
                            ),
                            class_name="flex flex-col items-center justify-center h-64",
                        ),
                        class_name="bg-white rounded-lg border-2 border-dashed border-gray-200",
                    ),
                ),
                class_name="p-8",
            ),
            class_name="flex-1",
            on_mount=MainState.on_files_page_load,
        ),
        class_name="flex min-h-screen w-full bg-gray-50/50",
    )