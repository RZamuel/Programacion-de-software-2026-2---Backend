from src.entities.membresia import Membresia

_membresias_db: list[Membresia] = []


def crear_membresia(membresia: Membresia) -> bool:
    """Crea un nuevo registro de membresía."""
    _membresias_db.append(membresia)
    return True


def leer_membresias() -> list[Membresia]:
    """Consulta todos los registros de membresías."""
    return _membresias_db


def leer_membresia_por_id(id_membresia: int) -> Membresia | None:
    """Consulta una membresía específica por su ID."""
    for membresia in _membresias_db:
        if membresia.id_membresia == id_membresia:
            return membresia
    return None


def actualizar_membresia(
    id_membresia: int,
    tipo: str | None = None,
    precio: float | None = None,
    duracion_dias: int | None = None,
    estado: str | None = None,
) -> bool:
    """Actualiza los datos de una membresía."""
    for membresia in _membresias_db:
        if membresia.id_membresia == id_membresia:
            if tipo is not None:
                membresia.tipo = tipo

            if precio is not None:
                membresia.precio = precio

            if duracion_dias is not None:
                membresia.duracion_dias = duracion_dias

            if estado is not None:
                membresia.estado = estado

            return True

    return False


def eliminar_membresia(id_membresia: int) -> bool:
    """Elimina un registro de membresía."""
    for i, membresia in enumerate(_membresias_db):
        if membresia.id_membresia == id_membresia:
            _membresias_db.pop(i)
            return True
    return False
