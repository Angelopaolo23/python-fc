class EquipoError(Exception):
    pass

class GolesInvalidosError(EquipoError):
    pass

class EdadInvalidaError(EquipoError):
    pass

class PosicionInvalidaError(EquipoError):
    pass

class LargoNombreError(EquipoError):
    pass