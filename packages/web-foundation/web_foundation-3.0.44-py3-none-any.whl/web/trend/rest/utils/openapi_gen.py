import os, os.path
from json import dump, load

import loguru
from sanic import Request, json, Sanic
from sanic_routing import Route
from sanic_ext.config import add_fallback_config
from sanic_ext.extensions.openapi.blueprint import blueprint_factory
from sanic_ext.extensions.openapi.builders import SpecificationBuilder
from sanic_ext.extensions.openapi import extension

from web import settings


def generate_openapi(sanic: Sanic, json_filepath: str | None):
    """
    Generate openapi json
    NOTE: After generation you can't start _sanic app

    """
    settings.OPENAPI = True
    sanic.router.open_api = True

    sanic.router.set_routes(None)
    sanic.finalize()
    sanic.config = add_fallback_config(sanic)
    oas_bp = blueprint_factory(sanic.config)
    for listener in oas_bp._future_listeners:
        if "build_spec" == listener.listener.__name__:
            listener.listener(sanic, None)
    oas_json = SpecificationBuilder().build(sanic).serialize()
    if not json_filepath:
        try:
            if hasattr(sanic.router.conf, "openapi_filepath") and sanic.router.conf.openapi_filepath:
                json_filepath = sanic.router.conf.openapi_filepath
            else:
                raise Exception("openapi_filepath not set in config")
        except RuntimeError:
            raise Exception("openapi_filepath not set in config")
    with open(json_filepath, 'w') as f:
        dump(oas_json, f)


def add_openapi(sanic: Sanic, openapi_filepath: str):
    """
    Overwrite Openapi _sanic extension startup method for reading openapi json from file

    """
    if not openapi_filepath:
        sanic.router.open_api = False
        sanic.config.OAS = False
        return
    if not os.path.exists(openapi_filepath):
        loguru.logger.error('OPENAPI FILE NOT FOUND')
        sanic.router.open_api = False
        sanic.config.OAS = False
        return

    sanic.router.open_api = True
    sanic.config.OAS = True

    async def spec(request: Request):
        with open(openapi_filepath) as f:
            return json(load(f))

    if hasattr(sanic.config, "OAS_URL_PREFIX") and hasattr(sanic.config, "OAS_URI_TO_JSON"):
        for route_path, route in sanic.router.routes_all.items():
            route: Route
            if route.uri == f"{sanic.config.OAS_URL_PREFIX}{sanic.config.OAS_URI_TO_JSON}":
                route.handler = spec

    def startup(self, bootstrap) -> None:
        if self.app.config.OAS:
            self.bp = blueprint_factory(self.app.config)
            for route in self.bp._future_routes:
                if route.uri == self.app.config.OAS_URI_TO_JSON:
                    self.bp._future_routes.remove(route)
                    self.bp.add_route(spec, self.app.config.OAS_URI_TO_JSON)
                    break
            for listener in self.bp._future_listeners:
                if "build_spec" == listener.listener.__name__:
                    self.bp._future_listeners.remove(listener)
            self.app.blueprint(self.bp)
            bootstrap._openapi = SpecificationBuilder()

    extension.OpenAPIExtension.startup = startup
