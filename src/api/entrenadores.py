from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    EntrenadorCreate,
    EntrenadorListResponse,
    EntrenadorRead,
    EntrenadorUpdate,
    EntrenadorPostResponse,
    EntrenadorPutResponse,
)
from src.crud import crud_entrenador as entrenador_crud

entrenadores_router = APIRouter(prefix="/entrenadores", tags=["entrenadores"])


@entrenadores_router.get("/", response_model=EntrenadorListResponse)
def get_entrenadores() -> Dict[str, Any]:
    entrenadores = entrenador_crud.listar()

    if not entrenadores:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron entrenadores",
        )

    return {
        "data": entrenadores,
        "status": HTTPStatus.OK.value,
        "message": "Entrenadores encontrados",
    }


@entrenadores_router.get("/{id_entrenador}", response_model=EntrenadorRead)
def obtener_entrenador(id_entrenador: UUID):
    entrenador = entrenador_crud.obtener_por_id(id_entrenador)
    if entrenador is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Entrenador no encontrado",
        )
    return entrenador


@entrenadores_router.post(
    "/",
    response_model=EntrenadorPostResponse,
    status_code=HTTPStatus.CREATED.value,
)
def crear_entrenador(datos: EntrenadorCreate):
    entrenador = entrenador_crud.crear(**datos.model_dump())

    if entrenador is None:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Error al crear el entrenador",
        )

    return {
        "data": entrenador,
        "status": HTTPStatus.CREATED.value,
        "message": f"Entrenador {entrenador.nombre} {entrenador.apellido} creado",
    }


@entrenadores_router.put("/{id_entrenador}", response_model=EntrenadorPutResponse)
def actualizar_entrenador(id_entrenador: UUID, datos: EntrenadorUpdate):
    if entrenador_crud.obtener_por_id(id_entrenador) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Entrenador no encontrado",
        )

    entrenador = entrenador_crud.actualizar(
        id_entrenador,
        **datos.model_dump(exclude_unset=True),
    )
    if entrenador is None:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Error al actualizar el entrenador",
        )

    return {
        "data": entrenador,
        "status": HTTPStatus.OK.value,
        "message": f"Entrenador {entrenador.nombre} {entrenador.apellido} actualizado",
    }


@entrenadores_router.delete(
    "/{id_entrenador}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_entrenador(id_entrenador: UUID):
    if not entrenador_crud.eliminar(id_entrenador):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Entrenador no encontrado o tiene clases/rutinas asociadas",
        )
