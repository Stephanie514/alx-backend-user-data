#!/usr/bin/env python3
"""
API module
"""
from flask import Flask, jsonify, request, abort
from os import getenv
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
from flasgger import Swagger
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

# Create an instance of Flask
app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
Swagger(app)

auth_type = getenv('AUTH_TYPE')

# Importing SessionAuth if AUTH_TYPE is session_auth
if auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
else:
    auth = BasicAuth()


@app.before_request
def before_request_func():
    """
    Filter requests based on the authentication method
    """
    if auth is None:
        return

    if not auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/']):
        return

    if not auth.authorization_header(request) and \
       not auth.session_cookie(request):
        abort(401)

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Calls storage.close() on teardown
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    404 error handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """
    401 error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    403 error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request_handler():
    """ Before request handler to filter each request """
    if auth is None:
        return
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
        '/api/v1/auth_session/login/'
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


@app.before_request
def before_request():
    """Runs before each request"""
    excluded_paths = ['/api/v1/auth_session/login/']

    if request.path in excluded_paths:
        return None

    if auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        abort(401)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
