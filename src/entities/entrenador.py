import uuid

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Entrenador(Base):
    __tablename__ = "entrenadores"

    id_entrenador: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )

    nombre: Mapped[str] = mapped_column(String(80))
    apellido: Mapped[str] = mapped_column(String(80))
    especialidad: Mapped[str] = mapped_column(String(80))
    telefono: Mapped[str] = mapped_column(String(20))
    salario: Mapped[float] = mapped_column(Float)

    def __str__(self) -> str:
        return (
            f"Entrenador(ID: {self.id_entrenador}, "
            f"Nombre: {self.nombre} {self.apellido})"
        )
