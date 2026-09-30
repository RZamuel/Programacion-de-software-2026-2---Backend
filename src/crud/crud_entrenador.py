from typing import Any
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.entrenador import Entrenador


def _buscar_por_id(session, id_entrenador: UUID) -> Entrenador | None:
    return session.query(Entrenador).filter_by(id_entrenador=id_entrenador).first()


def crear(
    nombre: str,
    apellido: str,
    especialidad: str,
    telefono: str,
    salario: float,
) -> Entrenador | None:
    session = get_session()
    try:
        entrenador = Entrenador(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            especialidad=especialidad.strip(),
            telefono=telefono.strip(),
            salario=salario,
        )
        session.add(entrenador)
        session.commit()
        session.refresh(entrenador)
        return entrenador
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def listar() -> list[Entrenador]:
    session = get_session()
    try:
        return session.query(Entrenador).all()
    finally:
        session.close()


def obtener_por_id(id_entrenador: UUID) -> Entrenador | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_entrenador)
    finally:
        session.close()


def actualizar(id_entrenador: UUID, **kwargs: Any) -> Entrenador | None:
    session = get_session()
    try:
        entrenador = _buscar_por_id(session, id_entrenador)
        if entrenador is None:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(
                    entrenador, key, value.strip() if isinstance(value, str) else value
                )

        session.commit()
        session.refresh(entrenador)
        return entrenador
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_entrenador: UUID) -> bool:
    session = get_session()
    try:
        entrenador = _buscar_por_id(session, id_entrenador)
        if entrenador is None:
            return False

        session.delete(entrenador)
        session.commit()
        return True
    except IntegrityError:
        # La BD bloquea la eliminación si hay clases/rutinas asociadas
        session.rollback()
        return False
    finally:
        session.close()
