from src.entities.pago import Pago

_pagos_db: list[Pago] = []


def crear_pago(pago: Pago) -> bool:
    """Crea un nuevo registro de pago."""
    _pagos_db.append(pago)
    return True


def leer_pagos() -> list[Pago]:
    """Consulta todos los registros de pagos."""
    return _pagos_db


def leer_pago_por_id(id_pago: int) -> Pago | None:
    """Consulta un pago específico por su ID."""
    for pago in _pagos_db:
        if pago.id_pago == id_pago:
            return pago
    return None


def actualizar_pago(
    id_pago: int,
    monto: float | None = None,
    metodo_pago: str | None = None,
    concepto: str | None = None,
) -> bool:
    """Actualiza el monto, método de pago o concepto."""
    for pago in _pagos_db:
        if pago.id_pago == id_pago:
            if monto is not None:
                pago.monto = monto

            if metodo_pago is not None:
                pago.metodo_pago = metodo_pago

            if concepto is not None:
                pago.concepto = concepto

            return True

    return False


def eliminar_pago(id_pago: int) -> bool:
    """Elimina un registro de pago."""
    for i, pago in enumerate(_pagos_db):
        if pago.id_pago == id_pago:
            _pagos_db.pop(i)
            return True

    return False
