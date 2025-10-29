import reflex as rx
from app.states.main_state import MainState
from app.components.sidebar import sidebar


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Welcome to Hydrogen Builder", class_name="text-2xl font-bold"
                ),
                rx.el.p(
                    "Select a section from the sidebar to get started.",
                    class_name="text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center h-full text-center p-8",
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


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, route="/")
app.add_page(specs, route="/specs")