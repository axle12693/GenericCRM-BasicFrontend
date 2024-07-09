from .Resource import Resource
import falcon
import json
import requests  # Assuming you are using requests to make HTTP calls


class AuthResource(Resource):
    def on_get_login(self, req, resp):
        # Assuming the login page is a static HTML file or a template rendered as HTML
        session_id = req.context.get("session_id")
        token = self.config.redis_client.get(f"Session:{session_id};JWT")
        if token:
            raise falcon.redirects.HTTPFound(location=req.scheme + "://" + req.netloc)
        csrf = req.context["current_CSRF"]
        login_page_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login</title>
        </head>
        <body>
            <h1>Login Page</h1>
            <form method="POST" action="/login">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username"><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password"><br>
                <input type="submit" value="Login">
                <input type="hidden" name="CSRF-Token" value="{csrf}">
            </form>
        </body>
        </html>
        """
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = login_page_html

    def on_post_login(self, req, resp):
        body = req.media
        protocol = "https://" if self.config.backend_https else "http://"
        response = requests.post(f"{protocol}{self.config.backend_url}/login", json=body)
        if response.status_code == 200:
            session_id = req.context.get("session_id")
            self.config.redis_client.set(f"Session:{session_id};JWT", response.text, ex=60 * 60)
            raise falcon.redirects.HTTPFound(location=req.scheme + "://" + req.netloc)
        else:
            resp.status = falcon.HTTP_401
            resp.body = json.dumps({'error': 'Authentication failed'})

    def on_get_register(self, req, resp):
        # Assuming the register page is a static HTML file or a template rendered as HTML
        csrf = req.context["current_CSRF"]
        register_page_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Register</title>
        </head>
        <body>
            <h1>Register Page</h1>
            <form method="POST" action="/register">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username"><br>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email"><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password"><br>
                <input type="submit" value="Register">
                <input type="hidden" name="CSRF-Token" value="{csrf}">
            </form>
        </body>
        </html>
        """
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = register_page_html

    def on_post_register(self, req, resp):
        try:
            body = req.media
            protocol = "https://" if self.config.backend_https else "http://"
            response = requests.post(f"{protocol}{self.config.backend_url}/register", json=body)
            if response.status_code == 201:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps({'message': 'Registration successful'})
            elif response.status_code == 409:
                resp.status = falcon.HTTP_409
                resp.body = json.dumps({'error': 'User already exists'})
            else:
                resp.status = falcon.HTTP_400
                resp.body = json.dumps({'error': 'Registration failed'})
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.body = json.dumps({'error': str(e)})
