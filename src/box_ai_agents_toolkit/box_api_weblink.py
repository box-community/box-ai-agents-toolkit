from typing import Any, Dict, Optional
from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    CreateWebLinkParent,
    UpdateWebLinkByIdParent,
)

from .box_api_util_generic import log_box_api_error


def box_web_link_create(
    client: BoxClient,
    url: str,
    parent_folder_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a web link in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        url (str): URL of the web link.
        parent_folder_id (str): ID of the parent folder for the web link.
        name (Optional[str]): Name of the web link.
        description (Optional[str]): Description of the web link.
    Returns:
        Dict[str, Any]: Dictionary containing web link details or error message.
    """
    parent = CreateWebLinkParent(id=parent_folder_id, type="folder")
    try:
        web_link = client.web_links.create_web_link(
            url=url,
            parent=parent,
            name=name,
            description=description,
        )
        return {"web_link": web_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_web_link_get_by_id(
    client: BoxClient,
    web_link_id: str,
) -> Dict[str, Any]:
    """
    Get a web link by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        web_link_id (str): ID of the web link to retrieve.
    Returns:
        Dict[str, Any]: Dictionary containing web link details or error message."""

    try:
        web_link = client.web_links.get_web_link_by_id(web_link_id)
        return {"web_link": web_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_web_link_update_by_id(
    client: BoxClient,
    web_link_id: str,
    url: Optional[str] = None,
    parent_folder_id: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update a web link by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        web_link_id (str): ID of the web link to update.
        url (Optional[str]): New URL for the web link.
        parent_folder_id (Optional[str]): New parent folder ID for the web link.
        name (Optional[str]): New name for the web link.
        description (Optional[str]): New description for the web link.
    Returns:
        Dict[str, Any]: Dictionary containing updated web link details or error message.
    """

    parent = (
        UpdateWebLinkByIdParent(id=parent_folder_id, type="folder")
        if parent_folder_id
        else None
    )

    try:
        web_link = client.web_links.update_web_link_by_id(
            web_link_id,
            url=url,
            parent=parent,
            name=name,
            description=description,
        )
        return {"web_link": web_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_web_link_delete_by_id(
    client: BoxClient,
    web_link_id: str,
) -> Dict[str, Any]:
    """
    Delete a web link by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        web_link_id (str): ID of the web link to delete.
    Returns:
        Dict[str, Any]: Dictionary indicating success or containing error message.
    """

    try:
        client.web_links.delete_web_link_by_id(web_link_id)
        return {"message": f"Web link {web_link_id} deleted successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}
