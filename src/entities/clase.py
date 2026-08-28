class Clase:
    """Representa una clase grupal ofrecida en el gimnasio."""

    def __init__(
        self,
        id_clase: int,
        id_entrenador: int,
        nombre: str,
        dia_semana: str,
        hora: str,
        capacidad_maxima: int,
    ):
        """Inicializa una nueva instancia de Clase."""
        self.id_clase = id_clase
        self.id_entrenador = id_entrenador
        self.nombre = nombre
        self.dia_semana = dia_semana
        self.hora = hora
        self.capacidad_maxima = capacidad_maxima

    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        return (
            f"Clase(ID: {self.id_clase}, "
            f"Nombre: {self.nombre}, "
            f"Día: {self.dia_semana})"
        )
