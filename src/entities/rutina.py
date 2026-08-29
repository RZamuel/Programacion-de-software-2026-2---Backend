from datetime import date


class Rutina:
    """Representa una rutina de ejercicios asignada a un miembro."""

    def __init__(
        self,
        id_rutina: int,
        id_miembro: int,
        id_entrenador: int,
        nombre: str,
        descripcion: str,
        fecha_creacion: date,
    ):
        """Inicializa una nueva instancia de Rutina."""
        self.id_rutina = id_rutina
        self.id_miembro = id_miembro
        self.id_entrenador = id_entrenador
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion

    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        return f"Rutina(ID: {self.id_rutina}, Nombre: {self.nombre})"
