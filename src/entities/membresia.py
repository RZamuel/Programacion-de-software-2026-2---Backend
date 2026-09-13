import uuid
from datetime import date

from sqlalchemy import String, Float, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Membresia(Base):
    __tablename__ = "membresias"

    id_membresia: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )

    tipo: Mapped[str] = mapped_column(String(50))
    precio: Mapped[float] = mapped_column(Float)
    duracion_dias: Mapped[int] = mapped_column(Integer)
    fecha_inicio: Mapped[date] = mapped_column(Date, default=date.today)
    estado: Mapped[str] = mapped_column(String(20), default="activa")

    def __str__(self) -> str:
        return f"Membresia(ID: {self.id_membresia}, " f"Tipo: {self.tipo})"
