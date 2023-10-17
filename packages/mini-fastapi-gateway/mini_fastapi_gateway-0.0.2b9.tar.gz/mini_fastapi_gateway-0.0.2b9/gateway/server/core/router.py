import cachetools
from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import selectinload

from gateway.server.core.database import SessionLocal
from gateway.server.core.database.models import Scope
from gateway.server.core.database.crud import CRUD
from gateway.server.core.decorators import to_microservice
from gateway.server.utils.router import make_route, get_params_from_path, cache


class ApiGateway(APIRouter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_routes_from_db()

    def add_routes_from_db(self):
        scope_crud = CRUD(Scope)
        with SessionLocal() as db:
            scopes = scope_crud.get_multi(db, options=[selectinload(Scope.microservice)])
            for scope in scopes:
                if scope.is_active:
                    params = get_params_from_path(scope.path)
                    func_name = scope.name.replace(' ', '_').lower()
                    api_method = getattr(self, scope.method.lower())
                    to_microservice(api_method, make_route(func_name, scope, params), scope)


class GatewayRouter(FastAPI):
    _route_len: int = 0

    async def __call__(self, scope, receive, send):
        if not self._route_len or cache.get("need_reload", False):
            api_router = ApiGateway()
            if self._route_len:
                for route in self.routes[-self._route_len:]:
                    self.routes.remove(route)
            self.include_router(api_router)
            self._route_len = len(api_router.routes)
            cache["need_reload"] = False
        await super().__call__(scope, receive, send)

    @cachetools.cached(cache, key=lambda *args: "openapi_cache")
    def openapi(self):
        self.openapi_schema = None # noqa
        return super().openapi()
