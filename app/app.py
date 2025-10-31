import reflex as rx
from app.states.state import AppState
from app.states.agent_state import AgentState
from app.components.sidebar import sidebar
from app.components.dashboard import dashboard_page
from app.components.new_project import new_project_page
from app.components.projects import projects_page
from app.components.settings import settings_page
from app.components.project_details import project_details_page


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            sidebar(),
            rx.el.main(
                rx.match(
                    AppState.current_page,
                    ("Dashboard", dashboard_page()),
                    ("New Project", new_project_page()),
                    ("Projects", projects_page()),
                    ("Settings", settings_page()),
                    ("Project Details", project_details_page()),
                    dashboard_page(),
                ),
                class_name="flex-1 h-screen overflow-y-auto bg-gray-100",
            ),
            class_name="flex w-full h-screen",
        ),
        class_name="font-['Inter'] bg-white",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)