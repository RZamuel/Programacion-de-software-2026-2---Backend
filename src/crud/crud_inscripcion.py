from datetime import date

from database.connection import get_session
from entities.inscripcion import Inscripcion


def crear_inscripcion(
    id_miembro: str,
    id_membresia: str,
    fecha_inicio: date,
    fecha_fin: date,
    estado: str = "activa",
) -> Inscripcion | None:
    """Crea una nueva inscripción."""

    session = get_session()

    try:
        inscripcion = Inscripcion(
            id_miembro=id_miembro,
            id_membresia=id_membresia,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado,
        )

        session.add(inscripcion)
        session.commit()
        session.refresh(inscripcion)

        return inscripcion

    except Exception:
        session.rollback()
        return None

    finally:
        session.close()


def leer_inscripciones() -> list[Inscripcion]:
    """Obtiene todas las inscripciones."""

    session = get_session()

    try:
        return session.query(Inscripcion).all()

    finally:
        session.close()


def leer_inscripcion_por_id(
    id_inscripcion: str,
) -> Inscripcion | None:
    """Obtiene una inscripción por su UUID."""

    session = get_session()

    try:
        return (
            session.query(Inscripcion).filter_by(id_inscripcion=id_inscripcion).first()
        )

    finally:
        session.close()


def actualizar_inscripcion(
    id_inscripcion: str,
    fecha_inicio: date | None = None,
    fecha_fin: date | None = None,
    estado: str | None = None,
) -> bool:
    """Actualiza una inscripción existente."""

    session = get_session()

    try:
        inscripcion = (
            session.query(Inscripcion).filter_by(id_inscripcion=id_inscripcion).first()
        )

        if not inscripcion:
            return False

        if fecha_inicio is not None:
            inscripcion.fecha_inicio = fecha_inicio

        if fecha_fin is not None:
            inscripcion.fecha_fin = fecha_fin

        if estado is not None:
            inscripcion.estado = estado

        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()


def eliminar_inscripcion(id_inscripcion: str) -> bool:
    """Elimina una inscripción."""

    session = get_session()

    try:
        inscripcion = (
            session.query(Inscripcion).filter_by(id_inscripcion=id_inscripcion).first()
        )

        if not inscripcion:
            return False

        session.delete(inscripcion)
        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()
