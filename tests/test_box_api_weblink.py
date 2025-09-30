from box_ai_agents_toolkit import (
    box_web_link_create,
    box_web_link_get_by_id,
    box_web_link_update_by_id,
    box_web_link_delete_by_id,
)
from box_sdk_gen import (
    BoxClient,
    Folder,
    WebLink,
    CreateWebLinkParent,
)
from .conftest import TestData


def _create_test_web_link(
    client: BoxClient, parent_folder: Folder, url: str
) -> WebLink:
    parent_folder_id = parent_folder.id

    return client.web_links.create_web_link(
        url=url,
        parent=CreateWebLinkParent(id=parent_folder_id),
    )


def test_box_web_link_create(box_client_ccg: BoxClient, web_link_test_data: TestData):
    url = "https://www.example.com"

    # make sure the folder exists
    assert web_link_test_data.test_folder is not None
    assert web_link_test_data.test_folder.id is not None

    parent_folder_id = web_link_test_data.test_folder.id
    name = "Example Web Link"
    description = "A link to example.com"

    result = box_web_link_create(
        client=box_client_ccg,
        url=url,
        parent_folder_id=parent_folder_id,
        name=name,
        description=description,
    )

    error = result.get("error")
    message = result.get("message")
    web_link = result.get("web_link")

    assert error is None
    assert message is None
    assert web_link is not None
    assert isinstance(web_link, dict)
    assert web_link.get("url") == url
    assert web_link.get("name") == name
    assert web_link.get("description") == description

    # Clean up by deleting the created web link
    box_client_ccg.web_links.delete_web_link_by_id(web_link["id"])


def test_box_web_link_create_with_error(
    box_client_ccg: BoxClient,
):
    url = "https://www.example.com"
    name = "Example Web Link"
    description = "A link to example.com"

    # create with an error (invalid parent folder id)
    result = box_web_link_create(
        client=box_client_ccg,
        url=url,
        parent_folder_id="1234",  # invalid folder id
        name=name,
        description=description,
    )

    error = result.get("error")
    message = result.get("message")
    web_link = result.get("web_link")

    assert error is not None
    assert message is None
    assert web_link is None


def test_box_web_link_get_by_id(
    box_client_ccg: BoxClient, web_link_test_data: TestData
):
    existing_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=web_link_test_data.test_folder,
        url="https://www.box.com",
    )

    web_link_id = existing_web_link.id

    result = box_web_link_get_by_id(
        client=box_client_ccg,
        web_link_id=web_link_id,
    )

    error = result.get("error")
    message = result.get("message")
    web_link = result.get("web_link")

    assert error is None
    assert message is None
    assert web_link is not None
    assert isinstance(web_link, dict)
    assert web_link.get("id") == existing_web_link.id
    assert web_link.get("url") == existing_web_link.url

    # Clean up by deleting the created web link
    box_client_ccg.web_links.delete_web_link_by_id(web_link_id)


def test_box_web_link_get_by_id_with_error(
    box_client_ccg: BoxClient, web_link_test_data: TestData
):
    web_link_id = "1234"  # invalid web link id

    result = box_web_link_get_by_id(
        client=box_client_ccg,
        web_link_id=web_link_id,
    )

    error = result.get("error")
    message = result.get("message")
    web_link = result.get("web_link")

    assert error is not None
    assert message is None
    assert web_link is None


def test_box_web_link_update_by_id(
    box_client_ccg: BoxClient, web_link_test_data: TestData
):
    existing_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=web_link_test_data.test_folder,
        url="https://www.box-old.com",
    )

    web_link_id = existing_web_link.id
    new_url = "https://www.box-new.com"
    new_name = "Updated Web Link"
    new_description = "An updated description"

    result = box_web_link_update_by_id(
        client=box_client_ccg,
        web_link_id=web_link_id,
        url=new_url,
        name=new_name,
        description=new_description,
    )

    error = result.get("error")
    message = result.get("message")
    web_link = result.get("web_link")

    assert error is None
    assert message is None
    assert web_link is not None
    assert isinstance(web_link, dict)
    assert web_link.get("id") == existing_web_link.id
    assert web_link.get("url") == new_url
    assert web_link.get("name") == new_name
    assert web_link.get("description") == new_description

    # Clean up by deleting the created web link
    box_client_ccg.web_links.delete_web_link_by_id(web_link_id)


def test_box_web_link_update_by_id_with_error(box_client_ccg: BoxClient):
    web_link_id = "1234"  # invalid web link id to trigger error
    new_url = "https://www.box-new.com"
    new_name = "Updated Web Link"
    new_description = "An updated description"

    result = box_web_link_update_by_id(
        client=box_client_ccg,
        web_link_id=web_link_id,
        url=new_url,
        name=new_name,
        description=new_description,
    )

    error = result.get("error")
    message = result.get("message")
    web_link = result.get("web_link")

    assert error is not None
    assert message is None
    assert web_link is None


def test_box_web_link_delete_by_id(
    box_client_ccg: BoxClient, web_link_test_data: TestData
):
    existing_web_link = _create_test_web_link(
        client=box_client_ccg,
        parent_folder=web_link_test_data.test_folder,
        url="https://www.box-delete.com",
    )

    web_link_id = existing_web_link.id

    result = box_web_link_delete_by_id(
        client=box_client_ccg,
        web_link_id=web_link_id,
    )

    error = result.get("error")
    message = result.get("message")
    web_link = result.get("web_link")

    assert error is None
    assert message is not None
    assert web_link is None

    assert "deleted successfully" in message

    # Verify the web link has been deleted
    get_result = box_web_link_get_by_id(
        client=box_client_ccg,
        web_link_id=web_link_id,
    )
    assert get_result.get("error") is not None
    assert get_result.get("web_link") is None


def test_box_web_link_delete_by_id_with_error(box_client_ccg: BoxClient):
    web_link_id = "1234"  # invalid web link id to trigger error

    result = box_web_link_delete_by_id(
        client=box_client_ccg,
        web_link_id=web_link_id,
    )

    error = result.get("error")
    message = result.get("message")
    web_link = result.get("web_link")

    assert error is not None
    assert message is None
    assert web_link is None
