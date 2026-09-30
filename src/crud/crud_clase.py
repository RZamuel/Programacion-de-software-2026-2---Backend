from typing import Any
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.database.connection import get_session
from src.entities.clase import Clase
from src.entities.entrenador import Entrenador


def _buscar_por_id(session, id_clase: UUID) -> Clase | None:
    return session.query(Clase).filter_by(id_clase=id_clase).first()


def crear(
    id_entrenador: UUID,
    nombre: str,
    dia_semana: str,
    hora: str,
    capacidad_maxima: int,
) -> Clase | None:
    session = get_session()
    try:
        # Validar que el entrenador exista
        if not session.query(Entrenador).filter_by(id_entrenador=id_entrenador).first():
            return None

        clase = Clase(
            id_entrenador=id_entrenador,
            nombre=nombre.strip(),
            dia_semana=dia_semana.strip(),
            hora=hora.strip(),
            capacidad_maxima=capacidad_maxima,
        )
        session.add(clase)
        session.commit()
        session.refresh(clase)
        return clase
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def listar() -> list[Clase]:
    session = get_session()
    try:
        return session.query(Clase).all()
    finally:
        session.close()


def obtener_por_id(id_clase: UUID) -> Clase | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_clase)
    finally:
        session.close()


def actualizar(id_clase: UUID, **kwargs: Any) -> Clase | None:
    session = get_session()
    try:
        clase = _buscar_por_id(session, id_clase)
        if clase is None:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(clase, key, value.strip() if isinstance(value, str) else value)

        session.commit()
        session.refresh(clase)
        return clase
    except IntegrityError:
        session.rollback()
        return None
    finally:
        session.close()


def eliminar(id_clase: UUID) -> bool:
    session = get_session()
    try:
        clase = _buscar_por_id(session, id_clase)
        if clase is None:
            return False

        session.delete(clase)
        session.commit()
        return True
    except IntegrityError:
        # La BD bloquea la eliminación si hay reservas asociadas
        session.rollback()
        return False
    finally:
        session.close()
