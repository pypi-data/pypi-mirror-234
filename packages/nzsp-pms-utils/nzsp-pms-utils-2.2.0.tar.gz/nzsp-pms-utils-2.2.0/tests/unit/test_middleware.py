"""
Middleware functions integration test
"""
import unittest
from tests.assets.mock_flask_app import create_app
from tests.assets.mock_missconfigured_flask_app import (
    create_app as create_missconfigured_app,
)
import unittest.mock as mock
from flask import g


class TestMiddleware(unittest.TestCase):
    """
    Test
    """

    @classmethod
    def setUpClass(self) -> None:
        app = create_app()
        app.config.update({"TESTING": True})
        self.app = app
        self.client = app.test_client()

    def test_verify_authorization_return_None_on_request_method_OPTIONS(self):
        """Return None on request method OPTIONS test"""
        response = self.client.options("/")
        self.assertEqual(response.status, "200 OK")

    def test_verify_authorization_raises_key_error(self):
        """Raises KeyError when no service_name set globally test"""
        app = create_missconfigured_app()
        app.config.update({"TESTING": True})
        client = app.test_client()
        with self.assertRaises(KeyError):
            client.get("/")

    @mock.patch("nzsp_pms_utils.middleware.requests")
    def test_verify_authorization_status_500(self, mock_requests):
        """Response jsonify status in status different that 200 test"""
        mock_requests.session.return_value.get.return_value.status_code = 500
        response = self.client.get("/")
        self.assertEqual(response.status, "500 INTERNAL SERVER ERROR")

    @mock.patch("nzsp_pms_utils.middleware.requests")
    def test_verify_authorization_status_200(self, mock_requests):
        """Assign user identifier globally in status 200 test"""
        user_identifier = "Test"
        user_email = "Test@danone.com"
        mock_requests.session.return_value.get.return_value.status_code = 200
        mock_requests.session.return_value.get.return_value.json.return_value = {
            "user_identifier": user_identifier,
            "user_email": user_email,
        }
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status, "200 OK")
            self.assertEqual(g.get("user_identifier"), user_identifier)
            self.assertEqual(g.get("user_email"), user_email)


if __name__ == "__main__":
    unittest.main()
