from datetime import date

from database.connection import get_session
from entities.membresia import Membresia


def crear_membresia(
    tipo: str,
    precio: float,
    duracion_dias: int,
    fecha_inicio: date | None = None,
    estado: str = "activa",
) -> Membresia | None:
    """Crea una nueva membresía."""
    session = get_session()

    try:
        if session.query(Membresia).filter_by(tipo=tipo).first():
            return None

        membresia = Membresia(
            tipo=tipo,
            precio=precio,
            duracion_dias=duracion_dias,
            fecha_inicio=fecha_inicio if fecha_inicio else date.today(),
            estado=estado,
        )

        session.add(membresia)
        session.commit()
        session.refresh(membresia)

        return membresia

    except Exception:
        session.rollback()
        return None

    finally:
        session.close()


def leer_membresias() -> list[Membresia]:
    """Obtiene todas las membresías."""
    session = get_session()

    try:
        return session.query(Membresia).all()

    finally:
        session.close()


def leer_membresia_por_id(
    id_membresia: str,
) -> Membresia | None:
    """Obtiene una membresía por su UUID."""
    session = get_session()

    try:
        return session.query(Membresia).filter_by(id_membresia=id_membresia).first()

    finally:
        session.close()


def actualizar_membresia(
    id_membresia: str,
    tipo: str | None = None,
    precio: float | None = None,
    duracion_dias: int | None = None,
    fecha_inicio: date | None = None,
    estado: str | None = None,
) -> bool:
    """Actualiza una membresía existente."""
    session = get_session()

    try:
        membresia = (
            session.query(Membresia).filter_by(id_membresia=id_membresia).first()
        )

        if not membresia:
            return False

        if tipo is not None:
            membresia.tipo = tipo

        if precio is not None:
            membresia.precio = precio

        if duracion_dias is not None:
            membresia.duracion_dias = duracion_dias

        if fecha_inicio is not None:
            membresia.fecha_inicio = fecha_inicio

        if estado is not None:
            membresia.estado = estado

        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()


def eliminar_membresia(id_membresia: str) -> bool:
    """Elimina una membresía."""
    session = get_session()

    try:
        membresia = (
            session.query(Membresia).filter_by(id_membresia=id_membresia).first()
        )

        if not membresia:
            return False

        session.delete(membresia)
        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()
