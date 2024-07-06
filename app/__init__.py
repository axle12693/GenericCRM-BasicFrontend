import falcon

from app.resources.RootResource import RootResource
from app.middleware.auth import CSRFMiddleware
from .config import Config


def create_app():
    config = Config()
    root_resource = RootResource(config)
    app = falcon.App(middleware=[CSRFMiddleware(config)])
    app.add_route("/", root_resource)
    return app
