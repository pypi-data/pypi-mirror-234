from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List
from typing import cast

from pydantic import BaseModel

from web.trend.rest.utils.openapi_gen import generate_openapi

try:
    import orjson
    from sanic import Sanic
except ImportError:
    raise ImportError("poetry install --with rest")

from web import settings
from web.kernel.transport import Transport
from web.kernel.types import ConfAble, AppNameAble, ISocket, IService, TransportConf
from web.trend.rest.custom import CustomRouter, CustomErrorHandler, RouterConf


class SanicConf(BaseModel):
    access_log: bool | None = False
    noisy_exceptions: bool | None = False
    debug: bool = False


class SanicExtConf(BaseModel):
    params: SanicConf | None


class RestTransportConfig(TransportConf):
    sanic: SanicExtConf
    router: RouterConf | None


class RestTransport(Transport, AppNameAble, ConfAble[RestTransportConfig]):
    """
    Transport for serving REST API (via Sanic)
    """
    sanic: Sanic
    _router: CustomRouter

    def __init__(self,
                 services: List[IService],
                 routes: dict,
                 priority: int = 0, workers: int = 0, ignore_balance: bool = False
                 ):
        super().__init__(services, priority=priority, workers=workers, ignore_balance=ignore_balance)
        sanic_name = "__broken__name"
        if Sanic._app_registry.get(sanic_name):
            count = 1
            while Sanic._app_registry.get(sanic_name):
                sanic_name += str(count)
                count += 1
        self.sanic = Sanic(sanic_name,
                           loads=orjson.loads,
                           dumps=orjson.dumps,
                           error_handler=CustomErrorHandler())
        self._router = CustomRouter(routes)
        self._router.ctx.app = self.sanic
        self.sanic.router = self._router

    def generate_openapi_file(self, json_filepath: str | None = None):
        generate_openapi(self.sanic, json_filepath)

    def extend_routes(self, new_routes: dict[str, dict[str, dict]]):
        self._router.extend_routes(new_routes)

    async def run(self, socket: ISocket):
        self.sanic.name = self.app_name
        cast(CustomRouter, self.sanic.router).set_routes(self)

        start_args = self.conf.sanic.params.dict() if self.conf else {}
        if settings.DEBUG:
            start_args["debug"] = True
        server = await self.sanic.create_server(**start_args,
                                                sock=socket,
                                                return_asyncio_server=True)
        await server.startup()
        await server.before_start()
        await server.after_start()
        await server.serve_forever()
