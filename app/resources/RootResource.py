from .Resource import Resource
import falcon

class RootResource(Resource):
    def on_get(self, req, resp):
        resp.media = {'message': f'Hello, world!'}