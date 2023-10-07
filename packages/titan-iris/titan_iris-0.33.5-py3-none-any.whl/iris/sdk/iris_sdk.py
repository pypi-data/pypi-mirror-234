"""This module will contain all the sdk functions for the iris command sdk, including login, logout, get, post, pull."""
import ast
import json
import logging
import os
from datetime import datetime
from importlib import util
from pathlib import Path
from typing import List, Optional, Union, Dict, Any
from urllib.parse import urljoin

# for iris infer
import numpy as np

# for iris pull
import requests
import tritonclient.http
from rich import print

from .conf_manager import conf_mgr
from .exception import (
    ArtefactNotFoundError,
    ArtefactTypeInferError,
    ArtefactTypeNotAFolderError,
    BadRequestError,
    InvalidCommandError,
    InvalidDatasetFormatError,
    JobStillRunningError,
    MissingTokenizerError,
    UnknownFamilyError,
    UnsafeTensorsError,
    UploadOnPostError,
)

# internal imports
from .utils.auth_utils import auth, handle_bad_response
from .utils.display_utils import (
    dump,
    handle_iris_get_response,
    print_status_dict_results,
)
from .utils.docker_utils import check_docker, pull_fastapi_image, pull_image, get_takeoff_image_name
from .utils.io_utils import download_model, make_targz, upload_from_file
from .utils.telemetry_utils import telemetry_decorator
from .utils.utils import valid_qlora

from .utils.validation_utils import (
    check_filenames,
    get_df,
    valid_for_question_answering,
    valid_for_sequence_classification,
    valid_for_conditional_language_modelling,
    valid_for_unconditional_language_modelling,
    get_columns,
    get_rows,
)

try:
    from importlib import metadata as import_metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as import_metadata


# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #


# Whether to use tqdm for progress bars
TQDM = True

# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                  IRIS USERS SDK                                                     #
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# ------------------------------------      Setup Logger      ------------------------------------ #
# Logger config
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(conf_mgr.LOG_LEVEL)


# --------------------------------------      iris login    -------------------------------------- #
@auth
def login():
    """Login to Iris."""
    logger.debug("logging in")
    return conf_mgr.current_user["name"]


# --------------------------------------     iris logout    -------------------------------------- #


def logout():
    """Logout from iris.

    Just deletes the keyfile.
    """
    logger.info("logging out")
    path = Path.home() / Path(conf_mgr.config.keyfile_name)
    if path.exists():
        path.unlink()
    if not path.exists():
        return True
    else:
        return False


# --------------------------------------      iris post     -------------------------------------- #


@auth
@telemetry_decorator
def post(
    headers: dict = None,
    json_output: bool = False,
    **flags: dict,
) -> None:
    """Dispatch a job to iris.

    Args:
        headers (dict, optional): Additional headers to add. Defaults to {}.
        json_output(bool, optional): Whether to return the response as a json object. Defaults to False.
        **flags (dict): The flags to send to the server. These must conform to the API specification.

    Raises:
        UploadOnPostError: If there's an error uploading the artefact.
        handle_bad_response(...): If there's a bad response from the server.
    """
    if headers is None:
        headers = {}
    endpoint = "experiment"
    # detype the flags, so we can send them
    payload = {k: str(val) if val is not None else None for k, val in flags.items()}
    logger.debug(f"Dispatching job with payload {payload}")
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/")

    local_family = None
    for local_artefact_field in ["model", "dataset"]:
        local_artefact = payload[local_artefact_field]
        if os.path.exists(local_artefact):
            print(
                f"Local {local_artefact_field} found. \
                If you intended to use a huggingface module then rename the local file."
            )
            server_artefact = upload(
                name=local_artefact.split("/")[-1],
                src=local_artefact,
                description="Experiment model",
                model_family_override=None,
                internal_artefact_type=local_artefact_field,
            )
            if server_artefact:
                payload[local_artefact_field] = server_artefact["uuid"]
                if local_artefact_field == "model":
                    local_family = json.loads(server_artefact["metadata"])["local_model_family"]
            else:
                raise UploadOnPostError

    if flags["task"] == "language_modelling":
        if flags["no_qlora"] and valid_qlora(flags["model"], local_family):
            # If want to disable qlora, but qlora is available:
            print(f"QLoRA manually disabled for {flags['model']}")
            use_qlora = False
        elif not flags["no_qlora"] and not valid_qlora(flags["model"], local_family):
            # If qlora isn't explicitly disabled, but is not available.
            print(f"QLoRA not available for {flags['model']}. Proceeding without QLoRA.")
            use_qlora = False
        elif flags["no_qlora"] and not valid_qlora(flags["model"], local_family):
            # Qlora disabled, but it wasn't available anyways.
            use_qlora = False
        else:  # Qlora not explicitly disabled, and qlora is available.
            print("QLoRA is available and will be used.")
            use_qlora = True
        payload.pop("no_qlora")
    else:
        use_qlora = False
    payload.update({"use_qlora": use_qlora})
    payload.update({"local_model_family": local_family})

    headers.update({"Authorization": f"Bearer {conf_mgr.access_token}"})
    response = requests.post(url=url, headers=headers, data=payload)
    if not response.ok:
        raise handle_bad_response(response, endpoint)  # already returns json object
    else:
        dumped_response = dump(response)
        if json_output:
            print(dumped_response)
            return dumped_response
        else:
            print_status_dict_results(json.loads(dumped_response)["response"])
            return dumped_response


# --------------------------------------       iris get     -------------------------------------- #


@auth
@telemetry_decorator
def get(
    object: str = "experiment",
    id: Optional[str] = None,
    query: Optional[str] = None,
    headers: dict = None,
    json_output: bool = False,
):
    """Get objects from the TitanML Store.

    Args:
        object (str, optional): The object to get. Defaults to "experiment".
        id (Optional[str], optional): The id of the object. Defaults to None.
        query (Optional[str], optional): A JMESPath query to run against the returned json.
                                         Defaults to None, i.e. return everything.
        headers (dict): Custom headers to send with the get request
        json_output (bool): Whether to return the response as a json object

    Returns:
        (str) A json response, formatted as: {"status": <http_response>, "response": <queried_json_response>}
    """
    if headers is None:
        headers = {}

    logger.debug(f"Getting from ... {conf_mgr.base}, auth from {conf_mgr.AUTH0_DOMAIN}")
    logger.debug(f"Applying custom headers {headers}")
    endpoint = f"{object}/"
    if id:
        endpoint += id
    url = urljoin(conf_mgr.runner_url, endpoint)
    headers.update({"Authorization": f"Bearer {conf_mgr.access_token}"})

    response = requests.get(url=url, headers=headers)
    if not response.ok:
        raise handle_bad_response(response, url)
    try:
        # get the response as a json object, this will make sure the response is valid json

        if os.getenv("IRIS_LOG_LEVEL") == "DEBUG":
            print(response.json())
        dumped_response = dump(response, query)
        if json_output:
            print(dumped_response)
        else:
            # better user information display, return the response in a prettier table format
            # this func only turns a valid json response into a table
            handle_iris_get_response(dumped_response)
        return dumped_response
    except json.JSONDecodeError:
        print("JSON decoding error occurred.")
        print(response)
        return None


# --------------------------------------     iris delete    -------------------------------------- #


@auth
@telemetry_decorator
def delete(
    object: str,
    id: Optional[str],
    json_output: bool = False,
):
    """Get objects from the TitanML Store.

    Args:
        object (str, optional): The object to get. Defaults to "experiment".
        id (str): The id of the object to delete
        json_output (bool, optional): Whether to return the response as a json object. Defaults to False.

    Returns:
        (str) A json response, formatted as:
        {"status": <http_response>, "response": <queried_json_response>}
    """
    logger.debug(f"Getting from ... {conf_mgr.base}, auth from {conf_mgr.AUTH0_DOMAIN}")
    endpoint = object + "/" + str(id) if id is not None else ""
    url = urljoin(conf_mgr.runner_url, endpoint)
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    response = requests.delete(url=url, headers=headers)
    if not response.ok:
        raise handle_bad_response(response, endpoint)
    else:
        if response.status_code == 204:
            response_message = {"status": "success", "response": "deleted"}
            if json_output:
                result = json.dumps(response_message, indent=4)
                print(result)
            else:
                print_status_dict_results(response_message)
        return None


# --------------------------------------     iris download  -------------------------------------- #


@auth
@telemetry_decorator
def download(experiment_cmd: str, json_output: bool = False):
    """Downloading the models to local machine.

    Args:
        experiment_cmd (str): pulling command string. it should be formatted as <experiment_id>:<job_tag>
        json_output (bool, optional): Whether to return the response as a json object. Defaults to False.

    Raises:
        InvalidCommandError: Invalid command error
        BadRequestError: Bad request error
        ArtefactNotFoundError: Artefact not found error

    Returns:
        model_name: name of the model
        task_name: name of the task
        baseline_model_name: name of the baseline model
        baseline: whether the model is baseline or not
    """
    # create a model_storage folder if it doesn't exist
    Path("model_storage").mkdir(parents=True, exist_ok=True)

    # parse the command string
    experiment_id_name, _, job_tag = experiment_cmd.rpartition(":")

    # check if the job tag is valid
    if job_tag not in {"baseline", "fp16", "XS", "S", "M"}:
        raise InvalidCommandError

    experiment_id, _, experiment_name = experiment_id_name.partition("-")

    # check if the experiment id is valid
    if experiment_id == "":
        raise InvalidCommandError

    # check if the experiment name is valid
    if experiment_name == "" and not json_output:
        print(f"Downloading model_id {experiment_id} with job tag {job_tag} ...")
    elif not json_output:
        print(f"Downloading model {experiment_name} with job tag {job_tag} ...")

    # get the experiment info
    endpoint = "experiment"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/{experiment_id}")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    response = requests.get(url=url, headers=headers)
    response_json = response.json()

    # check if the request is successful
    if response_json["status"] != "success":
        raise BadRequestError

    jobs_list = response_json["experiment"]["jobs"]
    tasks_list = jobs_list[0]["tasks"]

    model_uuid = None
    baseline = False
    download_url, model_name, task_name, baseline_model_name = None, None, None, None
    # loop through the jobs list and find the job with the same tag
    for i in range(len(tasks_list)):
        if job_tag == tasks_list[i]["name"].split("_")[-1]:
            model_uuid = tasks_list[i]["out_art_id"]
            model_name = tasks_list[i]["name"]
            task_name = tasks_list[i]["flags"]["task"]

            results = tasks_list[i]["results"]
            status = tasks_list[i]["status"]

            # check if the job is still running
            if results is None and status == "active":
                raise JobStillRunningError

            # check if the baseline model is available
            # if baseline_model_name == "null":
            #     baseline_model_name = jobs_list[i]["flags"]["model.student"]
            #     baseline = True

            # check if text fields is valid in sequence classification task
            if task_name == "sequence_classification":
                text_fields = ast.literal_eval(tasks_list[i]["flags"]["data.text_fields"])  # convert string to list
                if len(text_fields) == 1:
                    task_name = "sequence_classification"
                elif len(text_fields) == 2:
                    task_name = "pair_classification"
                else:
                    raise ValueError("Invalid number of text fields")

            # check if dataset name is valid in glue task
            if task_name == "glue":
                dataset_name = tasks_list[i]["flags"]["data.dataset_config_name"]  # convert string to list
                if dataset_name in {"sst2", "cola"}:
                    task_name = "sequence_classification"  # cola and sst2 only has one sentence as input
                else:
                    task_name = "pair_classification"

            # check if artifact is available
            if model_uuid is None:
                raise ArtefactNotFoundError
            url = urljoin(
                conf_mgr.runner_url,
                f"artefact/link/{model_uuid}/download?refresh=true",
            )
            # get the download url
            response = requests.get(url=url, headers=headers)
            response_json = response.json()
            download_url = response_json["link"]["link"]
            break

    # download the model
    if download_url is not None:
        download_model(download_url, model_name, json_output=json_output)
    if json_output:
        print(json.dumps(response_json, indent=4))
    else:
        print(f"\nModel {model_name} downloaded successfully")
    return model_name, task_name, baseline_model_name, baseline


# --------------------------------------      iris pull     -------------------------------------- #


@auth
@telemetry_decorator
def pull(experiment_cmd: str, json_output: bool = False):
    """Download the model and pull the hephaestus image from the server.

    Args:
        experiment_cmd (str): pulling command string. it should be formatted as <experiment_id>:<job_tag>
        json_output (bool, optional): Whether to return the response as a json object. Defaults to False.

    """
    # parse the command string
    args = experiment_cmd.split(":")
    if len(args) != 2:
        raise InvalidCommandError
    experiment_id: str = args[0].lower()
    job_tag: str = args[1]

    # download the model
    logger.info("***Executing pull command***")
    model_name, task_name, baseline_model_name, baseline = download(
        experiment_cmd, json_output=json_output
    )  # this is a hack to get the function to work without the auth decorator

    # pull the image
    logger.info("Pulling image from the server")
    pull_image(
        model_folder_path=f"model_storage/{model_name}/models",
        container_name=f"iris-triton-{experiment_id}",
        job_tag=job_tag,
        task_name=task_name,
        baseline_model_name=baseline_model_name,
        baseline=baseline,
        json_output=json_output,
    )
    logger.info("All done!")
    if json_output:
        result = {"status": "success"}
        return json.dumps(result, indent=4)


# --------------------------------------    iris upload     -------------------------------------- #


def get_local_model_family(src: str) -> str:
    """Uses the model files to discern the overall model family e.g. bert, roberta, falcon (as refinedwebmodel).

    First uses the 'model_type' field of config.json, falling back to the tokenizer_class field of tokenzier.json.
    If no family can be determined, an UnknownFamilyError is raised, prompting the user to use Iris Upload with --mf,
    such that a family type can be manually specified.

    Args:
        src: The filepath of the input model

    Returns: Model family determined.

    """
    # Family examples: DebertaV2, Albert, DistilBert, Roberta, Electra, Bert
    # Detect model family
    if os.path.isfile(os.path.join(src, "config.json")):
        with open(os.path.join(src, "config.json"), "r") as f:
            config_file = json.load(f)
            model_type = config_file.get("model_type", None)
            if model_type:
                return model_type.lower()
    elif os.path.isfile(os.path.join(src, "tokenizer_config.json")):
        with open(os.path.join(src, "tokenizer_config.json"), "r") as f:
            tokenizer_class = json.load(f).get("tokenizer_class", None)
        if tokenizer_class:
            return tokenizer_class.replace("Tokenizer", "").lower()

    raise UnknownFamilyError()


@auth
@telemetry_decorator
def upload(
    name: str,
    src: Union[str, Path],
    description: str,
    model_family_override: Optional[str],
    internal_artefact_type: Optional[str] = None,
    json_output: bool = False,
):
    """Upload an artefact to the TitanML Store.

    Args:
        model_family_override: A manually specified model family.
        internal_artefact_type (Union[str, None]): One of ['model','dataset'] - the type of artefact purpotedly being
        uploaded when calling from iris post.
        name (str): The name of the artefact
        src (Union[str, Path]): The source of the artefact on disk
        description (str): A short description of the artefact.
        json_output (bool, optional): Whether to return the response as a json object. Defaults to False.

    Raises:
        ArtefactNotFoundError: If the path to the artefact doesn't exist.
        UnsafeTensorsError: If the artefact is a model, and the model has not been saved in safetensors format.
    """
    # cast from path to str.
    src = str(src)

    metadata = {}

    # cast object from path to str within the metadata dictionary
    metadata["src"] = str(Path(src))

    endpoint = "artefact"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    # Catches if you accidentally put a tilde in quotes:
    if src[0] == "~":
        src = os.path.expanduser(src)

    if not Path(src).is_dir():
        raise ArtefactNotFoundError(details=src)

    ext = ".tar.gz"

    namelist = os.listdir(src)

    # Set of checks to determine if the input files' format matches that expected for either a dataset or a model
    safetensors_check = tokenizer_check = val_file_check = train_file_check = False

    for x in namelist:
        # Check that safetensors are being used for the intended model
        if ".safetensors" in Path(x).suffixes:
            safetensors_check = True
            # Check the intended model has a tokenizer
        elif "tokenizer_config.json" in x:
            tokenizer_check = True
            # Check the intended dataset contains a validation and training file (csvs)
        elif "val" in x and x.endswith(".csv"):
            val_file_check = True
        elif "train" in x and x.endswith(".csv"):
            train_file_check = True

    # Check that the type of artefact being sent from iris post (for uploads originating from post rather than iris
    # upload itself) matches that of its content.
    if internal_artefact_type == "model" or safetensors_check or tokenizer_check:
        art_type = "model"
        if not safetensors_check:
            raise UnsafeTensorsError()

        if not tokenizer_check:
            raise MissingTokenizerError()

        if model_family_override:
            metadata["local_model_family"] = model_family_override
        else:
            metadata["local_model_family"] = get_local_model_family(src)

    elif internal_artefact_type == "dataset" or val_file_check or train_file_check:
        art_type = "dataset"
        if not val_file_check and train_file_check:
            raise InvalidDatasetFormatError()
    else:
        if os.path.isdir(src):
            raise ArtefactTypeInferError()
        else:
            raise ArtefactTypeNotAFolderError()

    logger.debug(f"Uploading {art_type} from {src} to {url}")
    # Make post request to seshat for instantiation of artefact object, and provision of presigned upload link.

    tarred = None
    try:
        tarred, unipart_hashval, file_size = make_targz(src)
        post_req_data = {
            "name": name,
            "artefact_type": art_type,
            "description": description,
            "ext": ext,
            "src": src,
            "metadata": json.dumps({k: str(v) for k, v in metadata.items()}),
            "hash": unipart_hashval,
            "size": file_size,
        }

        logger.debug(f"posting {post_req_data} to {url}")
        post_req_response = requests.post(url=url, headers=headers, data=post_req_data)
        if not post_req_response.ok:
            logger.debug("post unsuccessful")
            raise handle_bad_response(post_req_response, endpoint)
        else:
            # On succesful response receipt:
            logger.debug("post successful")

            # Check if artefact-already-exists response has been received.
            if post_req_response.status_code == 202:
                existing_artefact = post_req_response.json()["artefact"]
                created_time = str(
                    datetime.strptime(existing_artefact["time_created"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                )
                # Return artefact data for found/existing artefact.
                if not internal_artefact_type and not json_output:
                    print(f"Artefact was already uploaded at {created_time} with ID: {existing_artefact['uuid']}")
                return existing_artefact

        art_uuid = post_req_response.json()["artefact"]["uuid"]

        upl_link_obj = post_req_response.json()["link"]
        logger.debug("got link")

        if not json_output:
            print("Beginning upload...")
        post_upload_data = {}

        # Upload file
        post_upload_data["hashval"] = unipart_hashval
        upload_response = upload_from_file(tarred, upl_link_obj["link"], file_size, json_output=json_output)

        # If Upload completes succesfully, send the hash to seshat in a patch request. Patch req confirms matching hash,
        # then returns the artefact ID for further use by user.
        if upload_response is not None and upload_response.status_code == 200:
            endpoint = "artefact"
            if not json_output:
                print(f"Upload Complete -  Validating {art_type} server-side")
            url = urljoin(conf_mgr.runner_url, f"{endpoint}/{art_uuid}")
            patch_req_response = requests.patch(url=url, headers=headers, json=post_upload_data)
            if not patch_req_response.ok:
                raise handle_bad_response(patch_req_response, endpoint)
            else:
                if json_output:
                    result = {"status": "success", "artefact id": str(art_uuid)}
                    print(json.dumps(result, indent=4))
                else:
                    print(
                        f"Upload validated. This {art_type} can now be used in experiments \
                        by referring to it by UUID: {art_uuid}"
                    )
                    print(f"Alternatively, you can continue to use the {art_type}'s filepath.")
                return post_req_response.json()["artefact"]
        else:
            print("Upload failed")
            for key, value in upload_response.items():
                if isinstance(value, Path):
                    upload_response[key] = str(value)
            return dump(upload_response)
    finally:
        if tarred and hasattr(tarred, "name") and os.path.isfile(tarred.name):
            os.unlink(tarred.name)


# --------------------------------------      iris infer    -------------------------------------- #


@telemetry_decorator
def infer(
    url: str,
    task_name: str,
    text: List[str],
    context: Optional[str] = None,
    runtime: str = "trt",
):
    """Infer the hosted tytn model using triton client.

    Args:
        task_name (str): task name of the model (sequence_classification, question_answering)
        runtime (str): choose the runtime for inference (trt, onnx)
        text (str): input text field used for inference
        context (Optional[str]): input context field used for inference. Only used in question_answering task.
                                    Defaults to None.
        url (str): The url of the triton server


    Returns:
        infer_res(dict): dictionary of the inference result
    """
    # check if the runtime is valid
    print("runtime is ", runtime)
    if runtime not in ["trt", "onnx"]:
        raise ValueError("runtime must be either trt or onnx")

    model_name = "transformer_onnx_inference" if runtime == "onnx" else "transformer_tensorrt_inference"
    model_version = "1"
    batch_size = 1

    triton_client = tritonclient.http.InferenceServerClient(url=url, verbose=False)

    triton_client.get_model_metadata(model_name=model_name, model_version=model_version)
    triton_client.get_model_config(model_name=model_name, model_version=model_version)
    text_1, text_2 = None, None
    if task_name == "sequence_classification":
        if len(text) == 1:
            # if only one text is provided, this is a single sentence classification task inference
            text_1 = tritonclient.http.InferInput(name="TEXT", shape=(batch_size,), datatype="BYTES")
            text_1.set_data_from_numpy(np.asarray([text[0]] * batch_size, dtype=object))
        elif len(text) == 2:
            # if two texts are provided, this is a pair sentence classification task inference
            text_1 = tritonclient.http.InferInput(name="TEXT_1", shape=(batch_size,), datatype="BYTES")
            text_2 = tritonclient.http.InferInput(name="TEXT_2", shape=(batch_size,), datatype="BYTES")
            text_1.set_data_from_numpy(np.asarray([text[0]] * batch_size, dtype=object))
            text_2.set_data_from_numpy(np.asarray([text[1]] * batch_size, dtype=object))
        else:
            raise ValueError("Invalid number of texts provided for sequence classification task")
    elif task_name == "question_answering":
        if context is None:
            raise ValueError("Context must be provided for question answering task")
        text_1 = tritonclient.http.InferInput(name="QUESTION", shape=(batch_size,), datatype="BYTES")
        text_2 = tritonclient.http.InferInput(name="CONTEXT", shape=(batch_size,), datatype="BYTES")
        text_1.set_data_from_numpy(np.asarray([text[0]] * batch_size, dtype=object))
        text_2.set_data_from_numpy(np.asarray([context] * batch_size, dtype=object))
    else:
        raise ValueError("Invalid task name provided")

    # bind outputs to the server
    outputs = tritonclient.http.InferRequestedOutput(name="logits", binary_data=False)

    infer_res = triton_client.infer(
        model_name=model_name,
        model_version=model_version,
        inputs=[text_1, text_2] if text_2 is not None else [text_1],
        outputs=[outputs],
    )
    return json.loads(infer_res.as_numpy("logits").item())


# --------------------------------------     iris makesafe    -------------------------------------- #


def makesafe(
    model: str,
):
    """Convert a model's weights to the safetensors format.

    Args:
        model (str): The path of the local model to be converted.
    """
    if not os.path.exists(model):
        raise FileNotFoundError
    # else
    print("Checking for requirements...")
    failed_packages = list(filter(lambda x: not util.find_spec(x), ["torch", "safetensors", "transformers"]))
    if failed_packages:
        print(
            "To use the safetensors convert, you must have the following packages installed: ",
            failed_packages,
        )
        print("NB: These packages do not need to be installed with gpu support.")
        return
    if import_metadata.version("transformers") < "4.27.0":
        print(
            "To use makesafe you must have transformers >= 4.27.0. You currently have "
            + import_metadata.version("transformers")
        )
        return
    # else
    from .safe_convert import do_convert

    do_convert(model)


# --------------------------------------     iris inference    -------------------------------------- #


@auth
@telemetry_decorator
def query_inference(artefact: str, data: str) -> Dict[str, Any]:
    """Simple inference test."""
    endpoint = "inference-session"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/{artefact}")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}

    response = requests.post(url=url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


@auth
@telemetry_decorator
def create_inference(artefact: str, duration: int, no_expiration: bool) -> Dict[str, Any]:
    """Simple inference test."""
    endpoint = "inference-session"
    url = urljoin(conf_mgr.runner_url, f"{endpoint}/{artefact}")
    headers = {"Authorization": f"Bearer {conf_mgr.access_token}"}
    body = {"duration": False if not no_expiration else duration}

    response = requests.put(url=url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


# ----------------------------------------------------------------------------------------------------------


@auth
@telemetry_decorator
def takeoff(
    model_folder_path: str,
    device: str,
    port: int = 8000,
    quant: Optional[str] = "int8",
    extra_env_vars: Optional[Dict[str, str]] = None,
):
    """Takeoff the model to fastapi server.

    This function will pull the fastapi image. Start the docker container and mount the model folder.
    Start the fastapi server and expose the port 8000.

    Args:
        model_folder_path (str): The path of the model folder to be mounted.
        device (str): The device to run the model on.
        port (int, optional): The port to expose the fastapi server. Defaults to 8000.
        quant (Optional[str], optional): The quantization level to be used. Defaults to "int8".
        extra_env_vars (Optional[Dict[str, str]], optional): Extra environment variables
           to be passed to the docker container. Defaults to None.
    """
    logger.info("Pulling image from the server")

    # check if docker is installed
    try:
        check_docker()
        logger.info("Docker is running.")
    except EnvironmentError as e:
        print(e)

    # pull the fastapi image, notice this will also run the docker container mounting the model folder
    pull_fastapi_image(
        image_name=get_takeoff_image_name(),
        model_folder_path=model_folder_path,
        device=device,
        quant=quant,
        port=port,
        extra_env_vars={} if not extra_env_vars else extra_env_vars,
    )

    logger.info("All done!")


# ------------------------------------     iris validate    ------------------------------------ #
@auth
@telemetry_decorator
def validate(
    src: Union[str, Path],
):
    """Validates a dataset for use with Iris.

    Args:
        src (Union[str, Path]): The path to the dataset to be validated.

    Returns:
        results (dict): A dictionary containing the results of the validation.
    """
    # cast from path to str.
    src = str(src)

    # Catches if you accidentally put a tilde in quotes:
    if src[0] == "~":
        src = os.path.expanduser(src)

    if not Path(src).is_dir():
        raise ArtefactNotFoundError(details=src)

    results = {}

    try:
        # Check if filenames are valid
        [train_filename, validation_filename] = check_filenames(src)
        results["filenames"] = [train_filename, validation_filename]
        if train_filename is None or validation_filename is None:
            return results
        # Check if files are valid
        [df_train, df_validation] = get_df(src, train_filename, validation_filename)
        results["file_validity"] = [df_train is not None, df_validation is not None]
        if df_train is None or df_validation is None:
            return results

        # Get dimensions of data
        results["rows"] = get_rows(df_train, df_validation)
        results["columns"] = get_columns(df_train, df_validation)

        # Check if dataset is valid for each task
        results["sequence_classification"] = valid_for_sequence_classification(df_train, df_validation)
        results["question_answering"] = valid_for_question_answering(df_train, df_validation)
        results["conditional_language_modelling"] = valid_for_conditional_language_modelling(df_train, df_validation)
        results["unconditional_language_modelling"] = valid_for_unconditional_language_modelling(
            df_train, df_validation
        )
    except Exception as e:
        logger.error(e)
        results["error"] = str(e)
    finally:
        return results
