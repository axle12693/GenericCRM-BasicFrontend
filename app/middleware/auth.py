import falcon
import secrets
import base64

def generate_token():
    token = secrets.token_bytes(64)
    encoded_token = base64.b64encode(token).decode('utf-8')
    return encoded_token

class CSRFMiddleware:

    def __init__(self, config):
        self.config = config

    def set_csrf_token(self, resp):
        cookie_token = generate_token()
        resp.set_cookie("CSRF-Token", cookie_token, max_age=60 * 60 * 24 * 14, secure=True, http_only=True, same_site="Lax")
        self.config.redis_client.set("CSRF:" + cookie_token, 'valid', ex=60 * 60 * 24 * 14)
        return cookie_token

    def process_request(self, req, resp):
        req.context['CSRF-Valid'] = False
        if req.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            cookie_token = req.get_cookie("CSRF-Token")
            form_token = req.media.get("CSRF-Token") if req.media else None
            if form_token and form_token == cookie_token:
                if self.config.redis_client.get("CSRF:" + form_token) == 'valid':
                    req.context["CSRF-Valid"] = True

            if not req.context["CSRF-Valid"]:
                self.set_csrf_token(resp)
                raise falcon.HTTPForbidden(description='Invalid or missing CSRF token.')
        else:
            self.set_csrf_token(resp)




