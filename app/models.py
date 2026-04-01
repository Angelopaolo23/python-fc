class Jugador:
    def __init__(self, nombre: str, edad: int, posicion: str, goles: int) -> None:
        self.nombre = nombre
        self.edad = edad
        self.posicion = posicion
        self.goles = goles
    
    def mostrar_info(self) -> str:
        return f"Nombre jugador: {self.nombre}\nEdad: {self.edad}\nPosicion: {self.posicion}\nGoles: {self.goles}"


class Capitan(Jugador):
    def __init__(self, nombre: str, edad: int, posicion: str, goles: int, liderazgo: int) -> None:
        super().__init__(nombre, edad, posicion, goles)
        self.liderazgo: int = liderazgo
    
    def mostrar_info(self):
        info_jugador = super().mostrar_info()
        return f"{info_jugador}\nLiderazgo: {self.liderazgo}"

