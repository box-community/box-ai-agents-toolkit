from datetime import timezone, datetime
from typing import Any, Dict, List, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    CopyFileParent,
    FileFull,
    GetFileThumbnailUrlExtension,
    UpdateFileByIdLock,
    UpdateFileByIdParent,
    UpdateFileByIdPermissions,
)

from .box_api_util_generic import current_user_timezone, log_box_api_error


def box_file_info(client: BoxClient, file_id: str) -> Dict[str, Any]:
    """
    Retrieves information about a file in Box.
    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to retrieve information for.
    Returns:
        Dict[str, Any]: The file information.
    """
    try:
        file = client.files.get_file_by_id(file_id=file_id).to_dict()
        return {"file_info": file}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_thumbnail_url(
    client: BoxClient,
    file_id: str,
    extension: Optional[str] = "png",
    min_height: Optional[int] = None,
    min_width: Optional[int] = None,
    max_height: Optional[int] = None,
    max_width: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Retrieves the thumbnail URL of a file from Box.
    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to get the thumbnail for.
        extension (str, optional): The image format for the thumbnail ('png' or 'jpg'). Defaults to 'png'.
        min_height (int, optional): Minimum height of the thumbnail, min 32, max 320. Defaults to None.
        min_width (int, optional): Minimum width of the thumbnail, min 32, max 320. Defaults to None.
        max_height (int, optional): Maximum height of the thumbnail, min 32, max 320. Defaults to None.
        max_width (int, optional): Maximum width of the thumbnail, min 32, max 320. Defaults to None.
    Returns:
        Dict[str, Any]: The thumbnail URL or an error message.
    """
    try:
        ext = (
            GetFileThumbnailUrlExtension.PNG
            if extension.lower() == "png"
            else GetFileThumbnailUrlExtension.JPG
        )
        thumbnail_url = client.files.get_file_thumbnail_url(
            file_id=file_id,
            extension=ext,
            min_height=min_height,
            min_width=min_width,
            max_height=max_height,
            max_width=max_width,
        )
        if thumbnail_url is None or thumbnail_url == "":
            return {"message": "Thumbnail not available for this file."}
        return {"thumbnail_url": thumbnail_url}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_thumbnail_download(
    client: BoxClient,
    file_id: str,
    extension: Optional[str] = "png",
    min_height: Optional[int] = None,
    min_width: Optional[int] = None,
    max_height: Optional[int] = None,
    max_width: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Downloads the thumbnail image of a file from Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to download the thumbnail for.
        extension (str, optional): The image format for the thumbnail ('png' or 'jpg'). Defaults to 'png'.
        min_height (int, optional): Minimum height of the thumbnail, min 32, max 320. Defaults to None.
        min_width (int, optional): Minimum width of the thumbnail, min 32, max 320. Defaults to None.
        max_height (int, optional): Maximum height of the thumbnail, min 32, max 320. Defaults to None.
        max_width (int, optional): Maximum width of the thumbnail, min 32, max 320. Defaults to None.

    Returns:
        Dict[str, Any]: The thumbnail image content in bytes or an error message.
    """
    try:
        ext = (
            GetFileThumbnailUrlExtension.PNG
            if extension.lower() == "png"
            else GetFileThumbnailUrlExtension.JPG
        )
        thumbnail_stream = client.files.get_file_thumbnail_by_id(
            file_id=file_id,
            extension=ext,
            min_height=min_height,
            min_width=min_width,
            max_height=max_height,
            max_width=max_width,
        )
        if thumbnail_stream is None:
            return {"message": "Thumbnail not available for this file."}
        thumbnail_content = thumbnail_stream.read()
        return {"thumbnail_content": thumbnail_content}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_copy(
    client: BoxClient,
    file_id: str,
    destination_folder_id: str,
    new_name: Optional[str] = None,
    version_number: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Copies a file to a specified folder in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to copy.
        destination_folder_id (str): The ID of the destination folder.
        new_name (str, optional): New name for the copied file. Defaults to None.
        version_number (int, optional): The version number of the file to copy. Defaults to None.

    Returns:
        Dict[str, Any]: Information about the copied file including id and name.

    """

    try:
        parent = CopyFileParent(id=destination_folder_id)
        copied_file = client.files.copy_file(
            file_id=file_id,
            parent=parent,
            name=new_name,
            version=version_number,
        )
        return {"copied_file": copied_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_move(
    client: BoxClient,
    file_id: str,
    destination_folder_id: str,
) -> Dict[str, Any]:
    """
    Moves a file to a specified folder in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to move.
        destination_folder_id (str): The ID of the destination folder.

    Returns:
        Dict[str, Any]: Information about the moved file including id and name.

    """

    try:
        parent = UpdateFileByIdParent(id=destination_folder_id)
        moved_file = client.files.update_file_by_id(
            file_id=file_id,
            parent=parent,
        )
        return {"moved_file": moved_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_delete(
    client: BoxClient,
    file_id: str,
    recursive: bool = False,
) -> Dict[str, Any]:
    """
    Deletes a file from Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to delete.
        recursive (bool, optional): Whether to delete all versions of the file. Defaults to False.

    Returns:
        Dict[str, Any]: A message indicating success or an error message.

    """

    try:
        client.files.delete_file_by_id(
            file_id=file_id,
        )
        return {"message": f"File {file_id} deleted successfully."}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_rename(
    client: BoxClient,
    file_id: str,
    new_name: str,
) -> Dict[str, Any]:
    """
    Renames a file in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to rename.
        new_name (str): The new name for the file.

    Returns:
        Dict[str, Any]: Information about the renamed file including id and name.

    """

    try:
        renamed_file = client.files.update_file_by_id(
            file_id=file_id,
            name=new_name,
        )
        return {"renamed_file": renamed_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_set_description(
    client: BoxClient,
    file_id: str,
    description: str,
) -> Dict[str, Any]:
    """
    Sets the description of a file in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to update.
        description (str): The new description for the file.

    Returns:
        Dict[str, Any]: Information about the updated file including id and description.

    """

    try:
        updated_file = client.files.update_file_by_id(
            file_id=file_id,
            description=description,
        )
        return {"updated_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_retention_date_set(
    client: BoxClient,
    file_id: str,
    retention_date: datetime,
) -> Dict[str, Any]:
    """
    Sets the retention date of a file in Box.  This date cannot be shortened once set on a file.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to update.
        retention_date (DateTime): The new retention date for the file.

    Returns:
        Dict[str, Any]: Information about the updated file including id and retention date.

    """

    try:
        if retention_date is not None:
            # If datetime is naive (no timezone), add user's timezone or UTC
            if retention_date.tzinfo is None:
                user_tz = current_user_timezone(client)
                if user_tz is not None:
                    retention_date = retention_date.replace(tzinfo=user_tz)
                else:
                    retention_date = retention_date.replace(tzinfo=timezone.utc)
        # '400 not a valid rfc 3339 formatted date; Request ID: 4fh1m2i7fxxmr844'
        date_str = retention_date.strftime("%Y-%m-%dT%H:%M:%S%z")
        updated_file: FileFull = client.files.update_file_by_id(
            file_id=file_id,
            disposition_at=date_str,
        )
        return {"updated_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_retention_date_clear(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """
    Clears the retention date of a file in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to update.

    Returns:
        Dict[str, Any]: Information about the updated file including id and retention date.

    """

    try:
        updated_file: FileFull = client.files.update_file_by_id(
            file_id=file_id,
            disposition_at=None,
        )
        return {"updated_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_lock(
    client: BoxClient,
    file_id: str,
    lock_expires_at: Optional[datetime] = None,
    is_download_prevented: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Defines a lock on an item.
    This prevents the item from being moved, renamed, or otherwise changed by anyone other than the user who created the lock.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to lock.
        lock_expires_at (DateTime, optional): The date and time when the lock expires. Defaults to None.
        is_download_prevented (bool, optional): Whether to prevent downloads while the file is

    Returns:
        Dict[str, Any]: Information about the locked file including id and lock details.

    """

    try:
        lock = UpdateFileByIdLock(
            type="lock",
            is_download_prevented=is_download_prevented,
            expires_at=lock_expires_at,
        )
        updated_file = client.files.update_file_by_id(
            file_id=file_id,
            lock=lock,
        )
        return {"locked_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_unlock(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """
    Removes a lock from an item.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to unlock.

    Returns:
        Dict[str, Any]: Information about the unlocked file including id and lock details.

    """

    try:
        lock = None  # Setting lock to None removes the lock
        updated_file = client.files.update_file_by_id(
            file_id=file_id,
            lock=lock,
        )
        return {"unlocked_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_set_download_open(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """
    Allows anyone with access to the file to download it.
    This setting overrides the download permissions that are normally part of the role of a collaboration.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to update.

    Returns:
        Dict[str, Any]: Information about the updated file including id and download settings.

    """

    try:
        updated_file = client.files.update_file_by_id(
            file_id=file_id,
            permissions=UpdateFileByIdPermissions(can_download="open"),
        )
        return {"updated_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_set_download_company(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """
    Sets a file to be downloadable and openable.
    This setting overrides the download permissions that are normally part of the role of a collaboration.
    When set to company, this essentially removes the download option for external users with viewer or editor roles.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to update.

    Returns:
        Dict[str, Any]: Information about the updated file including id and download settings.

    """

    try:
        updated_file = client.files.update_file_by_id(
            file_id=file_id,
            permissions=UpdateFileByIdPermissions(can_download="company"),
        )
        return {"updated_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_set_download_reset(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """
    Resets the download permissions of a file to the default behavior based on collaboration roles.
    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to update.
    Returns:
        Dict[str, Any]: Information about the updated file including id and download settings.

    """

    try:
        updated_file = client.files.update_file_by_id(
            file_id=file_id,
            permissions=None,
        )
        return {"updated_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_tag_list(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """
    Lists the tags associated with a file in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to retrieve tags for.

    Returns:
        Dict[str, Any]: The list of tags or an error message.

    """

    try:
        file = client.files.get_file_by_id(
            file_id=file_id,
            fields=["tags"],
        )
        tags = [tag for tag in file.tags] if file.tags else []
        if tags is None or len(tags) == 0:
            return {"message": "No tags found for this file."}
        return {"tags": tags}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_tag_add(
    client: BoxClient,
    file_id: str,
    tag: str,
) -> Dict[str, Any]:
    """
    Adds a tag to a file in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to add a tag to.
        tag (str): The tag to add.

    Returns:
        Dict[str, Any]: Information about the updated file including id and tags.

    """

    try:
        existing_tags: List[str] = client.files.get_file_by_id(
            file_id=file_id,
            fields=["tags"],
        ).tags
        tags = [t for t in existing_tags] if existing_tags else []
        if tag not in tags:
            tags.append(tag)

        updated_file = client.files.update_file_by_id(
            file_id=file_id,
            tags=tags,
            fields=["tags"],
        )
        return {"updated_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_file_tag_remove(
    client: BoxClient,
    file_id: str,
    tag: str,
) -> Dict[str, Any]:
    """
    Removes a tag from a file in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to remove a tag from.
        tag (str): The tag to remove.

    Returns:
        Dict[str, Any]: Information about the updated file including id and tags.

    """

    try:
        existing_tags = client.files.get_file_by_id(
            file_id=file_id,
            fields=["tags"],
        ).tags
        tags = [t for t in existing_tags] if existing_tags else []
        if tag in tags:
            tags.remove(tag)

        updated_file = client.files.update_file_by_id(
            file_id=file_id,
            tags=tags,
            fields=["tags"],
        )
        return {"updated_file": updated_file.to_dict()}

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}
