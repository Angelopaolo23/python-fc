from typing import Dict, Union, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.box import Box

from app.models import Jugador, Capitan

# Box personalizado: solo líneas verticales blancas entre columnas, sin bordes ni horizontales
SOLO_VERTICALES = Box(
    "    \n"  # top
    " │  \n"  # head
    "    \n"  # head_row
    " │  \n"  # mid
    "    \n"  # row
    "    \n"  # foot_row
    " │  \n"  # foot
    "    \n"  # bottom
)


console = Console()

# Cada lista interna es una COLUMNA (línea de formación), de portería hacia adelante.
FORMACION_433: list[list[str]] = [
    ["ARQ"],                              # columna 1: arquero
    ["DEF1", "DEF2", "DEF3", "DEF4"],    # columna 2: defensa
    ["MED1", "MED2", "MED3"],            # columna 3: mediocampista
    ["DEL1", "DEL2", "DEL3"],            # columna 4: delantero
]

# Número de filas = la columna más larga (defensa, con 4 jugadores)
MAX_FILAS: int = max(len(col) for col in FORMACION_433)


def _celda_jugador(pos: str, equipo: Dict[str, Union[Jugador, Capitan]]) -> Text:
    """
    Retorna un objeto Text de Rich para una posición dada.

    Text es el tipo de Rich que representa texto con estilo.
    Es más robusto que los f-strings con tags porque permite
    construir el texto programáticamente sin riesgo de tags mal cerrados.
    """
    if pos in equipo:
        jugador = equipo[pos]
        es_capitan = isinstance(jugador, Capitan)

        # El nombre se muestra completo (sin truncar) porque la tabla
        # maneja el ancho de columna automáticamente
        estilo = "bold yellow" if es_capitan else "bold white"
        sufijo = " ©" if es_capitan else ""   # símbolo de capitán

        texto = Text(f"{jugador.nombre}{sufijo}", style=estilo, justify="center")
    else:
        # Slot vacío: se muestra la posición en gris tenue
        texto = Text(pos, style="dim white", justify="center")

    return texto


def _construir_cancha(equipo: Dict[str, Union[Jugador, Capitan]]) -> Table:
    """
    Construye la tabla que representa la cancha en vista horizontal.

    Cada COLUMNA de la tabla es una línea de la formación (GK, DEF, MC, ATQ).
    Cada FILA es un slot dentro de esa línea.
    Se lee de izquierda a derecha: portería → ataque.

    El centrado vertical se logra calculando el offset de cada columna:
    offset = (MAX_FILAS - len(linea)) // 2
    Así GK (1 jugador) queda centrado en las 4 filas disponibles.

    El centrado horizontal lo maneja Rich automáticamente con justify='center'
    y expand=True en la tabla.
    """
    tabla = Table(
        show_header=False,
        show_edge=False,
        show_lines=False,
        padding=(1, 4),   # padding generoso para centrado horizontal
        expand=True,
        box=None,
    )

    # Columnas de formación intercaladas con separadores blancos
    for i in range(len(FORMACION_433)):
        tabla.add_column(justify="center", style="on dark_green", vertical="middle")
        if i < len(FORMACION_433) - 1:
            tabla.add_column(justify="center", width=1, style="on dark_green")

    SEPARADOR = Text("│", style="white", justify="center")
    LABELS = ["ARQ", "DEF", "MED", "DEL"]

    # Primera fila: etiquetas de línea alineadas con sus columnas
    fila_labels = []
    for j, label in enumerate(LABELS):
        fila_labels.append(Text(label, style="bold white", justify="center"))
        if j < len(LABELS) - 1:
            fila_labels.append(SEPARADOR)
    tabla.add_row(*fila_labels)

    # Offset por columna para centrado vertical de los jugadores
    offsets = [(MAX_FILAS - len(linea)) // 2 for linea in FORMACION_433]

    for i in range(MAX_FILAS):
        fila = []
        for j, linea in enumerate(FORMACION_433):
            player_index = i - offsets[j]
            if 0 <= player_index < len(linea):
                fila.append(_celda_jugador(linea[player_index], equipo))
            else:
                fila.append(Text("", justify="center"))
            if j < len(FORMACION_433) - 1:
                fila.append(SEPARADOR)
        tabla.add_row(*fila)

    return tabla


def _construir_ficha(jugador: Optional[Union[Jugador, Capitan]]) -> Panel:
    """
    Construye el panel lateral con la información del último jugador agregado.

    Retorna un Panel vacío si todavía no se ha agregado ningún jugador.
    """
    if jugador is None:
        contenido = Text("Agrega un jugador\npara ver su ficha.", style="dim white", justify="center")
        return Panel(contenido, title="Ficha", border_style="dim green", width=28)

    # Construimos el texto de la ficha línea por línea
    ficha = Text()
    ficha.append("Nombre:   ", style="dim white")
    ficha.append(f"{jugador.nombre}\n", style="bold white")

    ficha.append("Edad:     ", style="dim white")
    ficha.append(f"{jugador.edad} años\n", style="white")

    ficha.append("Posición: ", style="dim white")
    ficha.append(f"{jugador.posicion}\n", style="white")

    ficha.append("Goles:    ", style="dim white")
    ficha.append(f"{jugador.goles}\n", style="bold green")

    if isinstance(jugador, Capitan):
        ficha.append("Liderazgo:", style="dim white")
        ficha.append(f" {jugador.liderazgo}/10 ★\n", style="bold yellow")
        titulo = "[bold yellow]Capitán[/]"
    else:
        titulo = "Jugador"

    return Panel(ficha, title=titulo, border_style="green", width=28)


class CanchaRendererV2:
    """
    Renderer de segunda generación.

    A diferencia del CanchaRenderer v1 (template string), este construye
    el layout programáticamente usando los componentes de Rich:
    - Table para la formación (alineación automática)
    - Panel para los bordes y títulos
    - Columns para mostrar cancha y ficha lado a lado

    La interfaz pública es idéntica a v1: renderizar(equipo, ultimo_jugador)
    Esto significa que main.py no necesita ningún cambio al hacer el upgrade.
    """

    def __init__(self) -> None:
        self._ultimo_jugador: Optional[Union[Jugador, Capitan]] = None

    def renderizar(
        self,
        equipo: Dict[str, Union[Jugador, Capitan]],
        ultimo_jugador: Optional[Union[Jugador, Capitan]] = None,
    ) -> None:
        # Actualizamos la ficha solo si se pasa un jugador nuevo
        if ultimo_jugador is not None:
            self._ultimo_jugador = ultimo_jugador

        cancha_tabla = _construir_cancha(equipo)

        # Marco interno: sin título, solo el borde visual
        marco_interno = Panel(
            cancha_tabla,
            border_style="dim green",
            padding=(0, 1),
        )

        # Marco externo: nombre del equipo
        marco_externo = Panel(
            marco_interno,
            title="[bold green]⚽  Python FC[/]",
            border_style="green",
        )

        ficha_panel = _construir_ficha(self._ultimo_jugador)

        console.clear()
        console.print(Columns([marco_externo, ficha_panel], expand=False))
