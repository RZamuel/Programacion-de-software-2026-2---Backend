from src.database.connection import get_session
from src.entities.entrenador import Entrenador


def crear_entrenador(
    nombre: str,
    apellido: str,
    especialidad: str,
    telefono: str,
    salario: float,
) -> Entrenador | None:
    """Crea un nuevo entrenador."""

    session = get_session()

    try:
        entrenador = Entrenador(
            nombre=nombre,
            apellido=apellido,
            especialidad=especialidad,
            telefono=telefono,
            salario=salario,
        )

        session.add(entrenador)
        session.commit()
        session.refresh(entrenador)

        return entrenador

    except Exception:
        session.rollback()
        return None

    finally:
        session.close()


def leer_entrenadores() -> list[Entrenador]:
    """Obtiene todos los entrenadores."""

    session = get_session()

    try:
        return session.query(Entrenador).all()

    finally:
        session.close()


def leer_entrenador_por_id(
    id_entrenador: str,
) -> Entrenador | None:
    """Obtiene un entrenador por su UUID."""

    session = get_session()

    try:
        return session.query(Entrenador).filter_by(id_entrenador=id_entrenador).first()

    finally:
        session.close()


def actualizar_entrenador(
    id_entrenador: str,
    especialidad: str | None = None,
    telefono: str | None = None,
    salario: float | None = None,
) -> bool:
    """Actualiza los datos de un entrenador."""

    session = get_session()

    try:
        entrenador = (
            session.query(Entrenador).filter_by(id_entrenador=id_entrenador).first()
        )

        if not entrenador:
            return False

        if especialidad is not None:
            entrenador.especialidad = especialidad

        if telefono is not None:
            entrenador.telefono = telefono

        if salario is not None:
            entrenador.salario = salario

        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()


def eliminar_entrenador(id_entrenador: str) -> bool:
    """Elimina un entrenador."""

    session = get_session()

    try:
        entrenador = (
            session.query(Entrenador).filter_by(id_entrenador=id_entrenador).first()
        )

        if not entrenador:
            return False

        session.delete(entrenador)
        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()
