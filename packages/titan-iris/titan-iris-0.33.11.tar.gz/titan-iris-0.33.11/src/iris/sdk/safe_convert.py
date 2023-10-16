"""Safetensors conversion script."""
import os
from collections import defaultdict
from pathlib import Path
from typing import Sequence, Union

import torch
from safetensors.torch import load_file, save_file
from transformers import AutoModel


def shared_pointers(tensors: Sequence[torch.Tensor]):
    """Finds all pointers who share a matrix value.

    Args:
        tensors: The tensors stored in a model's state_dict

    Returns:
        object: A list of lists of pointers which point to a given tensor, where this is more than 1.
    """
    ptrs = defaultdict(list)
    for k, v in tensors.items():
        ptrs[v.data_ptr()].append(k)
    failing = []
    for ptr, names in ptrs.items():
        if len(names) > 1:
            failing.append(names)
    return failing


def check_file_size(sf_filename: str, pt_filename: str) -> None:
    """Check file sizes.

    Checks that only shared tensors have been replaced by asserting that the input and output
    weights files are the same size.

    Args:
        sf_filename: Filename of the converted safetensor file.
        pt_filename: Filename of the input model file.

    Raises:
        RuntimeError: If the file sizes are different by more than 1%.

    """
    sf_size = os.stat(sf_filename).st_size
    pt_size = os.stat(pt_filename).st_size

    if (sf_size - pt_size) / pt_size > 0.01:
        raise RuntimeError(
            f"""The file size different is more than 1%:
         - {sf_filename}: {sf_size}
         - {pt_filename}: {pt_size}
         """
        )


def convert_file(
    pt_filename: str,
    sf_filename: str,
):
    """Converts a standard pytorch model into a safetensors-saved one.

    Args:
        pt_filename: Filename of input pytorch model.
        sf_filename: Filename to which output safetensors file is to be saved.
    """
    loaded = torch.load(pt_filename, map_location="cpu")
    if "state_dict" in loaded:
        loaded = loaded["state_dict"]

    # To prevent the same matrix being safetensor-ized multiple times, a given matrix can only be
    # pointed to from a state_dict entry once. Find all matrices who have more than one pointer to them,
    # then delete all but the first of these references from state_dict. Then save as safetensor.
    # The deleted references are restored on model load by huggingface transformers voodoo.
    shared = shared_pointers(loaded)
    for shared_weights in shared:
        for name in shared_weights[1:]:
            loaded.pop(name)

    # For tensors to be contiguous
    loaded = {k: v.contiguous() for k, v in loaded.items()}
    dirname = os.path.dirname(sf_filename)
    os.makedirs(dirname, exist_ok=True)
    save_file(loaded, sf_filename, metadata={"format": "pt"})
    check_file_size(sf_filename, pt_filename)
    reloaded = load_file(sf_filename)
    for k in loaded:
        pt_tensor = loaded[k]
        sf_tensor = reloaded[k]
        if not torch.equal(pt_tensor, sf_tensor):
            raise RuntimeError(f"The output tensors do not match for key {k}")


def do_convert(model_path: Union[Path, str]) -> None:
    """Takes an input model, and tries to convert it to safetensors.

    Checks if it is already in safetenors format, else attempts to convert it by two methods.
    Method 1: The safetensors/transformers safe_serialization=True method (quicker, works for non-shared-weight models).
    Method 2: Adaptation of weight-sharing-compatible conversion in convert_file.
    Method 2 is adapted from https://github.com/huggingface/safetensors/issues/98

    Args:
        model_path (str): an input pytorch model path (pointing to a folder which contains pytorch_model.bin).

    Returns:
        None.

    """
    sf_filename = os.path.join(model_path, "model.safetensors")
    if os.path.exists(sf_filename):
        print("Model is already in safetensors format")
        return

    print(f"Attempting conversion of {model_path} to safetensors format...")

    try:
        model = AutoModel.from_pretrained(model_path)
        model.save_pretrained(model_path, safe_serialization=True)
        print("Conversion completed.")
    except RuntimeError:
        print(
            "Basic conversion method failed (likely due to the selected model using shared weights), \
                attempting secondary method..."
        )
        convert_file(model_path + "/pytorch_model.bin", sf_filename)
        print("Conversion completed.")
