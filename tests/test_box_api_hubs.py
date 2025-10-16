import datetime
import uuid
from time import sleep

from box_sdk_gen import (
    BoxClient,
)

from box_ai_agents_toolkit import (
    box_hub_copy,
    box_hub_create,
    box_hub_delete,
    box_hub_get,
    box_hub_list,
    box_hub_update,
)


def _hub_title_generate(suffix: str = "") -> str:
    # prefix the hub with YYYYMMDDHHMMSS to help with sorting and cleanup
    # add Test Hub to the end
    return f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')} Test Hub {suffix}"


def _create_x_hubs_for_testing(
    client: BoxClient, number_of_hubs: int = 1, hub_title_suffix: str = ""
) -> list[str]:
    created_hub_ids = []
    for i in range(number_of_hubs):
        title = _hub_title_generate(f"List {i}")
        description = f"This is test hub number {i}."
        created_hub = client.hubs.create_hub_v2025_r0(
            title=title,
            description=description,
        )
        created_hub_ids.append(created_hub.id)
    return created_hub_ids


def test_box_hub_create(box_client_ccg: BoxClient):
    # Create a new Hub
    title = _hub_title_generate("Create")
    description = "This is a test hub."
    result = box_hub_create(box_client_ccg, title, description)

    # no error found
    assert "error" not in result, f"Error occurred: {result.get('error')}"

    # validate result
    assert "id" in result, f"Hub creation failed: {result}"
    assert result["title"] == title
    assert result["description"] == description

    # Test creation failure using a very long name (over 50 chars)  (should NOT be allowed)
    title = "A" * 300
    description = "This is a test hub with a very long name."
    result_error = box_hub_create(box_client_ccg, title, description)
    assert "error" in result_error, "Expected error when creating duplicate Hub title."
    assert "message" not in result_error, (
        f"Unexpected message: {result_error.get('message')}"
    )

    # Clean up
    box_client_ccg.hubs.delete_hub_by_id_v2025_r0(result["id"])


def test_box_hub_get(box_client_ccg: BoxClient):
    # Create a new Hub to retrieve
    created_hub_id = _create_x_hubs_for_testing(box_client_ccg, 1, "Get")[0]
    assert created_hub_id is not None, "Hub creation failed."

    try:
        # Retrieve the Hub by ID
        result = box_hub_get(box_client_ccg, created_hub_id)

        # no error found
        assert "error" not in result, f"Error occurred: {result.get('error')}"

        # validate result
        assert result["id"] == created_hub_id
    finally:
        # Clean up
        box_client_ccg.hubs.delete_hub_by_id_v2025_r0(created_hub_id)


def test_box_hub_get_all_pages(box_client_ccg: BoxClient):
    # Create 5 Hubs to ensure multiple pages
    number_of_hubs = 5
    created_hub_ids = _create_x_hubs_for_testing(box_client_ccg, number_of_hubs, "List")

    assert len(created_hub_ids) == number_of_hubs, "Hub creation failed."

    try:
        # it takes a few seconds for the list to update
        sleep(10)

        # List Hubs with a small limit to force pagination
        result = box_hub_list(box_client_ccg, limit=2)

        # no error found
        assert "error" not in result, f"Error occurred: {result.get('error')}"

        # no message found
        assert "message" not in result, f"Error occurred: {result.get('message')}"

        # validate result
        assert "hubs" in result, f"Hub list failed: {result}"
        assert len(result["hubs"]) >= number_of_hubs, (
            f"Expected at least 10 hubs, got {len(result['hubs'])}"
        )
        returned_hub_ids = [hub["id"] for hub in result["hubs"]]
        for hub_id in created_hub_ids:
            assert hub_id in returned_hub_ids, f"Hub ID {hub_id} not found in list."

    finally:
        # Clean up
        for hub_id in created_hub_ids:
            box_client_ccg.hubs.delete_hub_by_id_v2025_r0(hub_id)


def test_box_hub_update(box_client_ccg: BoxClient):
    # Create a new Hub to update
    created_hub_id = _create_x_hubs_for_testing(box_client_ccg, 1, "Update")[0]
    assert created_hub_id is not None, "Hub creation failed."

    try:
        # Update the Hub
        new_title = _hub_title_generate("Updated")
        new_description = "This is an updated test hub."
        result = box_hub_update(
            box_client_ccg,
            created_hub_id,
            new_title,
            new_description,
            is_ai_enabled=True,
            is_collaboration_restricted_to_enterprise=True,
            can_non_owners_invite=False,
            can_shared_link_be_created=False,
        )

        # no error found
        assert "error" not in result, f"Error occurred: {result.get('error')}"

        # validate result
        assert result["id"] == created_hub_id
        assert result["title"] == new_title
        assert result["description"] == new_description
        assert result["is_ai_enabled"] is True
        assert result["is_collaboration_restricted_to_enterprise"] is True
        assert result["can_non_owners_invite"] is False
        assert result["can_shared_link_be_created"] is False

        # try to update a hub that does not exists
        result = box_hub_update(
            box_client_ccg,
            str(uuid.uuid4()),
            new_title,
            new_description,
            is_ai_enabled=True,
            is_collaboration_restricted_to_enterprise=True,
            can_non_owners_invite=False,
            can_shared_link_be_created=False,
        )
        assert "error" in result, "Expected error when updating non-existent Hub."
        assert "message" not in result, f"Unexpected message: {result.get('message')}"

    finally:
        # Clean up
        box_client_ccg.hubs.delete_hub_by_id_v2025_r0(created_hub_id)


def test_box_hub_copy(box_client_ccg: BoxClient):
    # Create a new Hub to copy
    created_hub_id = _create_x_hubs_for_testing(box_client_ccg, 1, "Copy")[0]
    assert created_hub_id is not None, "Hub creation failed."

    result = None

    try:
        # Copy the Hub
        new_title = _hub_title_generate("Copy of Hub")
        result = box_hub_copy(box_client_ccg, created_hub_id, new_title)

        # no error found
        assert "error" not in result, f"Error occurred: {result.get('error')}"

        # validate result
        assert "id" in result, f"Hub copy failed: {result}"
        assert result["title"] == new_title
        assert result["id"] != created_hub_id  # Ensure it's a different Hub

        # Try to copy a hub that does not exists
        result_error = box_hub_copy(box_client_ccg, str(uuid.uuid4()), new_title)
        assert "error" in result_error, "Expected error when copying non-existent Hub."

    finally:
        # Clean up
        box_client_ccg.hubs.delete_hub_by_id_v2025_r0(created_hub_id)
        if result and "id" in result:
            box_client_ccg.hubs.delete_hub_by_id_v2025_r0(result["id"])


def test_box_hub_delete(box_client_ccg: BoxClient):
    # Create a new Hub to delete
    created_hub_id = _create_x_hubs_for_testing(box_client_ccg, 1, "Delete")[0]
    assert created_hub_id is not None, "Hub creation failed."

    try:
        # Delete the Hub
        result = box_hub_delete(box_client_ccg, created_hub_id)

        # no error found
        assert "error" not in result, f"Error occurred: {result.get('error')}"

        # there is a message
        assert "message" in result, f"Hub deletion failed: {result}"

        # get the message
        message = result["message"]

        # message contains the word deleted
        assert message is not None, f"Hub deletion failed: {result}"
        assert "deleted" in message.lower(), f"Hub deletion failed: {result}"

    except Exception as e:
        # If any exception occurs, ensure the Hub is deleted in cleanup
        box_client_ccg.hubs.delete_hub_by_id_v2025_r0(created_hub_id)
        raise e

    # Try to get the deleted Hub to confirm deletion
    get_result = box_hub_get(box_client_ccg, created_hub_id)

    # Expect an error indicating the Hub was not found
    assert get_result is not None, "Expected an error when retrieving deleted Hub."
    assert "error" in get_result or "message" in get_result, (
        "Expected an error or message when retrieving deleted Hub."
    )

    # try to delete a hub that does not exist
    result = box_hub_delete(box_client_ccg, str(uuid.uuid4()))
    assert "error" in result, "Expected error when deleting non-existent Hub."
    assert "message" not in result, f"Unexpected message: {result.get('message')}"


def test_box_hub_search(box_client_ccg: BoxClient):
    # Create a new Hub to search
    created_hub_id = _create_x_hubs_for_testing(box_client_ccg, 5, "Search")
    assert created_hub_id is not None, "Hub creation failed."

    try:
        # it takes a few seconds for the list to update
        sleep(15)

        hub_first = box_client_ccg.hubs.get_hub_by_id_v2025_r0(created_hub_id[0])
        assert hub_first is not None, "Hub retrieval failed."

        # Search for the Hub by its unique suffix
        result = box_hub_list(box_client_ccg, query=hub_first.title)

        # no error found
        assert "error" not in result, f"Error occurred: {result.get('error')}"

        # validate result
        assert "hubs" in result, f"Hub search failed: {result}"
        assert len(result["hubs"]) >= 1, (
            f"Expected at least 1 hub, got {len(result['hubs'])}"
        )
        # returned_hub_ids = [hub["id"] for hub in result["hubs"]]
        # assert created_hub_id in returned_hub_ids, (
        #     f"Hub ID {created_hub_id} not found in search results."
        # )

        # try listing all sorted by view_count desc
        result = box_hub_list(
            box_client_ccg,
            sort="view_count",
            direction="DESC",
        )
        assert "hubs" in result, f"Hub list failed: {result}"
        assert len(result["hubs"]) >= 1, (
            f"Expected at least 1 hub, got {len(result['hubs'])}"
        )

    finally:
        # Clean up
        for hub_id in created_hub_id:
            box_client_ccg.hubs.delete_hub_by_id_v2025_r0(hub_id)

    # try to search using an order that does not exist
    result = box_hub_list(box_client_ccg, sort="invalid_sort", direction="DESC")
    assert "error" in result, "Expected error when using invalid sort."
    assert "message" not in result, f"Unexpected message: {result.get('message')}"

    # try to search using a direction that does not exist
    result = box_hub_list(
        box_client_ccg, sort="view_count", direction="INVALID_DIRECTION"
    )
    assert "error" in result, "Expected error when using invalid direction."
    assert "message" not in result, f"Unexpected message: {result.get('message')}"
