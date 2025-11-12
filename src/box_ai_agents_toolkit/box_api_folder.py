from dataclasses import fields
from typing import Any, List, Optional, Union

from box_sdk_gen import (
    BoxClient,
    BoxAPIError,
    CreateFolderParent,
    File,
    Folder,
    FolderMini,
    UpdateFolderByIdParent,
    UpdateFolderByIdCollections,
    Collections,
    Collection,
)

from .box_api_util_generic import log_box_api_error


def box_folder_info(client: BoxClient, folder_id: str) -> dict[str, Any]:
    """Retrieve information about a specific folder in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): ID of the folder to retrieve information for.
    Returns:
        dict[str, Any]: Dictionary containing folder information or error message.
    """
    try:
        folder_info = client.folders.get_folder_by_id(folder_id)
        return {"folder": folder_info.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_items_list(
    client: BoxClient,
    folder_id: str,
    is_recursive: bool = False,
    limit: Optional[int] = 1000,
) -> dict[str, Any]:
    """List items in a Box folder with optional recursive traversal.

    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): ID of the folder to list items from.
        is_recursive (bool, optional): Whether to recursively list subfolder contents. Defaults to False.
        limit (Optional[int], optional): Maximum items per API call. Defaults to 1000.

    Returns:
        dict[str, Any]: Dictionary containing folder items list or error message.
    """

    def process_items(entries: List[Any]) -> List[dict]:
        """Process folder entries, recursively traversing subfolders if needed."""
        items = []
        for item in entries:
            item_dict = item.to_dict()
            if item.type == "folder" and is_recursive:
                subfolder_result = box_folder_items_list(
                    client, item.id, is_recursive, limit
                )
                # Nest subfolder items under the 'items' attribute
                if "folder_items" in subfolder_result:
                    item_dict["items"] = subfolder_result["folder_items"]
            items.append(item_dict)
        return items

    try:
        result: List[dict] = []
        marker: Optional[str] = None

        while True:
            folder_items = client.folders.get_folder_items(
                folder_id=folder_id,
                usemarker=True,
                limit=limit,
                marker=marker,
            )

            if not folder_items.entries:
                break

            result.extend(process_items(folder_items.entries))

            if folder_items.next_marker is None:
                break
            marker = folder_items.next_marker

        return (
            {"folder_items": result}
            if result
            else {"message": "No items found in folder."}
        )

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_create(
    client: BoxClient, name: str, parent_folder_id: str
) -> dict[str, Any]:
    """
    Creates a new folder in Box.
    Args:
        client (BoxClient): An authenticated Box client
        name (str): Name of the new folder
        parent_folder_id (str): ID of the parent folder where the new folder will be created, use "0" for root folder
    Returns:
        dict[str, Any]: Dictionary containing the created folder object or error message
    """
    try:
        parent = CreateFolderParent(id=parent_folder_id)
        new_folder = client.folders.create_folder(name=name, parent=parent)
        return {"folder": new_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_delete(
    client: BoxClient, folder_id: str, recursive: bool = False
) -> dict[str, Any]:
    """
    Deletes a folder from Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (Any): ID of the folder to delete. Can be string or int.
        recursive (bool, optional): Whether to delete recursively. Defaults to False.

    Raises:
        BoxSDKError: If an error occurs during folder deletion
    """
    try:
        client.folders.delete_folder_by_id(folder_id=folder_id, recursive=recursive)
        return {"message": f"Folder {folder_id} deleted successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_copy(
    client: BoxClient,
    folder_id: Any,
    destination_parent_folder_id: Any,
    name: Optional[str] = None,
) -> dict[str, Any]:
    """
    Copies a folder to a new location in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (Any): ID of the folder to copy. Can be string or int.
        destination_parent_folder_id (Any): ID of the destination parent folder. Can be string or int.
        name (str, optional): New name for the copied folder. If not provided, original name is used.
    Returns:
        dict[str, Any]: Dictionary containing the copied folder object or error message
    """
    try:
        destination_parent = CreateFolderParent(id=str(destination_parent_folder_id))
        copied_folder = client.folders.copy_folder(
            folder_id=str(folder_id),
            parent=destination_parent,
            name=name,
        )
        return {"folder": copied_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_move(
    client: BoxClient,
    folder_id: str,
    destination_parent_folder_id: str,
) -> dict[str, Any]:
    """
    Moves a folder to a new location in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to move.
        destination_parent_folder_id (str): ID of the destination parent folder.
    Returns:
        dict[str, Any]: Dictionary containing the moved folder object or error message
    """
    try:
        destination_parent = CreateFolderParent(id=destination_parent_folder_id)
        moved_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            parent=destination_parent,
        )
        return {"folder": moved_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_rename(
    client: BoxClient,
    folder_id: str,
    new_name: str,
) -> dict[str, Any]:
    """
    Renames a folder in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to rename.
        new_name (str): New name for the folder.
    Returns:
        dict[str, Any]: Dictionary containing the renamed folder object or error message
    """
    try:
        renamed_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            name=new_name,
        )
        return {"folder": renamed_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_set_description(
    client: BoxClient,
    folder_id: str,
    description: str,
) -> dict[str, Any]:
    """
    Sets the description of a folder in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to set description for.
        description (str): Description text to set for the folder.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    try:
        updated_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            description=description,
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_set_collaboration(
    client: BoxClient,
    folder_id: str,
    can_non_owners_invite: bool,
    can_non_owners_view_collaborators: bool,
) -> dict[str, Any]:
    """
    Sets collaboration settings for a folder in Box.
    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to set collaboration settings for.
        can_non_owners_invite (bool): Whether non-owners can invite collaborators.
        can_non_owners_view_collaborators (bool): Whether non-owners can view collaborators.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    try:
        updated_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            can_non_owners_invite=can_non_owners_invite,
            can_non_owners_view_collaborators=can_non_owners_view_collaborators,
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_favorites_add(client: BoxClient, folder_id: str) -> dict[str, Any]:
    """
    Adds a folder to the user's favorites in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to add to favorites.

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    try:
        # list all collections to find the "Favorites" collection
        collections = client.collections.get_collections().entries
        favorites_collection = next(
            (c for c in collections if c.name == "Favorites"), None
        )
        if not favorites_collection:
            raise ValueError("Favorites collection not found")

        folder_favorite_collection = UpdateFolderByIdCollections(
            id=favorites_collection.id, type=favorites_collection.type
        )
        updated_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            collections=[folder_favorite_collection],
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_favorites_remove(client: BoxClient, folder_id: str) -> dict[str, Any]:
    """
    Removes a folder from the user's favorites in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to remove from favorites.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    try:
        # list all collections to find the "Favorites" collection
        collections = client.collections.get_collections().entries
        favorites_collection = next(
            (c for c in collections if c.name == "Favorites"), None
        )
        if not favorites_collection:
            raise ValueError("Favorites collection not found")

        # get folder details with collections
        fields = ["id", "type", "name", "collections"]
        folder = client.folders.get_folder_by_id(folder_id, fields=fields)

        folder_collections = folder.collections or []

        # remove favorites collection from folder collections if exists
        folder_collections = [
            c for c in folder_collections if c.id != favorites_collection.id
        ]

        updated_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            collections=folder_collections,
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_set_updload_email(
    client: BoxClient,
    folder_id: str,
    upload_email_access: Optional[str] = "collaborators",
) -> dict[str, Any]:
    """
    Sets or removes the upload email address for a folder in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to set the upload email for.
        upload_email_access (Optional[str]): The upload email access level to set. If None, removes the upload email.

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    try:
        updated_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            upload_email=upload_email,
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_update_folder(
    client: BoxClient,
    folder_id: Any,
    name: Optional[str] = None,
    description: Optional[str] = None,
    parent_folder_id: Optional[Any] = None,
) -> Folder:
    """
    Updates a folder's properties in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (Any): ID of the folder to update. Can be string or int.
        name (str, optional): New name for the folder
        description (str, optional): New description for the folder
        parent_folder_id (Any, optional): ID of the new parent folder (for moving). Can be string or int.

    Returns:
        FolderFull: The updated folder object

    Raises:
        BoxSDKError: If an error occurs during folder update
    """
    # Ensure folder_id is a string
    folder_id_str = str(folder_id)

    update_params = {}
    if name:
        update_params["name"] = name
    if description:
        update_params["description"] = description
    if parent_folder_id is not None:
        # Ensure parent_folder_id is a string
        parent_folder_id_str = str(parent_folder_id)
        update_params["parent"] = UpdateFolderByIdParent(id=parent_folder_id_str)

    return client.folders.update_folder_by_id(folder_id=folder_id_str, **update_params)
