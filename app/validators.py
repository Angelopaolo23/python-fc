from app.exceptions import (
    GolesInvalidosError,
    EdadInvalidaError,
    PosicionInvalidaError,
    LargoNombreError
)

POSICIONES_VALIDAS: list[str] = [
    "ARQ",
    "DEF1", "DEF2", "DEF3", "DEF4",
    "MED1", "MED2", "MED3",
    "DEL1", "DEL2", "DEL3",
]

MIN_NOMBRE: int = 2
MAX_NOMBRE: int = 25


class PlayerValidator:
    @staticmethod
    def validar_nombre(nombre: str) -> None: 
        largo = len(nombre.strip())
        if largo < MIN_NOMBRE or largo > MAX_NOMBRE:
            raise LargoNombreError(
                    f"El nombre debe tener entre {MIN_NOMBRE} y {MAX_NOMBRE} caracteres "
                    f"(recibido: {largo})."
                )
    @staticmethod
    def validar_edad(edad: int) -> None:
        if not isinstance(edad, int) or edad < 15 or edad > 50:
            raise EdadInvalidaError(
                f"Edad '{edad}' invalida. Debe ser un entero entre 15 y 50."    
            )

    @staticmethod
    def validar_goles(goles: int) -> None:
        if not isinstance(goles, int) or goles < 0:
            raise GolesInvalidosError(
                f"Goles '{goles}' invalidos. No pueden ser negativos."
            )
        
    @staticmethod
    def validar_posicion(posicion: str) -> None:
        if posicion not in POSICIONES_VALIDAS:
            raise PosicionInvalidaError(
                f"Posicion '{posicion}' invalida. "
                f"Opciones validas: {', '.join(POSICIONES_VALIDAS)}"
            )
        
    @staticmethod
    def validar_liderazgo(liderazgo: int) -> None:
        if not isinstance(liderazgo, int) or liderazgo < 1 or liderazgo > 10:
            raise GolesInvalidosError(
                f"Liderazgo '{liderazgo}' invalido. Debe ser un entero entre 1 y 10."
            )

    @classmethod
    def validar_jugador(cls, nombre: str, edad: int, posicion: str, goles: int) -> None:
        """Valida todos los campos de un jugador base de una vez."""
        cls.validar_nombre(nombre)
        cls.validar_edad(edad)
        cls.validar_goles(goles)
        cls.validar_posicion(posicion)

    @classmethod
    def validar_capitan(cls, nombre: str, edad: int, posicion: str, goles: int, liderazgo: int) -> None:
        """Valida todos los campos de un capitán de una vez."""
        cls.validar_jugador(nombre, edad, posicion, goles)
        cls.validar_liderazgo(liderazgo)