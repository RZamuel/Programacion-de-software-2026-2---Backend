from datetime import date


class Miembro:

    def __init__(
        self,
        id_miembro: int,
        nombre: str,
        apellido: str,
        email: str,
        telefono: str,
        fecha_registro: date,
    ):
        self.id_miembro = id_miembro
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.fecha_registro = fecha_registro

    def __str__(self) -> str:
        return f"Miembro(ID: {self.id_cliente}, Nombre: {self.nombre} {self.apellido})"
