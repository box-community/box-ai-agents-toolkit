"""Integration tests for Box file API functions.

Tests use real Box API calls without mocks to validate actual API behavior
and ensure file operations work correctly against the Box service.
"""

import uuid
from datetime import datetime, timedelta

import pytest

from src.box_ai_agents_toolkit import (
    box_file_copy,
    box_file_delete,
    box_file_info,
    box_file_lock,
    box_file_move,
    box_file_rename,
    box_file_retention_date_clear,
    box_file_retention_date_set,
    box_file_set_description,
    box_file_set_download_company,
    box_file_set_download_open,
    box_file_set_download_reset,
    box_file_tag_add,
    box_file_tag_list,
    box_file_tag_remove,
    box_file_thumbnail_download,
    box_file_thumbnail_url,
    box_file_unlock,
)
from tests.conftest import BoxClient, SampleData

# ==================== File Info Tests ====================


def test_box_file_info_success(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test retrieving information about an existing file."""
    file_id = file_test_data.test_files[0].id
    response = box_file_info(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    assert "file_info" in response
    file_info = response["file_info"]
    assert file_info["id"] == file_id
    assert file_info["type"] == "file"
    assert file_info["name"] is not None


def test_box_file_info_not_found(box_client_ccg: BoxClient):
    """Test error handling when file does not exist."""
    non_existent_id = "999999999999"
    response = box_file_info(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== File Thumbnail URL Tests ====================


def test_box_file_thumbnail_url_png(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test retrieving thumbnail URL in PNG format."""
    file_id = file_test_data.test_files[0].id
    response = box_file_thumbnail_url(box_client_ccg, file_id, extension="png")

    assert response is not None
    assert "error" not in response
    # Response should contain either thumbnail_url or message indicating unavailability
    assert "thumbnail_url" in response or "message" in response


def test_box_file_thumbnail_url_jpg(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test retrieving thumbnail URL in JPG format."""
    file_id = file_test_data.test_files[0].id
    response = box_file_thumbnail_url(box_client_ccg, file_id, extension="jpg")

    assert response is not None
    assert "error" not in response
    assert "thumbnail_url" in response or "message" in response


def test_box_file_thumbnail_url_with_dimensions(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test retrieving thumbnail URL with specific dimensions."""
    file_id = file_test_data.test_files[0].id
    response = box_file_thumbnail_url(
        box_client_ccg, file_id, min_height=100, max_height=200
    )

    assert response is not None
    assert "error" not in response
    assert "thumbnail_url" in response or "message" in response


def test_box_file_thumbnail_url_not_found(box_client_ccg: BoxClient):
    """Test error handling when file does not exist."""
    non_existent_id = "999999999999"
    response = box_file_thumbnail_url(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== File Thumbnail Download Tests ====================


def test_box_file_thumbnail_download(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test downloading a file thumbnail."""
    file_id = file_test_data.test_files[0].id
    response = box_file_thumbnail_download(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    # Response should contain thumbnail_content or message indicating unavailability
    assert "thumbnail_content" in response or "message" in response


def test_box_file_thumbnail_download_jpg(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test downloading a file thumbnail in JPG format."""
    file_id = file_test_data.test_files[0].id
    response = box_file_thumbnail_download(box_client_ccg, file_id, extension="jpg")

    assert response is not None
    assert "error" not in response
    assert "thumbnail_content" in response or "message" in response


def test_box_file_thumbnail_download_not_found(box_client_ccg: BoxClient):
    """Test error handling when file does not exist."""
    non_existent_id = "999999999999"
    response = box_file_thumbnail_download(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== File Copy Tests ====================


def test_box_file_copy_with_new_name(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test copying a file with a new name."""
    source_file_id = file_test_data.test_files[0].id
    destination_folder_id = file_test_data.test_folder.id
    new_name = f"Copied File {uuid.uuid4()}.txt"

    response = box_file_copy(
        box_client_ccg,
        source_file_id,
        destination_folder_id,
        new_name=new_name,
    )

    assert response is not None
    assert "error" not in response
    assert "copied_file" in response
    copied_file = response["copied_file"]
    assert copied_file["name"] == new_name
    assert copied_file["parent"]["id"] == destination_folder_id

    # Cleanup
    box_client_ccg.files.delete_file_by_id(copied_file["id"])


def test_box_file_copy_default_name(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test copying a file and preserving its original name."""
    source_file_id = file_test_data.test_files[0].id
    destination_folder_id = file_test_data.test_folder.id

    response = box_file_copy(
        box_client_ccg,
        source_file_id,
        destination_folder_id,
    )

    assert response is not None
    assert "error" not in response
    assert "copied_file" in response
    copied_file = response["copied_file"]
    # Box may append a number or suffix to the copy
    assert copied_file["name"] is not None
    assert copied_file["parent"]["id"] == destination_folder_id

    # Cleanup
    box_client_ccg.files.delete_file_by_id(copied_file["id"])


def test_box_file_copy_source_not_found(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test error handling when copying a non-existent source file."""
    non_existent_id = "999999999999"
    destination_folder_id = file_test_data.test_folder.id

    response = box_file_copy(
        box_client_ccg,
        non_existent_id,
        destination_folder_id,
    )

    assert response is not None
    assert "error" in response


def test_box_file_copy_destination_not_found(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test error handling when copying to a non-existent destination folder."""
    source_file_id = file_test_data.test_files[0].id
    non_existent_dest = "999999999999"

    response = box_file_copy(
        box_client_ccg,
        source_file_id,
        non_existent_dest,
    )

    assert response is not None
    assert "error" in response


# ==================== File Move Tests ====================


def test_box_file_move_success(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test moving a file to a different folder."""
    # Create a file to move
    from pathlib import Path

    from box_sdk_gen import UploadFileAttributes, UploadFileAttributesParentField

    source_folder_id = file_test_data.test_folder.id
    test_data_path = Path(__file__).parent.joinpath("test_data").joinpath("Files")

    # Upload a test file to move
    file_to_move_path = list(test_data_path.glob("*.*"))[0]
    with file_to_move_path.open("rb") as f:
        file_name = f"{uuid.uuid4()}_{file_to_move_path.name}"
        file_attributes = UploadFileAttributes(
            name=file_name,
            parent=UploadFileAttributesParentField(id=source_folder_id),
        )
        uploaded_file = box_client_ccg.uploads.upload_file(
            attributes=file_attributes,
            file_file_name=file_name,
            file=f,
        )
        file_id = uploaded_file.entries[0].id

    # Move to the test folder (same location for this test)
    response = box_file_move(box_client_ccg, file_id, source_folder_id)

    assert response is not None
    assert "error" not in response
    assert "moved_file" in response
    moved_file = response["moved_file"]
    assert moved_file["parent"]["id"] == source_folder_id

    # Cleanup
    box_client_ccg.files.delete_file_by_id(file_id)


def test_box_file_move_not_found(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test error handling when moving a non-existent file."""
    non_existent_id = "999999999999"
    destination_folder_id = file_test_data.test_folder.id

    response = box_file_move(box_client_ccg, non_existent_id, destination_folder_id)

    assert response is not None
    assert "error" in response


def test_box_file_move_destination_not_found(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test error handling when moving to a non-existent destination."""
    non_existent_dest = "999999999999"
    file_id = file_test_data.test_files[0].id

    response = box_file_move(box_client_ccg, file_id, non_existent_dest)

    assert response is not None
    assert "error" in response


# ==================== File Delete Tests ====================


def test_box_file_delete_success(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test deleting a file."""
    # Create a file to delete
    from pathlib import Path

    from box_sdk_gen import UploadFileAttributes, UploadFileAttributesParentField

    folder_id = file_test_data.test_folder.id
    test_data_path = Path(__file__).parent.joinpath("test_data").joinpath("Files")

    file_to_delete_path = list(test_data_path.glob("*.*"))[0]
    with file_to_delete_path.open("rb") as f:
        file_name = f"{uuid.uuid4()}_{file_to_delete_path.name}"
        file_attributes = UploadFileAttributes(
            name=file_name,
            parent=UploadFileAttributesParentField(id=folder_id),
        )
        uploaded_file = box_client_ccg.uploads.upload_file(
            attributes=file_attributes,
            file_file_name=file_name,
            file=f,
        )
        file_id = uploaded_file.entries[0].id

    # Delete the file
    response = box_file_delete(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    assert "message" in response
    assert "deleted successfully" in response["message"]


def test_box_file_delete_not_found(box_client_ccg: BoxClient):
    """Test error handling when deleting a non-existent file."""
    non_existent_id = "999999999999"
    response = box_file_delete(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== File Rename Tests ====================


def test_box_file_rename_success(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test renaming a file."""
    file_id = file_test_data.test_files[0].id
    new_name = f"Renamed File {uuid.uuid4()}.txt"

    response = box_file_rename(box_client_ccg, file_id, new_name)

    assert response is not None
    assert "error" not in response
    assert "renamed_file" in response
    renamed_file = response["renamed_file"]
    assert renamed_file["name"] == new_name
    assert renamed_file["id"] == file_id


def test_box_file_rename_not_found(box_client_ccg: BoxClient):
    """Test error handling when renaming a non-existent file."""
    non_existent_id = "999999999999"
    new_name = f"New Name {uuid.uuid4()}.txt"

    response = box_file_rename(box_client_ccg, non_existent_id, new_name)

    assert response is not None
    assert "error" in response


# ==================== File Description Tests ====================


def test_box_file_set_description(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test setting a description on a file."""
    file_id = file_test_data.test_files[0].id
    description = f"Test Description {uuid.uuid4()}"

    response = box_file_set_description(box_client_ccg, file_id, description)

    assert response is not None
    assert "error" not in response
    assert "updated_file" in response
    file_info = response["updated_file"]
    assert file_info["description"] == description


def test_box_file_set_description_empty(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test clearing a file's description."""
    file_id = file_test_data.test_files[0].id

    # Set description first
    set_response = box_file_set_description(
        box_client_ccg, file_id, "Initial Description"
    )
    assert "error" not in set_response

    # Clear it
    clear_response = box_file_set_description(box_client_ccg, file_id, "")

    assert clear_response is not None
    assert "error" not in clear_response


def test_box_file_set_description_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting description on non-existent file."""
    non_existent_id = "999999999999"
    description = "This should fail"

    response = box_file_set_description(box_client_ccg, non_existent_id, description)

    assert response is not None
    assert "error" in response


# ==================== File Retention Date Tests ====================


@pytest.mark.skip(reason="No retention policies configured in test environment")
def test_box_file_retention_date_set(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test setting a retention date on a file."""
    file_id = file_test_data.test_files[0].id
    # Set retention date to 30 days from now
    retention_date = datetime.now() + timedelta(days=30)

    response = box_file_retention_date_set(box_client_ccg, file_id, retention_date)
    assert response is not None
    # assert "error" in response or "updated_file" in response


@pytest.mark.skip(reason="No retention policies configured in test environment")
def test_box_file_retention_date_clear(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test clearing a retention date on a file."""
    file_id = file_test_data.test_files[0].id
    # Set retention date first
    retention_date = datetime.now() + timedelta(days=30)
    set_response = box_file_retention_date_set(box_client_ccg, file_id, retention_date)
    assert "error" not in set_response

    # Clear it
    clear_response = box_file_retention_date_clear(box_client_ccg, file_id)

    assert clear_response is not None
    assert "error" not in clear_response


def test_box_file_retention_date_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting retention date on non-existent file."""
    non_existent_id = "999999999999"
    retention_date = datetime.now() + timedelta(days=30)

    response = box_file_retention_date_set(
        box_client_ccg, non_existent_id, retention_date
    )
    assert response is not None
    assert "error" in response


def test_box_file_retention_date_clear_not_found(box_client_ccg: BoxClient):
    """Test error handling when clearing retention date on non-existent file."""
    non_existent_id = "999999999999"

    response = box_file_retention_date_clear(box_client_ccg, non_existent_id)
    assert response is not None
    assert "error" in response


# ==================== File Lock/Unlock Tests ====================


def test_box_file_lock_success(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test locking a file."""
    file_id = file_test_data.test_files[0].id

    response = box_file_lock(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    assert "locked_file" in response
    locked_file = response["locked_file"]
    assert locked_file["id"] == file_id

    # Unlock for cleanup
    box_file_unlock(box_client_ccg, file_id)


def test_box_file_lock_with_download_prevention(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test locking a file with download prevention."""
    file_id = file_test_data.test_files[0].id

    response = box_file_lock(box_client_ccg, file_id, is_download_prevented=True)

    assert response is not None
    assert "error" not in response
    assert "locked_file" in response
    locked_file = response["locked_file"]
    assert locked_file["id"] == file_id

    # Unlock for cleanup
    box_file_unlock(box_client_ccg, file_id)


def test_box_file_lock_not_found(box_client_ccg: BoxClient):
    """Test error handling when locking a non-existent file."""
    non_existent_id = "999999999999"
    response = box_file_lock(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


def test_box_file_unlock_success(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test unlocking a file."""
    file_id = file_test_data.test_files[0].id

    # Lock first
    box_file_lock(box_client_ccg, file_id)

    # Unlock
    response = box_file_unlock(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    assert "unlocked_file" in response


def test_box_file_unlock_not_found(box_client_ccg: BoxClient):
    """Test error handling when unlocking a non-existent file."""
    non_existent_id = "999999999999"
    response = box_file_unlock(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== File Download Permission Tests ====================


def test_box_file_set_download_open(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test setting file download permissions to open."""
    file_id = file_test_data.test_files[0].id

    response = box_file_set_download_open(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    assert "updated_file" in response


def test_box_file_set_download_company(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test setting file download permissions to company."""
    file_id = file_test_data.test_files[0].id

    response = box_file_set_download_company(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    assert "updated_file" in response


def test_box_file_set_download_reset(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test resetting file download permissions."""
    file_id = file_test_data.test_files[0].id

    response = box_file_set_download_reset(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    assert "updated_file" in response


def test_box_file_set_download_open_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting download permissions on non-existent file."""
    non_existent_id = "999999999999"

    response = box_file_set_download_open(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


def test_box_file_set_download_company_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting download permissions on non-existent file."""
    non_existent_id = "999999999999"

    response = box_file_set_download_company(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


def test_box_file_set_download_reset_not_found(box_client_ccg: BoxClient):
    """Test error handling when setting download permissions on non-existent file."""
    non_existent_id = "999999999999"

    response = box_file_set_download_reset(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response


# ==================== File Tag Tests ====================


def test_box_file_tag_add_single(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test adding a single tag to a file."""
    file_id = file_test_data.test_files[0].id
    tag = "test-tag"

    response = box_file_tag_add(box_client_ccg, file_id, tag)

    assert response is not None
    assert "updated_file" in response
    assert "tags" in response["updated_file"]
    assert "test-tag" in response["updated_file"]["tags"]


def test_box_file_tag_add_multiple(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test adding multiple tags to a file."""
    file_id = file_test_data.test_files[1].id  # Use different file
    tag1 = "tag-one"
    tag2 = "tag-two"

    # Add first tag
    response1 = box_file_tag_add(box_client_ccg, file_id, tag1)
    assert response1 is not None
    assert "updated_file" in response1
    assert "tags" in response1["updated_file"]
    assert "tag-one" in response1["updated_file"]["tags"]

    # Add second tag
    response2 = box_file_tag_add(box_client_ccg, file_id, tag2)
    assert response2 is not None
    assert "updated_file" in response2
    assert "tags" in response2["updated_file"]
    assert "tag-two" in response2["updated_file"]["tags"]
    assert "tag-one" in response2["updated_file"]["tags"]


def test_box_file_tag_list(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test listing tags on a file."""
    file_id = file_test_data.test_files[0].id
    tag = "test-tag"

    response = box_file_tag_add(box_client_ccg, file_id, tag)

    assert response is not None
    assert "updated_file" in response
    assert "tags" in response["updated_file"]
    assert "test-tag" in response["updated_file"]["tags"]

    response = box_file_tag_list(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    assert "tags" in response
    assert "test-tag" in response["tags"]


def test_box_file_tag_list_empty(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test listing tags on a file with no tags."""
    # Use a file that likely has no tags
    file_id = file_test_data.test_files[-1].id  # Get the last file

    response = box_file_tag_list(box_client_ccg, file_id)

    assert response is not None
    assert "error" not in response
    # Should have either tags list or a message
    assert "tags" in response or "message" in response


def test_box_file_tag_remove(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test removing a tag from a file."""
    file_id = file_test_data.test_files[2].id  # Use different file
    tag = "tag-to-remove"

    # Add tag first
    add_response = box_file_tag_add(box_client_ccg, file_id, tag)
    assert add_response is not None
    assert "updated_file" in add_response
    assert "tags" in add_response["updated_file"]
    assert "tag-to-remove" in add_response["updated_file"]["tags"]

    remove_response = box_file_tag_remove(box_client_ccg, file_id, tag)

    assert remove_response is not None
    assert "error" not in remove_response
    assert "updated_file" in remove_response


def test_box_file_tag_add_not_found(box_client_ccg: BoxClient):
    """Test error handling when adding tag to non-existent file."""
    non_existent_id = "999999999999"
    tag = f"test-tag-{uuid.uuid4()}"

    response = box_file_tag_add(box_client_ccg, non_existent_id, tag)

    assert response is not None
    assert "error" in response


def test_box_file_tag_remove_not_found(box_client_ccg: BoxClient):
    """Test error handling when removing tag from non-existent file."""
    non_existent_id = "999999999999"
    tag = f"test-tag-{uuid.uuid4()}"

    response = box_file_tag_remove(box_client_ccg, non_existent_id, tag)

    assert response is not None
    assert "error" in response


def test_box_file_tag_list_not_found(box_client_ccg: BoxClient):
    """Test error handling when listing tags on non-existent file."""
    non_existent_id = "999999999999"

    response = box_file_tag_list(box_client_ccg, non_existent_id)

    assert response is not None
    assert "error" in response
