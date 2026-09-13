from datetime import date

from src.database.connection import get_session
from src.entities.rutina import Rutina


def crear(
    id_miembro: int,
    id_entrenador: int,
    nombre: str,
    descripcion: str,
    fecha_creacion: date | None = None,
) -> Rutina | None:
    session = get_session()

    try:
        rutina = Rutina(
            id_miembro=id_miembro,
            id_entrenador=id_entrenador,
            nombre=nombre,
            descripcion=descripcion,
            fecha_creacion=fecha_creacion if fecha_creacion else date.today(),
        )

        session.add(rutina)
        session.commit()
        session.refresh(rutina)

        return rutina

    except Exception:
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


def obtener(id_rutina: int) -> Rutina | None:
    session = get_session()

    try:
        return session.query(Rutina).filter_by(id_rutina=id_rutina).first()

    finally:
        session.close()


def actualizar(
    id_rutina: int,
    nombre: str | None = None,
    descripcion: str | None = None,
) -> bool:
    session = get_session()

    try:
        rutina = session.query(Rutina).filter_by(id_rutina=id_rutina).first()

        if not rutina:
            return False

        if nombre is not None:
            rutina.nombre = nombre

        if descripcion is not None:
            rutina.descripcion = descripcion

        session.commit()
        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()


def eliminar(id_rutina: int) -> bool:
    session = get_session()

    try:
        rutina = session.query(Rutina).filter_by(id_rutina=id_rutina).first()

        if not rutina:
            return False

        session.delete(rutina)
        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()
