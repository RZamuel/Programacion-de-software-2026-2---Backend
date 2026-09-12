import uuid

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Clase(Base):
    __tablename__ = "clases"

    id_clase: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    id_entrenador: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("entrenadores.id_entrenador")
    )

    nombre: Mapped[str] = mapped_column(String(80))
    dia_semana: Mapped[str] = mapped_column(String(20))
    hora: Mapped[str] = mapped_column(String(20))
    capacidad_maxima: Mapped[int] = mapped_column(Integer)

    def __str__(self) -> str:
        return (
            f"Clase(ID: {self.id_clase}, "
            f"Nombre: {self.nombre}, "
            f"Día: {self.dia_semana})"
        )
