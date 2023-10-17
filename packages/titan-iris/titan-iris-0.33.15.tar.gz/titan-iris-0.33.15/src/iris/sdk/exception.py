"""Iris Exception Types."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

from typing import Optional

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Iris Exception Types                                                  #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class IrisException(Exception):
    """Error raised when occurs an unidentified internal error in the iris package."""

    message = "Iris Command Error"

    def __init__(self, message: Optional[str] = None, details: Optional[str] = None):
        """Create an IrisException.

        Args:
            message (str): Error message. This will replace the defined class message.
            details (str): Details about the error.
        """
        self.message = self._compose_message(message=message, details=details)
        super().__init__(self.message)

    def __str__(self):
        """String representation of the error."""
        return self.message

    def _compose_message(self, message: Optional[str] = None, details: Optional[str] = None) -> str:
        """Composition of the error message.

        Args:
            message (str): Error message. This will replace the defined class message.
            details (str): Details about the error.

        Returns:
            message (str): A message  error with the following format:
                self.message: message - details
        """
        return " - ".join([msg for msg in [message or self.message, details] if msg])


# ────────────────────────────────────────────── BAD REQUEST Exceptions ────────────────────────────────────────────── #


class InvalidLoginError(IrisException):
    """Error raised when the login is invalid."""

    message = "Invalid login credentials. Are you logged in?"


class EndpointNotFoundError(IrisException):
    """Error raised when the endpoint is not found."""

    message = "Endpoint not found: "


class BadRequestError(IrisException):
    """Error raised when there are input data errors."""

    message = "Bad request error. Please check your input data"


class UnprocessableEntityError(IrisException):
    """Error raised when there are input data errors."""

    message = "Unprocessable entity error. Please check your input data"


class DownloadLinkNotFoundError(IrisException):
    """Error raised when the download link is not found."""

    message = "Download link not found"


class KeyFileDoesntExistError(IrisException):
    """Error raised when the keyfile is not found, which means that the user is not logged in."""

    message = "Keyfile doesn't exist. User should login"


class KeyFileExpiredError(IrisException):
    """Error raised when the user stored key has expired."""

    message = "Stored key has expired. Please login again"


class InvalidCommandError(IrisException):
    """Error raised when the command is invalid."""

    message = "Invalid command. Please check your command again!"


class DownloadLinkExpiredError(IrisException):
    """Error raised when the download link is expired."""

    message = "This download link is already expired. This expire time is: "


class ArtefactNotFoundError(IrisException):
    """Error raised when attempting to upload a nonexistent artefact."""

    message = "File not found"


class ArtefactTypeNotAFolderError(IrisException):
    """Error raised when attempting to upload an artefact which is not a folder."""

    message = "Only directories are supported as a container for artefact uploads."


class ArtefactTypeInferError(IrisException):
    """Artefact type inference error.

    Error raised when attempting to upload an artefact whose type
    cannot be ascertained due to lacking the format to be considered any of the artefact types.
    """

    message = "The contents of the given directory do not match the format of any permitted artefact type."


class UnsafeTensorsError(IrisException):
    """Error raised when attempting to upload a model (artefact) which does not contain a .safetensors file."""

    message = (
        "Only models safely saved using safetensors are compatible. Use Iris makesafe <model> to convert the model, "
        "or see https://huggingface.co/docs/safetensors/index"
    )


class MissingTokenizerError(IrisException):
    """Error raised when attempting to upload a model (artefact) which doesn't have a tokenizer."""

    message = "Only models saved alongside tokenizers are compatible."


class InvalidDatasetFormatError(IrisException):
    """Error raised when a dataset is missing train.csv and val.csv."""

    message = "Folders with (at least) train.csv and val.csv are the only permitted formats for datasets"


class UnknownFamilyError(IrisException):
    """Error raised when a model's tokenizer_config.json file has a missing or unrecognised 'tokenizer_class'."""

    message = (
        "Model family could not be specified. If not detailed in config.json or tokenizer_config.json, "
        "the model must be uploaded via Iris Upload with the -model-family arg (--mf)"
    )


class UploadOnPostError(IrisException):
    """Error raised when a local model provided to Iris Post for upload fails to upload properly."""

    message = "Specified local model could not be uploaded. Try 'iris upload <model>' for a more specific diagnosis'"


class JobStillRunningError(IrisException):
    """Error raised when a job is still running."""

    message = "Job still running. Please wait until it finishes."
