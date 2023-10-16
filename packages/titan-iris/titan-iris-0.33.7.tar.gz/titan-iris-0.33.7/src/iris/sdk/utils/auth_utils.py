"""This module contains the authentication utils for the iris package."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import functools
import json
import logging
import os
import time
from pathlib import Path
from typing import Union

import jwt
import requests
import typer
from auth0.v3.authentication.token_verifier import (
    AsymmetricSignatureVerifier,
    TokenVerifier,
)
from requests import Response
from rich import print

from ..conf_manager import conf_mgr

# internal imports
from ..exception import (
    EndpointNotFoundError,
    InvalidLoginError,
    KeyFileDoesntExistError,
    KeyFileExpiredError,
)

# Logger config
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(conf_mgr.LOG_LEVEL)


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      Auth Utils                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def validate_token(id_token: str) -> None:
    """Verify the token and its precedence.

    Args:
        id_token (str): The token to be verified
    """
    jwks_url = f"https://{conf_mgr.AUTH0_DOMAIN}/.well-known/jwks.json"
    issuer = f"https://{conf_mgr.AUTH0_DOMAIN}/"
    sv = AsymmetricSignatureVerifier(jwks_url)
    tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=conf_mgr.AUTH0_CLIENT_ID)
    tv.verify(id_token)


def client_credentials_flow() -> None:
    """Runs the client credentials flow and stores the user object in the keyfile.

    Raises:
        InvalidLoginError: If there's an error during login
    """
    logger.debug("starting client_credentials_flow")
    client_id = conf_mgr.AUTH0_CLIENT_ID

    try:
        client_secret = os.environ["IRIS_AUTH0_CLIENT_SECRET"]
    except KeyError:
        raise InvalidLoginError(
            "IRIS_AUTH0_CLIENT_SECRET must be provided as an environment variable when client_credentials_flow is used"
        )

    url = f"https://{conf_mgr.AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": "https://seshat/",
        "grant_type": "client_credentials",
    }

    headers = {"content-type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    token_data = response.json()

    conf_mgr.access_token = token_data.get("access_token", None)
    conf_mgr.current_user = client_id


def device_authorization_flow() -> None:
    """Runs the device authorization flow and stores the user object in the keyfile.

    Prints (by design) since it's an interactive flow.
    """
    logger.debug("initiating device authorization flow")
    device_code_payload = {
        "client_id": conf_mgr.AUTH0_CLIENT_ID,
        "scope": "openid profile",
        "audience": conf_mgr.AUTH0_AUDIENCE,
    }
    logger.debug(
        f"Posting device code payload: {device_code_payload} to https://{conf_mgr.AUTH0_DOMAIN}/oauth/device/code"
    ),
    device_code_response = requests.post(
        f"https://{conf_mgr.AUTH0_DOMAIN}/oauth/device/code",
        data=device_code_payload,
    )

    if device_code_response.status_code != 200:
        print("Error generating the device code")
        raise typer.Exit(code=1)

    device_code_data = device_code_response.json()
    print(
        "1. On your computer or mobile device navigate to: ",
        device_code_data["verification_uri_complete"],
    )
    print("2. Enter the following code: ", device_code_data["user_code"])

    token_payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code_data["device_code"],
        "client_id": conf_mgr.AUTH0_CLIENT_ID,
    }

    authenticated = False
    time_waited = 0
    while not authenticated:
        logger.debug(f"Waiting for input... {time_waited}s")

        logger.debug(f"Posting {token_payload} to https://{conf_mgr.AUTH0_DOMAIN}/oauth/token")
        token_response = requests.post(f"https://{conf_mgr.AUTH0_DOMAIN}/oauth/token", data=token_payload)

        token_data = token_response.json()

        if token_response.status_code == 200:
            validate_token(token_data["id_token"])

            logger.debug("Token verified!")
            logger.debug("Decoding the id token")
            conf_mgr.current_user = jwt.decode(
                token_data["id_token"],
                algorithms=conf_mgr.ALGORITHMS,
                options={"verify_signature": False},
                audience=conf_mgr.AUTH0_CLIENT_ID,
            )
            logger.debug("Storing the access token")
            conf_mgr.access_token = token_data.get("access_token", None)
            authenticated = True
        elif token_data["error"] not in ("authorization_pending", "slow_down"):
            logger.debug("failed")
            print(token_data["error_description"])
            raise typer.Exit(code=1)
        else:
            time.sleep(device_code_data["interval"])
            time_waited += device_code_data["interval"]


def store_credentials(filename: Union[Path, str]) -> None:
    """Store the credentials in filename.

    Args:
        filename (Path | str): The filename in which to store the credentials.
    """
    json.dump(
        {"current_user": conf_mgr.current_user, "access_token": conf_mgr.access_token},
        open(filename, "w"),
    )


def load_credentials(filename: Union[Path, str]) -> None:
    """Load the credentials from filename.

    Args:
        filename (Path | str): The filename from which to load the credentials.

    Raises:
        KeyFileDoesntExistError: _description_
    """
    try:
        credentials = json.load(open(filename, "r"))
    except FileNotFoundError:
        logger.debug("Keyfile doesnt exist")
        raise KeyFileDoesntExistError

    conf_mgr.current_user = credentials["current_user"]
    conf_mgr.access_token = credentials["access_token"]


def auth(fn: callable):
    """A decorator to add the key from the storage to the function kwargs.

    Reruns the login flow on expiry

    Args:
        fn (callable): The function to decorate
    Returns:
        callable: The decorated function.
    """

    @functools.wraps(fn)
    def auth0_wrapper(*args, **kwargs):
        if conf_mgr.CREDENTIALS_FLOW == "device":
            try:
                logger.debug("Loading credentials from conf_mgr.CREDENTIALS_PATH")
                logger.debug(f"{conf_mgr.current_user}")
                load_credentials(conf_mgr.CREDENTIALS_PATH)

                expired = conf_mgr.current_user["exp"] < time.time()
                logger.debug(f"Expired: {expired}: {conf_mgr.current_user['exp']}, {time.time()}")
                if expired:
                    print("Credentials expired. Please login again.")
                    raise KeyFileExpiredError
            except (KeyFileDoesntExistError, KeyFileExpiredError):
                # if the keyfile doesn't exist, or the keyfile has expired, try and login
                try:
                    device_authorization_flow()
                except Exception as e:
                    # if we can't login, just reraise
                    raise e
                else:
                    # on successful login, store the credentials
                    store_credentials(conf_mgr.CREDENTIALS_PATH)  # store if no errors in login

        elif conf_mgr.CREDENTIALS_FLOW == "client_credentials":
            logger.info(f"authenticating with {conf_mgr.CREDENTIALS_FLOW} flow")
            # no storing credentials for client_credentials flow
            client_credentials_flow()
        else:
            raise ValueError(f"Flow {conf_mgr.CREDENTIALS_FLOW} not recognised")
        return fn(*args, **kwargs)

    @functools.wraps(fn)
    def dummy_wrapper(*args, **kwargs):
        """Dummy wrapper, if authenticate is disabled.

        Args:
            *args: The args to pass to the function
            **kwargs: The kwargs to pass to the function
        """
        logger.debug("in dummy wrapper")
        return fn(*args, **kwargs)

    # if conf_mgr.AUTHENTICATE is not set, then don't set the token
    # on the config manager, and don't send it on requests.
    # NOTE: This will likely cause those requests to fail.
    return auth0_wrapper if conf_mgr.AUTHENTICATE else dummy_wrapper


def handle_bad_response(response: Response, endpoint: str):
    """Given a bad response from endpoint, return an appropriate exception.

    Args:
        response (requests.Response): the response object
        endpoint (str): The endpoint that was queried for the response

    Returns:
        Exception: The exception to handle.
    """
    if response.status_code == 401:
        print(
            json.dumps(
                {
                    "status": 401,
                    "message": "Invalid login credentials. Are you logged in?",
                },
                indent=4,
            )
        )
        return InvalidLoginError
    elif response.status_code == 404:
        print(
            json.dumps(
                {
                    "status": 404,
                    "message": f"Endpoint {endpoint} not found",
                },
                indent=4,
            )
        )
        return EndpointNotFoundError(details=endpoint)
    elif response.status_code == 422:
        print(
            json.dumps(
                {
                    "status": 422,
                    "message": "Validation error",
                    "validation_errors": response.json(),
                },
                indent=4,
            )
        )
        raise Exception("Validation error")
    elif response.status_code == 500:
        print(json.dumps({"status": 500, "message": "Internal server error"}, indent=4))
        return Exception("Internal server error")
    else:
        try:
            response_content = response.json()
        except Exception:
            response_content = response.content
        print(
            json.dumps(
                {
                    "status": response.status_code,
                    "message": f"Received bad response, code {response.status_code}: \n{response_content}",
                },
                indent=4,
            )
        )
        return Exception(str(response))
