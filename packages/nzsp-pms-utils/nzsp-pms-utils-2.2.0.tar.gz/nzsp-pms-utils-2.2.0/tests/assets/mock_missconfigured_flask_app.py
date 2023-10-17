import os
from flask import Flask, g, Response
from nzsp_pms_utils.middleware import verify_authorization

def create_app():
    app = Flask(__name__)

    app.before_request(verify_authorization)

    @app.route('/')
    def mock_route():
        return Response(status=200)

    return app