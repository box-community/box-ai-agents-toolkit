from box_ai_agents_toolkit import (
    box_shared_link_file_get,
    box_shared_link_file_create_or_update,
    box_shared_link_file_remove,
    box_shared_link_file_find_by_shared_link_url,
    box_shared_link_folder_create_or_update,
    box_shared_link_folder_get,
    box_shared_link_folder_remove,
    box_shared_link_folder_find_by_shared_link_url,
    box_shared_link_web_link_create_or_update,
    box_shared_link_web_link_get,
    box_shared_link_web_link_remove,
    box_shared_link_web_link_find_by_shared_link_url,
)
from box_sdk_gen import (
    BoxClient,
    Folder,
    WebLink,
    CreateWebLinkParent,
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
    response = box_shared_link_file_create_or_update(
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
    response = box_shared_link_file_create_or_update(
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
    response = box_shared_link_file_create_or_update(
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
    create_response = box_shared_link_file_create_or_update(
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
    create_response = box_shared_link_file_create_or_update(
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


@pytest.mark.order(index=70)
def test_box_shared_link_file_find_by_shared_link_url(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test file to work with
    assert shared_link_test_files.test_files is not None
    assert len(shared_link_test_files.test_files) > 0

    test_file = shared_link_test_files.test_files[0]
    file_id = test_file.id
    assert file_id is not None

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_file_create_or_update(
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
    assert "url" in shared_link

    shared_link_url = shared_link.get("url")
    assert shared_link_url is not None

    # Now, find the file by the shared link URL using the function under test
    find_response = box_shared_link_file_find_by_shared_link_url(
        client=box_client_ccg, shared_link_url=shared_link_url, password=None
    )
    find_error = find_response.get("error")
    find_message = find_response.get("message")
    found_file = find_response.get("file")

    assert find_error is None
    assert find_message is None
    assert found_file is not None
    assert isinstance(found_file, dict)
    assert found_file.get("id") == file_id
    assert found_file.get("name") == test_file.name

    # Clean up by removing the shared link
    fields = "shared_link"
    box_client_ccg.shared_links_files.remove_shared_link_from_file(
        file_id=file_id,
        fields=fields,
    )

    # test with invalid shared link URL
    find_response_no_link = box_shared_link_file_find_by_shared_link_url(
        client=box_client_ccg,
        shared_link_url="https://box.com/s/invalid",
        password=None,
    )
    find_error = find_response_no_link.get("error")
    find_message = find_response_no_link.get("message")
    found_file = find_response_no_link.get("file")

    assert find_error is not None
    assert "404 Not Found" in find_error
    assert find_message is None
    assert found_file is None


@pytest.mark.order(index=80)
def test_box_shared_link_file_find_by_shared_link_url_with_password(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test file to work with
    assert shared_link_test_files.test_files is not None
    assert len(shared_link_test_files.test_files) > 0

    test_file = shared_link_test_files.test_files[0]
    file_id = test_file.id
    assert file_id is not None

    password = "TestPassword123!"

    # First, create a shared link with a password to ensure one exists
    create_response = box_shared_link_file_create_or_update(
        client=box_client_ccg,
        file_id=file_id,
        access="open",
        can_download=True,
        can_preview=True,
        can_edit=False,
        password=password,
        vanity_name=None,
        unshared_at=None,
    )
    create_error = create_response.get("error")
    message = create_response.get("message")
    shared_link = create_response.get("shared_link")

    assert create_error is None
    assert message is None
    assert shared_link is not None
    assert "url" in shared_link

    shared_link_url = shared_link.get("url")
    assert shared_link_url is not None

    # Now, find the file by the shared link URL and correct password using the function under test
    find_response = box_shared_link_file_find_by_shared_link_url(
        client=box_client_ccg, shared_link_url=shared_link_url, password=password
    )
    find_error = find_response.get("error")
    find_message = find_response.get("message")
    found_file = find_response.get("file")

    assert find_error is None
    assert find_message is None
    assert found_file is not None
    assert isinstance(found_file, dict)
    assert found_file.get("id") == file_id
    assert found_file.get("name") == test_file.name


@pytest.mark.order(index=110)
def test_box_shared_link_folder_get_no_shared_link(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert shared_link_test_files.test_folder is not None

    test_folder = shared_link_test_files.test_folder
    folder_id = test_folder.id
    assert folder_id is not None

    # First, ensure there is no shared link
    response = box_shared_link_folder_get(client=box_client_ccg, folder_id=folder_id)

    error = response.get("error")
    message = response.get("message")
    shared_link = response.get("shared_link")

    assert error is None
    assert message is not None
    assert message == "No shared link found for this folder."

    assert shared_link is None

    # Get from a non-existent folder
    response = box_shared_link_folder_get(client=box_client_ccg, folder_id="invalid_id")
    error = response.get("error")
    message = response.get("message")
    shared_link = response.get("shared_link")

    assert error is not None
    assert message is None
    assert shared_link is None


@pytest.mark.order(index=120)
def test_box_shared_link_folder_create(
    box_client_ccg: BoxClient,
    shared_link_test_files: TestData,
):
    # Ensure we have a test folder to work with
    assert shared_link_test_files.test_folder is not None
    test_folder = shared_link_test_files.test_folder
    folder_id = test_folder.id
    assert folder_id is not None

    # Create a shared link
    response = box_shared_link_folder_create_or_update(
        client=box_client_ccg,
        folder_id=folder_id,
        access="company",
        can_download=True,
        can_preview=True,
        can_edit=False,
        password=None,
        vanity_name=None,
        unshared_at=None,
    )

    error = response.get("error")
    message = response.get("message")
    shared_link = response.get("shared_link")

    assert error is None
    assert message is None
    assert shared_link is not None
    assert isinstance(shared_link, dict)
    assert "url" in shared_link

    permissions = shared_link.get("permissions")
    assert permissions is not None
    assert isinstance(permissions, dict)
    assert permissions.get("can_download") is True
    assert permissions.get("can_preview") is True
    assert permissions.get("can_edit") is False

    # Remove shared link
    fields = "shared_link"
    box_client_ccg.shared_links_folders.remove_shared_link_from_folder(
        folder_id=folder_id,
        fields=fields,
    )


@pytest.mark.order(index=140)
def test_box_shared_link_folder_create_with_errors(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert shared_link_test_files.test_folder is not None
    test_folder = shared_link_test_files.test_folder
    folder_id = test_folder.id
    assert folder_id is not None

    # Test with invalid access level
    response = box_shared_link_folder_create_or_update(
        client=box_client_ccg,
        folder_id=folder_id,
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

    # Test with invalid folder ID
    response = box_shared_link_folder_create_or_update(
        client=box_client_ccg,
        folder_id="invalid_folder_id",  # Invalid folder ID
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


@pytest.mark.order(index=150)
def test_box_shared_link_folder_get_existing_shared_link(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert shared_link_test_files.test_folder is not None

    test_folder = shared_link_test_files.test_folder
    folder_id = test_folder.id
    assert folder_id is not None

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_folder_create_or_update(
        client=box_client_ccg,
        folder_id=folder_id,
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
    get_response = box_shared_link_folder_get(
        client=box_client_ccg, folder_id=folder_id
    )
    get_error = get_response.get("error")
    get_message = get_response.get("message")
    get_shared_link = get_response.get("shared_link")

    assert get_error is None
    assert get_message is None
    assert get_shared_link is not None
    assert get_shared_link == shared_link

    # Clean up by removing the shared link
    fields = "shared_link"
    box_client_ccg.shared_links_folders.remove_shared_link_from_folder(
        folder_id=folder_id,
        fields=fields,
    )


@pytest.mark.order(index=160)
def test_box_shared_link_folder_remove(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert shared_link_test_files.test_folder is not None

    test_folder = shared_link_test_files.test_folder
    folder_id = test_folder.id
    assert folder_id is not None

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_folder_create_or_update(
        client=box_client_ccg,
        folder_id=folder_id,
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
    remove_response = box_shared_link_folder_remove(
        client=box_client_ccg, folder_id=folder_id
    )
    remove_error = remove_response.get("error")
    remove_message = remove_response.get("message")

    assert remove_error is None
    assert remove_message == "Shared link removed successfully."

    # Verify the shared link has been removed
    get_response = box_shared_link_folder_get(
        client=box_client_ccg, folder_id=folder_id
    )
    get_error = get_response.get("error")
    get_message = get_response.get("message")
    get_shared_link = get_response.get("shared_link")

    assert get_error is None
    assert get_shared_link is None
    assert get_message == "No shared link found for this folder."

    # Test removing shared link from a folder with no shared link return no error or message
    remove_response = box_shared_link_folder_remove(
        client=box_client_ccg, folder_id=folder_id
    )

    remove_error = remove_response.get("error")
    remove_message = remove_response.get("message")
    remove_shared_link = remove_response.get("shared_link")

    assert remove_error is None
    assert remove_shared_link is None
    assert remove_message is not None
    assert remove_message == "Shared link removed successfully."

    # Test removing shared link from a non-existent folder
    remove_response_error = box_shared_link_folder_remove(
        client=box_client_ccg, folder_id="invalid_id"
    )
    remove_error = remove_response_error.get("error")
    remove_message = remove_response_error.get("message")
    remove_shared_link = remove_response_error.get("shared_link")

    assert remove_error is not None
    assert "405 Method Not Allowed" in remove_error
    assert remove_message is None
    assert remove_shared_link is None


@pytest.mark.order(index=170)
def test_box_shared_link_folder_find_by_shared_link_url(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert shared_link_test_files.test_folder is not None

    test_folder = shared_link_test_files.test_folder
    folder_id = test_folder.id
    assert folder_id is not None

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_folder_create_or_update(
        client=box_client_ccg,
        folder_id=folder_id,
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
    assert "url" in shared_link

    shared_link_url = shared_link.get("url")
    assert shared_link_url is not None

    # Now, find the folder by the shared link URL using the function under test
    find_response = box_shared_link_folder_find_by_shared_link_url(
        client=box_client_ccg, shared_link_url=shared_link_url, password=None
    )
    find_error = find_response.get("error")
    find_message = find_response.get("message")
    found_folder = find_response.get("folder")

    assert find_error is None
    assert find_message is None
    assert found_folder is not None
    assert isinstance(found_folder, dict)
    assert found_folder.get("id") == folder_id
    assert found_folder.get("name") == test_folder.name

    # Clean up by removing the shared link
    fields = "shared_link"
    box_client_ccg.shared_links_folders.remove_shared_link_from_folder(
        folder_id=folder_id,
        fields=fields,
    )

    # test with invalid shared link URL
    find_response_no_link = box_shared_link_folder_find_by_shared_link_url(
        client=box_client_ccg,
        shared_link_url="https://box.com/s/invalid",
        password=None,
    )
    find_error = find_response_no_link.get("error")
    find_message = find_response_no_link.get("message")
    found_folder = find_response_no_link.get("folder")

    assert find_error is not None
    assert "404 Not Found" in find_error
    assert find_message is None
    assert found_folder is None


@pytest.mark.order(index=180)
def test_box_shared_link_folder_find_by_shared_link_url_with_password(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert shared_link_test_files.test_folder is not None

    test_folder = shared_link_test_files.test_folder
    folder_id = test_folder.id
    assert folder_id is not None

    password = "TestPassword123!"

    # First, create a shared link with a password to ensure one exists
    create_response = box_shared_link_folder_create_or_update(
        client=box_client_ccg,
        folder_id=folder_id,
        access="open",
        can_download=True,
        can_preview=True,
        can_edit=False,
        password=password,
        vanity_name=None,
        unshared_at=None,
    )
    create_error = create_response.get("error")
    message = create_response.get("message")
    shared_link = create_response.get("shared_link")

    assert create_error is None
    assert message is None
    assert shared_link is not None
    assert "url" in shared_link

    shared_link_url = shared_link.get("url")
    assert shared_link_url is not None

    # Now, find the folder by the shared link URL and correct password using the function under test
    find_response = box_shared_link_folder_find_by_shared_link_url(
        client=box_client_ccg, shared_link_url=shared_link_url, password=password
    )
    find_error = find_response.get("error")
    find_message = find_response.get("message")
    found_folder = find_response.get("folder")

    assert find_error is None
    assert find_message is None
    assert found_folder is not None
    assert isinstance(found_folder, dict)
    assert found_folder.get("id") == folder_id
    assert found_folder.get("name") == test_folder.name


def _create_test_web_link(
    client: BoxClient, parent_folder: Folder, url: str
) -> WebLink:
    parent_folder_id = parent_folder.id

    return client.web_links.create_web_link(
        url=url,
        parent=CreateWebLinkParent(id=parent_folder_id),
    )


@pytest.mark.order(index=210)
def test_box_shared_link_web_link_get_no_shared_link(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # create a test web link
    test_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=shared_link_test_files.test_folder,
        url="https://www.box-share.com",
    )
    assert test_web_link is not None
    assert test_web_link.id is not None
    web_link_id = test_web_link.id

    # get the shared link for this web link - should be none
    response = box_shared_link_web_link_get(
        client=box_client_ccg, web_link_id=web_link_id
    )

    error = response.get("error")
    message = response.get("message")
    shared_link = response.get("shared_link")

    assert error is None
    assert message is not None
    assert shared_link is None

    assert message == "No shared link found for this web link."


@pytest.mark.order(index=220)
def test_box_shared_link_web_link_create(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # create a test web link
    test_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=shared_link_test_files.test_folder,
        url="https://www.box-share-weblink-create.com",
    )
    assert test_web_link is not None
    assert test_web_link.id is not None
    web_link_id = test_web_link.id

    # Create a shared link
    response = box_shared_link_web_link_create_or_update(
        client=box_client_ccg,
        web_link_id=web_link_id,
        access="company",
        password=None,
        vanity_name=None,
        unshared_at=None,
    )

    error = response.get("error")
    message = response.get("message")
    shared_link = response.get("shared_link")

    assert error is None
    assert message is None
    assert shared_link is not None
    assert isinstance(shared_link, dict)

    assert "url" in shared_link
    # assert "download_url" in shared_link
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

    # delete web link
    box_client_ccg.web_links.delete_web_link_by_id(web_link_id=web_link_id)


@pytest.mark.order(index=240)
def test_box_shared_link_web_link_create_with_errors(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # create a test web link
    test_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=shared_link_test_files.test_folder,
        url="https://www.box-share-weblink-create-error.com",
    )
    assert test_web_link is not None
    assert test_web_link.id is not None
    web_link_id = test_web_link.id

    # Test with invalid access level
    response = box_shared_link_web_link_create_or_update(
        client=box_client_ccg,
        web_link_id=web_link_id,
        access="invalid_access",  # Invalid access level
        password=None,
        vanity_name=None,
        unshared_at=None,
    )

    error = response.get("error")
    shared_link = response.get("shared_link")

    assert error is not None
    assert "Invalid access" in error
    assert shared_link is None

    # Test with invalid web link ID
    response = box_shared_link_web_link_create_or_update(
        client=box_client_ccg,
        web_link_id="invalid_web_link_id",  # Invalid web link ID
        access="company",
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

    # delete web link
    box_client_ccg.web_links.delete_web_link_by_id(web_link_id=web_link_id)


@pytest.mark.order(index=250)
def test_box_shared_link_web_link_get_existing_shared_link(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # create a test web link
    test_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=shared_link_test_files.test_folder,
        url="https://www.box-share-weblink-get.com",
    )
    assert test_web_link is not None
    assert test_web_link.id is not None
    web_link_id = test_web_link.id

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_web_link_create_or_update(
        client=box_client_ccg,
        web_link_id=web_link_id,
        access="company",
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
    get_response = box_shared_link_web_link_get(
        client=box_client_ccg, web_link_id=web_link_id
    )
    get_error = get_response.get("error")
    get_message = get_response.get("message")
    get_shared_link = get_response.get("shared_link")

    assert get_error is None
    assert get_message is None
    assert get_shared_link is not None
    assert get_shared_link == shared_link

    # Clean up by deleting the web link
    box_client_ccg.web_links.delete_web_link_by_id(web_link_id=web_link_id)


@pytest.mark.order(index=260)
def test_box_shared_link_web_link_remove(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # create a test web link
    test_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=shared_link_test_files.test_folder,
        url="https://www.box-share-weblink-remove.com",
    )
    assert test_web_link is not None
    assert test_web_link.id is not None
    web_link_id = test_web_link.id

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_web_link_create_or_update(
        client=box_client_ccg,
        web_link_id=web_link_id,
        access="company",
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
    remove_response = box_shared_link_web_link_remove(
        client=box_client_ccg, web_link_id=web_link_id
    )
    remove_error = remove_response.get("error")
    remove_message = remove_response.get("message")

    assert remove_error is None
    assert remove_message == "Shared link removed successfully."

    # Verify the shared link has been removed
    get_response = box_shared_link_web_link_get(
        client=box_client_ccg, web_link_id=web_link_id
    )
    get_error = get_response.get("error")
    get_message = get_response.get("message")
    get_shared_link = get_response.get("shared_link")

    assert get_error is None
    assert get_shared_link is None
    assert get_message == "No shared link found for this web link."

    # Test removing shared link from a web link with no shared link return no error or message
    remove_response = box_shared_link_web_link_remove(
        client=box_client_ccg, web_link_id=web_link_id
    )

    remove_error = remove_response.get("error")
    remove_message = remove_response.get("message")
    remove_shared_link = remove_response.get("shared_link")

    assert remove_error is None
    assert remove_shared_link is None
    assert remove_message is not None
    assert remove_message == "Shared link removed successfully."

    # Test removing shared link from a non-existent web link
    remove_response_error = box_shared_link_web_link_remove(
        client=box_client_ccg, web_link_id="invalid_id"
    )
    remove_error = remove_response_error.get("error")
    remove_message = remove_response_error.get("message")
    remove_shared_link = remove_response_error.get("shared_link")

    assert remove_error is not None
    assert "405 Method Not Allowed" in remove_error
    assert remove_message is None
    assert remove_shared_link is None


@pytest.mark.order(index=270)
def test_box_shared_link_web_link_find_by_shared_link_url(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # create a test web link
    test_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=shared_link_test_files.test_folder,
        url="https://www.box-share-weblink-find.com",
    )
    assert test_web_link is not None
    assert test_web_link.id is not None
    web_link_id = test_web_link.id

    # First, create a shared link to ensure one exists
    create_response = box_shared_link_web_link_create_or_update(
        client=box_client_ccg,
        web_link_id=web_link_id,
        access="company",
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
    assert "url" in shared_link

    shared_link_url = shared_link.get("url")
    assert shared_link_url is not None

    # Now, find the web link by the shared link URL using the function under test
    find_response = box_shared_link_web_link_find_by_shared_link_url(
        client=box_client_ccg, shared_link_url=shared_link_url, password=None
    )
    find_error = find_response.get("error")
    find_message = find_response.get("message")
    found_web_link = find_response.get("web_link")

    assert find_error is None
    assert find_message is None
    assert found_web_link is not None
    assert isinstance(found_web_link, dict)
    assert found_web_link.get("id") == web_link_id
    assert found_web_link.get("name") == test_web_link.name

    # Clean up by deleting the web link
    box_client_ccg.web_links.delete_web_link_by_id(web_link_id=web_link_id)

    # test with invalid shared link URL
    find_response_no_link = box_shared_link_web_link_find_by_shared_link_url(
        client=box_client_ccg,
        shared_link_url="https://box.com/s/invalid",
        password=None,
    )
    find_error = find_response_no_link.get("error")
    find_message = find_response_no_link.get("message")
    found_web_link = find_response_no_link.get("web_link")

    assert find_error is not None
    assert "404 Not Found" in find_error
    assert find_message is None
    assert found_web_link is None


@pytest.mark.order(index=280)
def test_box_shared_link_web_link_find_by_shared_link_url_with_password(
    box_client_ccg: BoxClient, shared_link_test_files: TestData
):
    # create a test web link
    test_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=shared_link_test_files.test_folder,
        url="https://www.box-share-weblink-find-password.com",
    )
    assert test_web_link is not None
    assert test_web_link.id is not None
    web_link_id = test_web_link.id

    password = "TestPassword123!"

    # First, create a shared link with a password to ensure one exists
    create_response = box_shared_link_web_link_create_or_update(
        client=box_client_ccg,
        web_link_id=web_link_id,
        access="open",
        password=password,
        vanity_name=None,
        unshared_at=None,
    )
    create_error = create_response.get("error")
    message = create_response.get("message")
    shared_link = create_response.get("shared_link")

    assert create_error is None
    assert message is None
    assert shared_link is not None
    assert "url" in shared_link

    shared_link_url = shared_link.get("url")
    assert shared_link_url is not None

    # Now, find the web link by the shared link URL and correct password using the function under test
    find_response = box_shared_link_web_link_find_by_shared_link_url(
        client=box_client_ccg, shared_link_url=shared_link_url, password=password
    )
    find_error = find_response.get("error")
    find_message = find_response.get("message")
    found_web_link = find_response.get("web_link")

    assert find_error is None
    assert find_message is None
    assert found_web_link is not None
    assert isinstance(found_web_link, dict)
    assert found_web_link.get("id") == web_link_id
    assert found_web_link.get("name") == test_web_link.name

    # Clean up by deleting the web link
    box_client_ccg.web_links.delete_web_link_by_id(web_link_id=web_link_id)
