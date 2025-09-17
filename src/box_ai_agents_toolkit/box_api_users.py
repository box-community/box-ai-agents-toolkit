import logging
from typing import Any, Dict, List, Optional
from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    GetUsersUserType,
)

logging.basicConfig(level=logging.INFO)


def _box_users_list(
    client: BoxClient,
    limit: int = 1000,
) -> List[Dict[str, Any]]:
    """List users in the Box account."""
    fields = ["id", "type", "name", "login", "role"]
    marker = None

    users = client.users.get_users(
        user_type=GetUsersUserType.ALL,
        fields=fields,
        limit=limit,
        usemarker=True,
        marker=marker,
    )
    if users.entries is None:
        result = []
    else:
        result = [user.to_dict() for user in users.entries]

    # check if api returned a marker for next page
    if users.next_marker:
        marker = users.next_marker
        while marker:
            users = client.users.get_users(
                user_type=GetUsersUserType.ALL,
                fields=fields,
                limit=limit,
                usemarker=True,
                marker=marker,
            )
            if users.entries:
                result.extend(user.to_dict() for user in users.entries)
            marker = users.next_marker if users.next_marker else None
    return result


def _box_users_search(
    client: BoxClient,
    filter_term: Optional[str] = None,
    limit: int = 1000,
) -> List[Dict[str, Any]]:
    """Search for users in the Box account based on a filter term."""
    fields = ["id", "type", "name", "login", "role"]
    offset = 0

    users = client.users.get_users(
        filter_term=filter_term,
        user_type=GetUsersUserType.ALL,
        fields=fields,
        limit=limit,
        offset=offset,
    )
    if users.entries is None:
        result = []
    else:
        result = [user.to_dict() for user in users.entries]

    # check if there are more pages using total_count and offset (offset-based pagination)
    while users.total_count is not None and users.total_count > (offset + limit):
        offset += limit
        users = client.users.get_users(
            filter_term=filter_term,
            user_type=GetUsersUserType.ALL,
            fields=fields,
            limit=limit,
            offset=offset,
        )
        if users.entries:
            result.extend(user.to_dict() for user in users.entries)

    return result


def box_users_list(
    client: BoxClient,
) -> Dict[str, Any]:
    """List all users in the Box account."""
    try:
        result = _box_users_list(client)
        return {"users": result}
    except BoxAPIError as e:
        logging.error(f"Error listing users: {e.message}")
        return {"error": e.message}


def box_users_locate_by_email(
    client: BoxClient,
    email: str,
) -> Dict[str, Any]:
    """Locate a user by their email address."""
    try:
        users = _box_users_search(client, filter_term=email)
        # this returns more than on, lets make sure we have only one exact match
        user = [user for user in users if user.get("login") == email]
        if user is None or len(user) == 0:
            return {"message": "No user found"}
        if len(user) >= 1:
            return {"user": user[0]}
    except BoxAPIError as e:
        logging.error(f"Error locating user by email: {e.message}")
        return {"error": e.message}
    return {"message": "No user found"}


def box_users_locate_by_name(
    client: BoxClient,
    name: str,
) -> Dict[str, Any]:
    """Locate a user by their name."""
    try:
        users = _box_users_search(client, filter_term=name)
        # this returns more than on, lets make sure we have only one exact match
        user = [user for user in users if user.get("name", "") == name]
        if user is None or len(user) == 0:
            return {"message": "No user found"}
        if len(user) >= 1:
            return {"user": user[0]}
    except BoxAPIError as e:
        logging.error(f"Error locating user by name: {e.message}")
        return {"error": e.message}
    return {"message": "No user found"}


def box_users_search_by_name_or_email(
    client: BoxClient,
    query: str,
) -> Dict[str, Any]:
    """Search for users by name or email."""
    try:
        users = _box_users_search(client, filter_term=query)
        return {"users": users}
    except BoxAPIError as e:
        logging.error(f"Error searching users: {e.message}")
        return {"error": e.message}
