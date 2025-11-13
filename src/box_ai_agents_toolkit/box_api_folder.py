from typing import Any, List, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    Collection,
    CreateFolderParent,
    Folder,
    FolderFull,
    UpdateFolderByIdCollections,
    UpdateFolderByIdFolderUploadEmail,
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
        folder_id (str): ID of the folder to delete. Can be string or int.
        recursive (bool, optional): Whether to delete recursively. Defaults to False.
    Returns:
        dict[str, Any]: Dictionary containing success message or error message
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
    is_collaboration_restricted_to_enterprise: bool,
) -> dict[str, Any]:
    """
    Sets collaboration settings for a folder in Box.
    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to set collaboration settings for.
        can_non_owners_invite (bool): Specifies if users who are not the owner of the folder can invite new collaborators to the folder.
        can_non_owners_view_collaborators (bool): Restricts collaborators who are not the owner of this folder from viewing other collaborations on this folder.
        is_collaboration_restricted_to_enterprise (bool): Specifies if new invites to this folder are restricted to users within the enterprise. This does not affect existing collaborations.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    try:
        updated_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            can_non_owners_invite=can_non_owners_invite,
            can_non_owners_view_collaborators=can_non_owners_view_collaborators,
            is_collaboration_restricted_to_enterprise=is_collaboration_restricted_to_enterprise,
            fields=[
                "can_non_owners_invite",
                "can_non_owners_view_collaborators",
                "is_collaboration_restricted_to_enterprise",
            ],
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
        collections: List[Collection] = client.collections.get_collections().entries
        favorites_collection: Collection = next(
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
            fields=["collections"],
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
        folder: FolderFull = client.folders.get_folder_by_id(folder_id, fields=fields)

        folder_collections: List[Collection] = folder.collections or []

        folder_collections = [
            col
            for col in folder_collections
            if col.get("id") != favorites_collection.id
        ]

        # for col in folder_collections:
        #     if col.get("id") == favorites_collection.id:
        #         folder_collections.remove(col)
        #         break

        updated_folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            collections=folder_collections,
            fields=["collections"],
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_set_sync(
    client: BoxClient,
    folder_id: str,
    sync_state: str,
) -> dict[str, Any]:
    """
    Sets the sync state for a folder in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to set sync state for.
        sync_state (str): Specifies whether a folder should be synced to a user's device or not. This is used by Box Sync (discontinued) and is not used by Box Drive. Value is one of synced,not_synced,partially_synced

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    try:
        updated_folder: Folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            sync_state=sync_state,
            fields=["sync_state"],
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_tag_add(
    client: BoxClient,
    folder_id: str,
    tag: str,
) -> dict[str, Any]:
    """
    Adds a tag to a folder in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to add tag to.
        tag (str): Tag to add to the folder.

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """

    try:
        # get folder existing tags
        folder = client.folders.get_folder_by_id(folder_id, fields=["tags"])
        existing_tags = folder.tags or []

        # combine existing tags with new tags
        all_tags = list(set(existing_tags + [tag]))
        updated_folder: Folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            tags=all_tags,
            fields=["tags"],
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_tag_remove(
    client: BoxClient,
    folder_id: str,
    tag: str,
) -> dict[str, Any]:
    """
    Removes a tag from a folder in Box.
    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to remove tag from.
        tag (str): Tag to remove from the folder.
    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """

    try:
        # get folder existing tags
        folder = client.folders.get_folder_by_id(folder_id, fields=["tags"])
        existing_tags = folder.tags or []

        # remove the specified tag
        updated_tags = [t for t in existing_tags if t != tag]
        updated_folder: Folder = client.folders.update_folder_by_id(
            folder_id=folder_id,
            tags=updated_tags,
            fields=["tags"],
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_list_tags(
    client: BoxClient,
    folder_id: str,
) -> dict[str, Any]:
    """
    Lists tags associated with a folder in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to list tags for.

    Returns:
        dict[str, Any]: Dictionary containing the list of tags or error message
    """
    try:
        folder = client.folders.get_folder_by_id(folder_id, fields=["tags"])
        tags = folder.tags or []
        if not tags:
            return {"message": "No tags found for the folder."}
        return {"tags": tags}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_folder_set_upload_email(
    client: BoxClient,
    folder_id: str,
    folder_upload_email_access: Optional[str] = "collaborators",
) -> dict[str, Any]:
    """
    Sets or removes the upload email address for a folder in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (str): ID of the folder to set the upload email for.
        folder_upload_email_access (Optional[str]): The upload email access level to set. If None, removes the upload email.
                                            When set to open it will accept emails from any email address.
                                            Value is one of open,collaborators

    Returns:
        dict[str, Any]: Dictionary containing the updated folder object or error message
    """
    try:
        folder_upload_email = UpdateFolderByIdFolderUploadEmail(
            access=folder_upload_email_access
        )
        updated_folder: FolderFull = client.folders.update_folder_by_id(
            folder_id=folder_id,
            folder_upload_email=folder_upload_email,
            fields=["folder_upload_email"],
        )
        return {"folder": updated_folder.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}
