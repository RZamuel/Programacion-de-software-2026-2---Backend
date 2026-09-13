import uuid
from datetime import date

from sqlalchemy import String, Float, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Pago(Base):
    __tablename__ = "pagos"

    id_pago: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    id_miembro: Mapped[uuid.UUID] = mapped_column(ForeignKey("miembros.id_miembro"))

    monto: Mapped[float] = mapped_column(Float)
    fecha_pago: Mapped[date] = mapped_column(Date, default=date.today)
    metodo_pago: Mapped[str] = mapped_column(String(50))
    concepto: Mapped[str] = mapped_column(String(100))

    def __str__(self) -> str:
        return (
            f"Pago(ID: {self.id_pago}, "
            f"Monto: ${self.monto}, "
            f"Concepto: {self.concepto})"
        )
