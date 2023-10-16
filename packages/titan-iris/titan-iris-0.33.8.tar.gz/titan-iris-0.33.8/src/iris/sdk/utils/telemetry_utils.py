"""This file contains the telemetry helper functions for the Iris package."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import functools
import json
from logging import getLogger
from typing import Callable

import requests

from ..conf_manager import conf_mgr

logger = getLogger("iris.utils.telemetry_utils")

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   Telemetry Utils                                                    #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def telemetry_decorator(function: Callable):
    """Decorator to send telemetry data to the metrics server."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # Nickname is only present if the user is logged in, and
        # if the user is _a user_ i.e. not a client credentials flow machine.
        nickname = (
            conf_mgr.current_user["nickname"]
            if conf_mgr.current_user is not None and "nickname" in conf_mgr.current_user
            else None
        )
        # if str(obj) (w/ obj in args) contains any of these strings, it won't be sent
        mask_args = ["Authorization"]

        # any kwargs with these keys won't be sent
        mask_kwargs = []

        url = conf_mgr.metrics_url

        try:
            func = function(*args, **kwargs)

            headers = {"Content-Type": "application/json"}
            headers.update({"Authorization": f"Bearer {conf_mgr.access_token}"})
            payload = {
                "username": nickname,
                "method": function.__name__,
                "args": tuple(str(i) for i in args if all(arg not in str(i) for arg in mask_args)),
                "kwargs": {k: v for k, v in kwargs.items() if all(arg not in k for arg in mask_kwargs)},
                "error": None,
            }
            requests.post(url=url, headers=headers, json=payload)

            return func
        except requests.exceptions.ConnectionError:  # a more understandable message than the default ConnectionError
            ConnectionErrorMsg = json.dumps(
                {
                    "status": "failed",
                    "error": f"Error reaching {url}. Please check your internet connection.",
                    "type": "ConnectionError",
                },
                indent=4,
            )
            logger.error(str(ConnectionErrorMsg))
        except Exception as e:
            try:
                headers = {"Content-Type": "application/json"}
                headers.update({"Authorization": f"Bearer {conf_mgr.access_token}"})
                url = conf_mgr.metrics_url

                payload = {
                    "username": nickname,
                    "method": function.__name__,
                    "args": tuple(str(i) for i in args if all(arg not in str(i) for arg in mask_args)),
                    "kwargs": {k: v for k, v in kwargs.items() if k not in mask_kwargs},
                    "error": str(e),
                }
                requests.post(url=url, headers=headers, json=payload)
            except Exception as exc:
                raise exc

            raise e.with_traceback(None)

    @functools.wraps(function)
    def dummy_wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper if conf_mgr.TELEMETRY else dummy_wrapper
