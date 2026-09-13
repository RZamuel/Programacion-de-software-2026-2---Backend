import uuid

from src.database.connection import get_session
from src.entities.clase import Clase
from src.entities.reserva_clase import ReservaClase


def crear(
    id_entrenador: str,
    nombre: str,
    dia_semana: str,
    hora: str,
    capacidad_maxima: int,
) -> Clase | None:
    """Crea una nueva clase."""
    session = get_session()
    try:
        # Convertimos el ID del entrenador a UUID para asegurar la coherencia
        id_entrenador_uuid = uuid.UUID(str(id_entrenador))

        clase = Clase(
            id_entrenador=id_entrenador_uuid,
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


def leer_clases() -> list[Clase]:
    """Obtiene todas las clases."""
    session = get_session()
    try:
        return session.query(Clase).all()
    finally:
        session.close()


def leer_clase_por_id(id_clase) -> Clase | None:
    """Obtiene una clase por su UUID."""
    session = get_session()
    try:
        id_uuid = uuid.UUID(str(id_clase))
        return session.query(Clase).filter_by(id_clase=id_uuid).first()
    finally:
        session.close()


def actualizar_clase(
    id_clase,
    nombre: str | None = None,
    dia_semana: str | None = None,
    hora: str | None = None,
    capacidad_maxima: int | None = None,
) -> bool:
    """Actualiza los datos de una clase."""
    session = get_session()
    try:
        id_uuid = uuid.UUID(str(id_clase))
        clase = session.query(Clase).filter_by(id_clase=id_uuid).first()

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


def eliminar_clase(id_clase) -> bool:
    """Elimina una clase validando que no tenga reservas asociadas."""
    session = get_session()
    try:
        id_uuid = uuid.UUID(str(id_clase))
        clase = session.query(Clase).filter_by(id_clase=id_uuid).first()

        if not clase:
            return False

        # Validar que no existan reservas asociadas (Integridad Referencial)
        reservas_asociadas = (
            session.query(ReservaClase).filter_by(id_clase=id_uuid).count()
        )
        if reservas_asociadas > 0:
            return False  # No se puede eliminar si tiene reservas

        session.delete(clase)
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()
