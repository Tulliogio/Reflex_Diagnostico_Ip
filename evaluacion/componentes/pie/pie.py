import reflex as rx

def footer() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text("© 2025 Mi Sitio Web. Todos los derechos reservados."),
            rx.unordered_list(
                rx.list_item(rx.link("Política de privacidad", href="#",class_name="pl-3 text-lg font-semibold text-blue-600")),
                rx.list_item(rx.link("Términos de uso", href="#",class_name="pl-3 text-lg font-semibold text-blue-600")),
                rx.list_item(rx.link("Contacto", href="#",class_name="pl-3 text-lg font-semibold text-blue-600")),
                list_style_type="none",
                class_name="flex space-x-4"
            ),
            class_name="flex justify-between items-center w-full px-6 py-4"
        ),
        class_name="w-full bg-zinc-200 text-sm",
        justify="center"
    )
