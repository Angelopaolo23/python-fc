from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm

from app.models import Jugador, Capitan
from app.exceptions import EquipoError
from app.validators import PlayerValidator
from app.repository import EquipoRepository
from app.renderer_v2 import CanchaRendererV2
from app.validators import POSICIONES_VALIDAS

console = Console()


def pedir_jugador() -> tuple:
    """Solicita los datos de un jugador y los retorna como tupla (esto porque el return devuelve los valores divididos por coma, eso los hace retornar como tupla)"""
    console.print("\n[bold cyan]--- Agregar Jugador ---[/]")
    nombre = Prompt.ask("Nombre del jugador")
    edad = IntPrompt.ask("Edad")
    posicion = Prompt.ask("Posicion", choices=POSICIONES_VALIDAS, case_sensitive=False).upper()
    goles = IntPrompt.ask("Goles")
    es_capitan = Confirm.ask("¿Es capitan?")

    if es_capitan:
        liderazgo = IntPrompt.ask("Liderazgo (1-10)")
        return nombre, edad, posicion, goles, True, liderazgo
    return nombre, edad, posicion, goles, False, None


def main() -> None:
    repo = EquipoRepository()
    renderer = CanchaRendererV2()

    console.print("[bold green]Bienvenido a Python FC[/]")
    renderer.renderizar(repo.obtener_equipo())

    while True:
        try:
            datos = pedir_jugador()
            nombre, edad, posicion, goles, es_capitan, liderazgo = datos

            if es_capitan:
                PlayerValidator.validar_capitan(nombre, edad, posicion, goles, liderazgo)
                jugador = Capitan(nombre, edad, posicion, goles, liderazgo)
            else:
                PlayerValidator.validar_jugador(nombre, edad, posicion, goles)
                jugador = Jugador(nombre, edad, posicion, goles)

            repo.agregar_jugador(jugador)
            renderer.renderizar(repo.obtener_equipo(), ultimo_jugador=jugador)
            console.print(f"[bold green]✓ {nombre} agregado en {posicion}[/]")

        except EquipoError as e:
            console.print(f"\n[bold red]Error de validacion:[/] {e}")
        except KeyboardInterrupt:
            console.print("\n\n[yellow]¡Hasta pronto, Python FC![/]")
            break


if __name__ == "__main__":
    main()