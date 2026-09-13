from datetime import date

from database.connection import get_session
from entities.reserva_clase import ReservaClase


def crear(
    id_miembro: int,
    id_clase: int,
    fecha_reserva: date,
    estado: str = "confirmada",
) -> ReservaClase | None:
    session = get_session()

    try:
        reserva = ReservaClase(
            id_miembro=id_miembro,
            id_clase=id_clase,
            fecha_reserva=fecha_reserva,
            estado=estado,
        )

        session.add(reserva)
        session.commit()
        session.refresh(reserva)

        return reserva

    except Exception:
        session.rollback()
        return None

    finally:
        session.close()


def listar() -> list[ReservaClase]:
    session = get_session()

    try:
        return session.query(ReservaClase).all()

    finally:
        session.close()


def obtener(id_reserva: int) -> ReservaClase | None:
    session = get_session()

    try:
        return session.query(ReservaClase).filter_by(id_reserva=id_reserva).first()

    finally:
        session.close()


def actualizar(
    id_reserva: int,
    estado: str | None = None,
) -> bool:
    session = get_session()

    try:
        reserva = session.query(ReservaClase).filter_by(id_reserva=id_reserva).first()

        if not reserva:
            return False

        if estado is not None:
            reserva.estado = estado

        session.commit()
        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()


def eliminar(id_reserva: int) -> bool:
    session = get_session()

    try:
        reserva = session.query(ReservaClase).filter_by(id_reserva=id_reserva).first()

        if not reserva:
            return False

        session.delete(reserva)
        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()
