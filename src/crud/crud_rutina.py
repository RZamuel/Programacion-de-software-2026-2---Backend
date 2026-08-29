from src.entities.rutina import Rutina

_rutinas_db: list[Rutina] = []


def crear_rutina(rutina: Rutina) -> bool:
    """Crea un nuevo registro de rutina."""
    _rutinas_db.append(rutina)
    return True


def leer_rutinas() -> list[Rutina]:
    """Consulta todos los registros de rutinas."""
    return _rutinas_db


def leer_rutina_por_id(id_rutina: int) -> Rutina | None:
    """Consulta una rutina específica por su ID."""
    for rutina in _rutinas_db:
        if rutina.id_rutina == id_rutina:
            return rutina
    return None


def actualizar_rutina(
    id_rutina: int, nombre: str | None = None, descripcion: str | None = None
) -> bool:
    """Actualiza los datos de una rutina."""
    for rutina in _rutinas_db:
        if rutina.id_rutina == id_rutina:
            if nombre is not None:
                rutina.nombre = nombre

            if descripcion is not None:
                rutina.descripcion = descripcion

            return True

    return False


def eliminar_rutina(id_rutina: int) -> bool:
    """Elimina un registro de rutina."""
    for i, rutina in enumerate(_rutinas_db):
        if rutina.id_rutina == id_rutina:
            _rutinas_db.pop(i)
            return True
    return False
