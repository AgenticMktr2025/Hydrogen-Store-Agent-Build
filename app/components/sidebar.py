import reflex as rx
from app.states.main_state import MainState


def nav_item(label: str, href: str, icon: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(label),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-gray-100 px-3 py-2 text-gray-900 transition-all hover:text-gray-900",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("package-2", class_name="h-6 w-6"),
                    rx.el.span("Hydrogen Builder", class_name="sr-only"),
                    href="#",
                    class_name="flex items-center gap-2 font-semibold",
                ),
                class_name="flex h-[60px] items-center border-b px-6",
            ),
            rx.el.div(
                rx.el.nav(
                    nav_item(
                        "Brief", "/", "file-text", MainState.router.page.path == "/"
                    ),
                    nav_item(
                        "Specification",
                        "/specs",
                        "file-json-2",
                        MainState.router.page.path == "/specs",
                    ),
                    nav_item(
                        "Generated Files",
                        "/files",
                        "folder-git-2",
                        MainState.router.page.path == "/files",
                    ),
                    nav_item(
                        "Review & Deploy",
                        "/review",
                        "git-pull-request-draft",
                        MainState.router.page.path == "/review",
                    ),
                    nav_item(
                        "Settings",
                        "/settings",
                        "settings",
                        MainState.router.page.path == "/settings",
                    ),
                    class_name="grid items-start px-4 text-sm font-medium",
                ),
                class_name="flex-1 overflow-auto py-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Progress", class_name="text-sm font-semibold"),
                    rx.el.div(
                        rx.el.div(
                            class_name="bg-blue-500 h-2 rounded-full",
                            style={"width": f"{MainState.current_progress}%"},
                        ),
                        class_name="w-full bg-gray-200 rounded-full h-2 mt-2",
                    ),
                    rx.el.p(
                        MainState.progress_message,
                        class_name="text-xs text-gray-500 mt-1",
                    ),
                    class_name="p-4",
                ),
                class_name="mt-auto border-t",
            ),
        ),
        class_name="hidden border-r bg-gray-50/40 md:block w-72",
    )