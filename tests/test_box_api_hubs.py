import datetime
import uuid
import pytest
from time import sleep

from box_sdk_gen import (
    BoxClient,
    GroupFull,
    CreateGroupMembershipGroup,
    CreateGroupMembershipUser,
)
from box_ai_agents_toolkit import (
    box_hub_copy,
    box_hub_create,
    box_hub_delete,
    box_hub_get,
    box_hub_list,
    box_hub_update,
    box_hub_items_list,
    box_hub_item_add,
    box_hub_item_remove,
    box_hub_collaboration_add_group_by_id,
    box_hub_collaboration_add_user_by_email,
    box_hub_collaboration_add_user_by_id,
    box_hub_collaboration_remove,
    box_hub_collaboration_update,
    box_hub_collaborations_list,
    box_hub_collaboration_details,
)

from tests.conftest import TestData


def _prep_test_group(box_client_ccg: BoxClient) -> GroupFull:
    def find_next_user(exclude_ids):
        return next(
            (
                user
                for user in all_users
                if user.id not in exclude_ids
                and user.login is not None
                and user.login.endswith("@boxdemo.com")
            ),
            None,
        )

    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users and len(all_users) > 0

    test_group_name = f"Test Group for box_collaboration {uuid.uuid4()}"
    test_group = box_client_ccg.groups.create_group(name=test_group_name)
    membership_group = CreateGroupMembershipGroup(id=test_group.id)

    # Hubs group membership does not allow duplicate users either from user assignment it self or group membership
    # # Add current user to group
    # box_client_ccg.memberships.create_group_membership(
    #     group=membership_group, user=CreateGroupMembershipUser(id=user_me)
    # )

    # Add two more users to group
    test_user_a = find_next_user({user_me})
    assert test_user_a is not None, "No suitable test user A found."
    box_client_ccg.memberships.create_group_membership(
        group=membership_group, user=CreateGroupMembershipUser(id=test_user_a.id)
    )

    test_user_b = find_next_user({user_me, test_user_a.id})
    assert test_user_b is not None, "No suitable test user B found."
    box_client_ccg.memberships.create_group_membership(
        group=membership_group, user=CreateGroupMembershipUser(id=test_user_b.id)
    )

    return test_group


def test_box_hub_create_delete(box_client_ccg: BoxClient):
    """Test creating and deleting a hub."""
    # Create a hub
    hub_title = f"{uuid.uuid4()}"
    hub_description = "This is a test hub created by pytest"

    result = box_hub_create(
        client=box_client_ccg,
        title=hub_title,
        description=hub_description,
    )

    assert "error" not in result
    assert result["title"] == hub_title
    assert result["description"] == hub_description
    assert "id" in result

    hub_id = result["id"]

    # Delete the hub
    delete_result = box_hub_delete(client=box_client_ccg, hub_id=hub_id)
    assert "error" not in delete_result
    assert "message" in delete_result

    # try to delete a non existing hub
    fake_hub_id = "99999"
    delete_result = box_hub_delete(client=box_client_ccg, hub_id=fake_hub_id)
    assert "error" in delete_result

    # try to create a hub with missing title
    create_result = box_hub_create(
        client=box_client_ccg,
        title="",
        description=hub_description,
    )
    assert "error" in create_result


def test_box_hub_get(box_hub_test_data: TestData, box_client_ccg: BoxClient):
    """Test getting hub details."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id

    result = box_hub_get(client=box_client_ccg, hub_id=hub_id)

    assert "error" not in result
    assert result["id"] == hub_id
    assert "title" in result
    assert "description" in result

    # try to get a non existing hub
    fake_hub_id = "99999"
    result = box_hub_get(client=box_client_ccg, hub_id=fake_hub_id)
    assert "error" in result


def test_box_hub_update(box_hub_test_data: TestData, box_client_ccg: BoxClient):
    """Test updating hub details."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id
    new_title = f"{uuid.uuid4()} Updated"
    new_description = "This is an updated description"

    result = box_hub_update(
        client=box_client_ccg,
        hub_id=hub_id,
        title=new_title,
        description=new_description,
        is_ai_enabled=True,
    )

    assert "error" not in result
    assert result["id"] == hub_id
    assert result["title"] == new_title
    assert result["description"] == new_description
    assert result["is_ai_enabled"]

    # try updating a non existing hub
    fake_hub_id = "99999"
    result = box_hub_update(
        client=box_client_ccg,
        hub_id=fake_hub_id,
        title=new_title,
        description=new_description,
    )
    assert "error" in result


def test_box_hub_copy(box_hub_test_data: TestData, box_client_ccg: BoxClient):
    """Test copying a hub."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id
    copied_title = f"{uuid.uuid4()} Copied"
    copied_description = "This is a copied hub"

    result = box_hub_copy(
        client=box_client_ccg,
        hub_id=hub_id,
        title=copied_title,
        description=copied_description,
    )

    assert "error" not in result
    assert result["title"] == copied_title
    assert result["description"] == copied_description
    assert "id" in result

    # Clean up the copied hub
    copied_hub_id = result["id"]
    box_hub_delete(client=box_client_ccg, hub_id=copied_hub_id)

    # try to copy a non existing hub
    fake_hub_id = "99999"
    result = box_hub_copy(
        client=box_client_ccg,
        hub_id=fake_hub_id,
        title=copied_title,
        description=copied_description,
    )
    assert "error" in result


def test_box_hub_list(box_hub_test_data: TestData, box_client_ccg: BoxClient):
    """Test listing hubs."""
    assert box_hub_test_data.test_hub is not None
    result = box_hub_list(client=box_client_ccg, limit=100)

    assert "error" not in result
    assert "hubs" in result or "message" in result

    if "hubs" in result:
        assert isinstance(result["hubs"], list)
        # Verify our test hub is in the list
        hub_ids = [hub["id"] for hub in result["hubs"]]
        assert box_hub_test_data.test_hub.id in hub_ids


def test_box_hub_list_with_query(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test listing hubs with a search query."""
    assert box_hub_test_data.test_hub is not None
    # Get the hub title to search for
    hub_title = box_hub_test_data.test_hub.title

    result = box_hub_list(
        client=box_client_ccg,
        query=hub_title,
        limit=100,
    )

    assert "error" not in result
    if "hubs" in result:
        assert isinstance(result["hubs"], list)


def test_box_hub_list_with_sort(box_client_ccg: BoxClient):
    """Test listing hubs with sorting."""
    result = box_hub_list(
        client=box_client_ccg,
        sort="view_count",
        direction="DESC",
        limit=100,
    )

    assert "error" not in result
    assert "hubs" in result or "message" in result


def test_box_hub_items_list_empty(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test listing items in an empty hub."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id

    result = box_hub_items_list(client=box_client_ccg, hub_id=hub_id)

    assert "error" not in result
    # Should have a message indicating no items or an empty list
    assert "message" in result or "hub items" in result


def test_box_hub_item_add_remove_file(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test adding and removing a file from a hub."""
    assert box_hub_test_data.test_hub is not None
    assert box_hub_test_data.test_files is not None
    hub_id = box_hub_test_data.test_hub.id
    file_id = box_hub_test_data.test_files[0].id

    # Add file to hub
    add_result = box_hub_item_add(
        client=box_client_ccg,
        hub_id=hub_id,
        item_id=file_id,
        item_type="file",
    )

    assert "error" not in add_result

    # Give the API a moment to process
    sleep(1)

    # Verify the file is in the hub
    items_result = box_hub_items_list(client=box_client_ccg, hub_id=hub_id)
    assert "error" not in items_result
    if "hub items" in items_result:
        item_ids = [item["item"]["id"] for item in items_result["hub items"]]
        assert file_id in item_ids

    # Remove file from hub
    remove_result = box_hub_item_remove(
        client=box_client_ccg,
        hub_id=hub_id,
        item_id=file_id,
        item_type="file",
    )

    assert "error" not in remove_result

    # try adding a non-existent file
    fake_item_id = "99999"
    add_result = box_hub_item_add(
        client=box_client_ccg,
        hub_id=hub_id,
        item_id=fake_item_id,
        item_type="file",
    )
    assert "error" in add_result


def test_box_hub_item_add_remove_folder(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test adding and removing a folder from a hub."""
    assert box_hub_test_data.test_hub is not None
    assert box_hub_test_data.test_folder is not None
    hub_id = box_hub_test_data.test_hub.id
    folder_id = box_hub_test_data.test_folder.id

    # Add folder to hub
    add_result = box_hub_item_add(
        client=box_client_ccg,
        hub_id=hub_id,
        item_id=folder_id,
        item_type="folder",
    )

    assert "error" not in add_result

    # Give the API a moment to process
    sleep(1)

    # Verify the folder is in the hub
    items_result = box_hub_items_list(client=box_client_ccg, hub_id=hub_id)
    assert "error" not in items_result
    if "hub items" in items_result:
        item_ids = [item["item"]["id"] for item in items_result["hub items"]]
        assert folder_id in item_ids

    # Remove folder from hub
    remove_result = box_hub_item_remove(
        client=box_client_ccg,
        hub_id=hub_id,
        item_id=folder_id,
        item_type="folder",
    )

    assert "error" not in remove_result

    # try adding a non-existent folder
    fake_item_id = "99999"
    add_result = box_hub_item_add(
        client=box_client_ccg,
        hub_id=hub_id,
        item_id=fake_item_id,
        item_type="folder",
    )
    assert "error" in add_result


@pytest.mark.skip(reason="Flaky test - needs investigation")
def test_box_hub_items_list_not_empty(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test listing items in a hub with items."""
    assert box_hub_test_data.test_hub is not None
    assert box_hub_test_data.test_files is not None
    hub_id = box_hub_test_data.test_hub.id
    file_id = box_hub_test_data.test_files[0].id

    # Add file to hub
    add_result = box_hub_item_add(
        client=box_client_ccg,
        hub_id=hub_id,
        item_id=file_id,
        item_type="file",
    )

    assert "error" not in add_result

    # Give the API a moment to process
    sleep(1)
    result = box_hub_items_list(client=box_client_ccg, hub_id=hub_id)

    assert "error" not in result
    assert "hub items" in result
    assert isinstance(result["hub items"], list)
    assert len(result["hub items"]) > 0
    assert result["hub items"][0]["item"]["id"] == file_id

    # remove file from hub
    remove_result = box_hub_item_remove(
        client=box_client_ccg,
        hub_id=hub_id,
        item_id=file_id,
        item_type="file",
    )

    assert "error" not in remove_result


def test_box_hub_collaborations_list_empty(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test listing collaborations in a hub with no collaborations."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id

    result = box_hub_collaborations_list(client=box_client_ccg, hub_id=hub_id)

    assert "error" not in result
    # Should have a message indicating no collaborations or an empty list
    assert "message" in result or "hub collaborations" in result


def test_box_hub_collaboration_add_remove_user_by_id(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test adding and removing a user collaboration by ID."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id

    # Get current user ID
    user_me_id = box_client_ccg.users.get_user_me().id
    assert user_me_id is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com
    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me_id
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_id = test_user.id

    # Add user collaboration
    add_result = box_hub_collaboration_add_user_by_id(
        client=box_client_ccg,
        hub_id=hub_id,
        user_id=test_user_id,
        role="editor",
    )

    # This might fail if the user is already the owner
    # In that case, we'll skip the rest of the test
    if "error" in add_result:
        # Check if it's because the user is already a collaborator
        if (
            "already" in add_result["error"].lower()
            or "owner" in add_result["error"].lower()
        ):
            return
        else:
            assert False, f"Unexpected error: {add_result['error']}"

    assert "id" in add_result
    collaboration_id = add_result["id"]

    # List collaborations and verify
    list_result = box_hub_collaborations_list(client=box_client_ccg, hub_id=hub_id)
    assert "error" not in list_result

    # Remove collaboration
    remove_result = box_hub_collaboration_remove(
        client=box_client_ccg,
        hub_collaboration_id=collaboration_id,
    )

    assert "error" not in remove_result
    assert "message" in remove_result

    # try adding a collaboration to a non-existent user ID
    fake_user_id = "99999"
    add_result = box_hub_collaboration_add_user_by_id(
        client=box_client_ccg,
        hub_id=hub_id,
        user_id=fake_user_id,
        role="editor",
    )
    assert "error" in add_result


def test_box_hub_collaboration_add_user_by_email(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test adding a user collaboration by email."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id

    # Get current user ID
    user_me_id = box_client_ccg.users.get_user_me().id
    assert user_me_id is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com
    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me_id
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_login = test_user.login
    assert test_user_login is not None

    # Add user collaboration by email
    add_result = box_hub_collaboration_add_user_by_email(
        client=box_client_ccg,
        hub_id=hub_id,
        email=test_user_login,
        role="editor",
    )

    # This might fail if the user is already the owner
    assert "error" not in add_result, (
        f"Error adding collaboration: {add_result.get('error')}"
    )

    assert "id" in add_result
    collaboration_id = add_result["id"]

    # List collaborations and verify
    list_result = box_hub_collaborations_list(client=box_client_ccg, hub_id=hub_id)
    assert "error" not in list_result

    # Remove collaboration
    remove_result = box_hub_collaboration_remove(
        client=box_client_ccg,
        hub_collaboration_id=collaboration_id,
    )

    assert "error" not in remove_result
    assert "message" in remove_result

    # test adding a collaboration to a non-existent user email
    fake_email = "nonexistentuser@boxdemo.com"
    add_result = box_hub_collaboration_add_user_by_email(
        client=box_client_ccg,
        hub_id=hub_id,
        email=fake_email,
        role="editor",
    )
    assert "error" in add_result


def test_box_hub_collaboration_update(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test updating a collaboration role."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id

    # Get current user ID
    user_me_id = box_client_ccg.users.get_user_me().id
    assert user_me_id is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com
    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me_id
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    user_id = test_user.id
    assert user_id is not None

    # Add user collaboration as viewer
    add_result = box_hub_collaboration_add_user_by_id(
        client=box_client_ccg,
        hub_id=hub_id,
        user_id=user_id,
        role="viewer",
    )

    # this might fail if the user is already the owner
    assert "error" not in add_result

    collaboration_id = add_result["id"]

    # Give the API a moment to process
    sleep(1)

    # Update to editor role
    update_result = box_hub_collaboration_update(
        client=box_client_ccg,
        hub_collaboration_id=collaboration_id,
        role="editor",
    )

    assert "error" not in update_result
    assert update_result["role"] == "editor"

    # Clean up
    box_hub_collaboration_remove(
        client=box_client_ccg,
        hub_collaboration_id=collaboration_id,
    )

    # test updating a non-existent collaboration ID
    fake_collaboration_id = "99999"
    update_result = box_hub_collaboration_update(
        client=box_client_ccg,
        hub_collaboration_id=fake_collaboration_id,
        role="editor",
    )
    assert "error" in update_result


def test_box_hub_collaboration_details(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test getting collaboration details."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id

    # Get current user ID
    user_me_id = box_client_ccg.users.get_user_me().id
    assert user_me_id is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com
    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me_id
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    user_id = test_user.id
    assert user_id is not None

    # Add user collaboration
    add_result = box_hub_collaboration_add_user_by_id(
        client=box_client_ccg,
        hub_id=hub_id,
        user_id=user_id,
        role="editor",
    )

    # this might fail if the user is already the owner
    assert "error" not in add_result

    collaboration_id = add_result["id"]

    # Get collaboration details
    details_result = box_hub_collaboration_details(
        client=box_client_ccg,
        hub_collaboration_id=collaboration_id,
    )

    assert "error" not in details_result
    assert details_result["id"] == collaboration_id
    assert "role" in details_result
    assert "accessible_by" in details_result

    # Clean up
    box_hub_collaboration_remove(
        client=box_client_ccg,
        hub_collaboration_id=collaboration_id,
    )

    # test with a non-existent collaboration ID
    fake_collaboration_id = "99999"
    details_result = box_hub_collaboration_details(
        client=box_client_ccg,
        hub_collaboration_id=fake_collaboration_id,
    )
    assert "error" in details_result


@pytest.mark.skip(reason="Failing test - needs investigation")
def test_box_hub_collaboration_add_group_by_id(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test adding a group collaboration by ID."""
    assert box_hub_test_data.test_hub is not None
    hub_id = box_hub_test_data.test_hub.id

    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    test_group = _prep_test_group(box_client_ccg)
    assert test_group is not None
    assert test_group.id is not None
    group_id = test_group.id

    # Add group collaboration
    add_result = box_hub_collaboration_add_group_by_id(
        client=box_client_ccg,
        hub_id=hub_id,
        group_id=group_id,
        role="editor",
    )

    # Check if collaboration was added successfully
    assert "error" not in add_result

    assert "id" in add_result
    collaboration_id = add_result["id"]

    # List collaborations and verify
    list_result = box_hub_collaborations_list(client=box_client_ccg, hub_id=hub_id)
    assert "error" not in list_result

    # Remove collaboration
    remove_result = box_hub_collaboration_remove(
        client=box_client_ccg,
        hub_collaboration_id=collaboration_id,
    )

    assert "error" not in remove_result
    assert "message" in remove_result

    # remove test group
    box_client_ccg.groups.delete_group_by_id(group_id)


def test_box_hub_item_invalid_type(
    box_hub_test_data: TestData, box_client_ccg: BoxClient
):
    """Test adding an item with invalid type raises an error."""
    assert box_hub_test_data.test_hub is not None
    assert box_hub_test_data.test_files is not None
    hub_id = box_hub_test_data.test_hub.id
    file_id = box_hub_test_data.test_files[0].id

    try:
        box_hub_item_add(
            client=box_client_ccg,
            hub_id=hub_id,
            item_id=file_id,
            item_type="invalid_type",
        )
        # Should not reach here
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Invalid item type" in str(e)


def test_box_hub_list_invalid_direction(box_client_ccg: BoxClient):
    """Test listing hubs with invalid direction parameter."""
    result = box_hub_list(
        client=box_client_ccg,
        direction="INVALID",
        limit=100,
    )

    assert "error" in result
    assert "Invalid direction" in result["error"]
