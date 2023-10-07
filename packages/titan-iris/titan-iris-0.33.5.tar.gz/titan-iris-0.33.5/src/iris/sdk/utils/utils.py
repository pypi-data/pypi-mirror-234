"""This file contains the helper functions for the Iris package."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

from logging import getLogger

import requests

logger = getLogger("iris.utils.utils")

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                         Utils                                                        #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# rw = RefinedWed ==> Falcon
VALID_QLORA_MODELS = ["t5", "pythia", "opt", "gptj", "gptneo", "falcon", "llama", "rw", "refinedweb"]


def valid_qlora(model_name: str, local_family: str):
    """Cleanses an input model name and then checks if QLoRA has been implemented for it.

    This is based on those available in Olympus.

    Args:
        model_name: A model name as from model_name_or_path
        local_family: The model family if it has previously been determined (for uploaded models).

    Returns: (Bool) Whether QLoRa is supported for the given model.

    """

    def clean(x: str) -> str:
        return x.replace("-", "").replace("_", "").lower()

    if local_family and local_family in VALID_QLORA_MODELS:
        return True

    if any(ext in clean(model_name) for ext in VALID_QLORA_MODELS):
        return True
    return False


def prompt(instruction: str):
    """Generate prompt text.

    Args:
        instruction (str): prompt text

    Returns:
        str: generated prompt text
    """
    return f"You are the Assistant, designed to help the user complete their task.\
             Below is an instruction from the user. Complete the user's instruction. \
             Do not end with the word User. \n\nUser:\n{instruction}\n\nAssistant:"


def stream_generate(text, port=8000):
    """Stream the response from the generate endpoint. This is used for the 'iris takeoff --infer' command.

    Args:
        text (str): the text to generate from.
        port (int): the port to send the request to.
    """
    text = prompt(text)
    response = requests.post(f"http://localhost:{port}/generate_stream", json={"text": text}, stream=True)

    if response.encoding is None:
        response.encoding = "utf-8"

    for text in response.iter_content(chunk_size=1, decode_unicode=True):
        if text:
            print(text, end="", flush=True)
