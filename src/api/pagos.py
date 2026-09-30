from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID
from fastapi import APIRouter, HTTPException
from src.api.schemas import (
    PagoCreate,
    PagoListResponse,
    PagoRead,
    PagoUpdate,
    PagoPostResponse,
    PagoPutResponse,
)
from src.crud import crud_pago as pago_crud

pagos_router = APIRouter(prefix="/pagos", tags=["pagos"])


@pagos_router.get("/", response_model=PagoListResponse)
def get_pagos() -> Dict[str, Any]:
    pagos = pago_crud.listar()
    if not pagos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron pagos",
        )
    return {
        "data": pagos,
        "status": HTTPStatus.OK.value,
        "message": "Pagos encontrados",
    }


@pagos_router.get("/{id_pago}", response_model=PagoRead)
def obtener_pago(id_pago: UUID):
    pago = pago_crud.obtener_por_id(id_pago)
    if pago is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Pago no encontrado",
        )
    return pago


@pagos_router.post(
    "/",
    response_model=PagoPostResponse,
    status_code=HTTPStatus.CREATED.value,
)
def crear_pago(datos: PagoCreate):
    pago = pago_crud.crear(**datos.model_dump())
    if pago is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="No se pudo crear el pago. Verifica que el miembro exista.",
        )
    return {
        "data": pago,
        "status": HTTPStatus.CREATED.value,
        "message": f"Pago de ${pago.monto} registrado",
    }


@pagos_router.put("/{id_pago}", response_model=PagoPutResponse)
def actualizar_pago(id_pago: UUID, datos: PagoUpdate):
    if pago_crud.obtener_por_id(id_pago) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Pago no encontrado",
        )
    pago = pago_crud.actualizar(
        id_pago,
        **datos.model_dump(exclude_unset=True),
    )
    if pago is None:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Error al actualizar el pago",
        )
    return {
        "data": pago,
        "status": HTTPStatus.OK.value,
        "message": f"Pago actualizado",
    }


@pagos_router.delete(
    "/{id_pago}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_pago(id_pago: UUID):
    if not pago_crud.eliminar(id_pago):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Pago no encontrado",
        )
