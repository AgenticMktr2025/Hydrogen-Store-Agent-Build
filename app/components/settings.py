import reflex as rx


def settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Settings", class_name="text-3xl font-bold text-gray-800 mb-6"),
        rx.el.p(
            "Manage your API keys and preferences here.", class_name="text-gray-600"
        ),
        class_name="p-6",
    )