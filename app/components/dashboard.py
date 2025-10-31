import reflex as rx


def dashboard_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Welcome to Hydrogen Store Agent",
            class_name="text-3xl font-bold text-gray-800",
        ),
        rx.el.p(
            "Create, manage, and deploy Shopify Hydrogen storefronts with the power of AI.",
            class_name="text-gray-600 mt-2",
        ),
        class_name="p-6",
    )