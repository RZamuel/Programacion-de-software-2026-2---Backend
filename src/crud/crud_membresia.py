from datetime import date
from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.membresia import Membresia


def _buscar_por_id(session, id_membresia: UUID) -> Membresia | None:
    return session.query(Membresia).filter_by(id_membresia=id_membresia).first()


def _buscar_por_tipo(session, tipo: str) -> Membresia | None:
    tipo_normalizado = tipo.strip().lower()
    return (
        session.query(Membresia)
        .filter(func.lower(Membresia.tipo) == tipo_normalizado)
        .first()
    )


def crear(
    tipo: str,
    precio: float,
    duracion_dias: int,
    fecha_inicio: date | None = None,
    estado: str = "activa",
) -> Membresia | None:
    session = get_session()
    try:
        # Validación case-insensitive
        if _buscar_por_tipo(session, tipo):
            return None

        membresia = Membresia(
            tipo=tipo.strip(),
            precio=precio,
            duracion_dias=duracion_dias,
            fecha_inicio=fecha_inicio if fecha_inicio else date.today(),
            estado=estado.strip(),
        )
        session.add(membresia)
        session.commit()
        session.refresh(membresia)
        return membresia
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def listar() -> list[Membresia]:
    session = get_session()
    try:
        return session.query(Membresia).all()
    finally:
        session.close()


def obtener_por_id(id_membresia: UUID) -> Membresia | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_membresia)
    finally:
        session.close()


def actualizar(id_membresia: UUID, tipo: str, **kwargs: Any) -> Membresia | None:
    session = get_session()
    try:
        membresia = _buscar_por_id(session, id_membresia)
        if membresia is None:
            return None

        # Si cambia el tipo, validar que no exista otra con ese tipo
        if tipo and tipo.strip().lower() != membresia.tipo.lower():
            existente = _buscar_por_tipo(session, tipo)
            if existente is not None and existente.id_membresia != id_membresia:
                return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(
                    membresia, key, value.strip() if isinstance(value, str) else value
                )

        session.commit()
        session.refresh(membresia)
        return membresia
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_membresia: UUID) -> bool:
    session = get_session()
    try:
        membresia = _buscar_por_id(session, id_membresia)
        if membresia is None:
            return False

        session.delete(membresia)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()
