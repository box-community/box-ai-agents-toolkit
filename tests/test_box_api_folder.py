"""Integration tests for Box folder API functions.

Tests use real Box API calls without mocks to validate actual API behavior
and ensure folder operations work correctly against the Box service.
"""

import uuid

from src.box_ai_agents_toolkit import (
    box_folder_copy,
    box_folder_create,
    box_folder_delete,
    box_folder_favorites_add,
    box_folder_favorites_remove,
    box_folder_info,
    box_folder_items_list,
    box_folder_list_tags,
    box_folder_move,
    box_folder_rename,
    box_folder_set_collaboration,
    box_folder_set_description,
    box_folder_set_sync,
    box_folder_set_upload_email,
    box_folder_tag_add,
    box_folder_tag_remove,
)
from tests.conftest import BoxClient, TestData

# ==================== Folder Info Tests ====================


def test_box_folder_info_success(box_client_ccg: BoxClient, folder_test_data: TestData):
    """Test retrieving information about an existing folder."""
    folder_id = folder_test_data.test_folder.id
    response = box_folder_info(box_client_ccg, folder_id)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    folder = response["folder"]
    assert folder["id"] == folder_id
    assert folder["type"] == "folder"
    assert folder["name"] is not None


def test_box_folder_info_not_found(box_client_ccg: BoxClient):
    """Test error handling when folder does not exist."""
    non_existent_id = "999999999999"
    response = box_folder_info(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== Folder Items List Tests ====================


def test_box_folder_items_list_non_recursive(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test listing items in a folder without recursion."""
    parent_id = folder_test_data.test_folder.id
    response = box_folder_items_list(box_client_ccg, parent_id, is_recursive=False)

    assert response is not None
    assert "error" not in response
    # Should find at least the subfolder
    assert "folder_items" in response or "message" in response


def test_box_folder_items_list_recursive(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test listing items recursively through nested folders."""
    parent_id = folder_test_data.test_folder.id
    response = box_folder_items_list(box_client_ccg, parent_id, is_recursive=True)

    assert response is not None
    assert "error" not in response
    # Response should contain folder_items or message indicating no items
    assert "folder_items" in response or "message" in response


def test_box_folder_items_list_with_limit(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test listing items with custom limit parameter."""
    parent_id = folder_test_data.test_folder.id
    response = box_folder_items_list(
        box_client_ccg, parent_id, is_recursive=False, limit=10
    )

    assert response is not None
    assert "error" not in response


def test_box_folder_items_list_not_found(box_client_ccg: BoxClient):
    """Test error handling when listing items from non-existent folder."""
    non_existent_id = "999999999999"
    response = box_folder_items_list(
        box_client_ccg, non_existent_id, is_recursive=False
    )

    assert response is not None
    assert "error" in response


# ==================== Folder Create Tests ====================


def test_box_folder_create_success(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test creating a new folder in an existing parent folder."""
    parent_folder_id = folder_test_data.test_folder.id
    new_folder_name = f"Test Folder {uuid.uuid4()}"

    response = box_folder_create(box_client_ccg, new_folder_name, parent_folder_id)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    folder = response["folder"]
    assert folder["name"] == new_folder_name
    assert folder["parent"]["id"] == parent_folder_id
    assert folder["type"] == "folder"

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(folder["id"], recursive=False)


def test_box_folder_create_invalid_parent(box_client_ccg: BoxClient):
    """Test error handling when parent folder does not exist."""
    invalid_parent_id = "999999999999"
    new_folder_name = f"Test Folder {uuid.uuid4()}"

    response = box_folder_create(box_client_ccg, new_folder_name, invalid_parent_id)

    assert response is not None
    assert "error" in response


def test_box_folder_create_duplicate_name(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test creating a folder with a name that already exists in parent."""
    parent_folder_id = folder_test_data.test_folder.id
    folder_name = f"Duplicate Test {uuid.uuid4()}"

    # Create first folder
    response1 = box_folder_create(box_client_ccg, folder_name, parent_folder_id)
    assert "error" not in response1
    folder_id_1 = response1["folder"]["id"]

    # Create second folder with same name - Box does not allow this
    response2 = box_folder_create(box_client_ccg, folder_name, parent_folder_id)
    assert "error" in response2

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(folder_id_1, recursive=False)


# ==================== Folder Delete Tests ====================


def test_box_folder_delete_empty(box_client_ccg: BoxClient, folder_test_data: TestData):
    """Test deleting an empty folder."""
    parent_folder_id = folder_test_data.test_folder.id
    folder_to_delete_name = f"Delete Me {uuid.uuid4()}"

    # Create folder to delete
    create_response = box_folder_create(
        box_client_ccg, folder_to_delete_name, parent_folder_id
    )
    folder_id = create_response["folder"]["id"]

    # Delete the folder
    response = box_folder_delete(box_client_ccg, folder_id, recursive=False)

    assert response is not None
    assert "error" not in response
    assert "message" in response
    assert "deleted successfully" in response["message"]


def test_box_folder_delete_recursive(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test deleting a folder with contents using recursive flag."""
    parent_folder_id = folder_test_data.test_folder.id
    folder_to_delete_name = f"Delete With Contents {uuid.uuid4()}"

    # Create folder to delete
    create_response = box_folder_create(
        box_client_ccg, folder_to_delete_name, parent_folder_id
    )
    folder_id = create_response["folder"]["id"]

    # Delete recursively
    response = box_folder_delete(box_client_ccg, folder_id, recursive=True)

    assert response is not None
    assert "error" not in response
    assert "message" in response


def test_box_folder_delete_non_existent(box_client_ccg: BoxClient):
    """Test error handling when deleting a non-existent folder."""
    non_existent_id = "999999999999"
    response = box_folder_delete(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== Folder Copy Tests ====================


def test_box_folder_copy_with_new_name(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test copying a folder with a new name."""
    source_folder_id = folder_test_data.test_files[0].id  # subfolder
    destination_parent_id = folder_test_data.test_files[2].id  # destination folder
    new_name = f"Copied Folder {uuid.uuid4()}"

    response = box_folder_copy(
        box_client_ccg,
        source_folder_id,
        destination_parent_id,
        name=new_name,
    )

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    copied_folder = response["folder"]
    assert copied_folder["name"] == new_name
    assert copied_folder["parent"]["id"] == destination_parent_id

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(copied_folder["id"], recursive=True)


def test_box_folder_copy_default_name(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test copying a folder and preserving its original name."""
    source_folder_id = folder_test_data.test_files[0].id  # subfolder
    source_name = folder_test_data.test_files[0].name
    destination_parent_id = folder_test_data.test_files[2].id  # destination folder

    response = box_folder_copy(
        box_client_ccg,
        source_folder_id,
        destination_parent_id,
    )

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    copied_folder = response["folder"]
    # Box may append a number or keep the same name
    assert source_name in copied_folder["name"] or copied_folder["name"] == source_name

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(copied_folder["id"], recursive=True)


def test_box_folder_copy_source_not_found(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test error handling when copying a non-existent source folder."""
    non_existent_id = "999999999999"
    destination_parent_id = folder_test_data.test_files[2].id

    response = box_folder_copy(
        box_client_ccg,
        non_existent_id,
        destination_parent_id,
        name="Should Fail",
    )

    assert response is not None
    assert "error" in response


def test_box_folder_copy_destination_not_found(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test error handling when copying to a non-existent destination folder."""
    source_folder_id = folder_test_data.test_files[0].id
    non_existent_dest = "999999999999"

    response = box_folder_copy(
        box_client_ccg,
        source_folder_id,
        non_existent_dest,
    )

    assert response is not None
    assert "error" in response


# ==================== Folder Move Tests ====================


def test_box_folder_move_success(box_client_ccg: BoxClient, folder_test_data: TestData):
    """Test moving a folder to a different parent."""
    # Create a folder to move
    source_parent_id = folder_test_data.test_folder.id
    folder_to_move_name = f"Move Me {uuid.uuid4()}"
    create_response = box_folder_create(
        box_client_ccg, folder_to_move_name, source_parent_id
    )
    folder_to_move_id = create_response["folder"]["id"]

    # Move to destination folder
    destination_parent_id = folder_test_data.test_files[2].id
    response = box_folder_move(box_client_ccg, folder_to_move_id, destination_parent_id)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    moved_folder = response["folder"]
    assert moved_folder["parent"]["id"] == destination_parent_id

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(folder_to_move_id, recursive=False)


def test_box_folder_move_folder_not_found(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test error handling when moving a non-existent folder."""
    non_existent_id = "999999999999"
    destination_parent_id = folder_test_data.test_files[2].id

    response = box_folder_move(box_client_ccg, non_existent_id, destination_parent_id)

    assert response is not None
    assert "error" in response


def test_box_folder_move_destination_not_found(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test error handling when moving to a non-existent destination."""
    source_parent_id = folder_test_data.test_folder.id
    folder_to_move_name = f"Move Me {uuid.uuid4()}"
    create_response = box_folder_create(
        box_client_ccg, folder_to_move_name, source_parent_id
    )
    folder_to_move_id = create_response["folder"]["id"]

    non_existent_dest = "999999999999"
    response = box_folder_move(box_client_ccg, folder_to_move_id, non_existent_dest)

    assert response is not None
    assert "error" in response

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(folder_to_move_id, recursive=False)


# ==================== Folder Rename Tests ====================


def test_box_folder_rename_success(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test renaming a folder."""
    # Create a folder to rename
    parent_folder_id = folder_test_data.test_folder.id
    original_name = f"Original Name {uuid.uuid4()}"
    create_response = box_folder_create(box_client_ccg, original_name, parent_folder_id)
    folder_id = create_response["folder"]["id"]

    # Rename the folder
    new_name = f"Renamed Folder {uuid.uuid4()}"
    response = box_folder_rename(box_client_ccg, folder_id, new_name)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    renamed_folder = response["folder"]
    assert renamed_folder["name"] == new_name
    assert renamed_folder["id"] == folder_id

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(folder_id, recursive=False)


def test_box_folder_rename_not_found(box_client_ccg: BoxClient):
    """Test error handling when renaming a non-existent folder."""
    non_existent_id = "999999999999"
    new_name = f"New Name {uuid.uuid4()}"

    response = box_folder_rename(box_client_ccg, non_existent_id, new_name)

    assert response is not None
    assert "error" in response


# ==================== Folder Description Tests ====================


def test_box_folder_set_description(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test setting a description on a folder."""
    folder_id = folder_test_data.test_folder.id
    description = f"Test Description {uuid.uuid4()}"

    response = box_folder_set_description(box_client_ccg, folder_id, description)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    folder = response["folder"]
    assert folder["description"] == description


def test_box_folder_set_description_empty(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test clearing a folder's description."""
    folder_id = folder_test_data.test_folder.id

    # Set description first
    set_response = box_folder_set_description(
        box_client_ccg, folder_id, "Initial Description"
    )
    assert "error" not in set_response

    # Clear it
    clear_response = box_folder_set_description(box_client_ccg, folder_id, "")

    assert clear_response is not None
    assert "error" not in clear_response


def test_box_folder_set_description_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting description on non-existent folder."""
    non_existent_id = "999999999999"
    description = "This should fail"

    response = box_folder_set_description(box_client_ccg, non_existent_id, description)

    assert response is not None
    assert "error" in response


# ==================== Folder Collaboration Tests ====================


def test_box_folder_set_collaboration_settings(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test setting collaboration settings on a folder."""
    folder_id = folder_test_data.test_folder.id

    response = box_folder_set_collaboration(
        box_client_ccg,
        folder_id,
        can_non_owners_invite=True,
        can_non_owners_view_collaborators=True,
        is_collaboration_restricted_to_enterprise=False,
    )

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    folder = response["folder"]
    assert "can_non_owners_invite" in folder


def test_box_folder_set_collaboration_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting collaboration on non-existent folder."""
    non_existent_id = "999999999999"

    response = box_folder_set_collaboration(
        box_client_ccg,
        non_existent_id,
        can_non_owners_invite=True,
        can_non_owners_view_collaborators=False,
        is_collaboration_restricted_to_enterprise=False,
    )

    assert response is not None
    assert "error" in response


# ==================== Folder Tags Tests ====================


def test_box_folder_tag_add_single(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test adding a single tag to a folder."""
    folder_id = folder_test_data.test_folder.id
    tag = f"test-tag-{uuid.uuid4()}"

    response = box_folder_tag_add(box_client_ccg, folder_id, tag)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    folder = response["folder"]
    assert "tags" in folder
    assert tag in folder["tags"]


def test_box_folder_tag_add_multiple(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test adding multiple tags to a folder."""
    folder_id = folder_test_data.test_folder.id
    tag1 = f"tag-one-{uuid.uuid4()}"
    tag2 = f"tag-two-{uuid.uuid4()}"

    # Add first tag
    response1 = box_folder_tag_add(box_client_ccg, folder_id, tag1)
    assert "error" not in response1
    assert tag1 in response1["folder"]["tags"]

    # Add second tag
    response2 = box_folder_tag_add(box_client_ccg, folder_id, tag2)
    assert "error" not in response2
    folder = response2["folder"]
    assert tag1 in folder["tags"]
    assert tag2 in folder["tags"]


def test_box_folder_tag_remove(box_client_ccg: BoxClient, folder_test_data: TestData):
    """Test removing a tag from a folder."""
    folder_id = folder_test_data.test_folder.id
    tag = f"tag-to-remove-{uuid.uuid4()}"

    # Add tag
    add_response = box_folder_tag_add(box_client_ccg, folder_id, tag)
    assert tag in add_response["folder"]["tags"]

    # Remove tag
    remove_response = box_folder_tag_remove(box_client_ccg, folder_id, tag)

    assert remove_response is not None
    assert "error" not in remove_response
    assert "folder" in remove_response
    folder = remove_response["folder"]
    assert tag not in folder["tags"]


def test_box_folder_tag_add_not_found(box_client_ccg: BoxClient):
    """Test error handling when adding tag to non-existent folder."""
    non_existent_id = "999999999999"
    tag = f"test-tag-{uuid.uuid4()}"

    response = box_folder_tag_add(box_client_ccg, non_existent_id, tag)

    assert response is not None
    assert "error" in response


def test_box_folder_tag_remove_not_found(box_client_ccg: BoxClient):
    """Test error handling when removing tag from non-existent folder."""
    non_existent_id = "999999999999"
    tag = f"test-tag-{uuid.uuid4()}"

    response = box_folder_tag_remove(box_client_ccg, non_existent_id, tag)

    assert response is not None
    assert "error" in response


def test_box_folder_list_tags(box_client_ccg: BoxClient, folder_test_data: TestData):
    """Test listing tags on a folder."""
    folder_id = folder_test_data.test_folder.id
    tag = f"list-tag-{uuid.uuid4()}"

    # Add a tag first
    box_folder_tag_add(box_client_ccg, folder_id, tag)

    # List tags
    response = box_folder_list_tags(box_client_ccg, folder_id)

    assert response is not None
    assert "error" not in response
    if "tags" in response:
        assert tag in response["tags"]
    else:
        # Message indicating no tags
        assert "message" in response


def test_box_folder_list_tags_empty(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test listing tags on a folder with no tags."""
    # Create a new folder with no tags
    parent_folder_id = folder_test_data.test_folder.id
    folder_name = f"No Tags Folder {uuid.uuid4()}"
    create_response = box_folder_create(box_client_ccg, folder_name, parent_folder_id)
    folder_id = create_response["folder"]["id"]

    response = box_folder_list_tags(box_client_ccg, folder_id)

    assert response is not None
    assert "error" not in response
    # Should have either empty tags list or a message
    assert "tags" in response or "message" in response

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(folder_id, recursive=False)


def test_box_folder_list_tags_not_found(box_client_ccg: BoxClient):
    """Test error handling when listing tags on non-existent folder."""
    non_existent_id = "999999999999"

    response = box_folder_list_tags(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== Folder Favorites Tests ====================


def test_box_folder_favorites_add(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test adding a folder to favorites."""
    folder_id = folder_test_data.test_folder.id
    response = box_folder_favorites_add(box_client_ccg, folder_id)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    folder = response["folder"]
    assert folder["id"] == folder_id


def test_box_folder_favorites_add_and_remove(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test adding and then removing a folder from favorites."""
    # Create a new folder for this test
    parent_folder_id = folder_test_data.test_folder.id
    folder_name = f"Favorite Test {uuid.uuid4()}"
    create_response = box_folder_create(box_client_ccg, folder_name, parent_folder_id)
    folder_id = create_response["folder"]["id"]

    # Add to favorites
    add_response = box_folder_favorites_add(box_client_ccg, folder_id)
    assert "error" not in add_response

    # Remove from favorites
    remove_response = box_folder_favorites_remove(box_client_ccg, folder_id)

    assert remove_response is not None
    assert "error" not in remove_response
    assert "folder" in remove_response

    # Cleanup
    box_client_ccg.folders.delete_folder_by_id(folder_id, recursive=False)


def test_box_folder_favorites_add_not_found(box_client_ccg: BoxClient):
    """Test error handling when adding non-existent folder to favorites."""
    non_existent_id = "999999999999"

    response = box_folder_favorites_add(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


def test_box_folder_favorites_remove_not_found(box_client_ccg: BoxClient):
    """Test error handling when removing non-existent folder from favorites."""
    non_existent_id = "999999999999"

    response = box_folder_favorites_remove(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== Folder Sync Tests ====================


def test_box_folder_set_sync_state(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test setting sync state for a folder."""
    folder_id = folder_test_data.test_folder.id
    sync_state = "synced"

    response = box_folder_set_sync(box_client_ccg, folder_id, sync_state)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    folder = response["folder"]
    assert folder["sync_state"] == sync_state


def test_box_folder_set_sync_state_not_synced(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test setting sync state to not_synced."""
    folder_id = folder_test_data.test_folder.id
    sync_state = "not_synced"

    response = box_folder_set_sync(box_client_ccg, folder_id, sync_state)

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    folder = response["folder"]
    assert folder["sync_state"] == sync_state


def test_box_folder_set_sync_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting sync state on non-existent folder."""
    non_existent_id = "999999999999"
    sync_state = "synced"

    response = box_folder_set_sync(box_client_ccg, non_existent_id, sync_state)

    assert response is not None
    assert "error" in response


# ==================== Folder Upload Email Tests ====================


def test_box_folder_set_upload_email_collaborators(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test setting upload email access to collaborators only."""
    folder_id = folder_test_data.test_folder.id

    response = box_folder_set_upload_email(
        box_client_ccg, folder_id, folder_upload_email_access="collaborators"
    )

    assert response is not None
    assert "error" not in response
    assert "folder" in response
    assert "folder_upload_email" in response["folder"]


def test_box_folder_set_upload_email_open(
    box_client_ccg: BoxClient, folder_test_data: TestData
):
    """Test setting upload email access to open."""
    folder_id = folder_test_data.test_folder.id

    response = box_folder_set_upload_email(
        box_client_ccg, folder_id, folder_upload_email_access="open"
    )

    assert response is not None
    assert "error" not in response
    assert "folder" in response


def test_box_folder_set_upload_email_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting upload email on non-existent folder."""
    non_existent_id = "999999999999"

    response = box_folder_set_upload_email(
        box_client_ccg, non_existent_id, folder_upload_email_access="collaborators"
    )

    assert response is not None
    assert "error" in response
