import uuid
from box_sdk_gen import (
    BoxClient,
    CreateGroupMembershipUser,
    CreateGroupMembershipGroup,
    CreateGroupMembershipRole,
)

from box_ai_agents_toolkit import (
    box_groups_search,
    box_groups_list_by_user,
    box_groups_list_members,
)


def _create_group(client: BoxClient, name: str) -> dict:
    """Helper function to create a group for testing purposes."""
    group = client.groups.create_group(name=name)
    return group.to_dict()


def _create_test_groups_n(client: BoxClient, n: int) -> list:
    """Helper function to create n test groups."""
    groups = []
    for i in range(n):
        group_name = f"Test Group {i} - {uuid.uuid4()}"
        group = _create_group(client, group_name)
        groups.append(group)
    return groups


def _delete_group(client: BoxClient, group_id: str) -> None:
    """Helper function to delete a group after testing."""
    client.groups.delete_group_by_id(group_id)


def test_box_groups_search(box_client_ccg: BoxClient):
    # create 10 test groups
    test_groups = _create_test_groups_n(box_client_ccg, 10)
    assert len(test_groups) == 10

    # Get the full groups list from the function
    list_result = box_groups_search(box_client_ccg, limit=5)
    group_result = list_result.get("groups", [])
    error = list_result.get("error", None)
    message = list_result.get("message", None)

    assert error is None, f"Error occurred: {error}"
    if message:
        assert message == "No groups found."
        assert group_result == []
    else:
        assert isinstance(group_result, list)
        assert all(isinstance(group, dict) for group in group_result)
        assert all(
            set(group.keys()) >= {"id", "type", "name", "group_type"}
            for group in group_result
        )

    # Create a new group to test filtering with a unique uuid
    test_group_name = f"Test Group for API {uuid.uuid4()}"
    new_group = _create_group(box_client_ccg, test_group_name)
    assert new_group["name"] == test_group_name

    try:
        # Search for the newly created group using filter_term with time stamp on name
        search_result = box_groups_search(
            box_client_ccg, filter_term=test_group_name, limit=5
        )

        group_result = search_result.get("groups", [])
        error_search = search_result.get("error", None)
        message_search = search_result.get("message", None)

        assert error_search is None, f"Error occurred: {error_search}"
        assert message_search is None, f"Unexpected message: {message_search}"
        # check if created group is in the search results
        assert any(
            group["id"] == new_group["id"] and group["name"] == test_group_name
            for group in group_result
        ), "Created group not found in search results."

        # search with a partial name
        partial_name = test_group_name.split(" ")[
            0
        ]  # Use the first word for partial search
        partial_search_result = box_groups_search(
            box_client_ccg, filter_term=partial_name, limit=5
        )
        partial_group_result = partial_search_result.get("groups", [])
        error_partial = partial_search_result.get("error", None)
        message_partial = partial_search_result.get("message", None)

        assert error_partial is None, f"Error occurred: {error_partial}"
        assert message_partial is None, f"Unexpected message: {message_partial}"
        assert any(
            group["id"] == new_group["id"] and group["name"] == test_group_name
            for group in partial_group_result
        ), "Created group not found in partial search results."
    finally:
        # Clean up by deleting the created group
        _delete_group(box_client_ccg, new_group["id"])
        # delete the 10 test groups created
        for group in test_groups:
            _delete_group(box_client_ccg, group["id"])


def test_box_groups_list_by_user(box_client_ccg: BoxClient):
    current_user = box_client_ccg.users.get_user_me()

    # create 10 test groups
    test_groups = _create_test_groups_n(box_client_ccg, 10)
    assert len(test_groups) == 10

    # add current user to all groups
    for group in test_groups:
        _ = box_client_ccg.memberships.create_group_membership(
            user=CreateGroupMembershipUser(id=current_user.id),
            group=CreateGroupMembershipGroup(id=group.get("id")),
            role=CreateGroupMembershipRole.ADMIN,
        )

    try:
        # check group memberships for current user
        list_result = box_groups_list_by_user(
            box_client_ccg, user_id=current_user.id, limit=5
        )
        memberships_result = list_result.get("memberships", [])
        error = list_result.get("error", None)
        message = list_result.get("message", None)

        assert error is None, f"Error occurred: {error}"
        if message:
            assert message == "No groups found for the user."
            assert memberships_result == []
        else:
            assert isinstance(memberships_result, list)
            assert all(
                isinstance(membership, dict) for membership in memberships_result
            )
            # check if created group exists within the memberships of the assigned groups
            for group in test_groups:
                assert any(
                    membership.get("group", {}).get("id") == group["id"]
                    for membership in memberships_result
                ), f"Group {group['name']} not found in memberships."
    finally:
        # Clean up by deleting the created group
        for group in test_groups:
            _delete_group(box_client_ccg, group["id"])


def test_box_groups_list_members(box_client_ccg: BoxClient):
    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # create 1 test group
    test_group = _create_group(box_client_ccg, f"Test Group for Members {uuid.uuid4()}")
    assert test_group is not None

    # add all users to this group
    for user in all_users:
        _ = box_client_ccg.memberships.create_group_membership(
            user=CreateGroupMembershipUser(id=user.id),
            group=CreateGroupMembershipGroup(id=test_group["id"]),
            role=CreateGroupMembershipRole.ADMIN,
        )

    try:
        # check group members for the created group
        list_result = box_groups_list_members(
            box_client_ccg, group_id=test_group.get("id", ""), limit=5
        )
        members_result = list_result.get("memberships", [])
        error = list_result.get("error", None)
        message = list_result.get("message", None)

        assert error is None, f"Error occurred: {error}"
        if message:
            assert message == "No members found for the group."
            assert members_result == []
        else:
            assert isinstance(members_result, list)
            assert all(isinstance(member, dict) for member in members_result)
            # check if all user exists within the group members
            for user in all_users:
                assert any(
                    member.get("user", {}).get("id") == user.id
                    for member in members_result
                ), f"User {user.name} not found in group members."
    finally:
        # Clean up by deleting the created group
        box_client_ccg.groups.delete_group_by_id(test_group["id"])
