from datetime import date


class Pago:
    """Representa un pago realizado por un miembro."""

    def __init__(
        self,
        id_pago: int,
        id_miembro: int,
        monto: float,
        fecha_pago: date,
        metodo_pago: str,
        concepto: str,
    ):
        """Inicializa una nueva instancia de Pago."""
        self.id_pago = id_pago
        self.id_miembro = id_miembro
        self.monto = monto
        self.fecha_pago = fecha_pago
        self.metodo_pago = metodo_pago
        self.concepto = concepto

    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        return (
            f"Pago(ID: {self.id_pago}, "
            f"Monto: ${self.monto}, "
            f"Concepto: {self.concepto})"
        )
