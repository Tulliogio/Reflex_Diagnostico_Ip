import reflex as rx
from rxconfig import config
from .componentes.encabezado.encabezado import header
from .componentes.pie.pie import footer
from .componentes.cuerpo.cuerpo import body

class State(rx.State):
    """The app state."""

def index():
    return rx.box(
        header(),
        body(),  # <<-- Aquí va el contenido principal
        footer(),
        width="100%",
        height="100vh",  # Ocupa toda la pantalla
        display="flex",
        flex_direction="column",  # Apila verticalmente
        background_color=rx.color("gray", 1),
    )

app = rx.App()
app.add_page(index)
app._compile()
