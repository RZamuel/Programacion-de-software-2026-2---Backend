from datetime import date
from typing import Any
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from src.database.connection import get_session
from src.entities.reserva_clase import ReservaClase
from src.entities.miembro import Miembro
from src.entities.clase import Clase

# Campos permitidos para actualizar (seguridad)
CAMPOS_PERMITIDOS = {"estado", "fecha_reserva"}

# Estados válidos
ESTADOS_VALIDOS = {"confirmada", "cancelada", "pendiente"}


def _buscar_por_id(session, id_reserva: UUID) -> ReservaClase | None:
    return session.query(ReservaClase).filter_by(id_reserva=id_reserva).first()


def _hay_cupo(session, id_clase: UUID, fecha: date) -> bool:
    clase = session.query(Clase).filter_by(id_clase=id_clase).first()
    if clase is None:
        return False

    reservas_confirmadas = (
        session.query(ReservaClase)
        .filter_by(id_clase=id_clase, fecha_reserva=fecha, estado="confirmada")
        .count()
    )

    return reservas_confirmadas < clase.capacidad_maxima


def _existe_duplicado(
    session,
    id_miembro: UUID,
    id_clase: UUID,
    fecha_reserva: date,
    excluir_id: UUID | None = None,
) -> bool:
    """Verifica si ya existe una reserva activa (no cancelada) para
    el mismo miembro, clase y fecha."""
    query = session.query(ReservaClase).filter(
        ReservaClase.id_miembro == id_miembro,
        ReservaClase.id_clase == id_clase,
        ReservaClase.fecha_reserva == fecha_reserva,
        ReservaClase.estado != "cancelada",
    )

    if excluir_id is not None:
        query = query.filter(ReservaClase.id_reserva != excluir_id)

    return query.first() is not None


def crear(
    id_miembro: UUID,
    id_clase: UUID,
    fecha_reserva: date,
    estado: str = "confirmada",
) -> ReservaClase | None:
    """Crea una nueva reserva con validaciones de negocio."""
    session = get_session()
    try:
        # 1. Validar que el miembro exista
        if not session.query(Miembro).filter_by(id_miembro=id_miembro).first():
            return None

        # 2. Validar que la clase exista
        if not session.query(Clase).filter_by(id_clase=id_clase).first():
            return None

        # 3. Validar estado
        if estado not in ESTADOS_VALIDOS:
            return None

        # 4. Validar duplicados
        if _existe_duplicado(session, id_miembro, id_clase, fecha_reserva):
            return None

        # 5. Validar cupo (solo si es confirmada)
        if estado == "confirmada" and not _hay_cupo(session, id_clase, fecha_reserva):
            return None

        reserva = ReservaClase(
            id_miembro=id_miembro,
            id_clase=id_clase,
            fecha_reserva=fecha_reserva,
            estado=estado.strip(),
        )

        session.add(reserva)
        session.commit()
        session.refresh(reserva)

        return reserva

    except IntegrityError:
        session.rollback()
        return None

    finally:
        session.close()


def listar() -> list[ReservaClase]:
    session = get_session()
    try:
        return session.query(ReservaClase).all()
    finally:
        session.close()


def listar_por_miembro(id_miembro: UUID) -> list[ReservaClase]:
    session = get_session()
    try:
        return session.query(ReservaClase).filter_by(id_miembro=id_miembro).all()
    finally:
        session.close()


def listar_por_clase(id_clase: UUID) -> list[ReservaClase]:
    session = get_session()
    try:
        return session.query(ReservaClase).filter_by(id_clase=id_clase).all()
    finally:
        session.close()


def obtener_por_id(id_reserva: UUID) -> ReservaClase | None:
    session = get_session()
    try:
        return _buscar_por_id(session, id_reserva)
    finally:
        session.close()


def actualizar(id_reserva: UUID, **kwargs: Any) -> ReservaClase | None:
    session = get_session()
    try:
        reserva = _buscar_por_id(session, id_reserva)
        if reserva is None:
            return None

        # Filtrar solo campos permitidos (seguridad)
        datos = {
            k: v for k, v in kwargs.items() if k in CAMPOS_PERMITIDOS and v is not None
        }

        if not datos:
            return reserva

        # Validar estado si viene
        nuevo_estado = datos.get("estado")
        if nuevo_estado is not None and nuevo_estado not in ESTADOS_VALIDOS:
            return None

        nueva_fecha = datos.get("fecha_reserva", reserva.fecha_reserva)
        estado_final = nuevo_estado if nuevo_estado is not None else reserva.estado

        # Si queda confirmada, revalidar
        if estado_final == "confirmada":
            # Revalidar duplicados (excluyendo esta misma reserva)
            if _existe_duplicado(
                session,
                reserva.id_miembro,
                reserva.id_clase,
                nueva_fecha,
                excluir_id=id_reserva,
            ):
                return None

            # Revalidar cupo si cambió el estado o la fecha
            cambia = (
                reserva.estado != "confirmada" or nueva_fecha != reserva.fecha_reserva
            )
            if cambia and not _hay_cupo(session, reserva.id_clase, nueva_fecha):
                return None

        # Aplicar cambios
        for key, value in datos.items():
            setattr(reserva, key, value.strip() if isinstance(value, str) else value)

        session.commit()
        session.refresh(reserva)

        return reserva

    except IntegrityError:
        session.rollback()
        return None

    finally:
        session.close()


def eliminar(id_reserva: UUID) -> bool:
    session = get_session()
    try:
        reserva = _buscar_por_id(session, id_reserva)
        if reserva is None:
            return False

        session.delete(reserva)
        session.commit()

        return True

    except IntegrityError:
        session.rollback()
        return False

    finally:
        session.close()
