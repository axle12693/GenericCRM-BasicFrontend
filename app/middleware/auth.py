import falcon
import secrets
import base64
import hmac


def generate_token():
    token = secrets.token_bytes(64)
    encoded_token = base64.b64encode(token).decode('utf-8')
    return encoded_token


class CSRFMiddleware:

    def __init__(self, config):
        self.config = config

    def set_csrf_token(self, req, resp):
        session_id = req.context["session_id"]
        cookie_token = generate_token()
        resp.set_cookie("CSRF-Token", cookie_token, max_age=60 * 60, secure=True, http_only=True, same_site="Lax")
        self.config.redis_client.set(f"Session:{session_id};CSRF", cookie_token, ex=60 * 60)
        return cookie_token

    def process_request(self, req, resp):
        session_id = req.context["session_id"]
        if not session_id:
            raise falcon.HTTPInternalServerError()
        req.context['CSRF-Valid'] = False
        if req.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            cookie_token = req.get_cookie("CSRF-Token")
            form_token = req.media.get("CSRF-Token") if req.media else None
            if form_token and hmac.compare_digest(cookie_token, form_token):
                redis_token = self.config.redis_client.get(f"Session:{session_id};CSRF")
                if hmac.compare_digest(form_token, redis_token):
                    req.context["CSRF-Valid"] = True

            if not req.context["CSRF-Valid"]:
                self.set_csrf_token(req, resp)
                raise falcon.HTTPForbidden(description='Invalid or missing CSRF token.')
        else:
            self.set_csrf_token(req, resp)


class SessionMiddleware:
    def __init__(self, config):
        self.config = config

    def process_request(self, req, resp):
        session = req.get_cookie("session")
        if session:
            if self.config.redis_client.get("Session:" + session) == "valid":
                req.context["session_id"] = session
        else:
            session_id = generate_token()
            self.config.redis_client.set("Session:" + session_id, 'valid', ex=60 * 60 * 24 * 14)
            resp.set_cookie("session", session_id, max_age=60 * 60 * 24 * 14, secure=True, http_only=True, same_site="Lax")
            req.context["session_id"] = session_id
