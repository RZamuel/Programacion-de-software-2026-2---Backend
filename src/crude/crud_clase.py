from src.entities.clase import Clase

_clases_db: list[Clase] = []


def crear_clase(clase: Clase) -> bool:
    """Crea un nuevo registro de clase."""
    _clases_db.append(clase)
    return True


def leer_clases() -> list[Clase]:
    """Consulta todos los registros de clases."""
    return _clases_db


def leer_clase_por_id(id_clase: int) -> Clase | None:
    """Consulta una clase específica por su ID."""
    for clase in _clases_db:
        if clase.id_clase == id_clase:
            return clase
    return None


def actualizar_clase(
    id_clase: int,
    id_entrenador: int | None = None,
    nombre: str | None = None,
    dia_semana: str | None = None,
    hora: str | None = None,
    capacidad_maxima: int | None = None,
) -> bool:
    """Actualiza los datos de una clase."""
    for clase in _clases_db:
        if clase.id_clase == id_clase:
            if id_entrenador is not None:
                clase.id_entrenador = id_entrenador

            if nombre is not None:
                clase.nombre = nombre

            if dia_semana is not None:
                clase.dia_semana = dia_semana

            if hora is not None:
                clase.hora = hora

            if capacidad_maxima is not None:
                clase.capacidad_maxima = capacidad_maxima

            return True

    return False


def eliminar_clase(id_clase: int) -> bool:
    """Elimina un registro de clase."""
    for i, clase in enumerate(_clases_db):
        if clase.id_clase == id_clase:
            _clases_db.pop(i)
            return True

    return False
