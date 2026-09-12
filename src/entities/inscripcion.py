import uuid
from datetime import date

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Inscripcion(Base):
    __tablename__ = "inscripciones"

    id_inscripcion: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )

    id_miembro: Mapped[uuid.UUID] = mapped_column(ForeignKey("miembros.id_miembro"))

    id_membresia: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("membresias.id_membresia")
    )

    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_fin: Mapped[date] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(20), default="activa")

    def __str__(self) -> str:
        return (
            f"Inscripcion(ID: {self.id_inscripcion}, "
            f"Miembro: {self.id_miembro}, "
            f"Estado: {self.estado})"
        )
