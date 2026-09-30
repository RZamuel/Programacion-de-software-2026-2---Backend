from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID
from fastapi import APIRouter, HTTPException
from src.api.schemas import (
    ReservaClaseCreate,
    ReservaClaseListResponse,
    ReservaClaseRead,
    ReservaClaseUpdate,
    ReservaClasePostResponse,
    ReservaClasePutResponse,
)
from src.crud import crud_reserva_clase as reserva_crud

reservas_router = APIRouter(prefix="/reservas", tags=["reservas"])


@reservas_router.get("/miembro/{id_miembro}", response_model=ReservaClaseListResponse)
def get_reservas_por_miembro(id_miembro: UUID) -> Dict[str, Any]:
    """Obtiene todas las reservas de un miembro específico."""
    reservas = reserva_crud.listar_por_miembro(id_miembro)
    if not reservas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron reservas para este miembro",
        )
    return {
        "data": reservas,
        "status": HTTPStatus.OK.value,
        "message": "Reservas del miembro encontradas",
    }


@reservas_router.get("/clase/{id_clase}", response_model=ReservaClaseListResponse)
def get_reservas_por_clase(id_clase: UUID) -> Dict[str, Any]:
    """Obtiene todas las reservas de una clase específica."""
    reservas = reserva_crud.listar_por_clase(id_clase)
    if not reservas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron reservas para esta clase",
        )
    return {
        "data": reservas,
        "status": HTTPStatus.OK.value,
        "message": "Reservas de la clase encontradas",
    }


@reservas_router.get("/", response_model=ReservaClaseListResponse)
def get_reservas() -> Dict[str, Any]:
    reservas = reserva_crud.listar()
    if not reservas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron reservas",
        )
    return {
        "data": reservas,
        "status": HTTPStatus.OK.value,
        "message": "Reservas encontradas",
    }


@reservas_router.get("/{id_reserva}", response_model=ReservaClaseRead)
def obtener_reserva(id_reserva: UUID):
    reserva = reserva_crud.obtener_por_id(id_reserva)
    if reserva is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Reserva no encontrada",
        )
    return reserva


@reservas_router.post(
    "/",
    response_model=ReservaClasePostResponse,
    status_code=HTTPStatus.CREATED.value,
)
def crear_reserva(datos: ReservaClaseCreate):
    reserva = reserva_crud.crear(**datos.model_dump())
    if reserva is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail=(
                "No se pudo crear la reserva. Verifica que: "
                "el miembro y la clase existan, "
                "no haya duplicados, "
                "el estado sea válido, "
                "y haya cupo disponible."
            ),
        )
    return {
        "data": reserva,
        "status": HTTPStatus.CREATED.value,
        "message": "Reserva creada correctamente",
    }


@reservas_router.put("/{id_reserva}", response_model=ReservaClasePutResponse)
def actualizar_reserva(id_reserva: UUID, datos: ReservaClaseUpdate):
    if reserva_crud.obtener_por_id(id_reserva) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Reserva no encontrada",
        )
    reserva = reserva_crud.actualizar(
        id_reserva,
        **datos.model_dump(exclude_unset=True),
    )
    if reserva is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail=(
                "No se pudo actualizar. Verifica que: "
                "el estado sea válido, "
                "no haya duplicados, "
                "y haya cupo disponible."
            ),
        )
    return {
        "data": reserva,
        "status": HTTPStatus.OK.value,
        "message": "Reserva actualizada",
    }


@reservas_router.delete(
    "/{id_reserva}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_reserva(id_reserva: UUID):
    if not reserva_crud.eliminar(id_reserva):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Reserva no encontrada",
        )
