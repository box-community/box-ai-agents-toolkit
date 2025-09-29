from box_ai_agents_toolkit import (
    box_shared_link_file_get,
    box_shared_link_file_create,
    box_shared_link_file_remove,
)
from box_sdk_gen import (
    BoxClient,
)
from .conftest import TestData
import pytest


@pytest.mark.order(index=10)
def test_box_shared_link_file_get_no_shared_link(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test file to work with
    assert shared_link_test_files.test_files is not None
    assert len(shared_link_test_files.test_files) > 0

    test_file = shared_link_test_files.test_files[0]
    file_id = test_file.id
    assert file_id is not None

    # First, ensure there is no shared link
    response = box_shared_link_file_get(client=box_client_ccg, file_id=file_id)

    error = response.get("error")
    message = response.get("message")
    shared_link = response.get("shared_link")

    assert error is None
    assert message is not None
    assert message == "No shared link found for this file."

    assert shared_link is None

    # Get from a non-existent file
    response = box_shared_link_file_get(client=box_client_ccg, file_id="invalid_id")
    error = response.get("error")
    message = response.get("message")
    shared_link = response.get("shared_link")

    assert error is not None
    assert message is None
    assert shared_link is None


@pytest.mark.order(index=20)
def test_box_shared_link_file_create(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test file to work with
    assert shared_link_test_files.test_files is not None
    assert len(shared_link_test_files.test_files) > 0

    test_file = shared_link_test_files.test_files[0]
    file_id = test_file.id
    assert file_id is not None

    # Create a shared link
    response = box_shared_link_file_create(
        client=box_client_ccg,
        file_id=file_id,
        access="company",
        can_download=True,
        can_preview=True,
        can_edit=False,
        password=None,
        vanity_name=None,
        unshared_at=None,
    )

    error = response.get("error")
    shared_link = response.get("shared_link")

    assert error is None
    assert shared_link is not None
    assert isinstance(shared_link, dict)
    assert "url" in shared_link
    assert "download_url" in shared_link
    # assert "vanity_url" in shared_link
    # assert "is_password_enabled" in shared_link
    # assert "unshared_at" in shared_link
    # assert "permissions" in shared_link

    permissions = shared_link.get("permissions")
    assert permissions is not None
    assert isinstance(permissions, dict)
    assert permissions.get("can_download") is True
    assert permissions.get("can_preview") is True
    assert permissions.get("can_edit") is False

    # Remove shared link
    fields = "shared_link"
    box_client_ccg.shared_links_files.remove_shared_link_from_file(
        file_id=file_id,
        fields=fields,
    )


@pytest.mark.order(index=40)
def test_box_shared_link_file_create_with_errors(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test file to work with
    assert shared_link_test_files.test_files is not None
    assert len(shared_link_test_files.test_files) > 0

    test_file = shared_link_test_files.test_files[0]
    file_id = test_file.id
    assert file_id is not None

    # Test with invalid access level
    response = box_shared_link_file_create(
        client=box_client_ccg,
        file_id=file_id,
        access="invalid_access",  # Invalid access level
        can_download=True,
        can_preview=True,
        can_edit=False,
        password=None,
        vanity_name=None,
        unshared_at=None,
    )

    error = response.get("error")
    shared_link = response.get("shared_link")

    assert error is not None
    assert "Invalid access" in error
    assert shared_link is None

    # Test with invalid file ID
    response = box_shared_link_file_create(
        client=box_client_ccg,
        file_id="invalid_file_id",  # Invalid file ID
        access="company",
        can_download=True,
        can_preview=True,
        can_edit=False,
        password=None,
        vanity_name=None,
        unshared_at=None,
    )

    error = response.get("error")
    shared_link = response.get("shared_link")

    assert error is not None
    # why is the API returning a 405 here? Should be a 404 not found
    assert "405 Method Not Allowed" in error
    assert shared_link is None


@pytest.mark.order(index=50)
def test_box_shared_link_file_get_existing_shared_link(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test file to work with
    assert shared_link_test_files.test_files is not None
    assert len(shared_link_test_files.test_files) > 0
    test_file = shared_link_test_files.test_files[0]
    file_id = test_file.id
    assert file_id is not None

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_file_create(
        client=box_client_ccg,
        file_id=file_id,
        access="company",
        can_download=True,
        can_preview=True,
        can_edit=False,
        password=None,
        vanity_name=None,
        unshared_at=None,
    )
    create_error = create_response.get("error")
    message = create_response.get("message")
    shared_link = create_response.get("shared_link")

    assert create_error is None
    assert message is None
    assert shared_link is not None

    # Get the shared link
    get_response = box_shared_link_file_get(client=box_client_ccg, file_id=file_id)
    get_error = get_response.get("error")
    get_message = get_response.get("message")
    get_shared_link = get_response.get("shared_link")

    assert get_error is None
    assert get_message is None
    assert get_shared_link is not None
    assert get_shared_link == shared_link

    # Clean up by removing the shared link
    fields = "shared_link"
    box_client_ccg.shared_links_files.remove_shared_link_from_file(
        file_id=file_id,
        fields=fields,
    )


@pytest.mark.order(index=60)
def test_box_shared_link_file_remove(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test file to work with
    assert shared_link_test_files.test_files is not None
    assert len(shared_link_test_files.test_files) > 0

    test_file = shared_link_test_files.test_files[0]
    file_id = test_file.id
    assert file_id is not None

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_file_create(
        client=box_client_ccg,
        file_id=file_id,
        access="company",
        can_download=True,
        can_preview=True,
        can_edit=False,
        password=None,
        vanity_name=None,
        unshared_at=None,
    )
    create_error = create_response.get("error")
    message = create_response.get("message")
    shared_link = create_response.get("shared_link")

    assert create_error is None
    assert message is None
    assert shared_link is not None

    # Now, remove the shared link using the function under test
    remove_response = box_shared_link_file_remove(
        client=box_client_ccg, file_id=file_id
    )
    remove_error = remove_response.get("error")
    remove_message = remove_response.get("message")

    assert remove_error is None
    assert remove_message == "Shared link removed successfully."

    # Verify the shared link has been removed
    get_response = box_shared_link_file_get(client=box_client_ccg, file_id=file_id)
    get_error = get_response.get("error")
    get_message = get_response.get("message")
    get_shared_link = get_response.get("shared_link")

    assert get_error is None
    assert get_shared_link is None
    assert get_message == "No shared link found for this file."

    # Test removing shared link from a file with no shared link return no error or message
    remove_response = box_shared_link_file_remove(
        client=box_client_ccg, file_id=file_id
    )

    remove_error = remove_response.get("error")
    remove_message = remove_response.get("message")
    remove_shared_link = remove_response.get("shared_link")

    assert remove_error is None
    assert remove_shared_link is None
    assert remove_message is not None
    assert remove_message == "Shared link removed successfully."

    # Test removing shared link from a non-existent file
    remove_response_error = box_shared_link_file_remove(
        client=box_client_ccg, file_id="invalid_id"
    )
    remove_error = remove_response_error.get("error")
    remove_message = remove_response_error.get("message")
    remove_shared_link = remove_response_error.get("shared_link")

    assert remove_error is not None
    assert "405 Method Not Allowed" in remove_error
    assert remove_message is None
    assert remove_shared_link is None


#
