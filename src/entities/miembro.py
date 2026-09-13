import uuid
from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Miembro(Base):
    __tablename__ = "miembros"

    id_miembro: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(80))
    apellido: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    telefono: Mapped[str] = mapped_column(String(20))
    fecha_registro: Mapped[date] = mapped_column(Date, default=date.today)

    def __str__(self) -> str:
        return f"Miembro(ID: {self.id_miembro}, Nombre: {self.nombre} {self.apellido})"
