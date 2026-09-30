from typing import Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.miembro import Miembro


def _buscar_por_id(session, id_miembro: UUID) -> Miembro | None:
    return session.query(Miembro).filter_by(id_miembro=id_miembro).first()


def _buscar_por_usuario(session, nombre_usuario: str) -> Miembro | None:
    nombre = nombre_usuario.strip().lower()
    return (
        session.query(Miembro)
        .filter(func.lower(Miembro.nombre_usuario) == nombre)
        .first()
    )


def crear(
    primer_nombre: str,
    segundo_nombre: str,
    primer_apellido: str,
    segundo_apellido: str,
    nombre_usuario: str,
    clave: str,
    email: str,
    telefono: str,
) -> Miembro | None:
    session = get_session()
    try:
        if _buscar_por_usuario(session, nombre_usuario):
            return None

        miembro = Miembro(
            primer_nombre=primer_nombre.strip(),
            segundo_nombre=(segundo_nombre or "").strip(),
            primer_apellido=primer_apellido.strip(),
            segundo_apellido=(segundo_apellido or "").strip(),
            nombre_usuario=nombre_usuario.strip(),
            clave=clave,
            email=email.strip(),
            telefono=telefono.strip(),
        )
        session.add(miembro)
        session.commit()
        session.refresh(miembro)
        return miembro
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_miembro: UUID) -> bool:
    session = get_session()
    try:
        miembro = _buscar_por_id(session, id_miembro)
        if miembro is None:
            return False
        session.delete(miembro)
        session.commit()
        return True
    finally:
        session.close()


def actualizar(id_miembro: UUID, nombre_usuario: str, **kwargs: Any) -> Miembro | None:
    session = get_session()
    try:
        miembro = _buscar_por_id(session, id_miembro)
        if miembro is None:
            return None

        if nombre_usuario:
            existente = _buscar_por_usuario(session, nombre_usuario)
            if existente is not None and existente.id_miembro != id_miembro:
                return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(
                    miembro, key, value.strip() if isinstance(value, str) else value
                )

        session.commit()
        session.refresh(miembro)
        return miembro
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def obtener(nombre_usuario: str, clave: str) -> Miembro | None:
    session = get_session()
    try:
        miembro = _buscar_por_usuario(session, nombre_usuario)
        if miembro is None or miembro.clave != clave:
            return None
        return miembro
    finally:
        session.close()


def obtener_por_id(id_miembro: UUID) -> Miembro | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_miembro)
    finally:
        session.close()


def listar() -> list[Miembro]:
    session = get_session()
    try:
        return session.query(Miembro).all()
    finally:
        session.close()
