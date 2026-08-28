from src.entities.inscripcion import Inscripcion
from datetime import date

_inscripciones_db: list[Inscripcion] = []


def crear_inscripcion(inscripcion: Inscripcion) -> bool:
    """Crea un nuevo registro de inscripción."""
    _inscripciones_db.append(inscripcion)
    return True


def leer_inscripciones() -> list[Inscripcion]:
    """Consulta todos los registros de inscripciones."""
    return _inscripciones_db


def leer_inscripcion_por_id(id_inscripcion: int) -> Inscripcion | None:
    """Consulta una inscripción específica por su ID."""
    for inscripcion in _inscripciones_db:
        if inscripcion.id_inscripcion == id_inscripcion:
            return inscripcion
    return None


def actualizar_inscripcion(
    id_inscripcion: int,
    fecha_fin: date | None = None,
    estado: str | None = None,
) -> bool:
    """Actualiza la fecha de finalización o estado de una inscripción."""
    for inscripcion in _inscripciones_db:
        if inscripcion.id_inscripcion == id_inscripcion:
            if fecha_fin is not None:
                inscripcion.fecha_fin = fecha_fin

            if estado is not None:
                inscripcion.estado = estado

            return True

    return False


def eliminar_inscripcion(id_inscripcion: int) -> bool:
    """Elimina un registro de inscripción."""
    for i, inscripcion in enumerate(_inscripciones_db):
        if inscripcion.id_inscripcion == id_inscripcion:
            _inscripciones_db.pop(i)
            return True
    return False
