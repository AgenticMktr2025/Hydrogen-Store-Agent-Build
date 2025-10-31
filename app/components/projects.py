import reflex as rx
from app.states.state import AppState, Project


def project_card(project: Project) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(project["name"], class_name="font-semibold text-lg"),
            rx.el.div(
                project["status"],
                class_name="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 w-fit",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(
            project["description"], class_name="text-sm text-gray-600 mt-2 truncate"
        ),
        rx.el.p(
            f"Created: {project['created_at']}", class_name="text-xs text-gray-400 mt-4"
        ),
        on_click=lambda: AppState.view_project(project["id"]),
        class_name="p-4 border rounded-lg hover:shadow-md transition-shadow cursor-pointer bg-white",
    )


def projects_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Projects", class_name="text-3xl font-bold text-gray-800 mb-6"),
        rx.cond(
            AppState.projects.length() > 0,
            rx.el.div(
                rx.foreach(AppState.projects, project_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            rx.el.div(
                rx.el.p("No projects yet. Click 'New Project' to get started."),
                class_name="text-center text-gray-500 py-12 border-2 border-dashed rounded-lg",
            ),
        ),
        class_name="p-6",
    )