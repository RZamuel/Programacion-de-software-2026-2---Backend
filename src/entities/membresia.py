from datetime import date


class Membresia:
    """Representa una membresía contratada por un miembro."""

    def __init__(
        self,
        id_membresia: int,
        id_miembro: int,
        tipo: str,
        precio: float,
        duracion_dias: int,
        fecha_inicio: date,
        estado: str = "activa",
    ) -> None:
        """Inicializa una nueva instancia de Membresia."""
        self.id_membresia = id_membresia
        self.id_miembro = id_miembro
        self.tipo = tipo
        self.precio = precio
        self.duracion_dias = duracion_dias
        self.fecha_inicio = fecha_inicio
        self.estado = estado

    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        return (
            f"Membresia(ID: {self.id_membresia}, "
            f"Miembro: {self.id_miembro}, "
            f"Tipo: {self.tipo}, "
            f"Estado: {self.estado})"
        )
