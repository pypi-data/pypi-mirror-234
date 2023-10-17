import os
from flask import Flask, g, Response
from nzsp_pms_utils.middleware import verify_authorization

def create_app():
    app = Flask(__name__)

    @app.before_request
    def set_service_variables_globally():
        """
        Set the service variables globally
        """
        app.logger.debug("Service variables were initialized")
        g.service_name = 'utils-middleware-test'

    app.before_request(verify_authorization)

    @app.route('/')
    def mock_route():
        return Response(status=200)

    return app