from datetime import date


class Inscripcion:
    """Representa la inscripción de un miembro a una membresía."""

    def __init__(
        self,
        id_inscripcion: int,
        id_miembro: int,
        id_membresia: int,
        fecha_inicio: date,
        fecha_fin: date,
        estado: str = "activa",
    ):
        """Inicializa una nueva instancia de Inscripcion."""
        self.id_inscripcion = id_inscripcion
        self.id_miembro = id_miembro
        self.id_membresia = id_membresia
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        return (
            f"Inscripcion(ID: {self.id_inscripcion}, "
            f"Miembro: {self.id_miembro}, Estado: {self.estado})"
        )
