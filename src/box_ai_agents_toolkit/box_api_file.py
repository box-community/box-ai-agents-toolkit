import logging
import mimetypes
import os
import tempfile
from typing import Any, Dict, Optional, Tuple

from box_sdk_gen import (
    BoxClient,
    File,
    UploadFileAttributes,
    UploadFileAttributesParentField,
)

from box_ai_agents_toolkit.box_api_util_http import _do_request

logger = logging.basicConfig(level=logging.DEBUG)


def box_file_get_by_id(client: BoxClient, file_id: str) -> File:
    return client.files.get_file_by_id(file_id=file_id)


def box_file_text_extract(client: BoxClient, file_id: str) -> str:
    # Request the file with the "extracted_text" representation hint
    file_text_representation = client.files.get_file_by_id(
        file_id,
        x_rep_hints="[extracted_text]",
        fields=["name", "representations"],
    )
    # Check if any representations exist
    if not file_text_representation.representations.entries:
        logger.debug(f"No representation for file {file_text_representation.id}")
        return ""

    # Find the "extracted_text" representation
    extracted_text_entry = next(
        (
            entry
            for entry in file_text_representation.representations.entries
            if entry.representation == "extracted_text"
        ),
        None,
    )
    if not extracted_text_entry:
        return ""

    # Handle cases where the extracted text needs generation
    if extracted_text_entry.status.state == "none":
        _do_request(extracted_text_entry.info.url)  # Trigger text generation

    # Construct the download URL and sanitize filename
    url = extracted_text_entry.content.url_template.replace("{+asset_path}", "")

    # Download and truncate the raw content
    raw_content = _do_request(client, url)

    # check to see if raw content is bytes
    if isinstance(raw_content, bytes):
        return raw_content.decode("utf-8")
    else:
        return raw_content


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
    client: BoxClient, content: str, file_name: str, folder_id: Optional[Any] = None
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
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
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
