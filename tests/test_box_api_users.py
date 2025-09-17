from box_sdk_gen import BoxClient
from box_ai_agents_toolkit import (
    box_users_list,
    box_users_locate_by_email,
    box_users_locate_by_name,
    box_users_search_by_name_or_email,
)


def _get_all_users_manually(client: BoxClient):
    # Manually get all users from the API to compare
    fields = ["id", "type", "name", "login", "role"]
    marker = None
    limit = 5

    users = client.users.get_users(
        fields=fields, limit=limit, usemarker=True, marker=marker
    )
    if users.entries is None:
        users_base = []
    else:
        users_base = [user.to_dict() for user in users.entries]

    # check if api returned a marker for next page
    if users.next_marker:
        marker = users.next_marker
        while marker:
            users = client.users.get_users(
                fields=fields, limit=limit, usemarker=True, marker=marker
            )
            if users.entries:
                users_base.extend(user.to_dict() for user in users.entries)
            marker = users.next_marker if users.next_marker else None

    return users_base


def test_box_users_list(box_client_ccg: BoxClient):
    # Get the full users list from the function
    users_base = _get_all_users_manually(box_client_ccg)
    assert users_base is not None

    list_result = box_users_list(box_client_ccg)
    user_result = list_result.get("users", [])
    error = list_result.get("error", None)

    assert error is None, f"Error occurred: {error}"
    assert isinstance(user_result, list)
    assert len(user_result) == len(users_base)
    assert all(user in users_base for user in user_result)
    assert all(user in user_result for user in users_base)
    assert all(
        set(user.keys()) == {"id", "type", "name", "login", "role"}
        for user in user_result
    )
    assert all(
        set(user.keys()) == {"id", "type", "name", "login", "role"}
        for user in users_base
    )
    assert user_result == users_base


def test_box_users_locate_by_email(box_client_ccg: BoxClient):
    # Get the full users list from the function
    users_base = _get_all_users_manually(box_client_ccg)
    assert users_base is not None
    assert len(users_base) > 0, "No users found in the Box account."

    # Pick a user to locate
    test_user = users_base[0]
    test_email = test_user["login"]

    locate_result = box_users_locate_by_email(box_client_ccg, test_email)
    located_user = locate_result.get("user", None)
    error = locate_result.get("error", None)

    assert error is None, f"Error occurred: {error}"
    assert located_user is not None, "No user located."
    assert located_user == test_user

    # Test with an email that doesn't exist
    locate_result_none = box_users_locate_by_email(
        box_client_ccg, "non.existing@email.com"
    )
    message = locate_result_none.get("message", None)
    error_none = locate_result_none.get("error", None)
    assert error_none is None, f"Error occurred: {error_none}"
    assert message == "No user found", "Expected 'No user found' message."


def test_box_users_locate_by_name(box_client_ccg: BoxClient):
    # Get the full users list from the function
    users_base = _get_all_users_manually(box_client_ccg)
    assert users_base is not None
    assert len(users_base) > 0, "No users found in the Box account."

    # Pick a user to locate
    test_user = users_base[0]
    test_name = test_user["name"]

    locate_result = box_users_locate_by_name(box_client_ccg, test_name)
    located_user = locate_result.get("user", None)
    error = locate_result.get("error", None)

    assert error is None, f"Error occurred: {error}"
    assert located_user is not None, "No user located."
    assert located_user == test_user

    # Test with a name that doesn't exist
    locate_result_none = box_users_locate_by_name(box_client_ccg, "Non Existent Name")
    message = locate_result_none.get("message", None)
    error_none = locate_result_none.get("error", None)
    assert error_none is None, f"Error occurred: {error_none}"
    assert message == "No user found", "Expected 'No user found' message."


def test_box_users_search_by_name_or_email(box_client_ccg: BoxClient):
    # Get the full users list from the function
    users_base = _get_all_users_manually(box_client_ccg)
    assert users_base is not None
    assert len(users_base) > 0, "No users found in the Box account."

    # Pick a user to search
    test_user = users_base[0]
    test_query = test_user["name"]

    search_result = box_users_search_by_name_or_email(box_client_ccg, test_query)
    found_users = search_result.get("users", [])
    error = search_result.get("error", None)

    assert error is None, f"Error occurred: {error}"
    assert isinstance(found_users, list)
    assert len(found_users) > 0, "No users found in search."
    assert test_user in found_users, "Test user not found in search results."

    # Now search by email
    test_query_email = test_user["login"]
    search_result_email = box_users_search_by_name_or_email(
        box_client_ccg, test_query_email
    )
    found_users_email = search_result_email.get("users", [])
    error_email = search_result_email.get("error", None)

    assert error_email is None, f"Error occurred: {error_email}"
    assert isinstance(found_users_email, list)
    assert len(found_users_email) > 0, "No users found in email search."
    assert test_user in found_users_email, (
        "Test user not found in email search results."
    )
