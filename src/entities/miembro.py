"""Modelo SQLAlchemy para la entidad Miembro."""

import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Miembro(Base):
    __tablename__ = "miembros"

    id_miembro: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    primer_nombre: Mapped[str] = mapped_column(String(80))
    segundo_nombre: Mapped[str] = mapped_column(String(80), default="")
    primer_apellido: Mapped[str] = mapped_column(String(80))
    segundo_apellido: Mapped[str] = mapped_column(String(80), default="")
    nombre_usuario: Mapped[str] = mapped_column(String(80), unique=True)
    clave: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    telefono: Mapped[str] = mapped_column(String(20))


def __str__(self) -> str:
    return f"Miembro(ID: {self.id_miembro}, Usuario: {self.nombre_usuario}, Nombre: {self.primer_nombre} {self.primer_apellido})"
