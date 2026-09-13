import uuid
from datetime import date

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class ReservaClase(Base):
    __tablename__ = "reservas_clase"

    id_reserva: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    id_miembro: Mapped[uuid.UUID] = mapped_column(ForeignKey("miembros.id_miembro"))

    id_clase: Mapped[uuid.UUID] = mapped_column(ForeignKey("clases.id_clase"))

    fecha_reserva: Mapped[date] = mapped_column(Date)
    estado: Mapped[str] = mapped_column(String(20), default="confirmada")

    def __str__(self) -> str:
        return (
            f"ReservaClase(ID: {self.id_reserva}, "
            f"Miembro: {self.id_miembro}, "
            f"Clase: {self.id_clase})"
        )
