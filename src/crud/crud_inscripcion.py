from datetime import date, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.inscripcion import Inscripcion
from src.entities.membresia import Membresia
from src.entities.miembro import Miembro


def _buscar_por_id(session, id_inscripcion: UUID) -> Inscripcion | None:
    return session.query(Inscripcion).filter_by(id_inscripcion=id_inscripcion).first()


def crear(
    id_miembro: UUID,
    id_membresia: UUID,
    fecha_inicio: date,
    estado: str = "activa",
) -> Inscripcion | None:

    session = get_session()
    try:
        # 1. Validar que el miembro exista
        if not session.query(Miembro).filter_by(id_miembro=id_miembro).first():
            return None

        # 2. Validar que la membresía exista y obtenerla para calcular fecha_fin
        membresia = (
            session.query(Membresia).filter_by(id_membresia=id_membresia).first()
        )
        if not membresia:
            return None

        # 3. Validar que no exista una inscripción activa duplicada
        inscripcion_existente = (
            session.query(Inscripcion)
            .filter_by(
                id_miembro=id_miembro,
                id_membresia=id_membresia,
                estado="activa",
            )
            .first()
        )
        if inscripcion_existente:
            return None

        # 4. Calcular la fecha de fin automáticamente
        fecha_fin = fecha_inicio + timedelta(days=membresia.duracion_dias)

        # 5. Crear la inscripción
        inscripcion = Inscripcion(
            id_miembro=id_miembro,
            id_membresia=id_membresia,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado.strip(),
        )
        session.add(inscripcion)
        session.commit()
        session.refresh(inscripcion)
        return inscripcion
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def listar() -> list[Inscripcion]:
    session = get_session()
    try:
        return session.query(Inscripcion).all()
    finally:
        session.close()


def listar_por_miembro(id_miembro: UUID) -> list[Inscripcion]:
    session = get_session()
    try:
        return session.query(Inscripcion).filter_by(id_miembro=id_miembro).all()
    finally:
        session.close()


def obtener_por_id(id_inscripcion: UUID) -> Inscripcion | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_inscripcion)
    finally:
        session.close()


def actualizar(
    id_inscripcion: UUID,
    estado: str | None = None,
    fecha_inicio: date | None = None,
) -> Inscripcion | None:
    session = get_session()
    try:
        inscripcion = _buscar_por_id(session, id_inscripcion)
        if inscripcion is None:
            return None

        # Si cambia la fecha de inicio, recalcular fecha_fin
        if fecha_inicio is not None:
            membresia = (
                session.query(Membresia)
                .filter_by(id_membresia=inscripcion.id_membresia)
                .first()
            )
            if membresia:
                inscripcion.fecha_inicio = fecha_inicio
                inscripcion.fecha_fin = fecha_inicio + timedelta(
                    days=membresia.duracion_dias
                )

        if estado is not None:
            inscripcion.estado = estado.strip()

        session.commit()
        session.refresh(inscripcion)
        return inscripcion
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_inscripcion: UUID) -> bool:
    session = get_session()
    try:
        inscripcion = _buscar_por_id(session, id_inscripcion)
        if inscripcion is None:
            return False

        session.delete(inscripcion)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()
