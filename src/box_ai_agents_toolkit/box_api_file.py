import logging
import mimetypes
import os
import tempfile
import time
from enum import Enum
from typing import Any, Dict, Optional, Tuple, Union

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    File,
    UploadFileAttributes,
    UploadFileAttributesParentField,
)
from requests import HTTPError

from .box_api_util_http import _do_request

logging.basicConfig(level=logging.INFO)


def box_file_get_by_id(client: BoxClient, file_id: str) -> File:
    return client.files.get_file_by_id(file_id=file_id)


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
        logging.error(f"Error retrieving file representation {file_id}: {e.message}")
        raise e

    if file_representation is None:
        logging.info(
            f"Representation of type {representation_type.value} is impossible for file {file_id}."
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
        logging.error(f"Error downloading markdown content: {e.response.reason}")
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
        logging.info(
            f"{representation_type.value} representation is impossible for file {file_id}."
        )
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

    representation = _process_file_representation(
        client, RepresentationType.EXTRACTED_TEXT, file_id
    )

    return representation


def box_file_download(
    client: BoxClient,
    file_id: Any,
    save_file: bool = False,
    save_path: Optional[str] = None,
) -> Tuple[Optional[str], Optional[bytes], Optional[str]]:
    """
    Downloads a file from Box and optionally saves it locally.

    Args:
        client (BoxClient): An authenticated Box client
        file_id (Any): The ID of the file to download. Can be string or int.
        save_file (bool, optional): Whether to save the file locally. Defaults to False.
        save_path (str, optional): Path where to save the file. Defaults to None.

    Returns:
        Tuple containing:
            - path_saved (str or None): Path where file was saved if save_file=True
            - file_content (bytes): Raw file content
            - mime_type (str): Detected MIME type

    Raises:
        BoxSDKError: If an error occurs during file download
    """
    # Ensure file_id is a string
    file_id_str = str(file_id)

    # Get file info first to check file type
    file_info = client.files.get_file_by_id(file_id_str)
    file_name = file_info.name

    # Download the file
    download_stream = client.downloads.download_file(file_id_str)
    file_content = download_stream.read()

    # Get file extension and detect mime type
    # apparently not used
    # file_extension = file_name.split(".")[-1].lower() if "." in file_name else ""
    mime_type, _ = mimetypes.guess_type(file_name)

    # Save file locally if requested
    saved_path = None
    if save_file:
        # Determine where to save the file
        if save_path:
            # Use provided path
            full_save_path = save_path
            if os.path.isdir(save_path):
                # If it's a directory, append the filename
                full_save_path = os.path.join(save_path, file_name)
        else:
            # Use temp directory with the original filename
            temp_dir = tempfile.gettempdir()
            full_save_path = os.path.join(temp_dir, file_name)

        # Save the file
        with open(full_save_path, "wb") as f:
            f.write(file_content)
        saved_path = full_save_path

    return saved_path, file_content, mime_type


# File Upload and Download Functions


def box_upload_file(
    client: BoxClient,
    content: Union[str, bytes],
    file_name: str,
    folder_id: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Uploads content as a file to Box.

    Args:
        client (BoxClient): An authenticated Box client
        content (str): The content to upload as a file
        file_name (str): The name to give the file in Box
        folder_id (Any, optional): The ID of the folder to upload to. Can be string or int.
                                  Defaults to "0" (root).

    Returns:
        Dict containing information about the uploaded file including id and name

    Raises:
        BoxSDKError: If an error occurs during file upload
    """
    # Create a temporary file; choose write mode based on content type
    is_bytes = isinstance(content, (bytes, bytearray))
    mode = "wb" if is_bytes else "w"
    with tempfile.NamedTemporaryFile(mode=mode, delete=False) as temp_file:
        # Write bytes or text
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # Upload the file
        with open(temp_file_path, "rb") as file:
            # Use root folder if folder_id is not provided
            parent_id = "0"
            if folder_id is not None:
                parent_id = str(folder_id)

            uploaded_file = client.uploads.upload_file(
                UploadFileAttributes(
                    name=file_name, parent=UploadFileAttributesParentField(id=parent_id)
                ),
                file,
            )

            # Return the first entry which contains file info
            return {
                "id": uploaded_file.entries[0].id,
                "name": uploaded_file.entries[0].name,
                "type": uploaded_file.entries[0].type,
            }
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)
