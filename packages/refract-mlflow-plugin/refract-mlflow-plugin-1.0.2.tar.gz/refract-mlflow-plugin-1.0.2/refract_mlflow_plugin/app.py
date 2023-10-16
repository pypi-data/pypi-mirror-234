"""
To run a tracking server with this app, use `mlflow server --app-name custom_app`.
"""
import os
import logging
import requests
# This would be all that plugin author is required to import
from mlflow.server import app as custom_app
from flask import Response, g, request
from mosaic_utils.ai.headers.utils import check_project_access

# Can do custom logging on either the app or logging itself
# but you'll possibly have to clear the existing handlers or there will be duplicate output
# See https://docs.python.org/3/howto/logging-cookbook.html

app_logger = logging.getLogger(__name__)

# Configure the app
custom_app.config["MY_VAR"] = "config-var"
app_logger.warning(f"Using {__name__}")
mlflow_ui_users = os.environ.get("MLFLOW_UI_USERS", "").split(",")
console_backend_uri = os.environ.get("CONSOLE_BACKEND_URI", "http://mosaic-console-backend/mosaic-console-backend")
authorization = str(os.environ.get("AUTHORIZATION", "true")).lower() == "true"
internal_server_error="Internal Server Error"
access_denied="Access Denied"


@custom_app.before_request
def before_req_hook():
    """A custom before request handler.
    Can implement things such as authentication, special handling, etc.
    """
    try:
        app_logger.warning("\nMiddleware Execution : ")
        app_logger.warning(request.url)
        app_logger.warning(request.headers)
        x_auth_username = request.headers.get("X-Auth-Username", "")
        if x_auth_username not in mlflow_ui_users \
                and "/ping" not in request.url\
                and authorization:
            app_logger.warning("Checking project access")
            x_project_id = request.headers.get("X-Project-Id", "")
            x_auth_userid = request.headers.get("X-Auth-Userid", "")
            x_auth_email = request.headers.get("X-Auth-Email", "")
            res = check_project_access(console_backend_uri,
                                       userid=x_auth_userid,
                                       email=x_auth_email,
                                       username=x_auth_username,
                                       project_id=x_project_id)
            app_logger.warning("RESPONSE : ")
            app_logger.warning(res)
            return res
        else:
            app_logger.warning("Skipping Authorization Checks")
    except ValueError as ex:
        app_logger.warning(ex)
        return access_denied, 403
    except Exception as ex:
        app_logger.warning(ex)
        return internal_server_error, 500

@custom_app.route("/ping", methods=["GET"])
def custom_endpoint():
    """A custom endpoint."""
    return "success", 200
