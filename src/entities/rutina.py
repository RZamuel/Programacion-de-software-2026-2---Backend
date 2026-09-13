import uuid
from datetime import date

from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Rutina(Base):
    __tablename__ = "rutinas"

    id_rutina: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    id_miembro: Mapped[uuid.UUID] = mapped_column(ForeignKey("miembros.id_miembro"))

    id_entrenador: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("entrenadores.id_entrenador")
    )

    nombre: Mapped[str] = mapped_column(String(80))
    descripcion: Mapped[str] = mapped_column(Text)
    fecha_creacion: Mapped[date] = mapped_column(Date, default=date.today)

    def __str__(self) -> str:
        return f"Rutina(ID: {self.id_rutina}, Nombre: {self.nombre})"
