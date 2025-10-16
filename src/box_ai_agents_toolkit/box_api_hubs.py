from typing import Any, Dict, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    GetHubsV2025R0Direction,
)

from .box_api_util_generic import log_box_api_error, log_generic_error


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
        sort (Optional[str]): he field to sort results by. Possible values include name, updated_at, last_accessed_at, view_count, and relevance. Default is relevance.
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
