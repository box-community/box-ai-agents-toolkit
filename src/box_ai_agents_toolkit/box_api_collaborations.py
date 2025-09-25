from typing import Any, Dict, Optional
from datetime import datetime as DateTime
from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    CreateCollaborationItem,
    CreateCollaborationItemTypeField,
    CreateCollaborationAccessibleBy,
    CreateCollaborationAccessibleByTypeField,
    CreateCollaborationRole,
    UpdateCollaborationByIdStatus,
    UpdateCollaborationByIdRole,
)

from .box_api_util_generic import log_box_api_error, log_generic_error


def _role_to_enum(role: str) -> CreateCollaborationRole:
    role = role.lower()
    valid_roles = [role.value for role in CreateCollaborationRole]
    if role in valid_roles:
        return CreateCollaborationRole(role)
    else:
        log_generic_error(ValueError(f"Invalid role: {role}"))
        raise ValueError(f"Invalid role: {role}. Accepted roles: {valid_roles}")


def _status_to_enum(status: str) -> UpdateCollaborationByIdStatus:
    status = status.lower()
    valid_statuses = [status.value for status in UpdateCollaborationByIdStatus]
    if status in valid_statuses:
        return UpdateCollaborationByIdStatus(status)
    else:
        log_generic_error(ValueError(f"Invalid status: {status}"))
        raise ValueError(
            f"Invalid status: {status}. Accepted statuses: {valid_statuses}"
        )


def _collaboration_item_create(
    client: BoxClient,
    item: CreateCollaborationItem,
    accessible_by: CreateCollaborationAccessibleBy,
    role: CreateCollaborationRole,
    is_access_only: Optional[bool] = None,
    can_view_path: Optional[bool] = None,
    expires_at: Optional[DateTime] = None,
    notify: Optional[bool] = None,
) -> Dict[str, Any]:
    try:
        collaboration = client.user_collaborations.create_collaboration(
            item=item,
            accessible_by=accessible_by,
            role=role,
            is_access_only=is_access_only,
            can_view_path=can_view_path,
            expires_at=expires_at,
            notify=notify,
        )
        return {"collaboration": collaboration.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_collaboration_file_user_by_user_id(
    client: BoxClient,
    file_id: str,
    user_id: str,
    role: str = "editor",
    is_access_only: Optional[bool] = None,
    expires_at: Optional[DateTime] = None,
    notify: Optional[bool] = None,
) -> Dict[str, Any]:
    """Create a collaboration on a file with a user specified by user ID.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): The ID of the file to collaborate on.
        user_id (str): The ID of the user to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    item = CreateCollaborationItem(
        type=CreateCollaborationItemTypeField.FILE, id=file_id
    )
    accessible_by = CreateCollaborationAccessibleBy(
        type=CreateCollaborationAccessibleByTypeField.USER,
        id=user_id,
    )
    try:
        role = _role_to_enum(role)
    except ValueError as e:
        return {"error": str(e)}

    return _collaboration_item_create(
        client=client,
        item=item,
        accessible_by=accessible_by,
        role=role,
        is_access_only=is_access_only,
        can_view_path=False,
        expires_at=expires_at,
        notify=notify,
    )


def box_collaboration_file_user_by_user_login(
    client: BoxClient,
    file_id: str,
    user_login: str,
    role: str = "editor",
    is_access_only: Optional[bool] = None,
    expires_at: Optional[DateTime] = None,
    notify: Optional[bool] = None,
) -> Dict[str, Any]:
    """Create a collaboration on a file with a user specified by user login.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): The ID of the file to collaborate on.
        user_login (str): The login (email) of the user to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    item = CreateCollaborationItem(
        type=CreateCollaborationItemTypeField.FILE, id=file_id
    )
    accessible_by = CreateCollaborationAccessibleBy(
        type=CreateCollaborationAccessibleByTypeField.USER,
        login=user_login,
    )
    try:
        role = _role_to_enum(role)
    except ValueError as e:
        return {"error": str(e)}

    return _collaboration_item_create(
        client=client,
        item=item,
        accessible_by=accessible_by,
        role=role,
        is_access_only=is_access_only,
        can_view_path=False,
        expires_at=expires_at,
        notify=notify,
    )


def box_collaboration_file_group_by_group_id(
    client: BoxClient,
    file_id: str,
    group_id: str,
    role: str = "editor",
    is_access_only: Optional[bool] = None,
    expires_at: Optional[DateTime] = None,
    notify: Optional[bool] = None,
) -> Dict[str, Any]:
    """Create a collaboration on a file with a group specified by group ID.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): The ID of the file to collaborate on.
        group_id (str): The ID of the group to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    item = CreateCollaborationItem(
        type=CreateCollaborationItemTypeField.FILE, id=file_id
    )
    accessible_by = CreateCollaborationAccessibleBy(
        type=CreateCollaborationAccessibleByTypeField.GROUP,
        id=group_id,
    )
    try:
        role = _role_to_enum(role)
    except ValueError as e:
        return {"error": str(e)}

    return _collaboration_item_create(
        client=client,
        item=item,
        accessible_by=accessible_by,
        role=role,
        is_access_only=is_access_only,
        can_view_path=False,
        expires_at=expires_at,
        notify=notify,
    )


def box_collaboration_folder_user_by_user_id(
    client: BoxClient,
    folder_id: str,
    user_id: str,
    role: str = "editor",
    is_access_only: Optional[bool] = None,
    can_view_path: Optional[bool] = None,
    expires_at: Optional[DateTime] = None,
    notify: Optional[bool] = None,
) -> Dict[str, Any]:
    """Create a collaboration on a folder with a user specified by user ID.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): The ID of the folder to collaborate on.
        user_id (str): The ID of the user to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        can_view_path (Optional[bool]): If set to true, collaborators can view the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    item = CreateCollaborationItem(
        type=CreateCollaborationItemTypeField.FOLDER, id=folder_id
    )
    accessible_by = CreateCollaborationAccessibleBy(
        type=CreateCollaborationAccessibleByTypeField.USER,
        id=user_id,
    )
    try:
        role = _role_to_enum(role)
    except ValueError as e:
        return {"error": str(e)}

    return _collaboration_item_create(
        client=client,
        item=item,
        accessible_by=accessible_by,
        role=role,
        is_access_only=is_access_only,
        can_view_path=can_view_path,
        expires_at=expires_at,
        notify=notify,
    )


def box_collaboration_folder_user_by_user_login(
    client: BoxClient,
    folder_id: str,
    user_login: str,
    role: str = "editor",
    is_access_only: Optional[bool] = None,
    can_view_path: Optional[bool] = None,
    expires_at: Optional[DateTime] = None,
    notify: Optional[bool] = None,
) -> Dict[str, Any]:
    """Create a collaboration on a folder with a user specified by user login.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): The ID of the folder to collaborate on.
        user_login (str): The login (email) of the user to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        can_view_path (Optional[bool]): If set to true, collaborators can view the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    item = CreateCollaborationItem(
        type=CreateCollaborationItemTypeField.FOLDER, id=folder_id
    )
    accessible_by = CreateCollaborationAccessibleBy(
        type=CreateCollaborationAccessibleByTypeField.USER,
        login=user_login,
    )
    try:
        role = _role_to_enum(role)
    except ValueError as e:
        return {"error": str(e)}

    return _collaboration_item_create(
        client=client,
        item=item,
        accessible_by=accessible_by,
        role=role,
        is_access_only=is_access_only,
        can_view_path=can_view_path,
        expires_at=expires_at,
        notify=notify,
    )


def box_collaboration_folder_group_by_group_id(
    client: BoxClient,
    folder_id: str,
    group_id: str,
    role: str = "editor",
    is_access_only: Optional[bool] = None,
    can_view_path: Optional[bool] = None,
    expires_at: Optional[DateTime] = None,
    notify: Optional[bool] = None,
) -> Dict[str, Any]:
    """Create a collaboration on a folder with a group specified by group ID.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): The ID of the folder to collaborate on.
        group_id (str): The ID of the group to collaborate with.
        role (str): The role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        is_access_only (Optional[bool]): If set to true, collaborators have access to shared items, but such items won't be visible in the All Files list. Additionally, collaborators won't see the path to the root folder for the shared item.
        can_view_path (Optional[bool]): If set to true, collaborators can view the path to the root folder for the shared item.
        expires_at (Optional[DateTime]): The expiration date of the collaboration.
        notify (Optional[bool]): Whether to notify the collaborator via email.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    item = CreateCollaborationItem(
        type=CreateCollaborationItemTypeField.FOLDER, id=folder_id
    )
    accessible_by = CreateCollaborationAccessibleBy(
        type=CreateCollaborationAccessibleByTypeField.GROUP,
        id=group_id,
    )
    try:
        role = _role_to_enum(role)
    except ValueError as e:
        return {"error": str(e)}

    return _collaboration_item_create(
        client=client,
        item=item,
        accessible_by=accessible_by,
        role=role,
        is_access_only=is_access_only,
        can_view_path=can_view_path,
        expires_at=expires_at,
        notify=notify,
    )


def box_collaboration_delete(
    client: BoxClient,
    collaboration_id: str,
) -> Dict[str, Any]:
    """Delete a collaboration by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        collaboration_id (str): The ID of the collaboration to delete.
    Returns:
        Dict[str, Any]: Dictionary indicating success or containing error message.
    """
    try:
        client.user_collaborations.delete_collaboration_by_id(collaboration_id)
        return {"message": f"Collaboration {collaboration_id} deleted successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_collaborations_list_by_file(
    client: BoxClient,
    file_id: str,
    limit: int = 1000,
) -> Dict[str, Any]:
    """List all collaborations for a specific file.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): The ID of the file to list collaborations for.
    Returns:
        Dict[str, Any]: Dictionary containing list of collaborations or error message.
    """

    marker = None

    try:
        collaborations = client.list_collaborations.get_file_collaborations(
            file_id=file_id,
            limit=limit,
        )
        if collaborations.entries is None:
            result = []
        else:
            result = [
                collaboration.to_dict() for collaboration in collaborations.entries
            ]

        # check if api returned a next marker and iterate over it
        if collaborations.next_marker:
            marker = collaborations.next_marker
            while marker:
                collaborations = client.list_collaborations.get_file_collaborations(
                    file_id=file_id,
                    limit=limit,
                    marker=marker,
                )
                if collaborations.entries:
                    result.extend(
                        collaboration.to_dict()
                        for collaboration in collaborations.entries
                    )
                marker = (
                    collaborations.next_marker if collaborations.next_marker else None
                )
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}

    if result is None or result == []:
        return {"message": "No collaborations found for the specified file."}

    return {"collaborations": result}


def box_collaborations_list_by_folder(
    client: BoxClient,
    folder_id: str,
    limit: int = 1000,
) -> Dict[str, Any]:
    """List all collaborations for a specific folder.
    Args:
        client (BoxClient): Authenticated Box client.
        folder_id (str): The ID of the folder to list collaborations for.
    Returns:
        Dict[str, Any]: Dictionary containing list of collaborations or error message.
    """

    marker = "0"

    try:
        collaborations = client.list_collaborations.get_folder_collaborations(
            folder_id=folder_id,
            limit=limit,
            marker=marker,
        )
        if collaborations.entries is None:
            result = []
        else:
            result = [
                collaboration.to_dict() for collaboration in collaborations.entries
            ]

        # check if api returned a next marker and iterate over it
        if collaborations.next_marker:
            marker = collaborations.next_marker
            while marker:
                collaborations = client.list_collaborations.get_folder_collaborations(
                    folder_id=folder_id,
                    limit=limit,
                    marker=marker,
                )
                if collaborations.entries:
                    result.extend(
                        collaboration.to_dict()
                        for collaboration in collaborations.entries
                    )
                marker = (
                    collaborations.next_marker if collaborations.next_marker else None
                )
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}

    if result is None or result == []:
        return {"message": "No collaborations found for the specified folder."}

    return {"collaborations": result}


def box_collaboration_update(
    client: BoxClient,
    collaboration_id: str,
    role: str = "editor",
    status: Optional[str] = None,
    expires_at: Optional[DateTime] = None,
    can_view_path: Optional[bool] = None,
) -> Dict[str, Any]:
    """Update a collaboration by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        collaboration_id (str): The ID of the collaboration to update.
        role (str): The new role to assign to the collaborator. Default is "editor". Available roles are editor, viewer, previewer, uploader, viewer_uploader, co-owner.
        status (Optional[str]): Set the status of a pending collaboration invitation, effectively accepting, or rejecting the invite. Accepted values are "accepted" or "rejected".
        expires_at (Optional[DateTime]): The new expiration date of the collaboration.
        can_view_path (Optional[bool]): If set to true, collaborators can view the path to the root folder for the shared item.
    Returns:
        Dict[str, Any]: Dictionary containing updated collaboration details or error message.
    """

    try:
        role = _role_to_enum(role)
    except ValueError as e:
        return {"error": str(e)}

    role = UpdateCollaborationByIdRole(role)

    try:
        status = _status_to_enum(status) if status else None
    except ValueError as e:
        return {"error": str(e)}

    try:
        result = client.user_collaborations.update_collaboration_by_id(
            collaboration_id=collaboration_id,
            role=role,
            status=status,
            expires_at=expires_at,
            can_view_path=can_view_path,
        )
        return (
            {"collaboration": result.to_dict()}
            if result
            else {"message": "No collaboration found with the specified ID."}
        )
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}
