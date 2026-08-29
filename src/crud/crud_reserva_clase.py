from src.entities.reserva_clase import ReservaClase

_reservas_db: list[ReservaClase] = []


def crear_reserva(reserva: ReservaClase) -> bool:
    """Crea un nuevo registro de reserva de clase."""
    _reservas_db.append(reserva)
    return True


def leer_reservas() -> list[ReservaClase]:
    """Consulta todos los registros de reservas."""
    return _reservas_db


def leer_reserva_por_id(id_reserva: int) -> ReservaClase | None:
    """Consulta una reserva específica por su ID."""
    for reserva in _reservas_db:
        if reserva.id_reserva == id_reserva:
            return reserva
    return None


def actualizar_reserva(
    id_reserva: int,
    **kwargs,
) -> bool:
    """Actualiza los datos de una reserva existente."""
    for reserva in _reservas_db:
        if reserva.id_reserva == id_reserva:
            for key, value in kwargs.items():
                if hasattr(reserva, key):
                    setattr(reserva, key, value)
            return True
    return False


def eliminar_reserva(id_reserva: int) -> bool:
    """Elimina un registro de reserva."""
    for i, reserva in enumerate(_reservas_db):
        if reserva.id_reserva == id_reserva:
            _reservas_db.pop(i)
            return True
    return False
