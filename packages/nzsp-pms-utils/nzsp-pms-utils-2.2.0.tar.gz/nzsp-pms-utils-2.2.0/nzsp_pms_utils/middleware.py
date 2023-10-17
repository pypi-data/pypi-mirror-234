"""Contains NZSP PMS flask server middleware"""
import os
import requests
from requests.adapters import HTTPAdapter
import flask
from flask.wrappers import Response
from urllib3.util.retry import Retry


def verify_authorization() -> Response:
    """
    Verify authorization using Plant Managment system
    IAM Authorize API. if status 200 (OK), sets user_identifier
    and user_email globally.

    Returns
    -------
    Response
        if status different than 200 (OK), reponse status.

    Raises
    ------
    KeyError
        When service_name is not set globally.

    Notes
    -----
    - Requires to set up the service name globally in
    an application before request.
    - Requires to set up environment vatiable IAM_AUTHORIZE_API.

    See Also
    --------
    - Check PMS IAM documentation to know more about this middleware.

    Examples
    --------
    Setting up application before request
    >>> @app.before_request
    ... def set_service_name_globally():
    ...    g.service_name = SERVICE_NAME
    Calling it in a blueprint
    >>> from nzsp_pms_utils.middleware import verify_authorization
    ... bp.before_request(verify_authorization)
    """
    if not flask.request.method == "OPTIONS":
        if not flask.g.get("service_name"):
            raise KeyError(
                "service_name was not set globally," + "read the docs to get more info"
            )
        request_session = requests.session()
        retry = Retry(status=5, status_forcelist=frozenset({504}))
        adapter = HTTPAdapter(max_retries=retry)
        request_session.mount("http://", adapter)
        request_session.mount("https://", adapter)
        request_session.keep_alive = False
        iam_authorize_response = request_session.get(
            url=os.getenv("IAM_AUTHORIZE_API"),
            headers={
                "authorization": flask.request.headers.get("authorization"),
                "service_name": flask.g.get("service_name"),
                "action_name": flask.request.method + flask.request.path,
            },
            verify=False,
        )
        request_session.close()
        if iam_authorize_response.status_code == 200:
            json_response = iam_authorize_response.json()
            flask.g.user_identifier = json_response["user_identifier"]
            flask.g.user_email = json_response["user_email"]
        else:
            return flask.Response(status=iam_authorize_response.status_code)
