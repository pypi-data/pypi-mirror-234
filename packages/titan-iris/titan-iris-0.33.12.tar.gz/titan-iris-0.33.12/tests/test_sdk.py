import os
import tempfile
import pandas as pd

# decorators get applied at import time, so we need to set the environment variables before importing the module
os.environ["IRIS_TELEMETRY_DISABLE"] = "True"
os.environ["IRIS_AUTHENTICATE_DISABLE"] = "True"

from iris.sdk import post, download, get, pull, upload, validate
import json
from iris.sdk.exception import InvalidLoginError, EndpointNotFoundError, InvalidCommandError, BadRequestError
import pytest
from pytest_mock import mocker
from unittest.mock import patch, MagicMock, Mock

# --------------------------------------    test json output flag   -------------------------------------- #


def test_get_returns_json(mocker):
    # current issue: the JSON object must be str, bytes or bytearray, not Mock, which is the same bug i had all last week and could not fix
    # mocking the response from the get request

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json = mocker.Mock()
    mock_response.json.return_value = {
        "status": "success",
        "experiment": {
            "jobs": [
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
                },
            ]
        },
    }

    mocker.patch("requests.get", return_value=mock_response)

    result = get(json_output=True)
    try:
        json.loads(result)
    except Exception:
        pytest.fail("get() did not return valid JSON")


def test_post_returns_json(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": {"status": "success", "message": "Success"}}
    mock_response.text = '{"response": {"status": "success", "message": "Success"}}'

    mock_post = mocker.Mock()
    mock_post.return_value = mock_response
    mocker.patch("requests.post", mock_post)

    result = post(None, json_output=True, model="prajjwal1/bert-tiny", dataset="mrpc", task="glue", test=True)
    try:
        json.loads(result)
    except Exception:
        pytest.fail("post() did not return valid JSON")


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
            "link": {"link": ""},
        }

        upload_response = mocker.Mock()
        upload_response.status_code = 200
        mocker.patch("iris.sdk.iris_sdk.upload_from_file", return_value=upload_response)

        patch_response = mocker.Mock()
        patch_response.json = mocker.Mock(return_value={"status": "success"})
        patch_response.ok = True
        patch_mock = mocker.patch("requests.patch", return_value=patch_response)
        mocker.patch("requests.patch", patch_mock)

        result = upload(
            json_output=True,
            src=temp_dir_path,
            name="test_name",
            description="test_description",
            model_family_override=None,
        )["uuid"]
        try:
            json.loads(result)
        except:
            pytest.fail("upload() did not return valid JSON")


# --------------------------------------    iris get     -------------------------------------- #


def test_iris_get_with_401_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mock_response.ok = False

    mock_get = mocker.Mock()
    mock_get.return_value = mock_response
    mocker.patch("requests.get", mock_get)
    with pytest.raises(InvalidLoginError):
        result = get()


def test_iris_get_with_404_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.ok = False

    mock_get = mocker.Mock()
    mock_get.return_value = mock_response
    mocker.patch("requests.get", mock_get)
    with pytest.raises(EndpointNotFoundError):
        result = get()


# --------------------------------------    iris download   -------------------------------------- #


def test_iris_download_with_invalid_experiment_cmd():
    download_func = download.__wrapped__
    with pytest.raises(InvalidCommandError) as exc:
        download_func("invalid")


# --------------------------------------      iris pull     -------------------------------------- #


def test_iris_pull_with_invalid_experiment_cmd():
    pull_func = pull.__wrapped__
    with pytest.raises(InvalidCommandError):
        pull_func("invalid")


# ------------------------------------      iris validation    ----------------------------------- #


def test_iris_validate_with_valid_filenames():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create files inside the temporary directory
        open(os.path.join(tmpdirname, "train.csv"), "a").close()
        open(os.path.join(tmpdirname, "validation.csv"), "a").close()

        # Call the check_files function
        results = validate(tmpdirname)

        # Check that the result is as expected
        assert results["filenames"] == ["train.csv", "validation.csv"]


def test_iris_validate_with_invalid_filenames():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create files inside the temporary directory
        open(os.path.join(tmpdirname, "t.csv"), "a").close()
        open(os.path.join(tmpdirname, "v.csv"), "a").close()

        # Call the check_files function
        results = validate(tmpdirname)

        # Check that the result is as expected
        assert results["filenames"] == [None, None]


def test_iris_validate_with_valid_file_format():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "formatting_valid")

    results = validate(directory)
    assert results["file_validity"] == [True, True]


def test_iris_validate_with_invalid_file_format():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "formatting_invalid")

    results = validate(directory)
    assert results["file_validity"] == [False, False]


def test_iris_validate_with_different_cols():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "formatting_invalid_cols")

    results = validate(directory)
    assert results["file_validity"] == [False, False]


def test_iris_validate_with_valid_sequence_classification_dataset():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "sequence_classification_valid")

    results = validate(directory)
    assert results["sequence_classification"][0] == True
    assert (
        results["sequence_classification"][1]
        == "Available text fields: premise, hypothesis. Suggested number of labels: 3"
    )


def test_iris_validate_with_invalid_sequence_classification_dataset_no_label():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "sequence_classification_invalid_no_label")

    results = validate(directory)
    assert results["sequence_classification"][0] == False
    assert results["sequence_classification"][1] == "Label column does not exist in dataset"


def test_iris_validate_with_invalid_sequence_classification_dataset_invalid_label():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "sequence_classification_invalid_label")

    results = validate(directory)
    assert results["sequence_classification"][0] == False
    assert results["sequence_classification"][1] == "Label column contains negative values"


def test_iris_validate_with_valid_question_answering_dataset():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "question_answering_valid")

    results = validate(directory)
    assert results["question_answering"][0] == True
    assert results["question_answering"][1] == "Dataset is valid"


def test_iris_validate_with_invalid_question_answering_dataset_invalid_answers_col():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "question_answering_invalid_answers_col")

    results = validate(directory)
    assert results["question_answering"][0] == False
    assert results["question_answering"][1] == "answer_start key does not exist in answers column"


def test_iris_validate_with_valid_conditional_language_modelling():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "conditional_language_modelling_valid")

    results = validate(directory)
    assert results["conditional_language_modelling"][0] == True
    assert (
        results["conditional_language_modelling"][1]
        == "Valid text fields: text, response. Specify two text fields for conditional language modelling."
    )


def test_iris_validate_with_invalid_conditional_language_modelling():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "conditional_language_modelling_invalid")

    results = validate(directory)
    assert results["conditional_language_modelling"][0] == False
    assert (
        results["conditional_language_modelling"][1] == "Dataset does not contain at least two columns that are strings"
    )


def test_iris_validate_with_valid_unconditional_language_modelling():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "unconditional_language_modelling_valid")

    results = validate(directory)
    assert results["unconditional_language_modelling"][0] == True
    assert (
        results["unconditional_language_modelling"][1]
        == "Valid text fields: text. Specify one text field for unconditional language modelling."
    )


def test_iris_validate_with_invalid_unconditional_language_modelling():
    directory = os.path.join(os.path.dirname(__file__), "fixtures", "unconditional_language_modelling_invalid")

    results = validate(directory)
    assert results["unconditional_language_modelling"][0] == False
    assert (
        results["unconditional_language_modelling"][1] == "Dataset does not contain at least a column that is a string"
    )
