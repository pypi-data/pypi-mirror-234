"""This file contains the display related helper functions for the Iris package."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import json
import os
from logging import getLogger
from typing import Mapping, Optional

import jmespath
from tabulate import tabulate

logger = getLogger("iris.utils.display_utils")

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                    Display Utils                                                     #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def dump(response, query: Optional[str] = None):
    """load, a response, optionally apply a query to its returned json, and then pretty print the result."""
    content = response
    if hasattr(response, "json"):
        content = response.json()  # shorthand for json.loads(response.text)
    if query:
        try:
            content = jmespath.search(query, content)
        except jmespath.exceptions.ParseError as e:
            print("Error parsing response")
            raise e

    return json.dumps(
        {"response": content},
        indent=4,
    )


def exception_to_json_error(e: Exception):
    """Convert an exception to a json string with the error message and type."""
    logger.error(e)
    if os.getenv("IRIS_LOG_LEVEL") == "DEBUG":
        import traceback

        print(traceback.print_exc())
        raise e
    error_dict = {"status": "failed", "error": str(e), "type": type(e).__name__}
    if hasattr(e, "status_code"):
        error_dict["status_code"] = e.status_code
    return json.dumps(error_dict, indent=4)


def flatten_dict(dict: dict) -> dict:
    """Flatten a nested dictionary.

    Args:
        dict (dict): a nested dictionary

    Returns:
        dict: a flattened dictionary
    """
    flattened_dict = {}
    for key, sub_dict in dict.items():
        for sub_key, value in sub_dict.items():
            flattened_key = f"{key}/{sub_key}"
            flattened_dict[flattened_key] = value
    return flattened_dict


def print_status_dict_results(dict: Mapping[str, float]) -> None:
    """Print a dictionary in a pretty format. Notice that the dictionary is flattened.

    e.g. input should be:
    {
        "status": "success",
        "message": "dispatched",
        "output": 15
    }.

    Args:
        dict (Mapping[str, float]): dictionary to print
    """
    headers = dict.keys()
    table = [[dict[k] for k in headers]]

    headers = [f"\033[1;31m{i}\033[0m" for i in headers]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def print_get_dict_results(dict: Mapping[str, float], experiment: bool = True, key_name: str = "UUID") -> None:
    """Print a dictionary in a pretty format.

    Args:
        dict (Mapping[str, float]): dictionary to print
        experiment (bool, optional): Whether the dict is a response from iris get experiment. Defaults to True.
        key_name (str, optional): The name of the key to use as the first column. Defaults to "UUID".
    """
    dict = flatten_dict(dict) if experiment else dict
    first_col = ["ID/Name"] if experiment else [key_name]

    headers = first_col + list(next(iter(dict.values())).keys())
    # Transform the data into a list of lists
    table = []  # table headers
    for key, values in dict.items():
        row = [key]
        for k in headers:
            if k in {"ID/Name", key_name}:
                pass
            elif k == "Job Results":
                if values[k] is not None:
                    row.append("\n".join(values[k]))
                else:
                    row.append("None")
            else:
                row.append(values[k])
        table.append(row)

    headers = [f"\033[1;31m{i}\033[0m" for i in headers]  # make the headers red and bold
    # Print the table
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def extract_experiment_results(experiment: dict, results_table: dict):
    """Extract the results from a experiment dict. return a clean format of dict of results.

    Args:
        experiment (dict): dict of detailed experiment information.
        results_table (dict): dict of results to be updated.
    """
    experiment_id = experiment["id"]  # store the numerical experiment id
    results_table[experiment_id] = {}
    if "jobs" in experiment:
        jobs = experiment["jobs"]
        if "tasks" in jobs[0]:
            tasks = jobs[0]["tasks"]

            # extract the results from the tasks
            for task in tasks:
                results_table[experiment_id][task["name"]] = {"Job Status": task["status"]}
                results_table[experiment_id][task["name"]]["Job Results"] = (
                    [f"{key}: {value}" for key, value in task["results"].items()] if task["results"] else None
                )


def handle_iris_get_response(response):
    """Handle the response from the iris get endpoint. Turn the json response into a pretty table.

    Args:
        response (str): a json format response from the iris get endpoint.
    """
    json_response = json.loads(response)
    if "response" in json_response:
        json_response = json_response["response"]
    # check if 'experiments' in the response, this is for the common case 'iris get'
    if "experiments" in json_response:
        experiments = json_response["experiments"]
        if experiments:
            results_table = {}
            for experiment in experiments:
                extract_experiment_results(experiment, results_table)
            # sort the results table by experiment id, get the most recent 5 experiments
            sorted_results_table = dict(sorted(results_table.items(), key=lambda item: item[0], reverse=True)[:5])
            print_get_dict_results(sorted_results_table)
        else:
            print_status_dict_results(json_response)
    elif "experiment" in json_response:
        experiment = json_response["experiment"]

        results_table = {}
        extract_experiment_results(experiment, results_table)
        print_get_dict_results(results_table)
    elif "artefacts" in json_response:
        artefacts = json_response["artefacts"]
        if artefacts:
            if not isinstance(artefacts, list):
                artefacts = [artefacts]
            results_table = {
                artefact["uuid"]: {
                    "name": artefact["name"],
                    "type": artefact["artefact_type"],
                }
                for artefact in artefacts
            }
            print_get_dict_results(results_table, experiment=False, key_name="UUID")
        else:
            print_status_dict_results(json_response)
    elif "sessions" in json_response:
        sessions = json_response["sessions"]
        if sessions:
            results_table = {
                session["uuid"]: {
                    "model": session["model"],
                    "status": session["status"],
                    "expiration_datetime (UTC)": session["expiration_datetime"],
                    "external_endpoint": session["external_endpoint"],
                    "endpoint_path": session["endpoint_path"],
                }
                for session in sessions
            }
            print_get_dict_results(results_table, experiment=False, key_name="UUID")
        else:
            print_status_dict_results(json_response)
    elif len(json_response) > 0 and len(json_response[0][0]) > 0 and "message" in json_response[0][0]:
        messages = json_response[0]
        results_table = {
            message["name"]: {
                "status": message["status"],
                "message": message["message"]["message"],
                "progress": message["message"]["progress"],
            }
            for message in messages
        }
        print_get_dict_results(results_table, experiment=False, key_name="Task Name")
    else:
        print(json.dumps(json_response, indent=4))
