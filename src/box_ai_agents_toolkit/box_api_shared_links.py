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
    AddShareLinkToFolderSharedLink,
    AddShareLinkToFolderSharedLinkAccessField,
    AddShareLinkToFolderSharedLinkPermissionsField,
    AddShareLinkToWebLinkSharedLink,
    AddShareLinkToWebLinkSharedLinkAccessField,
)

from .box_api_util_generic import log_box_api_error, log_generic_error


def _access_file_to_enum(access: str) -> AddShareLinkToFileSharedLinkAccessField:
    access = access.lower()
    valid_access = [access.value for access in AddShareLinkToFileSharedLinkAccessField]
    if access in valid_access:
        return AddShareLinkToFileSharedLinkAccessField(access)
    else:
        log_generic_error(ValueError(f"Invalid access: {access}"))
        raise ValueError(f"Invalid access: {access}. Accepted access: {valid_access}")


def box_shared_link_file_create_or_update(
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
        password (Optional[str]): Password for the shared link. Passwords must now be at least eight characters long and include a number, upper case letter, or a non-numeric or non-alphabetic character. A password can only be set when access is set to open.
        vanity_name (Optional[str]): Vanity name for the shared link.
        unshared_at (Optional[datetime]): Date and time when the shared link should be unshared.
    Returns:
        Dict[str, Any]: Dictionary containing shared link details or error message.
    """

    fields = "shared_link"

    access_enum: Optional[AddShareLinkToFileSharedLinkAccessField] = None
    if access:
        try:
            access_enum = _access_file_to_enum(access)
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


def box_shared_link_file_find_by_shared_link_url(
    client: BoxClient,
    shared_link_url: str,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the file details using a shared link URL in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        shared_link_url (str): Shared link URL to get the file details for.
        password (Optional[str]): Password for the shared link, if applicable.
    Returns:
        Dict[str, Any]: Dictionary containing file details or error message.
    """

    shared_link_url = f"shared_link={shared_link_url}"
    if password is not None:
        shared_link_url = f"{shared_link_url}&shared_link_password={password}"
    try:
        response = client.shared_links_files.find_file_for_shared_link(
            boxapi=shared_link_url,
        )
        return {"file": response.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def _access_folder_to_enum(access: str) -> AddShareLinkToFolderSharedLinkAccessField:
    access = access.lower()
    valid_access = [
        access.value for access in AddShareLinkToFolderSharedLinkAccessField
    ]
    if access in valid_access:
        return AddShareLinkToFolderSharedLinkAccessField(access)
    else:
        log_generic_error(ValueError(f"Invalid access: {access}"))
        raise ValueError(f"Invalid access: {access}. Accepted access: {valid_access}")


def box_shared_link_folder_create_or_update(
    client: BoxClient,
    folder_id: str,
    access: Optional[str] = "company",
    can_download: Optional[bool] = True,
    can_preview: Optional[bool] = True,
    can_edit: Optional[bool] = False,
    password: Optional[str] = None,
    vanity_name: Optional[str] = None,
    unshared_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Create a shared link for a folder in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): ID of the folder to create a shared link for.
        access (Optional[str]): Access level for the shared link. Defaults to "company".
            Accepted values: "open", "company", "collaborators".
        can_download (Optional[bool]): Whether the shared link can be downloaded. Defaults to True.
        can_preview (Optional[bool]): Whether the shared link can be previewed. Defaults to True.
        can_edit (Optional[bool]): Whether the shared link can be edited. Defaults to False.
        password (Optional[str]): Password for the shared link. Passwords must now be at least eight characters long and include a number, upper case letter, or a non-numeric or non-alphabetic character. A password can only be set when access is set to open.
        vanity_name (Optional[str]): Vanity name for the shared link.
        unshared_at (Optional[datetime]): Date and time when the shared link should be unshared.
    Returns:
        Dict[str, Any]: Dictionary containing shared link details or error message.
    """

    fields = "shared_link"

    access_enum: Optional[AddShareLinkToFolderSharedLinkAccessField] = None
    if access:
        try:
            access_enum = _access_folder_to_enum(access)
        except ValueError as e:
            return {"error": str(e)}

    permissions = AddShareLinkToFolderSharedLinkPermissionsField(
        can_download=can_download, can_preview=can_preview, can_edit=can_edit
    )

    shared_link = AddShareLinkToFolderSharedLink(
        access=access_enum,
        password=password,
        vanity_name=vanity_name,
        unshared_at=unshared_at,
        permissions=permissions,
    )
    try:
        response = client.shared_links_folders.add_share_link_to_folder(
            folder_id=folder_id, fields=fields, shared_link=shared_link
        )
        if not response.shared_link:
            return {"error": "Unable to create shared link."}
        return {"shared_link": response.shared_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_shared_link_folder_get(
    client: BoxClient,
    folder_id: str,
) -> Dict[str, Any]:
    """Get the shared link for a folder in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): ID of the folder to get the shared link for.
    Returns:
        Dict[str, Any]: Dictionary containing shared link details or error message.
    """

    fields = "shared_link"

    try:
        response = client.shared_links_folders.get_shared_link_for_folder(
            folder_id=folder_id, fields=fields
        )
        # if the shared link in response is null, then return massage indicating no shared link
        if not response.shared_link:
            return {"message": "No shared link found for this folder."}
        # otherwise, return the shared link
        return {"shared_link": response.shared_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_shared_link_folder_remove(
    client: BoxClient,
    folder_id: str,
) -> Dict[str, Any]:
    """Remove the shared link for a folder in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): ID of the folder to remove the shared link for.
    Returns:
        Dict[str, Any]: Dictionary indicating success or error message.
    """

    fields = "shared_link"
    # shared_link = RemoveSharedLinkFromFolderSharedLink()
    shared_link = create_null()
    try:
        client.shared_links_folders.remove_shared_link_from_folder(
            folder_id=folder_id, fields=fields, shared_link=shared_link
        )
        return {"message": "Shared link removed successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_shared_link_folder_find_by_shared_link_url(
    client: BoxClient,
    shared_link_url: str,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the folder details using a shared link URL in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        shared_link_url (str): Shared link URL to get the folder details for.
        password (Optional[str]): Password for the shared link, if applicable.
    Returns:
        Dict[str, Any]: Dictionary containing folder details or error message.
    """

    shared_link_url = f"shared_link={shared_link_url}"
    if password is not None:
        shared_link_url = f"{shared_link_url}&shared_link_password={password}"
    try:
        response = client.shared_links_folders.find_folder_for_shared_link(
            boxapi=shared_link_url,
        )
        return {"folder": response.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def _access_web_link_to_enum(access: str) -> AddShareLinkToWebLinkSharedLinkAccessField:
    access = access.lower()
    valid_access = [
        access.value for access in AddShareLinkToWebLinkSharedLinkAccessField
    ]
    if access in valid_access:
        return AddShareLinkToWebLinkSharedLinkAccessField(access)
    else:
        log_generic_error(ValueError(f"Invalid access: {access}"))
        raise ValueError(f"Invalid access: {access}. Accepted access: {valid_access}")


def box_shared_link_web_link_create_or_update(
    client: BoxClient,
    web_link_id: str,
    access: Optional[str] = "company",
    password: Optional[str] = None,
    vanity_name: Optional[str] = None,
    unshared_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    fields = "shared_link"

    access_enum: Optional[AddShareLinkToWebLinkSharedLinkAccessField] = None
    if access:
        try:
            access_enum = _access_web_link_to_enum(access)
        except ValueError as e:
            return {"error": str(e)}

    permissions = None

    shared_link = AddShareLinkToWebLinkSharedLink(
        access=access_enum,
        password=password,
        vanity_name=vanity_name,
        unshared_at=unshared_at,
        permissions=permissions,
    )

    try:
        response = client.shared_links_web_links.add_share_link_to_web_link(
            web_link_id=web_link_id, fields=fields, shared_link=shared_link
        )
        if not response.shared_link:
            return {"message": "Unable to create shared link."}
        return {"shared_link": response.shared_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_shared_link_web_link_get(
    client: BoxClient,
    web_link_id: str,
) -> Dict[str, Any]:
    fields = "shared_link"

    try:
        response = client.shared_links_web_links.get_shared_link_for_web_link(
            web_link_id=web_link_id, fields=fields
        )
        if not response.shared_link:
            return {"message": "No shared link found for this web link."}
        return {"shared_link": response.shared_link.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_shared_link_web_link_remove(
    client: BoxClient,
    web_link_id: str,
) -> Dict[str, Any]:
    fields = "shared_link"
    shared_link = create_null()
    try:
        client.shared_links_web_links.remove_shared_link_from_web_link(
            web_link_id=web_link_id, fields=fields, shared_link=shared_link
        )
        return {"message": "Shared link removed successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_shared_link_web_link_find_by_shared_link_url(
    client: BoxClient,
    shared_link_url: str,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    shared_link_url = f"shared_link={shared_link_url}"
    if password is not None:
        shared_link_url = f"{shared_link_url}&shared_link_password={password}"
    try:
        response = client.shared_links_web_links.find_web_link_for_shared_link(
            boxapi=shared_link_url,
        )
        return {"web_link": response.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}
