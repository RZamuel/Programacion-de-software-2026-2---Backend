from src.entities.entrenador import Entrenador

_entrenadores_db: list[Entrenador] = []


def crear_entrenador(entrenador: Entrenador) -> bool:
    """Crea un nuevo registro de entrenador."""
    _entrenadores_db.append(entrenador)
    return True


def leer_entrenadores() -> list[Entrenador]:
    """Consulta todos los registros de entrenadores."""
    return _entrenadores_db


def leer_entrenador_por_id(id_entrenador: int) -> Entrenador | None:
    """Consulta un entrenador específico por su ID."""
    for entrenador in _entrenadores_db:
        if entrenador.id_entrenador == id_entrenador:
            return entrenador
    return None


def actualizar_entrenador(
    id_entrenador: int,
    nombre: str | None = None,
    apellido: str | None = None,
    especialidad: str | None = None,
    telefono: str | None = None,
    salario: float | None = None,
) -> bool:
    """Actualiza los datos de un entrenador."""
    for entrenador in _entrenadores_db:
        if entrenador.id_entrenador == id_entrenador:
            if nombre is not None:
                entrenador.nombre = nombre

            if apellido is not None:
                entrenador.apellido = apellido

            if especialidad is not None:
                entrenador.especialidad = especialidad

            if telefono is not None:
                entrenador.telefono = telefono

            if salario is not None:
                entrenador.salario = salario

            return True

    return False


def eliminar_entrenador(id_entrenador: int) -> bool:
    """Elimina un registro de entrenador."""
    for i, entrenador in enumerate(_entrenadores_db):
        if entrenador.id_entrenador == id_entrenador:
            _entrenadores_db.pop(i)
            return True
    return False
