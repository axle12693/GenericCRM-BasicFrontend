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

    def process_request(self, req, resp):
        cookie_token = req.get_cookie("CSRF-Token")
        if cookie_token is None:
            cookie_token = generate_token()
            resp.set_cookie("CSRF-Token", cookie_token, max_age=60*60*24*14, secure=True, http_only=True, same_site="Lax")

        form_token = req.media.get("CSRF-Token")
        if form_token is not None and form_token == cookie_token:
            req.context["CSRF-Valid"] = True
        req.context['CSRF-Valid'] = False

