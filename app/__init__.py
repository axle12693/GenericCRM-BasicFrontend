import falcon


from .auth import CSRFMiddleware
from .config import Config


def create_app():
    config = Config()
    app = falcon.App(middleware=[CSRFMiddleware(config)])

    return app
