from datetime import date
import uuid

from database.connection import get_session
from entities.miembro import Miembro


def crear(
    nombre: str,
    apellido: str,
    email: str,
    telefono: str,
    fecha_registro: date | None = None,
) -> Miembro | None:
    """Crea un nuevo miembro."""

    session = get_session()

    try:
        # Evitar miembros con el mismo correo
        if session.query(Miembro).filter_by(email=email).first():
            return None

        miembro = Miembro(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            fecha_registro=(
                fecha_registro if fecha_registro is not None else date.today()
            ),
        )

        session.add(miembro)
        session.commit()
        session.refresh(miembro)

        return miembro

    except Exception:
        session.rollback()
        return None

    finally:
        session.close()


def listar() -> list[Miembro]:
    """Lista todos los miembros."""

    session = get_session()

    try:
        return session.query(Miembro).all()

    finally:
        session.close()


def obtener(id_miembro: uuid.UUID) -> Miembro | None:
    """Obtiene un miembro por su UUID."""

    session = get_session()

    try:
        return session.query(Miembro).filter_by(id_miembro=id_miembro).first()

    finally:
        session.close()


def actualizar(
    id_miembro: uuid.UUID,
    nombre: str | None = None,
    apellido: str | None = None,
    email: str | None = None,
    telefono: str | None = None,
) -> Miembro | None:
    """Actualiza los datos de un miembro."""

    session = get_session()

    try:
        miembro = session.query(Miembro).filter_by(id_miembro=id_miembro).first()

        if not miembro:
            return None

        # Si se cambia el email, verificar que no pertenezca
        # a otro miembro.
        if email is not None and email != miembro.email:
            email_existente = session.query(Miembro).filter_by(email=email).first()

            if email_existente:
                return None

            miembro.email = email

        if nombre is not None:
            miembro.nombre = nombre

        if apellido is not None:
            miembro.apellido = apellido

        if telefono is not None:
            miembro.telefono = telefono

        session.commit()
        session.refresh(miembro)

        return miembro

    except Exception:
        session.rollback()
        return None

    finally:
        session.close()


def eliminar(id_miembro: uuid.UUID) -> bool:
    """Elimina un miembro por su UUID."""

    session = get_session()

    try:
        miembro = session.query(Miembro).filter_by(id_miembro=id_miembro).first()

        if not miembro:
            return False

        session.delete(miembro)
        session.commit()

        return True

    except Exception:
        session.rollback()
        return False

    finally:
        session.close()
