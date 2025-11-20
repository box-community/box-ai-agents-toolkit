import time
from enum import Enum
from typing import Any, Dict, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
)
from requests import HTTPError

from .box_api_util_generic import log_box_api_error, log_generic_error
from .box_api_util_http import _do_request


class RepresentationError(Exception):
    pass


class RepresentationType(Enum):
    MARKDOWN = "markdown"
    EXTRACTED_TEXT = "extracted_text"


class FileRepresentationStatus(Enum):
    NONE = "none"
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"
    IMPOSSIBLE = "impossible"
    UNKNOWN = "unknown"


class FileRepresentationResult:
    def __init__(
        self,
        status: FileRepresentationStatus,
        info_url: Optional[str] = None,
        content_url: Optional[str] = None,
    ):
        self.status = status
        self.info_url = info_url
        self.content_url = content_url


def _file_representation_status_check(
    client: BoxClient, representation_type: RepresentationType, file_id: str
) -> FileRepresentationResult:
    """
    Checks the representations of a file and returns their status.

    Args:
        client (BoxClient): An authenticated Box client.
        representation_type (RepresentationType): The type of representation to check for.
        file_id (str): The ID of the file to check representations for.
    Returns:
        FileRepresentationResult: An object containing the status and URLs of the representation.

    """
    file_representation_status = FileRepresentationStatus.IMPOSSIBLE
    file_representation = None
    try:
        file = client.files.get_file_by_id(
            file_id,
            x_rep_hints=f"[{representation_type.value}]",
            fields=["name", "representations"],
        )
        if file.representations and file.representations.entries:
            file_representation = file.representations.entries[0]

    except BoxAPIError as e:
        log_box_api_error(e)
        raise e

    if file_representation is None:
        log_generic_error(
            RepresentationError(
                f"Representation of type {representation_type.value} is impossible for file {file_id}."
            )
        )
        file_representation_status = FileRepresentationStatus.IMPOSSIBLE

    # Convert all status
    if file_representation and file_representation.status:
        file_representation_status = FileRepresentationStatus(
            file_representation.status.state
        )

    info_url = None
    content_url = None

    if (
        file_representation
        and file_representation.info
        and file_representation.info.url
    ):
        info_url = file_representation.info.url

    if (
        file_representation
        and file_representation.content
        and file_representation.content.url_template
    ):
        content_url = file_representation.content.url_template

    return FileRepresentationResult(
        status=file_representation_status,
        info_url=info_url,
        content_url=content_url,
    )


def _request_file_representation_generation(
    client: BoxClient, info_url: Optional[str]
) -> Dict[str, Any]:
    if info_url is None:
        return {"error": "No URL provided for representation generation."}
    # request representation generation
    _do_request(client, info_url)
    return {"message": "Representation generation requested."}


def _download_file_representation(
    client: BoxClient, url_template: Optional[str]
) -> Dict[str, Any]:
    if url_template is None:
        return {"error": "No URL provided for representation download."}

    url = url_template.replace("{+asset_path}", "")

    try:
        response = _do_request(client, url)
        return {"content": f"{response.decode('utf-8')}"}
    except HTTPError as e:
        log_generic_error(e)
        return {"error": e.response.reason}


def _process_file_representation(
    client: BoxClient,
    representation_type: RepresentationType,
    file_id: str,
    is_recursive=False,
) -> Dict[str, Any]:
    representation = _file_representation_status_check(
        client, representation_type, file_id
    )

    if representation.status == FileRepresentationStatus.NONE:
        # request generation
        _request_file_representation_generation(client, representation.info_url)
        if not is_recursive:
            time.sleep(5)  # wait a bit before checking again
            return _process_file_representation(
                client, representation_type, file_id, is_recursive=True
            )
        return {
            "message": f"{representation_type.value} representation generation requested.",
            "status": representation.status.value,
        }

    if representation.status == FileRepresentationStatus.PENDING:
        if not is_recursive:
            time.sleep(5)  # wait a bit before checking again
            return _process_file_representation(
                client, representation_type, file_id, is_recursive=True
            )
        return {
            "message": f"{representation_type.value} representation is still being generated. Please try again later.",
            "status": representation.status.value,
        }

    if representation.status == FileRepresentationStatus.SUCCESS:
        return _download_file_representation(client, representation.content_url)

    if representation.status == FileRepresentationStatus.ERROR:
        return {
            "error": f"Error generating {representation_type.value} representation.",
            "status": representation.status.value,
        }

    if representation.status == FileRepresentationStatus.IMPOSSIBLE:
        return {
            "error": f"{representation_type.value} representation is impossible for this file.",
            "status": representation.status.value,
        }

    return {
        "error": f"Unknown status for {representation_type.value} representation.",
        "status": FileRepresentationStatus.UNKNOWN.value,
    }


def box_file_text_extract(client: BoxClient, file_id: str) -> Dict[str, Any]:
    """
    Extracts text from a file in Box. The result can be markdown or plain text.
    If a markdown representation is available, it will be preferred.
    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to extract text from.
    Returns:
        Dict[str, Any]: The extracted text.
    """
    try:
        # First we check if file representation markdown is available
        representation = _process_file_representation(
            client, RepresentationType.MARKDOWN, file_id
        )
        if (
            representation.get("status") != FileRepresentationStatus.IMPOSSIBLE.value
            and representation.get("status") != FileRepresentationStatus.ERROR.value
            and representation.get("status") != FileRepresentationStatus.UNKNOWN.value
        ):
            return representation

        # Fallback to extracted text representation
        representation = _process_file_representation(
            client, RepresentationType.EXTRACTED_TEXT, file_id
        )

        return representation
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": f"Box API Error: {e.message}"}
