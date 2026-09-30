from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    InscripcionCreate,
    InscripcionListResponse,
    InscripcionRead,
    InscripcionUpdate,
    InscripcionPostResponse,
    InscripcionPutResponse,
)
from src.crud import crud_inscripcion as inscripcion_crud

inscripciones_router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])


@inscripciones_router.get("/", response_model=InscripcionListResponse)
def get_inscripciones() -> Dict[str, Any]:
    inscripciones = inscripcion_crud.listar()

    if not inscripciones:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron inscripciones",
        )

    return {
        "data": inscripciones,
        "status": HTTPStatus.OK.value,
        "message": "Inscripciones encontradas",
    }


@inscripciones_router.get(
    "/miembro/{id_miembro}",
    response_model=InscripcionListResponse,
)
def get_inscripciones_por_miembro(id_miembro: UUID) -> Dict[str, Any]:
    inscripciones = inscripcion_crud.listar_por_miembro(id_miembro)

    if not inscripciones:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron inscripciones para este miembro",
        )

    return {
        "data": inscripciones,
        "status": HTTPStatus.OK.value,
        "message": f"Inscripciones del miembro {id_miembro} encontradas",
    }


@inscripciones_router.get("/{id_inscripcion}", response_model=InscripcionRead)
def obtener_inscripcion(id_inscripcion: UUID):
    inscripcion = inscripcion_crud.obtener_por_id(id_inscripcion)
    if inscripcion is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Inscripción no encontrada",
        )
    return inscripcion


@inscripciones_router.post(
    "/",
    response_model=InscripcionPostResponse,
    status_code=HTTPStatus.CREATED.value,
)
def crear_inscripcion(datos: InscripcionCreate):
    inscripcion = inscripcion_crud.crear(**datos.model_dump())

    if inscripcion is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail=(
                "No se pudo crear la inscripción. "
                "Verifica que el miembro y la membresía existan, "
                "y que no haya una inscripción activa duplicada."
            ),
        )

    return {
        "data": inscripcion,
        "status": HTTPStatus.CREATED.value,
        "message": "Inscripción creada correctamente",
    }


@inscripciones_router.put("/{id_inscripcion}", response_model=InscripcionPutResponse)
def actualizar_inscripcion(id_inscripcion: UUID, datos: InscripcionUpdate):
    if inscripcion_crud.obtener_por_id(id_inscripcion) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Inscripción no encontrada",
        )

    inscripcion = inscripcion_crud.actualizar(
        id_inscripcion,
        **datos.model_dump(exclude_unset=True),
    )
    if inscripcion is None:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Error al actualizar la inscripción",
        )

    return {
        "data": inscripcion,
        "status": HTTPStatus.OK.value,
        "message": "Inscripción actualizada correctamente",
    }


@inscripciones_router.delete(
    "/{id_inscripcion}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_inscripcion(id_inscripcion: UUID):
    if not inscripcion_crud.eliminar(id_inscripcion):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Inscripción no encontrada",
        )
