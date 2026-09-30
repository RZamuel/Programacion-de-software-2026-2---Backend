from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    MiembroCreate,
    MiembroListResponse,
    MiembroLogin,
    MiembroRead,
    MiembroUpdate,
    MiembroPostResponse,
    MiembroPutResponse,
)
from src.crud import crud_miembro as miembro_crud

miembros_router = APIRouter(prefix="/miembros", tags=["miembros"])


@miembros_router.get("/", response_model=MiembroListResponse)
def get_miembros() -> Dict[str, Any]:
    miembros = miembro_crud.listar()

    if not miembros:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron miembros"
        )

    return {
        "data": miembros,
        "status": HTTPStatus.OK.value,
        "message": "Miembros encontrados",
    }


@miembros_router.post("/login", response_model=MiembroRead)
def iniciar_sesion(datos: MiembroLogin):
    miembro = miembro_crud.obtener(datos.nombre_usuario, datos.clave)
    if miembro is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            detail="Nombre de usuario o clave incorrectos",
        )
    return miembro


@miembros_router.get("/{id_miembro}", response_model=MiembroRead)
def obtener_miembro(id_miembro: UUID):
    miembro = miembro_crud.obtener_por_id(id_miembro)
    if miembro is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Miembro no encontrado"
        )
    return miembro


@miembros_router.post(
    "/", response_model=MiembroPostResponse, status_code=HTTPStatus.CREATED.value
)
def crear_miembro(datos: MiembroCreate):
    miembro = miembro_crud.crear(**datos.model_dump())

    if miembro is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El nombre de usuario ya existe",
        )

    return {
        "data": miembro,
        "status": HTTPStatus.CREATED.value,
        "message": f"Miembro {miembro.nombre_usuario} creado",
    }


@miembros_router.put("/{id_miembro}", response_model=MiembroPutResponse)
def actualizar_miembro(id_miembro: UUID, datos: MiembroUpdate):
    if miembro_crud.obtener_por_id(id_miembro) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Miembro no encontrado"
        )

    miembro = miembro_crud.actualizar(
        id_miembro,
        **datos.model_dump(exclude_unset=True),
    )
    if miembro is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail="El nombre de usuario ya existe",
        )
    return {
        "data": miembro,
        "status": HTTPStatus.OK.value,
        "message": f"Miembro {miembro.nombre_usuario} actualizado",
    }


@miembros_router.delete("/{id_miembro}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_miembro(id_miembro: UUID):
    if not miembro_crud.eliminar(id_miembro):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Miembro no encontrado"
        )
