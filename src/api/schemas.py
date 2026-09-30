from typing import List, Literal
from uuid import UUID
from pydantic import BaseModel
from datetime import date


class MiembroCreate(BaseModel):
    primer_nombre: str
    segundo_nombre: str = ""
    primer_apellido: str
    segundo_apellido: str = ""
    nombre_usuario: str
    clave: str
    email: str
    telefono: str


class MiembroUpdate(BaseModel):
    primer_nombre: str | None = None
    segundo_nombre: str | None = None
    primer_apellido: str | None = None
    segundo_apellido: str | None = None
    nombre_usuario: str | None = None
    clave: str | None = None
    email: str | None = None
    telefono: str | None = None


class MiembroRead(BaseModel):
    id_miembro: UUID
    primer_nombre: str
    segundo_nombre: str
    primer_apellido: str
    segundo_apellido: str
    nombre_usuario: str
    email: str
    telefono: str


class MiembroLogin(BaseModel):
    nombre_usuario: str
    clave: str


# Schemas de respuesta (Wrappers)
class MiembroPostResponse(BaseModel):
    data: MiembroRead
    status: int
    message: str


class MiembroListResponse(BaseModel):
    data: List[MiembroRead]
    status: int
    message: str


class MiembroPutResponse(BaseModel):
    data: MiembroRead
    status: int
    message: str


# =====================================================================
# SCHEMAS DE MEMBRESÍA
# =====================================================================


class MembresiaCreate(BaseModel):
    tipo: str
    precio: float
    duracion_dias: int
    fecha_inicio: date | None = None
    estado: str = "activa"


class MembresiaUpdate(BaseModel):
    tipo: str | None = None
    precio: float | None = None
    duracion_dias: int | None = None
    fecha_inicio: date | None = None
    estado: str | None = None


class MembresiaRead(BaseModel):
    id_membresia: UUID
    tipo: str
    precio: float
    duracion_dias: int
    fecha_inicio: date
    estado: str


class MembresiaListResponse(BaseModel):
    data: List[MembresiaRead]
    status: int
    message: str


class MembresiaPostResponse(BaseModel):
    data: MembresiaRead
    status: int
    message: str


class MembresiaPutResponse(BaseModel):
    data: MembresiaRead
    status: int
    message: str


# =====================================================================
# SCHEMAS DE INSCRIPCIÓN
# =====================================================================


class InscripcionCreate(BaseModel):
    id_miembro: UUID
    id_membresia: UUID
    fecha_inicio: date
    estado: str = "activa"


class InscripcionUpdate(BaseModel):
    """Solo permite actualizar estado y fecha_inicio.
    fecha_fin se recalcula automáticamente en el CRUD."""

    estado: str | None = None
    fecha_inicio: date | None = None


class InscripcionRead(BaseModel):
    id_inscripcion: UUID
    id_miembro: UUID
    id_membresia: UUID
    fecha_inicio: date
    fecha_fin: date
    estado: str


class InscripcionListResponse(BaseModel):
    data: List[InscripcionRead]
    status: int
    message: str


class InscripcionPostResponse(BaseModel):
    data: InscripcionRead
    status: int
    message: str


class InscripcionPutResponse(BaseModel):
    data: InscripcionRead
    status: int
    message: str


# =====================================================================
# SCHEMAS DE ENTRENADOR
# =====================================================================


class EntrenadorCreate(BaseModel):
    nombre: str
    apellido: str
    especialidad: str
    telefono: str
    salario: float


class EntrenadorUpdate(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    especialidad: str | None = None
    telefono: str | None = None
    salario: float | None = None


class EntrenadorRead(BaseModel):
    id_entrenador: UUID
    nombre: str
    apellido: str
    especialidad: str
    telefono: str
    salario: float


class EntrenadorListResponse(BaseModel):
    data: List[EntrenadorRead]
    status: int
    message: str


class EntrenadorPostResponse(BaseModel):
    data: EntrenadorRead
    status: int
    message: str


class EntrenadorPutResponse(BaseModel):
    data: EntrenadorRead
    status: int
    message: str


# =====================================================================
# SCHEMAS DE CLASE
# =====================================================================


class ClaseCreate(BaseModel):
    id_entrenador: UUID
    nombre: str
    dia_semana: str
    hora: str
    capacidad_maxima: int


class ClaseUpdate(BaseModel):
    id_entrenador: UUID | None = None
    nombre: str | None = None
    dia_semana: str | None = None
    hora: str | None = None
    capacidad_maxima: int | None = None


class ClaseRead(BaseModel):
    id_clase: UUID
    id_entrenador: UUID
    nombre: str
    dia_semana: str
    hora: str
    capacidad_maxima: int


class ClaseListResponse(BaseModel):
    data: List[ClaseRead]
    status: int
    message: str


class ClasePostResponse(BaseModel):
    data: ClaseRead
    status: int
    message: str


class ClasePutResponse(BaseModel):
    data: ClaseRead
    status: int
    message: str


# =====================================================================
# SCHEMAS DE PAGO
# =====================================================================
class PagoCreate(BaseModel):
    id_miembro: UUID
    monto: float
    metodo_pago: str
    concepto: str
    fecha_pago: date | None = None


class PagoUpdate(BaseModel):
    monto: float | None = None
    metodo_pago: str | None = None
    concepto: str | None = None
    fecha_pago: date | None = None


class PagoRead(BaseModel):
    id_pago: UUID
    id_miembro: UUID
    monto: float
    fecha_pago: date
    metodo_pago: str
    concepto: str


class PagoListResponse(BaseModel):
    data: List[PagoRead]
    status: int
    message: str


class PagoPostResponse(BaseModel):
    data: PagoRead
    status: int
    message: str


class PagoPutResponse(BaseModel):
    data: PagoRead
    status: int
    message: str


# =====================================================================
# SCHEMAS DE RESERVA CLASE
# =====================================================================


class ReservaClaseCreate(BaseModel):
    id_miembro: UUID
    id_clase: UUID
    fecha_reserva: date
    estado: Literal["confirmada", "cancelada", "pendiente"] = "confirmada"


class ReservaClaseUpdate(BaseModel):
    estado: Literal["confirmada", "cancelada", "pendiente"] | None = None
    fecha_reserva: date | None = None


class ReservaClaseRead(BaseModel):
    id_reserva: UUID
    id_miembro: UUID
    id_clase: UUID
    fecha_reserva: date
    estado: str


class ReservaClaseListResponse(BaseModel):
    data: List[ReservaClaseRead]
    status: int
    message: str


class ReservaClasePostResponse(BaseModel):
    data: ReservaClaseRead
    status: int
    message: str


class ReservaClasePutResponse(BaseModel):
    data: ReservaClaseRead
    status: int
    message: str


# =====================================================================
# SCHEMAS DE RUTINA
# =====================================================================
class RutinaCreate(BaseModel):
    id_miembro: UUID
    id_entrenador: UUID
    nombre: str
    descripcion: str
    fecha_creacion: date | None = None


class RutinaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None


class RutinaRead(BaseModel):
    id_rutina: UUID
    id_miembro: UUID
    id_entrenador: UUID
    nombre: str
    descripcion: str
    fecha_creacion: date


class RutinaListResponse(BaseModel):
    data: List[RutinaRead]
    status: int
    message: str


class RutinaPostResponse(BaseModel):
    data: RutinaRead
    status: int
    message: str


class RutinaPutResponse(BaseModel):
    data: RutinaRead
    status: int
    message: str
