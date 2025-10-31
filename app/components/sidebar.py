import reflex as rx
from app.states.state import AppState

NAV_ITEMS = [
    {"name": "Dashboard", "icon": "layout-dashboard"},
    {"name": "New Project", "icon": "plus-square"},
    {"name": "Projects", "icon": "list-checks"},
    {"name": "Settings", "icon": "settings"},
]


def nav_item(item: dict) -> rx.Component:
    return rx.el.button(
        rx.icon(item["icon"], class_name="h-5 w-5"),
        rx.el.span(item["name"]),
        on_click=lambda: AppState.set_current_page(item["name"]),
        class_name=rx.cond(
            AppState.current_page == item["name"],
            "flex items-center gap-3 rounded-lg bg-gray-100 px-3 py-2 text-gray-900 transition-all hover:text-gray-900 w-full text-left",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 w-full text-left",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("store", class_name="h-6 w-6 text-blue-600"),
                rx.el.h2("Hydrogen Agent", class_name="text-xl font-bold"),
                class_name="flex items-center gap-2 p-4 border-b",
            ),
            rx.el.nav(
                rx.foreach(NAV_ITEMS, nav_item),
                class_name="flex flex-col gap-2 p-4 font-medium",
            ),
            class_name="flex-1 overflow-auto",
        ),
        class_name="hidden md:flex flex-col w-64 border-r bg-gray-50 h-screen",
    )