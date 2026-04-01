import json
from pathlib import Path
from typing import Dict, Union
from app.models import Jugador, Capitan


class EquipoRepository:
    def __init__(self, data_jugadores: str = "data/jugadores.json") -> None:
        self.path = Path(data_jugadores)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.equipo: Dict[str, Union[Jugador, Capitan]] = {}
        self.cargar_data()
    
    def guardar_data(self) -> None:
        data_serializada = {
            pos: {**obj.__dict__, "tipo": obj.__class__.__name__}
            for pos, obj in self.equipo.items()
        }
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data_serializada, f, indent=4, ensure_ascii=False)

    def cargar_data(self) -> None:
        if not self.path.exists():
            return
        if self.path.stat().st_size == 0:
            return

        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            for pos, datos in data.items():
                tipo = datos.pop("tipo")
                if tipo == "Capitan":
                    self.equipo[pos] = Capitan(**datos)
                else:
                    self.equipo[pos] = Jugador(**datos)
    
    def agregar_jugador(self, jugador: Union[Jugador, Capitan]) -> None:
        self.equipo[jugador.posicion] = jugador
        self.guardar_data()
    
    def obtener_equipo(self) -> Dict[str, Union[Jugador, Capitan]]:
        return self.equipo