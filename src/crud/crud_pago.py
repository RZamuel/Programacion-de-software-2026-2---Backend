from datetime import date

from database.connection import get_session
from entities.pago import Pago


def crear_pago(
    id_miembro: str,
    monto: float,
    metodo_pago: str,
    concepto: str,
    fecha_pago: date | None = None,
) -> Pago | None:
    """Crea un nuevo pago."""

    session = get_session()

    try:
        pago = Pago(
            id_miembro=id_miembro,
            monto=monto,
            fecha_pago=fecha_pago if fecha_pago else date.today(),
            metodo_pago=metodo_pago,
            concepto=concepto,
        )

        session.add(pago)
        session.commit()
        session.refresh(pago)

        return pago

    except Exception:
        session.rollback()
        return None

    finally:
        session.close()


def leer_pagos() -> list[Pago]:
    """Obtiene todos los pagos."""

    session = get_session()

    try:
        return session.query(Pago).all()

    finally:
        session.close()


def leer_pago_por_id(
    id_pago: str,
) -> Pago | None:
    """Obtiene un pago por su UUID."""

    session = get_session()

    try:
        return session.query(Pago).filter_by(id_pago=id_pago).first()

    finally:
        session.close()


def actualizar_pago(
    id_pago: str,
    monto: float | None = None,
    metodo_pago: str | None = None,
    concepto: str | None = None,
) -> bool:
    """Actualiza los datos de un pago."""

    session = get_session()

    try:
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()

        if not pago:
            return False

        if monto is not None:
            pago.monto = monto

        if metodo_pago is not None:
            pago.metodo_pago = metodo_pago

        if concepto is not None:
            pago.concepto = concepto

        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()


def eliminar_pago(id_pago: str) -> bool:
    """Elimina un pago."""

    session = get_session()

    try:
        pago = session.query(Pago).filter_by(id_pago=id_pago).first()

        if not pago:
            return False

        session.delete(pago)
        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()
