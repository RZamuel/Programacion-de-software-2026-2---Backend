"""Módulo para las operaciones CRUD de la entidad Miembro."""

from src.entities.miembro import Miembro

_miembros_db: list[Miembro] = []


def crear_miembro(miembro: Miembro) -> bool:
    """Crea un nuevo registro de miembro."""
    _miembros_db.append(miembro)
    return True


def leer_miembros() -> list[Miembro]:
    """Consulta todos los registros de miembros."""
    return _miembros_db


def leer_miembro_por_id(id_miembro: int) -> Miembro | None:
    """Consulta un miembro específico por su ID."""
    for miembro in _miembros_db:
        if miembro.id_miembro == id_miembro:
            return miembro
    return None


def actualizar_miembro(
    id_miembro: int,
    nombre: str,
    apellido: str,
    email: str,
    telefono: str,
) -> bool:
    """Actualiza los datos de un miembro existente."""
    for miembro in _miembros_db:
        if miembro.id_miembro == id_miembro:
            miembro.nombre = nombre
            miembro.apellido = apellido
            miembro.email = email
            miembro.telefono = telefono
            return True
    return False


def eliminar_miembro(id_miembro: int) -> bool:
    """Elimina un registro de miembro."""
    for i, miembro in enumerate(_miembros_db):
        if miembro.id_miembro == id_miembro:
            _miembros_db.pop(i)
            return True
    return False
