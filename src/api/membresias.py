from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    MembresiaCreate,
    MembresiaListResponse,
    MembresiaRead,
    MembresiaUpdate,
    MembresiaPostResponse,
    MembresiaPutResponse,
)
from src.crud import crud_membresia as membresia_crud

membresias_router = APIRouter(prefix="/membresias", tags=["membresias"])


@membresias_router.get("/", response_model=MembresiaListResponse)
def get_membresias() -> Dict[str, Any]:
    membresias = membresia_crud.listar()

    if not membresias:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron membresías",
        )

    return {
        "data": membresias,
        "status": HTTPStatus.OK.value,
        "message": "Membresías encontradas",
    }


@membresias_router.get("/{id_membresia}", response_model=MembresiaRead)
def obtener_membresia(id_membresia: UUID):
    membresia = membresia_crud.obtener_por_id(id_membresia)
    if membresia is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Membresía no encontrada",
        )
    return membresia


@membresias_router.post(
    "/",
    response_model=MembresiaPostResponse,
    status_code=HTTPStatus.CREATED.value,
)
def crear_membresia(datos: MembresiaCreate):
    membresia = membresia_crud.crear(**datos.model_dump())

    if membresia is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="Ya existe una membresía con ese tipo",
        )

    return {
        "data": membresia,
        "status": HTTPStatus.CREATED.value,
        "message": f"Membresía '{membresia.tipo}' creada",
    }


@membresias_router.put("/{id_membresia}", response_model=MembresiaPutResponse)
def actualizar_membresia(id_membresia: UUID, datos: MembresiaUpdate):
    if membresia_crud.obtener_por_id(id_membresia) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Membresía no encontrada",
        )

    membresia = membresia_crud.actualizar(
        id_membresia,
        **datos.model_dump(exclude_unset=True),
    )
    if membresia is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El tipo de membresía ya está en uso por otra",
        )

    return {
        "data": membresia,
        "status": HTTPStatus.OK.value,
        "message": f"Membresía '{membresia.tipo}' actualizada",
    }


@membresias_router.delete(
    "/{id_membresia}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_membresia(id_membresia: UUID):
    if not membresia_crud.eliminar(id_membresia):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Membresía no encontrada o tiene inscripciones asociadas",
        )
