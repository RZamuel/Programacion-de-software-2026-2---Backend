from datetime import date
from typing import Any
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from src.database.connection import get_session
from src.entities.pago import Pago
from src.entities.miembro import Miembro


def _buscar_por_id(session, id_pago: UUID) -> Pago | None:
    return session.query(Pago).filter_by(id_pago=id_pago).first()


def crear(
    id_miembro: UUID,
    monto: float,
    metodo_pago: str,
    concepto: str,
    fecha_pago: date | None = None,
) -> Pago | None:
    session = get_session()
    try:
        # Validar que el miembro exista
        if not session.query(Miembro).filter_by(id_miembro=id_miembro).first():
            return None

        pago = Pago(
            id_miembro=id_miembro,
            monto=monto,
            fecha_pago=fecha_pago if fecha_pago else date.today(),
            metodo_pago=metodo_pago.strip(),
            concepto=concepto.strip(),
        )

        session.add(pago)
        session.commit()
        session.refresh(pago)

        return pago

    except IntegrityError:
        session.rollback()
        return None

    finally:
        session.close()


def listar() -> list[Pago]:
    session = get_session()
    try:
        return session.query(Pago).all()
    finally:
        session.close()


def obtener_por_id(id_pago: UUID) -> Pago | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_pago)
    finally:
        session.close()


def actualizar(id_pago: UUID, **kwargs: Any) -> Pago | None:
    session = get_session()
    try:
        pago = _buscar_por_id(session, id_pago)
        if pago is None:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(pago, key, value.strip() if isinstance(value, str) else value)

        session.commit()
        session.refresh(pago)

        return pago

    except IntegrityError:
        session.rollback()
        return None

    finally:
        session.close()


def eliminar(id_pago: UUID) -> bool:
    session = get_session()
    try:
        pago = _buscar_por_id(session, id_pago)
        if pago is None:
            return False

        session.delete(pago)
        session.commit()

        return True

    except IntegrityError:
        session.rollback()
        return False

    finally:
        session.close()
