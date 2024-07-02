import falcon


from .auth import JWTAuthMiddleware
from .config import Config


def create_app():
    config = Config()
    app = falcon.App(middleware=[JWTAuthMiddleware(config)])

    return app
