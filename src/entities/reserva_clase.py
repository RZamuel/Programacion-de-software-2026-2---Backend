from datetime import date


class ReservaClase:
    """Representa la reserva de un miembro a una clase específica."""

    def __init__(
        self,
        id_reserva: int,
        id_miembro: int,
        id_clase: int,
        fecha_reserva: date,
        estado: str = "confirmada",
    ):
        """Inicializa una nueva instancia de ReservaClase."""
        self.id_reserva = id_reserva
        self.id_miembro = id_miembro
        self.id_clase = id_clase
        self.fecha_reserva = fecha_reserva
        self.estado = estado

    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        return f"ReservaClase(ID: {self.id_reserva}, Miembro: {self.id_miembro}, Clase: {self.id_clase})"
