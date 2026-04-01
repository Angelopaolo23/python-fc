from typing import Dict, Union
from rich.console import Console

from app.models import Jugador, Capitan

console = Console()

CANCHA_433: str = """
[bold white on green]
 _________________________________________________________________________
| ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , |
| ' . , ' . , ' . , ' . , ' .  __________  ' . , ' . , ' . , ' . , ' . , |
| ' . , ' . , ' . , ' . , ' . |  [GK]    | ' . , ' . , ' . , ' . , ' . , |
| ' . , ' . , ' . , ' . , ' . |__________| ' . , ' . , ' . , ' . , ' . , |
| ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , |
|  [DF1]           [DF2]                    [DF3]               [DF4]    |
| ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , |
| ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , |
|          [MC1]               [MC2]               [MC3]                 |
| ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , |
| ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , |
|  [DL1]                       [DL2]                        [DL3]        |
| ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , ' . , |
|_________________________________________________________________________|
[/bold white on green]
"""

POSICIONES: list[str] = [
    "GK", "DF1", "DF2", "DF3", "DF4",
    "MC1", "MC2", "MC3",
    "DL1", "DL2", "DL3"
]


class CanchaRenderer:

    def renderizar(self, equipo: Dict[str, Union[Jugador, Capitan]]) -> None:
        canvas: str = CANCHA_433

        for pos in POSICIONES:
            if pos in equipo:
                jugador = equipo[pos]
                color = "bold yellow" if isinstance(jugador, Capitan) else "bold white"
                tag = f"[{color}]{jugador.nombre[:7].center(7)}[/]"
            else:
                tag = f"[dim white]{pos.center(7)}[/]"

            canvas = canvas.replace(f"[{pos}]", tag)

        console.clear()
        console.print(canvas)