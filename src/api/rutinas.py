from http import HTTPStatus
from typing import Any, Dict
from uuid import UUID
from fastapi import APIRouter, HTTPException
from src.api.schemas import (
    RutinaCreate,
    RutinaListResponse,
    RutinaRead,
    RutinaUpdate,
    RutinaPostResponse,
    RutinaPutResponse,
)
from src.crud import crud_rutina as rutina_crud

rutinas_router = APIRouter(prefix="/rutinas", tags=["rutinas"])


@rutinas_router.get("/miembro/{id_miembro}", response_model=RutinaListResponse)
def get_rutinas_por_miembro(id_miembro: UUID) -> Dict[str, Any]:
    """Obtiene todas las rutinas de un miembro específico."""
    rutinas = rutina_crud.listar_por_miembro(id_miembro)
    if not rutinas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron rutinas para este miembro",
        )
    return {
        "data": rutinas,
        "status": HTTPStatus.OK.value,
        "message": "Rutinas del miembro encontradas",
    }


@rutinas_router.get("/entrenador/{id_entrenador}", response_model=RutinaListResponse)
def get_rutinas_por_entrenador(id_entrenador: UUID) -> Dict[str, Any]:
    """Obtiene todas las rutinas diseñadas por un entrenador específico."""
    rutinas = rutina_crud.listar_por_entrenador(id_entrenador)
    if not rutinas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron rutinas para este entrenador",
        )
    return {
        "data": rutinas,
        "status": HTTPStatus.OK.value,
        "message": "Rutinas del entrenador encontradas",
    }


@rutinas_router.get("/", response_model=RutinaListResponse)
def get_rutinas() -> Dict[str, Any]:
    rutinas = rutina_crud.listar()
    if not rutinas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron rutinas",
        )
    return {
        "data": rutinas,
        "status": HTTPStatus.OK.value,
        "message": "Rutinas encontradas",
    }


@rutinas_router.get("/{id_rutina}", response_model=RutinaRead)
def obtener_rutina(id_rutina: UUID):
    rutina = rutina_crud.obtener_por_id(id_rutina)
    if rutina is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Rutina no encontrada",
        )
    return rutina


@rutinas_router.post(
    "/",
    response_model=RutinaPostResponse,
    status_code=HTTPStatus.CREATED.value,
)
def crear_rutina(datos: RutinaCreate):
    rutina = rutina_crud.crear(**datos.model_dump())
    if rutina is None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT.value,
            detail=(
                "No se pudo crear la rutina. "
                "Verifica que el miembro y el entrenador existan."
            ),
        )
    return {
        "data": rutina,
        "status": HTTPStatus.CREATED.value,
        "message": f"Rutina '{rutina.nombre}' creada",
    }


@rutinas_router.put("/{id_rutina}", response_model=RutinaPutResponse)
def actualizar_rutina(id_rutina: UUID, datos: RutinaUpdate):
    if rutina_crud.obtener_por_id(id_rutina) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Rutina no encontrada",
        )
    rutina = rutina_crud.actualizar(
        id_rutina,
        **datos.model_dump(exclude_unset=True),
    )
    if rutina is None:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Error al actualizar la rutina",
        )
    return {
        "data": rutina,
        "status": HTTPStatus.OK.value,
        "message": f"Rutina '{rutina.nombre}' actualizada",
    }


@rutinas_router.delete(
    "/{id_rutina}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_rutina(id_rutina: UUID):
    if not rutina_crud.eliminar(id_rutina):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Rutina no encontrada",
        )
