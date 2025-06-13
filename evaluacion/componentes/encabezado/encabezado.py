import reflex as rx

def header() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.image(
                    src="./logos/network.webp",
                    class_name = "pl-3 h-10 w-auto object-cover",
                ),
                rx.text(
                    "Análisis de información de los ordenadores",
                    class_name="pl-3 text-lg font-semibold text-blue-600",
                ),
                class_name="items-center"
            ),    
            rx.flex(
                 rx.unordered_list(
                    rx.list_item(
                        rx.link(
                            "Ordenadores",
                            href="https://www.google.com",
                            class_name="pl-3 text-lg font-semibold text-blue-600"
                        )
                    ),
                    rx.list_item(
                        rx.link(
                            "Comunicaciones",
                            href="https://www.google.com",
                            class_name="pl-3 text-lg font-semibold text-blue-600"
                        )
                    ),
                     rx.list_item(
                        rx.link(
                            "Otros",
                            href="https://www.google.com",
                            class_name="pl-3 text-lg font-semibold text-blue-600"
                        )
                    ),
                    list_style_type="none",
                    width="100%",
                    class_name = "flex items-center space-x-3 pr-3"
                ),
                class_name="w-100",
            ),
            width="100%",
            justify="between",
            class_name = "items-center"
        ),
        width="100%",
        justify="between",
        class_name = "w-full h-20 bg-zinc-200",
    )
