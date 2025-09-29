from typing import Any, Dict, Optional
from datetime import datetime
from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    AddShareLinkToFileSharedLink,
    AddShareLinkToFileSharedLinkAccessField,
    AddShareLinkToFileSharedLinkPermissionsField,
    # RemoveSharedLinkFromFileSharedLink,
    create_null,
)

from .box_api_util_generic import log_box_api_error, log_generic_error


def _access_to_enum(access: str) -> AddShareLinkToFileSharedLinkAccessField:
    access = access.lower()
    valid_access = [access.value for access in AddShareLinkToFileSharedLinkAccessField]
    if access in valid_access:
        return AddShareLinkToFileSharedLinkAccessField(access)
    else:
        log_generic_error(ValueError(f"Invalid access: {access}"))
        raise ValueError(f"Invalid access: {access}. Accepted access: {valid_access}")


def box_shared_link_file_create(
    client: BoxClient,
    file_id: str,
    access: Optional[str] = "company",
    can_download: Optional[bool] = True,
    can_preview: Optional[bool] = True,
    can_edit: Optional[bool] = False,
    password: Optional[str] = None,
    vanity_name: Optional[str] = None,
    unshared_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Create a shared link for a file in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to create a shared link for.
        access (Optional[str]): Access level for the shared link. Defaults to "company".
            Accepted values: "open", "company", "collaborators".
        can_download (Optional[bool]): Whether the shared link can be downloaded. Defaults to True.
        can_preview (Optional[bool]): Whether the shared link can be previewed. Defaults to True.
        can_edit (Optional[bool]): Whether the shared link can be edited. Defaults to False.
        password (Optional[str]): Password for the shared link.
        vanity_name (Optional[str]): Vanity name for the shared link.
        unshared_at (Optional[datetime]): Date and time when the shared link should be unshared.
    Returns:
        Dict[str, Any]: Dictionary containing shared link details or error message.
    """

    fields = "shared_link"

    access_enum: Optional[AddShareLinkToFileSharedLinkAccessField] = None
    if access:
        try:
            access_enum = _access_to_enum(access)
        except ValueError as e:
            return {"error": str(e)}

    permissions = AddShareLinkToFileSharedLinkPermissionsField(
        can_download=can_download, can_preview=can_preview, can_edit=can_edit
    )

    shared_link = AddShareLinkToFileSharedLink(
        access=access_enum,
        password=password,
        vanity_name=vanity_name,
        unshared_at=unshared_at,
        permissions=permissions,
    )
    try:
        response = client.shared_links_files.add_share_link_to_file(
            file_id=file_id, fields=fields, shared_link=shared_link
        )
        if not response.shared_link:
            return {"error": "Unable to create shared link."}
        return {"shared_link": response.shared_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_shared_link_file_get(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """Get the shared link for a file in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to get the shared link for.
    Returns:
        Dict[str, Any]: Dictionary containing shared link details or error message.
    """

    fields = "shared_link"

    try:
        response = client.shared_links_files.get_shared_link_for_file(
            file_id=file_id, fields=fields
        )
        # if the shared link in response is null, then return massage indicating no shared link
        if not response.shared_link:
            return {"message": "No shared link found for this file."}
        # otherwise, return the shared link
        return {"shared_link": response.shared_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_shared_link_file_remove(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """Remove the shared link for a file in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to remove the shared link for.
    Returns:
        Dict[str, Any]: Dictionary indicating success or error message.
    """

    fields = "shared_link"
    # shared_link = RemoveSharedLinkFromFileSharedLink()
    shared_link = create_null()
    try:
        client.shared_links_files.remove_shared_link_from_file(
            file_id=file_id, fields=fields, shared_link=shared_link
        )
        return {"message": "Shared link removed successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}
