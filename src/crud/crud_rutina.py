from datetime import date
from typing import Any
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from src.database.connection import get_session
from src.entities.rutina import Rutina
from src.entities.miembro import Miembro
from src.entities.entrenador import Entrenador


def _buscar_por_id(session, id_rutina: UUID) -> Rutina | None:
    return session.query(Rutina).filter_by(id_rutina=id_rutina).first()


def crear(
    id_miembro: UUID,
    id_entrenador: UUID,
    nombre: str,
    descripcion: str,
    fecha_creacion: date | None = None,
) -> Rutina | None:
    session = get_session()
    try:
        # Validar que el miembro exista
        if not session.query(Miembro).filter_by(id_miembro=id_miembro).first():
            return None

        # Validar que el entrenador exista
        if not session.query(Entrenador).filter_by(id_entrenador=id_entrenador).first():
            return None

        rutina = Rutina(
            id_miembro=id_miembro,
            id_entrenador=id_entrenador,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            fecha_creacion=fecha_creacion if fecha_creacion else date.today(),
        )

        session.add(rutina)
        session.commit()
        session.refresh(rutina)

        return rutina

    except IntegrityError:
        session.rollback()
        return None

    finally:
        session.close()


def listar() -> list[Rutina]:
    session = get_session()
    try:
        return session.query(Rutina).all()
    finally:
        session.close()


def listar_por_miembro(id_miembro: UUID) -> list[Rutina]:
    session = get_session()
    try:
        return session.query(Rutina).filter_by(id_miembro=id_miembro).all()
    finally:
        session.close()


def listar_por_entrenador(id_entrenador: UUID) -> list[Rutina]:
    session = get_session()
    try:
        return session.query(Rutina).filter_by(id_entrenador=id_entrenador).all()
    finally:
        session.close()


def obtener_por_id(id_rutina: UUID) -> Rutina | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_rutina)
    finally:
        session.close()


def actualizar(id_rutina: UUID, **kwargs: Any) -> Rutina | None:
    session = get_session()
    try:
        rutina = _buscar_por_id(session, id_rutina)
        if rutina is None:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(rutina, key, value.strip() if isinstance(value, str) else value)

        session.commit()
        session.refresh(rutina)

        return rutina

    except IntegrityError:
        session.rollback()
        return None

    finally:
        session.close()


def eliminar(id_rutina: UUID) -> bool:
    session = get_session()
    try:
        rutina = _buscar_por_id(session, id_rutina)
        if rutina is None:
            return False

        session.delete(rutina)
        session.commit()

        return True

    except IntegrityError:
        session.rollback()
        return False

    finally:
        session.close()
