from .Resource import Resource
import falcon
import json

class RootResource(Resource):
    def on_get(self, req, resp):
        session_id = req.context.get("session_id")
        jwt = self.config.redis_client.get(f"Session:{session_id};JWT")
        resp.media = {'message': f'Hello, {"user" if jwt else "world"}!'}