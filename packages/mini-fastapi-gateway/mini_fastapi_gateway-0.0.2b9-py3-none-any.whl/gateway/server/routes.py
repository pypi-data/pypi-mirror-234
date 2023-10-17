from copy import deepcopy
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from gateway.server.core.database import get_db
from gateway.server.core.database.crud import CRUD
from gateway.server.core.database.models import Microservice, Scope
from gateway.server.core.database.schemas import (
    MicroserviceCreate,
    ScopeCreate,
    ScopeRead,
    MicroserviceRead,
    ScopeUpdate,
    MicroserviceUpdate
)
from gateway.server.utils.router import delete_cache, cache

gateway_router = APIRouter()


@gateway_router.get(
    '/api/v1/microservice',
    response_model=list[MicroserviceRead],
    tags=["Microservice Settings"])
async def get_microservices(db: Session = Depends(get_db)):
    microservice_crud = CRUD(Microservice)
    return microservice_crud.get_multi(db)


@gateway_router.get(
    '/api/v1/microservice/{microservice_id}',
    response_model=MicroserviceRead,
    tags=["Microservice Settings"])
async def get_microservice(microservice_id: int, db: Session = Depends(get_db)):
    microservice_crud = CRUD(Microservice)
    return microservice_crud.get(db, pk=microservice_id)


@gateway_router.post(
    '/api/v1/microservice',
    response_model=MicroserviceRead,
    tags=["Microservice Settings"])
async def create_microservice(microservice: MicroserviceCreate, db: Session = Depends(get_db)):
    microservice_crud = CRUD(Microservice)
    return microservice_crud.create(db, obj_in=microservice)


@gateway_router.put(
    '/api/v1/microservice/{microservice_id}',
    response_model=MicroserviceRead,
    tags=["Microservice Settings"])
async def update_microservice(microservice_id: int, microservice: MicroserviceUpdate,
                              db: Session = Depends(get_db)):
    microservice_crud = CRUD(Microservice)
    db_obj = microservice_crud.get(db, pk=microservice_id)
    return microservice_crud.update(db, db_obj=db_obj, obj_in=microservice)


@gateway_router.delete(
    '/api/v1/microservice/{microservice_id}',
    response_model=MicroserviceRead,
    tags=["Microservice Settings"])
async def delete_microservice(microservice_id: int, db: Session = Depends(get_db)):
    microservice_crud = CRUD(Microservice)
    return microservice_crud.remove(db, pk=microservice_id)


@gateway_router.get(
    '/api/v1/scope',
    response_model=list[ScopeRead],
    tags=["Scope Settings"])
async def get_scopes(db: Session = Depends(get_db)):
    scope_crud = CRUD(Scope)
    return scope_crud.get_multi(db)


@gateway_router.get(
    '/api/v1/scope/{scope_id}',
    response_model=ScopeRead,
    tags=["Scope Settings"])
async def get_scope(scope_id: int, db: Session = Depends(get_db)):
    scope_crud = CRUD(Scope)
    return scope_crud.get(db, pk=scope_id)


@gateway_router.post(
    '/api/v1/scope',
    response_model=ScopeRead,
    tags=["Scope Settings"])
async def create_scope(scope: ScopeCreate, db: Session = Depends(get_db)):
    scope_crud = CRUD(Scope)
    db_obj = scope_crud.create(db, obj_in=scope)
    delete_cache(db_obj)
    return db_obj


@gateway_router.put(
    '/api/v1/scope/{scope_id}',
    response_model=ScopeRead,
    tags=["Scope Settings"])
async def update_scope(scope_id: int, scope: ScopeUpdate, db: Session = Depends(get_db)):
    scope_crud = CRUD(Scope)
    db_obj = scope_crud.get(db, pk=scope_id)
    delete_cache(db_obj)
    return scope_crud.update(db, db_obj=db_obj, obj_in=scope)


@gateway_router.delete(
    '/api/v1/scope/{scope_id}',
    response_model=ScopeRead,
    tags=["Scope Settings"])
async def delete_scope(scope_id: int, db: Session = Depends(get_db)):
    scope_crud = CRUD(Scope)
    return scope_crud.remove(db, pk=scope_id)


@gateway_router.get(
    '/api/cache/clear',
    tags=["Cache Settings"])
async def clear_cache():
    # clear all caches
    _cache = deepcopy(cache)
    for cache_name in _cache.keys():
        del cache[cache_name]
    return {"message": "Cache cleared"}