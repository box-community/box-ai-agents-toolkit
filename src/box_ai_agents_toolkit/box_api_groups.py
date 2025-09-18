from typing import Any, Dict, Optional
from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
)

from .box_api_util_generic import log_box_api_error


def box_groups_search(
    client: BoxClient,
    filter_term: Optional[str] = None,
    limit: int = 1000,
) -> Dict[str, Any]:
    """Search for groups in the Box account.
    Args:
        client (BoxClient): Authenticated Box client.
        filter_term (Optional[str]): Term to filter groups by name. If none all groups are returned.
    Returns:
        Dict[str, Any]: Dictionary containing list of groups or error message.
    """

    offset = 0
    fields = ["id", "type", "name", "group_type", "description"]

    try:
        groups = client.groups.get_groups(
            filter_term=filter_term,
            fields=fields,
            limit=limit,
            offset=offset,
        )
        if groups.entries is None:
            result = []
        else:
            result = [group.to_dict() for group in groups.entries]

        # check if api returned more results than the limit
        while groups.total_count and len(result) < groups.total_count:
            offset += limit
            groups = client.groups.get_groups(
                filter_term=filter_term,
                fields=fields,
                limit=limit,
                offset=offset,
            )
            if groups.entries:
                result.extend(group.to_dict() for group in groups.entries)

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}

    if result is None or result == []:
        return {"message": "No groups found."}

    return {"groups": result}


def box_groups_list_by_user(
    client: BoxClient,
    user_id: str,
    limit: int = 1000,
) -> Dict[str, Any]:
    """List groups for a specific user.
    Args:
        client (BoxClient): Authenticated Box client.
        user_id (str): ID of the user to list groups for.
    Returns:
        Dict[str, Any]: Dictionary containing list of memberships or error message.
    """

    offset = 0

    try:
        memberships = client.memberships.get_user_memberships(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )
        if memberships.entries is None:
            result = []
        else:
            result = [memberships.to_dict() for memberships in memberships.entries]

        # check if api returned more results than the limit
        while memberships.total_count and len(result) < memberships.total_count:
            offset += limit
            memberships = client.memberships.get_user_memberships(
                user_id=user_id,
                limit=limit,
                offset=offset,
            )
            if memberships.entries:
                result.extend(group.to_dict() for group in memberships.entries)

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}

    if result is None or result == []:
        return {"message": "No groups found for the user."}

    return {"memberships": result}


def box_groups_list_members(
    client: BoxClient,
    group_id: str,
    limit: int = 1000,
) -> Dict[str, Any]:
    """List members of a specific group.
    Args:
        client (BoxClient): Authenticated Box client.
        group_id (str): ID of the group to list members for.
    Returns:
        Dict[str, Any]: Dictionary containing list of members or error message.
    """

    offset = 0

    try:
        memberships = client.memberships.get_group_memberships(
            group_id=group_id,
            limit=limit,
            offset=offset,
        )
        if memberships.entries is None:
            result = []
        else:
            result = [memberships.to_dict() for memberships in memberships.entries]

        # check if api returned more results than the limit
        while memberships.total_count and len(result) < memberships.total_count:
            offset += limit
            memberships = client.memberships.get_group_memberships(
                group_id=group_id,
                limit=limit,
                offset=offset,
            )
            if memberships.entries:
                result.extend(group.to_dict() for group in memberships.entries)

    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}

    if result is None or result == []:
        return {"message": "No members found for the group."}

    return {"memberships": result}
