# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os
import requests
from unittest import mock
from unittest.mock import patch, MagicMock, Mock

import pytest
from pytest_mock import mocker
from pathlib import Path
import tempfile

import json

# decorators get applied at import time, so we need to set the environment variables before importing the module
os.environ["IRIS_TELEMETRY_DISABLE"] = "True"
os.environ["IRIS_AUTHENTICATE_DISABLE"] = "True"

from iris.sdk import post as post
from iris.sdk import get as get
from iris.sdk import delete as delete
from iris.sdk import pull as pull
from iris.sdk import upload as upload
from iris.sdk import download as download
from iris.sdk.exception import (
    BadRequestError,
    EndpointNotFoundError,
    InvalidCommandError,
    InvalidLoginError,
)
from iris.sdk.utils.io_utils import upload_from_file

from typer.testing import CliRunner

from iris.main import main
import json

runner = CliRunner()


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Test Module                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# --------------------------------------    iris json_output_decorator     -------------------------------------- #


def test_get_returns_json(mocker):
    # current issue: the JSON object must be str, bytes or bytearray, not Mock, which is the same bug i had all last week and could not fix
    # mocking the response from the get request

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "experiment": {
            "jobs": [
                {
                    "tasks": [
                        {
                            "name": "job_1",
                            "out_art_id": "model_1",
                            "flags": {
                                "task": "sequence_classification",
                                "model.teacher": "baseline_teacher",
                                "model.student": "baseline_student",
                                "data.text_fields": '["text1", "text2"]',
                                "data.dataset_config_name": "sst2",
                            },
                            "results": {},
                            "status": "completed",
                        }
                    ]
                },
            ]
        },
    }

    mocker.patch("requests.get", return_value=mock_response)

    result = runner.invoke(main, ["get", "--json"])
    assert result.exit_code == 0

    try:
        json.loads(result.stdout or "null")
    except:
        pytest.fail(f"get did not return valid JSON: '{result.stdout}'")


def test_post_returns_json(mocker):
    # current issue: the JSON object must be str, bytes or bytearray, not Mock, which is the same bug i had all last week and could not fixmock_response = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "status": 200,
        "response": {"status": "success", "message": "dispatched", "output": 1234},
    }

    mocker.patch("requests.post", return_value=mock_response)

    result = runner.invoke(main, ["post", "-m", "prajjwal1/bert-tiny", "-d", "mrpc", "-t", "glue", "--json"])
    assert result.exit_code == 0

    try:
        json.loads(result.stdout or "null")
    except:
        pytest.fail(f"post did not return valid JSON: '{result.stdout}'")


def test_distil_returns_json(mocker):
    # current issue: the JSON object must be str, bytes or bytearray, not Mock, which is the same bug i had all last week and could not fixmock_response = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "status": 200,
        "response": {"status": "success", "message": "dispatched", "output": 1234},
    }

    mocker.patch("requests.post", return_value=mock_response)

    result = runner.invoke(main, ["distil", "-m", "prajjwal1/bert-tiny", "-d", "mrpc", "-t", "glue", "--json"])
    assert result.exit_code == 0

    try:
        json.loads(result.stdout or "null")
    except:
        pytest.fail(f"distil did not return valid JSON: '{result.stdout}'")


def test_finetune_returns_json(mocker):
    # current issue: the JSON object must be str, bytes or bytearray, not Mock, which is the same bug i had all last week and could not fixmock_response = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "status": 200,
        "response": {"status": "success", "message": "dispatched", "output": 1234},
    }

    mocker.patch("requests.post", return_value=mock_response)

    result = runner.invoke(main, ["finetune", "-m", "prajjwal1/bert-tiny", "-d", "mrpc", "-t", "glue", "--json"])
    assert result.exit_code == 0

    try:
        json.loads(result.stdout or "null")
    except:
        pytest.fail(f"finetune did not return valid JSON: '{result.stdout}'")


def test_download_returns_json(mocker):
    # current issue: experiments key not being recognised in response dict through runner, which is strange because i ran the experiment manually,
    # printed the dictionary, and it worked there. this function also now works completely perfectly manually.

    # mocking the response from the get request
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "experiment": {
            "jobs": [
                {
                    "tasks": [
                        {
                            "name": "job_1",
                            "out_art_id": "model_1",
                            "flags": {
                                "task": "sequence_classification",
                                "model.teacher": "baseline_teacher",
                                "model.student": "baseline_student",
                                "data.text_fields": '["text1", "text2"]',
                                "data.dataset_config_name": "sst2",
                            },
                            "results": {},
                            "status": "completed",
                        }
                    ]
                },
            ]
        },
    }

    mocker.patch("requests.get", return_value=mock_response)
    result = runner.invoke(main, ["download", "36:XS", "--json"])  # CHANGE THESE ARGS

    assert result.exit_code == 0

    try:
        print(result.stdout)
        json.loads(result.stdout or "null")  # try and load the stdout as json.
    except:
        # Fail the test if the stdout is not valid json.
        pytest.fail("get() did not return valid JSON")


def test_pull_returns_json(mocker):
    # as above but status key not being recognised
    # mocking response returned by download function
    results = ["model_name", "task_name", "baseline_model_name", "baseline"]

    mocker.patch("iris.sdk.iris_sdk.download", return_value=results)
    mocker.patch("iris.sdk.iris_sdk.pull_image", return_value=None)
    result = runner.invoke(main, ["pull", "36:XS", "--json"])
    print(result.stdout)
    assert result.exit_code == 0

    try:
        json.loads(result.stdout or "null")
    except:
        pytest.fail(f"pull did not return valid JSON: '{result.stdout}'")


def test_upload_returns_json(mocker):
    with tempfile.TemporaryDirectory() as temp_dir:
        train_file_path = os.path.join(temp_dir, "train.csv")
        val_file_path = os.path.join(temp_dir, "val.csv")

        with open(train_file_path, "w") as train_file:
            train_file.write("This is train.csv")

        with open(val_file_path, "w") as val_file:
            val_file.write("This is val.csv")

        temp_dir_path = temp_dir

        # mock post_req_response = requests.post(url=url, headers=headers, data=post_req_data)
        post_mock = mocker.patch("requests.post")
        post_mock.return_value.ok = True
        post_mock.return_value.status_code = 200
        post_mock.return_value.json.return_value = {
            "artefact": {
                "uuid": "123456",
                "name": "test_artefact",
                "description": "test_description",
                "ext": ".tar.gz",
                "metadata": '{"src": "/tmp/test_artefact"}',
                "time_created": "2022-01-01T00:00:00.000Z",
            },
            "link": {"link": "a"},
        }

        # mock upload_response = upload_from_file(tarred, upl_link, json_output=json_output)
        upload_response = mocker.Mock()
        upload_response.status_code = 200
        mocker.patch("iris.sdk.iris_sdk.upload_from_file", return_value=upload_response)

        patch_response = mocker.Mock()
        patch_response.json = mocker.Mock(return_value={"status": "success"})
        patch_response.ok = True
        patch_mock = mocker.patch("requests.patch", return_value=patch_response)
        mocker.patch("requests.patch", patch_mock)

        result = runner.invoke(main, ["upload", temp_dir_path, "--json"])  # CHANGE THESE ARGS

        assert result.exit_code == 0

        try:
            json.loads(result.stdout or "null")
        except:
            pytest.fail(f"upload did not return valid JSON: '{result.stdout}'")


def test_delete_returns_json(mocker):
    delete_mock = mocker.patch("requests.delete")
    delete_mock.return_value.ok = True
    delete_mock.return_value.status_code = 204

    result = runner.invoke(main, ["delete", "experiment", "-i", "34", "--json"])

    assert result.exit_code == 0

    try:
        json.loads(result.stdout or "null")
    except:
        pytest.fail(f"delete did not return valid JSON: '{result.stdout}'")
