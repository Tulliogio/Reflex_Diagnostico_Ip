import reflex as rx
from typing import TypedDict, List
from ..BBDD.db import MongoDBClient


class Port(TypedDict):
    protocol: str
    port: int
    state: str
    name: str
    product: str
    version: str
    extrainfo: str


class SelectState(rx.State):
    value: str = ""
    ip_list: List[str] = []
    doc_map: dict = {}

    @rx.event
    def load_data(self):
        """Carica i dati dal database MongoDB"""
        mongo_client = MongoDBClient()
        docs = mongo_client.get_all_docs()
        self.ip_list = [doc["ip"] for doc in docs]
        self.doc_map = {doc["ip"]: doc for doc in docs}
        if self.ip_list and not self.value:
            self.value = self.ip_list[0]

    @rx.event
    def change_value(self, value: str):
        """Cambia l'IP selezionato"""
        self.value = value

    @rx.var
    def current_doc(self) -> dict:
        """Restituisce il documento corrente basato sull'IP selezionato"""
        return self.doc_map.get(self.value, {})

    @rx.var
    def hostname(self) -> str:
        return self.current_doc.get("hostname", "N/A")

    @rx.var
    def mac(self) -> str:
        return self.current_doc.get("mac", "N/A")

    @rx.var
    def estado(self) -> str:
        return self.current_doc.get("state", "N/A")

    @rx.var
    def os(self) -> str:
        return self.current_doc.get("os", "N/A")

    @rx.var
    def ports(self) -> List[Port]:
        """Restituisce i primi 10 porte del dispositivo selezionato"""
        return self.current_doc.get("ports", [])[:10]


def create_info_card() -> rx.Component:
    """Crea la card con las informaciones del dispositivo"""
    return rx.box(
        rx.heading(
            "🔍 Información del Dispositivo",
            font_size="1.6rem",
            mb="1.5rem",
            color="#1A202C",
            font_weight="600"
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.cell(
                        "Campo", 
                        font_weight="bold", 
                        color="#2D3748",
                        background_color="#E2E8F0",
                        padding="1rem",
                        width="45%"
                    ),
                    rx.table.cell(
                        "Valor", 
                        font_weight="bold", 
                        color="#2D3748",
                        background_color="#E2E8F0",
                        padding="1rem",
                        width="55%"
                    ),
                )
            ),
            rx.table.body(
                rx.table.row(
                    rx.table.cell(
                        "📍 Dirección IP", 
                        font_weight="500", 
                        color="#4A5568",
                        padding="1rem",
                        border_bottom="1px solid #E2E8F0"
                    ),
                    rx.table.cell(
                        SelectState.value, 
                        color="#2D3748", 
                        font_weight="600",
                        padding="1rem",
                        border_bottom="1px solid #E2E8F0"
                    )
                ),
                rx.table.row(
                    rx.table.cell(
                        "🏠 Nombre de Host", 
                        font_weight="500", 
                        color="#4A5568",
                        padding="1rem",
                        border_bottom="1px solid #E2E8F0"
                    ),  
                    rx.table.cell(
                        SelectState.hostname, 
                        color="#2D3748", 
                        font_weight="600",
                        padding="1rem",
                        border_bottom="1px solid #E2E8F0"
                    )
                ),
                rx.table.row(
                    rx.table.cell(
                        "🔗 Dirección MAC", 
                        font_weight="500", 
                        color="#4A5568",
                        padding="1rem",
                        border_bottom="1px solid #E2E8F0"
                    ),
                    rx.table.cell(
                        SelectState.mac, 
                        color="#2D3748", 
                        font_weight="600",
                        padding="1rem",
                        border_bottom="1px solid #E2E8F0"
                    )
                ),
                rx.table.row(
                    rx.table.cell(
                        "⚡ Estado", 
                        font_weight="500", 
                        color="#4A5568",
                        padding="1rem",
                        border_bottom="1px solid #E2E8F0"
                    ),
                    rx.table.cell(
                        SelectState.estado, 
                        color="#2D3748", 
                        font_weight="600",
                        padding="1rem",
                        border_bottom="1px solid #E2E8F0"
                    )
                ),
                rx.table.row(
                    rx.table.cell(
                        "💻 Sistema Operativo", 
                        font_weight="500", 
                        color="#4A5568",
                        padding="1rem"
                    ),
                    rx.table.cell(
                        SelectState.os, 
                        color="#2D3748", 
                        font_weight="600",
                        padding="1rem"
                    )
                ),
            ),
            border="1px solid #E2E8F0",
            border_radius="8px",
            overflow="hidden",
            width="100%"
        ),
        padding="2rem",
        border_radius="12px",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        background_color="white",
        border="1px solid #E2E8F0",
        width="100%",
        min_width="450px",
    )


def create_ports_card() -> rx.Component:
    """Crea la card con la tabla de puertos"""
    return rx.box(
        rx.heading(
            "🌐 Puertos Abiertos",
            font_size="1.6rem",
            mb="1.5rem",
            color="#1A202C",
            font_weight="600"
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.cell("Protocolo", font_weight="bold", color="#2D3748", background_color="#E2E8F0", padding="0.75rem", min_width="80px", border_right="1px solid #CBD5E0"),
                        rx.table.cell("Puerto", font_weight="bold", color="#2D3748", background_color="#E2E8F0", padding="0.75rem", min_width="70px", border_right="1px solid #CBD5E0"),
                        rx.table.cell("Estado", font_weight="bold", color="#2D3748", background_color="#E2E8F0", padding="0.75rem", min_width="80px", border_right="1px solid #CBD5E0"),
                        rx.table.cell("Servicio", font_weight="bold", color="#2D3748", background_color="#E2E8F0", padding="0.75rem", min_width="100px", border_right="1px solid #CBD5E0"),
                        rx.table.cell("Producto", font_weight="bold", color="#2D3748", background_color="#E2E8F0", padding="0.75rem", min_width="120px", border_right="1px solid #CBD5E0"),
                        rx.table.cell("Versión", font_weight="bold", color="#2D3748", background_color="#E2E8F0", padding="0.75rem", min_width="100px", border_right="1px solid #CBD5E0"),
                        rx.table.cell("Info Extra", font_weight="bold", color="#2D3748", background_color="#E2E8F0", padding="0.75rem", min_width="150px"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        SelectState.ports,
                        lambda port: rx.table.row(
                            rx.table.cell(
                                port["protocol"], 
                                color="#4A5568", 
                                font_weight="500",
                                padding="0.75rem",
                                max_width="80px",
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap",
                                border_right="1px solid #E2E8F0",
                                border_bottom="1px solid #F1F5F9"
                            ),
                            rx.table.cell(
                                port["port"], 
                                color="#2B6CB0", 
                                font_weight="600",
                                padding="0.75rem",
                                max_width="70px",
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap",
                                border_right="1px solid #E2E8F0",
                                border_bottom="1px solid #F1F5F9"
                            ),
                            rx.table.cell(
                                rx.badge(
                                    port["state"],
                                    color_scheme=rx.cond(
                                        port["state"] == "open",
                                        "green",
                                        "red"
                                    ),
                                    size="1"
                                ),
                                padding="0.75rem",
                                max_width="80px",
                                border_right="1px solid #E2E8F0",
                                border_bottom="1px solid #F1F5F9"
                            ),
                            rx.table.cell(
                                port["name"], 
                                color="#4A5568",
                                padding="0.75rem",
                                max_width="100px",
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap",
                                title=port["name"],
                                border_right="1px solid #E2E8F0",
                                border_bottom="1px solid #F1F5F9"
                            ),
                            rx.table.cell(
                                port["product"], 
                                color="#4A5568",
                                padding="0.75rem",
                                max_width="120px",
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap",
                                title=port["product"],
                                border_right="1px solid #E2E8F0",
                                border_bottom="1px solid #F1F5F9"
                            ),
                            rx.table.cell(
                                port["version"], 
                                color="#4A5568",
                                padding="0.75rem",
                                max_width="100px",
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap",
                                title=port["version"],
                                border_right="1px solid #E2E8F0",
                                border_bottom="1px solid #F1F5F9"
                            ),
                            rx.table.cell(
                                port["extrainfo"], 
                                color="#4A5568",
                                padding="0.75rem",
                                max_width="150px",
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap",
                                title=port["extrainfo"],
                                border_bottom="1px solid #F1F5F9"
                            ),
                            _hover={"background_color": "#F7FAFC"}
                        )
                    )
                ),
                border="1px solid #E2E8F0",
                border_radius="8px",
                width="100%",
                table_layout="fixed"
            ),
            width="100%",
            height="400px",
            overflow_y="auto",
            overflow_x="hidden",
            border="1px solid #E2E8F0",
            border_radius="8px"
        ),
        padding="2rem",
        border_radius="12px",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        background_color="white",
        border="1px solid #E2E8F0",
        width="100%",
        flex="1",
        max_height="500px"
    )


def create_header() -> rx.Component:
    """Crea el header de la página"""
    return rx.box(
        rx.heading(
            "🛡️ Escáner de Seguridad de Red",
            font_size="2.5rem",
            color="#1A202C",
            font_weight="700",
            text_align="center",
            mb="2rem"
        ),
        rx.text(
            "Dashboard para el análisis y monitoreo de seguridad de red",
            font_size="1.1rem",
            color="#4A5568",
            text_align="center",
            mb="3rem"
        ),
        width="100%"
    )


def create_controls() -> rx.Component:
    """Crea los controles de la página"""
    return rx.hstack(
        rx.vstack(
            rx.text(
                "Acciones:",
                font_weight="600",
                color="#2D3748",
                text_align="center"
            ),
            rx.button(
                "🔄 Recargar Datos",
                on_click=SelectState.load_data,
                size="3",
                color_scheme="blue",
                font_weight="600",
                width="200px"
            ),
            spacing="2",
            align_items="center"
        ),
        rx.vstack(
            rx.text(
                "Seleccionar IP:", 
                font_weight="600", 
                color="#2D3748",
                text_align="center"
            ),
            rx.select(
                SelectState.ip_list,
                value=SelectState.value,
                on_change=SelectState.change_value,
                width="280px",
                size="3"
            ),
            spacing="2",
            align_items="center"
        ),
        rx.vstack(
            rx.text(
                "IP Activa:",
                font_weight="600",
                color="#2D3748",
                text_align="center"
            ),
            rx.badge(
                f"📡 {SelectState.value}",
                color_scheme="blue",
                size="3",
                padding="0.75rem 1rem",
                font_weight="600"
            ),
            spacing="2",
            align_items="center"
        ),
        justify="between",
        align_items="center",
        width="100%",
        mb="3rem",
        padding="2rem",
        background_color="white",
        border_radius="12px",
        box_shadow="0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        border="1px solid #E2E8F0"
    )


def render_main_content() -> rx.Component:
    """Renderiza el contenido principal"""
    return rx.container(
        rx.vstack(
            create_header(),
            create_controls(),
            rx.hstack(
                create_info_card(),
                create_ports_card(),
                spacing="4",
                width="100%",
                align_items="start"
            ),
            spacing="6",
            width="100%",
            align_items="center"
        ),
        max_width="1400px",
        padding="2rem"
    )


def body() -> rx.Component:
    """Componente body principale"""
    return rx.box(
        rx.cond(
            SelectState.doc_map == {},
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color="blue"),
                    rx.heading(
                        "Cargando Base de Datos...",
                        font_size="1.5rem",
                        color="#2D3748",
                        mt="2rem"
                    ),
                    rx.text(
                        "Conexión a MongoDB en curso",
                        color="#4A5568",
                        font_size="1.1rem"
                    ),
                    spacing="4",
                    align_items="center"
                ),
                height="100vh",
                background_color="#F7FAFC"
            ),
            render_main_content()
        ),
        min_height="100vh",
        background_color="#F7FAFC"
    )


def index():
    """Página principal de la aplicación"""
    return rx.page(
        body, 
        on_load=SelectState.load_data,
        title="Escáner de Seguridad de Red",
        description="Dashboard para análisis de seguridad de red"
    )