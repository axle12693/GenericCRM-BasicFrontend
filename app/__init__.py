import falcon

from app.resources import RootResource, AuthResource
from app.middleware.auth import CSRFMiddleware, SessionMiddleware
from .config import Config


def create_app():
    config = Config()
    root_resource = RootResource(config)
    auth_resource = AuthResource(config)
    app = falcon.App(middleware=[SessionMiddleware(config), CSRFMiddleware(config)])
    app.add_route("/", root_resource)
    app.add_route("/login", auth_resource, suffix="login")
    app.add_route("/register", auth_resource, suffix="register")
    return app
