from enum import Enum
from typing import Any, Dict, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    GetHubsV2025R0Direction,
    HubItemOperationV2025R0,
    HubItemOperationV2025R0ActionField,
    FileReferenceV2025R0,
    FolderReferenceV2025R0,
    WeblinkReferenceV2025R0,
    CreateHubCollaborationV2025R0AccessibleBy,
    CreateHubCollaborationV2025R0Hub,
)

from .box_api_util_generic import log_box_api_error, log_generic_error


class HubCollaborationAccessibleByType(str, Enum):
    """Enum for hub collaboration accessible by types."""

    USER = "user"
    GROUP = "group"


def _direction_to_enum(direction: str) -> GetHubsV2025R0Direction:
    direction = direction.upper()
    valid_direction = [direction.value for direction in GetHubsV2025R0Direction]
    if direction not in valid_direction:
        log_generic_error(ValueError(f"Invalid direction: {direction}"))
        raise ValueError(
            f"Invalid direction: {direction}. Valid directions are: {valid_direction}"
        )
    return GetHubsV2025R0Direction(direction)


def box_hub_create(
    client: BoxClient,
    title: str,
    description: Optional[str],
) -> Dict[str, Any]:
    """Create a new Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        title (str): The title of the Hub.
        description (Optional[str]): The description of the Hub.
    Returns:
        Dict[str, Any]: Dictionary containing Hub details or error message.
    """
    try:
        hub = client.hubs.create_hub_v2025_r0(
            title=title,
            description=description,
        )
        return hub.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_get(
    client: BoxClient,
    hub_id: str,
) -> Dict[str, Any]:
    """Get details of a Hub by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to retrieve.
    Returns:
        Dict[str, Any]: Dictionary containing Hub details or error message.
    """
    try:
        hub = client.hubs.get_hub_by_id_v2025_r0(hub_id=hub_id)
        return hub.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_update(
    client: BoxClient,
    hub_id: str,
    title: str,
    description: Optional[str],
    is_ai_enabled: Optional[bool] = None,
    is_collaboration_restricted_to_enterprise: Optional[bool] = None,
    can_non_owners_invite: Optional[bool] = None,
    can_shared_link_be_created: Optional[bool] = None,
) -> Dict[str, Any]:
    """Update details of a Hub by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to update.
        title (str): The new title of the Hub.
        description (Optional[str]): The new description of the Hub.
        is_ai_enabled (Optional[bool]): Whether AI features are enabled for the Hub.
        is_collaboration_restricted_to_enterprise (Optional[bool]): Whether collaboration is restricted to enterprise members.
        can_non_owners_invite (Optional[bool]): Whether non-owners can invite others to the Hub.
        can_shared_link_be_created (Optional[bool]): Whether shared links can be created for the Hub.
    Returns:
        Dict[str, Any]: Dictionary containing updated Hub details or error message.
    """
    try:
        hub = client.hubs.update_hub_by_id_v2025_r0(
            hub_id=hub_id,
            title=title,
            description=description,
            is_ai_enabled=is_ai_enabled,
            is_collaboration_restricted_to_enterprise=is_collaboration_restricted_to_enterprise,
            can_non_owners_invite=can_non_owners_invite,
            can_shared_link_be_created=can_shared_link_be_created,
        )
        return hub.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_delete(
    client: BoxClient,
    hub_id: str,
) -> Dict[str, Any]:
    """Delete a Hub by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to delete.
    Returns:
        Dict[str, Any]: Dictionary indicating success or error message.
    """
    try:
        client.hubs.delete_hub_by_id_v2025_r0(hub_id=hub_id)
        return {"message": f"Hub with ID {hub_id} deleted successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_copy(
    client: BoxClient,
    hub_id: str,
    title: str,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """Copy a Hub by its ID.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to copy.
        title (str): The title of the new copied Hub.
        description (Optional[str]): The description of the new copied Hub.
    Returns:
        Dict[str, Any]: Dictionary containing copied Hub details or error message.
    """
    try:
        hub = client.hubs.copy_hub_v2025_r0(
            hub_id=hub_id,
            title=title,
            description=description,
        )
        return hub.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_list(
    client: BoxClient,
    query: Optional[str] = None,
    scope: Optional[str] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    # marker: Optional[str] = None,
    limit: int = 200,  # the limit should be 1000, but the API returns an error above 200
) -> Dict[str, Any]:
    """List all Hubs.
    Args:
        client (BoxClient): Authenticated Box client.
        query (Optional[str]): Search query to filter Hubs by title or description.
        scope (Optional[str]): The scope of the Box Hubs to retrieve. Possible values include editable, view_only, and all. Default is all.
        sort (Optional[str]): The field to sort results by. Possible values include name, updated_at, last_accessed_at, view_count, and relevance. Default is relevance.
        direction (str): Sort direction, either "ASC" or "DESC". Default is "ASC".
    Returns:
        Dict[str, Any]: Dictionary containing list of Hubs or error message.
    """
    if direction:
        try:
            direction_enum = _direction_to_enum(direction)
        except ValueError as e:
            return {"error": str(e)}
    else:
        direction_enum = None

    marker = None

    try:
        hubs = client.hubs.get_hubs_v2025_r0(
            query=query,
            scope=scope,
            sort=sort,
            direction=direction_enum,
            marker=marker,
            limit=limit,
        )
        if not hubs.entries or len(hubs.entries) == 0:
            return {"message": "No hubs found."}
        else:
            result = [hub.to_dict() for hub in hubs.entries] if hubs else []  # type: ignore

        # check if api returned a marker for next page
        if hubs.next_marker:
            marker = hubs.next_marker
            while marker:
                hubs = client.hubs.get_hubs_v2025_r0(
                    query=query,
                    scope=scope,
                    sort=sort,
                    direction=direction_enum if direction else None,
                    marker=marker,
                    limit=limit,
                )
                if hubs.entries:
                    result.extend(hub.to_dict() for hub in hubs.entries)
                marker = hubs.next_marker if hubs.next_marker else None

        return {"hubs": result}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_items_list(
    client: BoxClient,
    hub_id: str,
    limit: int = 1000,
) -> Dict[str, Any]:
    """List all items in a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to retrieve items from.
        limit (int): The maximum number of items to retrieve.
    Returns:
        Dict[str, Any]: Dictionary containing list of items or error message.
    """

    marker = None

    try:
        items = client.hub_items.get_hub_items_v2025_r0(
            hub_id=hub_id,
            marker=marker,
            limit=limit,
        )

        if not items.entries or len(items.entries) == 0:
            return {"message": "No items found in the hub."}
        else:
            result = [item.to_dict() for item in items.entries] if items else []

        # check if api returned a marker for next page
        if items.next_marker:
            marker = items.next_marker
            while marker:
                items = client.hub_items.get_hub_items_v2025_r0(
                    hub_id=hub_id,
                    marker=marker,
                    limit=limit,
                )
                if items.entries:
                    result.extend(item.to_dict() for item in items.entries)
                marker = items.next_marker if items.next_marker else None

        return {"hub items": result}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_item_add(
    client: BoxClient,
    hub_id: str,
    item_id: str,
    item_type: str,
) -> Dict[str, Any]:
    """Add an item to a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to add the item to.
        item_id (str): The ID of the item to add.
        item_type (str): The type of the item to add (e.g., "file" or "folder" or "web_link").
    Returns:
        Dict[str, Any]: Dictionary containing added item details or error message.
    """
    match item_type.lower():
        case "file":
            item = FileReferenceV2025R0(id=item_id)
        case "folder":
            item = FolderReferenceV2025R0(id=item_id)
        case "web_link":
            item = WeblinkReferenceV2025R0(id=item_id)
        case _:
            log_generic_error(ValueError(f"Invalid item type: {item_type}"))
            raise ValueError(f"Invalid item type: {item_type}")

    action = HubItemOperationV2025R0ActionField.ADD
    operation = HubItemOperationV2025R0(
        action=action,
        item=item,
    )
    try:
        hub_item = client.hub_items.manage_hub_items_v2025_r0(
            hub_id=hub_id,
            operations=[operation],
        )
        return hub_item.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_item_remove(
    client: BoxClient,
    hub_id: str,
    item_id: str,
    item_type: str,
) -> Dict[str, Any]:
    """Remove an item from a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to remove the item from.
        item_id (str): The ID of the item to remove.
        item_type (str): The type of the item to remove (e.g., "file" or "folder" or "web_link").
    Returns:
        Dict[str, Any]: Dictionary containing removed item details or error message.
    """
    match item_type.lower():
        case "file":
            item = FileReferenceV2025R0(id=item_id)
        case "folder":
            item = FolderReferenceV2025R0(id=item_id)
        case "web_link":
            item = WeblinkReferenceV2025R0(id=item_id)
        case _:
            log_generic_error(ValueError(f"Invalid item type: {item_type}"))
            raise ValueError(f"Invalid item type: {item_type}")

    action = HubItemOperationV2025R0ActionField.REMOVE
    operation = HubItemOperationV2025R0(
        action=action,
        item=item,
    )
    try:
        hub_item = client.hub_items.manage_hub_items_v2025_r0(
            hub_id=hub_id,
            operations=[operation],
        )
        return hub_item.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def _create_hub_collaboration(
    client: BoxClient,
    hub_id: str,
    accessible_by_type: HubCollaborationAccessibleByType,
    role: str,
    accessible_by_id: Optional[str] = None,
    accessible_by_login: Optional[str] = None,
) -> Dict[str, Any]:
    """Private helper to create a hub collaboration.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to add the collaboration to.
        accessible_by_type (HubCollaborationAccessibleByType): The type of the collaborator.
        role (str): The level of access granted to a Box Hub. Possible values are editor, viewer, and co-owner.
        accessible_by_id (Optional[str]): The ID of the user or group.
        accessible_by_login (Optional[str]): The email of the user.
    Returns:
        Dict[str, Any]: Dictionary containing added collaboration details or error message.
    """
    hub = CreateHubCollaborationV2025R0Hub(id=hub_id)
    accessible_by = CreateHubCollaborationV2025R0AccessibleBy(
        type=accessible_by_type.value,
        id=accessible_by_id,
        login=accessible_by_login,
    )
    try:
        collaboration = client.hub_collaborations.create_hub_collaboration_v2025_r0(
            hub=hub,
            accessible_by=accessible_by,
            role=role,
        )
        return collaboration.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_collaborations_list(
    client: BoxClient,
    hub_id: str,
    limit: int = 1000,
) -> Dict[str, Any]:
    """List all collaborations in a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to retrieve collaborations from.
        limit (int): The maximum number of collaborations to retrieve.
    Returns:
        Dict[str, Any]: Dictionary containing list of collaborations or error message.
    """

    marker = None

    try:
        collaborations = client.hub_collaborations.get_hub_collaborations_v2025_r0(
            hub_id=hub_id,
            marker=marker,
            limit=limit,
        )

        if not collaborations.entries or len(collaborations.entries) == 0:
            return {"message": "No collaborations found in the hub."}
        else:
            result = (
                [collaboration.to_dict() for collaboration in collaborations.entries]
                if collaborations
                else []
            )

        # check if api returned a marker for next page
        if collaborations.next_marker:
            marker = collaborations.next_marker
            while marker:
                collaborations = (
                    client.hub_collaborations.get_hub_collaborations_v2025_r0(
                        hub_id=hub_id,
                        marker=marker,
                        limit=limit,
                    )
                )
                if collaborations.entries:
                    result.extend(
                        collaboration.to_dict()
                        for collaboration in collaborations.entries
                    )
                marker = (
                    collaborations.next_marker if collaborations.next_marker else None
                )

        return {"hub collaborations": result}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_collaboration_add_user_by_id(
    client: BoxClient,
    hub_id: str,
    user_id: str,
    role: str,
) -> Dict[str, Any]:
    """Add a collaboration to a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to add the collaboration to.
        user_id (str): The ID of the user to collaborate with.
        role (str): The level of access granted to a Box Hub. Possible values are editor, viewer, and co-owner.
    Returns:
        Dict[str, Any]: Dictionary containing added collaboration details or error message.
    """
    return _create_hub_collaboration(
        client=client,
        hub_id=hub_id,
        accessible_by_type=HubCollaborationAccessibleByType.USER,
        role=role,
        accessible_by_id=user_id,
    )


def box_hub_collaboration_add_user_by_email(
    client: BoxClient,
    hub_id: str,
    email: str,
    role: str,
) -> Dict[str, Any]:
    """Add a collaboration to a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to add the collaboration to.
        email (str): The email of the user to collaborate with.
        role (str): The level of access granted to a Box Hub. Possible values are editor, viewer, and co-owner.
    Returns:
        Dict[str, Any]: Dictionary containing added collaboration details or error message.
    """
    return _create_hub_collaboration(
        client=client,
        hub_id=hub_id,
        accessible_by_type=HubCollaborationAccessibleByType.USER,
        role=role,
        accessible_by_login=email,
    )


def box_hub_collaboration_add_group_by_id(
    client: BoxClient,
    hub_id: str,
    group_id: str,
    role: str,
) -> Dict[str, Any]:
    """Add a group collaboration to a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_id (str): The ID of the Hub to add the collaboration to.
        group_id (str): The ID of the group to collaborate with.
        role (str): The level of access granted to a Box Hub. Possible values are editor, viewer, and co-owner.
    Returns:
        Dict[str, Any]: Dictionary containing added collaboration details or error message.
    """
    return _create_hub_collaboration(
        client=client,
        hub_id=hub_id,
        accessible_by_type=HubCollaborationAccessibleByType.GROUP,
        role=role,
        accessible_by_id=group_id,
    )


def box_hub_collaboration_remove(
    client: BoxClient,
    hub_collaboration_id: str,
) -> Dict[str, Any]:
    """Remove a collaboration from a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_collaboration_id (str): The ID of the collaboration to remove.
    Returns:
        Dict[str, Any]: Dictionary containing removed collaboration details or error message.
    """
    try:
        client.hub_collaborations.delete_hub_collaboration_by_id_v2025_r0(
            hub_collaboration_id=hub_collaboration_id,
        )
        return {
            "message": f"Hub collaboration with ID {hub_collaboration_id} deleted successfully."
        }
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_collaboration_update(
    client: BoxClient,
    hub_collaboration_id: str,
    role: str,
) -> Dict[str, Any]:
    """Update a collaboration in a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_collaboration_id (str): The ID of the collaboration to update.
        role (str): The new level of access granted to a Box Hub. Possible values are editor, viewer, and co-owner.
    Returns:
        Dict[str, Any]: Dictionary containing updated collaboration details or error message.
    """
    try:
        collaboration = (
            client.hub_collaborations.update_hub_collaboration_by_id_v2025_r0(
                hub_collaboration_id=hub_collaboration_id,
                role=role,
            )
        )
        return collaboration.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_hub_collaboration_details(
    client: BoxClient,
    hub_collaboration_id: str,
) -> Dict[str, Any]:
    """Get details of a collaboration in a Hub.
    Args:
        client (BoxClient): Authenticated Box client.
        hub_collaboration_id (str): The ID of the collaboration to retrieve.
    Returns:
        Dict[str, Any]: Dictionary containing collaboration details or error message.
    """
    try:
        collaboration = client.hub_collaborations.get_hub_collaboration_by_id_v2025_r0(
            hub_collaboration_id=hub_collaboration_id,
        )
        return collaboration.to_dict()
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}
