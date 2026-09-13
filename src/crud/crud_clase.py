from database.connection import get_session
from entities.clase import Clase


def crear(
    id_entrenador: int,
    nombre: str,
    dia_semana: str,
    hora: str,
    capacidad_maxima: int,
) -> Clase | None:
    session = get_session()
    try:
        clase = Clase(
            id_entrenador=id_entrenador,
            nombre=nombre,
            dia_semana=dia_semana,
            hora=hora,
            capacidad_maxima=capacidad_maxima,
        )

        session.add(clase)
        session.commit()
        session.refresh(clase)

        return clase

    except Exception:
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


def obtener(id_clase: int) -> Clase | None:
    session = get_session()
    try:
        return session.query(Clase).filter_by(id_clase=id_clase).first()
    finally:
        session.close()


def actualizar(
    id_clase: int,
    nombre: str | None = None,
    dia_semana: str | None = None,
    hora: str | None = None,
    capacidad_maxima: int | None = None,
) -> bool:
    session = get_session()

    try:
        clase = session.query(Clase).filter_by(id_clase=id_clase).first()

        if not clase:
            return False

        if nombre is not None:
            clase.nombre = nombre

        if dia_semana is not None:
            clase.dia_semana = dia_semana

        if hora is not None:
            clase.hora = hora

        if capacidad_maxima is not None:
            clase.capacidad_maxima = capacidad_maxima

        session.commit()
        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()


def eliminar(id_clase: int) -> bool:
    session = get_session()

    try:
        clase = session.query(Clase).filter_by(id_clase=id_clase).first()

        if not clase:
            return False

        session.delete(clase)
        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()
