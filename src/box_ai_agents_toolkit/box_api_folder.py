from typing import Any, List, Optional, Union

from box_sdk_gen import (
    BoxClient,
    CreateFolderParent,
    File,
    Folder,
    FolderMini,
    UpdateFolderByIdParent,
)


def box_folder_list_content(
    client: BoxClient, folder_id: str, is_recursive: bool = False
) -> List[Union[File, Folder]]:
    # fields = "id,name,type"
    result: List[Union[File, FolderMini]] = []

    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "web_link":
            continue
        if item.type == "folder" and is_recursive:
            result.extend(box_folder_list_content(client, item.id, is_recursive))
        result.append(item)

    return result


def box_create_folder(client: BoxClient, name: str, parent_id: Any = "0") -> Folder:
    """
    Creates a new folder in Box.

    Args:
        client (BoxClient): An authenticated Box client
        name (str): Name for the new folder
        parent_id (Any, optional): ID of the parent folder. Can be string or int.
                                  Defaults to "0" (root folder).

    Returns:
        FolderFull: The created folder object

    Raises:
        BoxSDKError: If an error occurs during folder creation
    """
    # Ensure parent_id is a string
    parent_id_str = str(parent_id) if parent_id is not None else "0"

    return client.folders.create_folder(
        name=name, parent=CreateFolderParent(id=parent_id_str)
    )


def box_update_folder(
    client: BoxClient,
    folder_id: Any,
    name: Optional[str] = None,
    description: Optional[str] = None,
    parent_id: Optional[Any] = None,
) -> Folder:
    """
    Updates a folder's properties in Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (Any): ID of the folder to update. Can be string or int.
        name (str, optional): New name for the folder
        description (str, optional): New description for the folder
        parent_id (Any, optional): ID of the new parent folder (for moving). Can be string or int.

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
    if parent_id is not None:
        # Ensure parent_id is a string
        parent_id_str = str(parent_id)
        update_params["parent"] = UpdateFolderByIdParent(id=parent_id_str)

    return client.folders.update_folder_by_id(folder_id=folder_id_str, **update_params)


def box_delete_folder(
    client: BoxClient, folder_id: Any, recursive: bool = False
) -> None:
    """
    Deletes a folder from Box.

    Args:
        client (BoxClient): An authenticated Box client
        folder_id (Any): ID of the folder to delete. Can be string or int.
        recursive (bool, optional): Whether to delete recursively. Defaults to False.

    Raises:
        BoxSDKError: If an error occurs during folder deletion
    """
    # Ensure folder_id is a string
    folder_id_str = str(folder_id)

    client.folders.delete_folder_by_id(folder_id=folder_id_str, recursive=recursive)
    return None
