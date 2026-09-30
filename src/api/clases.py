from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    ClaseCreate,
    ClaseListResponse,
    ClaseRead,
    ClaseUpdate,
    ClasePostResponse,
    ClasePutResponse,
)
from src.crud import crud_clase as clase_crud

clases_router = APIRouter(prefix="/clases", tags=["clases"])


@clases_router.get("/", response_model=ClaseListResponse)
def get_clases() -> Dict[str, Any]:
    clases = clase_crud.listar()

    if not clases:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron clases",
        )

    return {
        "data": clases,
        "status": HTTPStatus.OK.value,
        "message": "Clases encontradas",
    }


@clases_router.get("/{id_clase}", response_model=ClaseRead)
def obtener_clase(id_clase: UUID):
    clase = clase_crud.obtener_por_id(id_clase)
    if clase is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Clase no encontrada",
        )
    return clase


@clases_router.post(
    "/",
    response_model=ClasePostResponse,
    status_code=HTTPStatus.CREATED.value,
)
def crear_clase(datos: ClaseCreate):
    clase = clase_crud.crear(**datos.model_dump())

    if clase is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail=("No se pudo crear la clase. " "Verifica que el entrenador exista."),
        )

    return {
        "data": clase,
        "status": HTTPStatus.CREATED.value,
        "message": f"Clase '{clase.nombre}' creada",
    }


@clases_router.put("/{id_clase}", response_model=ClasePutResponse)
def actualizar_clase(id_clase: UUID, datos: ClaseUpdate):
    if clase_crud.obtener_por_id(id_clase) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Clase no encontrada",
        )

    clase = clase_crud.actualizar(
        id_clase,
        **datos.model_dump(exclude_unset=True),
    )
    if clase is None:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Error al actualizar la clase",
        )

    return {
        "data": clase,
        "status": HTTPStatus.OK.value,
        "message": f"Clase '{clase.nombre}' actualizada",
    }


@clases_router.delete(
    "/{id_clase}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_clase(id_clase: UUID):
    if not clase_crud.eliminar(id_clase):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Clase no encontrada o tiene reservas asociadas",
        )
