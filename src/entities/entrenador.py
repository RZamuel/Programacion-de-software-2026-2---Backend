class Entrenador:
    """Representa a un entrenador del gimnasio."""

    def __init__(
        self,
        id_entrenador: int,
        nombre: str,
        apellido: str,
        especialidad: str,
        telefono: str,
        salario: float,
    ) -> None:
        """Inicializa una nueva instancia de Entrenador."""
        self.id_entrenador = id_entrenador
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.telefono = telefono
        self.salario = salario

    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        return (
            f"Entrenador(ID: {self.id_entrenador}, "
            f"Nombre: {self.nombre} {self.apellido})"
        )
