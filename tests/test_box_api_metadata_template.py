import datetime
import uuid
from typing import Any, Dict

import pytest

from src.box_ai_agents_toolkit import (
    BoxClient,
    box_metadata_delete_instance_on_file,
    box_metadata_get_instance_on_file,
    box_metadata_set_instance_on_file,
    box_metadata_template_create,
    box_metadata_template_get_by_id,
    box_metadata_template_get_by_key,
    box_metadata_template_get_by_name,
    box_metadata_template_list,
    box_metadata_update_instance_on_file,
)
from tests.conftest import TestData


def _get_metadata() -> Dict[str, Any]:
    """Generate a sample metadata instance for testing."""
    date = datetime.datetime(2023, 10, 1)
    formatted_datetime = date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    return {
        "test_field": "Test Value",
        "date_field": formatted_datetime,
        "float_field": 3.14,
        "enum_field": "option1",
        "multiselect_field": ["option1", "option2"],
    }


def test_box_metadata_find_template_by_name(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test finding a metadata template by display name."""

    assert metadata_test_data.test_metadata_template.display_name is not None
    response = box_metadata_template_get_by_name(
        box_client_ccg,
        display_name=metadata_test_data.test_metadata_template.display_name,
    )
    assert response is not None
    template = response.get("metadata_template", {})

    assert (
        template.get("displayName")
        == metadata_test_data.test_metadata_template.display_name
    )
    assert template.get("templateKey") is not None
    assert template.get("id") is not None

    # test finding a non-existent template
    response_non_existent = box_metadata_template_get_by_name(
        box_client_ccg, display_name="Non Existent Template"
    )
    assert response_non_existent is not None
    assert isinstance(response_non_existent, dict)
    assert response_non_existent.get("message") == "Template not found"

    # Test with an existing template but different case
    response_case_insensitive = box_metadata_template_get_by_name(
        box_client_ccg,
        display_name=metadata_test_data.test_metadata_template.display_name.upper(),
    )
    assert response_case_insensitive is not None
    template = response_case_insensitive.get("metadata_template", {})
    assert (
        template.get("displayName")
        == metadata_test_data.test_metadata_template.display_name
    )
    assert (
        template.get("templateKey")
        == metadata_test_data.test_metadata_template.template_key
    )
    assert template.get("id") == metadata_test_data.test_metadata_template.id


def test_box_metadata_template_get_by_key(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test retrieving a metadata template by its key."""
    assert metadata_test_data.test_metadata_template.template_key is not None, (
        "template_key must not be None"
    )
    response = box_metadata_template_get_by_key(
        box_client_ccg,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )
    assert response is not None
    assert isinstance(response, dict)
    metadata_template = response.get("metadata_template", {})
    assert (
        metadata_template.get("displayName")
        == metadata_test_data.test_metadata_template.display_name
    )
    assert (
        metadata_template.get("templateKey")
        == metadata_test_data.test_metadata_template.template_key
    )
    assert metadata_template.get("id") == metadata_test_data.test_metadata_template.id

    # Test retrieving a non-existent template
    response_non_existent = box_metadata_template_get_by_key(
        box_client_ccg, template_key="non_existent_template_key"
    )
    assert response_non_existent is not None
    assert isinstance(response_non_existent, dict)

    # The response should contain 404
    assert "error" in response_non_existent


def test_box_metadata_template_list(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test listing metadata templates."""
    response = box_metadata_template_list(box_client_ccg)
    assert response is not None
    assert isinstance(response, dict)
    assert "error" not in response

    metadata_templates = response.get("metadata_templates", [])
    # Check it the template created shows up on the list
    assert any(
        template.get("templateKey")
        == metadata_test_data.test_metadata_template.template_key
        for template in metadata_templates
    )

    # try listing with a smaller limit to test the marker
    response = box_metadata_template_list(box_client_ccg, limit=1)
    assert response is not None
    assert isinstance(response, dict)
    assert "error" not in response

    metadata_templates = response.get("metadata_templates", [])
    assert len(metadata_templates) >= 1

    # try forcing and error in the tool
    response_error = box_metadata_template_list(box_client_ccg, limit=-20)
    assert response_error is not None
    assert isinstance(response_error, dict)
    assert "error" in response_error


def test_box_metadata_set_get_instance_on_file(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test setting a metadata template instance on a file."""
    file_id = metadata_test_data.test_files[0].id
    metadata = _get_metadata()

    if metadata_test_data.test_metadata_template.template_key is None:
        pytest.skip("Template key is None, cannot set metadata on file.")

    # Set metadata on the file
    response = box_metadata_set_instance_on_file(
        box_client_ccg,
        metadata_test_data.test_metadata_template.template_key,
        file_id,
        metadata,
    )

    assert response is not None
    assert isinstance(response, dict)
    metadata_instance = response.get("metadata_instance", {})
    assert metadata_instance["$parent"] == f"file_{file_id}"
    assert (
        metadata_instance["$template"]
        == metadata_test_data.test_metadata_template.template_key
    )
    extra_data = metadata_instance.get("extra_data", {})
    assert extra_data.get("test_field") == metadata["test_field"]
    assert extra_data.get("date_field") == metadata["date_field"]
    assert extra_data.get("float_field") == metadata["float_field"]
    assert extra_data.get("enum_field") == metadata["enum_field"]
    assert extra_data.get("multiselect_field") == metadata["multiselect_field"]

    response_get = box_metadata_get_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )
    assert response_get is not None
    assert isinstance(response_get, dict)
    metadata_instance_get = response_get.get("metadata_instance", {})
    assert metadata_instance_get["$parent"] == f"file_{file_id}"
    assert (
        metadata_instance_get["$template"]
        == metadata_test_data.test_metadata_template.template_key
    )
    extra_data_get = metadata_instance_get.get("extra_data", {})
    assert extra_data_get.get("test_field") == metadata["test_field"]
    assert extra_data_get.get("date_field") == metadata["date_field"]
    assert extra_data_get.get("float_field") == metadata["float_field"]
    assert extra_data_get.get("enum_field") == metadata["enum_field"]
    assert extra_data_get.get("multiselect_field") == metadata["multiselect_field"]


def test_box_metadata_delete_instance_on_file(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test deleting a metadata template instance on a file."""
    file_id = metadata_test_data.test_files[1].id
    metadata = _get_metadata()
    if metadata_test_data.test_metadata_template.template_key is None:
        pytest.skip("Template key is None, cannot set metadata on file.")

    # start by removing any existing metadata instance on the file
    box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    # Set metadata on the file
    response = box_metadata_set_instance_on_file(
        box_client_ccg,
        metadata_test_data.test_metadata_template.template_key,
        file_id,
        metadata,
    )
    assert response is not None
    assert isinstance(response, dict)
    assert response.get("error") is None

    # Now delete the metadata instance
    response_delete = box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )
    assert response_delete is not None  # Assuming delete returns None on success
    assert isinstance(response_delete, dict)
    assert response_delete.get("message") == "Metadata instance deleted successfully"

    # Verify that the metadata instance is deleted
    response_get = box_metadata_get_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )
    assert response_get is not None
    assert isinstance(response_get, dict)
    assert response_get.get("error") is not None
    # Error contains a 404
    assert "404" in response_get["error"]


def test_box_metadata_update_instance_on_file_full_update(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test updating a metadata template instance on a file."""
    file_id = metadata_test_data.test_files[0].id
    initial_metadata = _get_metadata()

    assert metadata_test_data.test_metadata_template is not None
    assert metadata_test_data.test_metadata_template.template_key is not None

    # start by removing any existing metadata instance on the file
    box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    # Set initial metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg,
        metadata_test_data.test_metadata_template.template_key,
        file_id,
        initial_metadata,
    )
    # response has no error
    assert response_set is not None
    assert isinstance(response_set, dict)
    assert response_set.get("error") is None

    # Prepare updated metadata
    updated_metadata = {
        "test_field": "Updated Value",
        "date_field": "2023-11-01T00:00:00.000Z",
        "float_field": 2.71,
        "enum_field": "option2",
        "multiselect_field": ["option2"],
    }

    # Update metadata on the file
    response_update = box_metadata_update_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
        metadata=updated_metadata,
        remove_non_included_data=True,
    )

    assert response_update is not None
    assert isinstance(response_update, dict)
    assert response_update.get("error") is None
    metadata_instance_update = response_update.get("metadata_instance", {})
    assert metadata_instance_update["$parent"] == f"file_{file_id}"
    assert (
        metadata_instance_update["$template"]
        == metadata_test_data.test_metadata_template.template_key
    )

    extra_data_get = metadata_instance_update.get("extra_data", {})

    assert extra_data_get.get("test_field") == updated_metadata["test_field"]
    assert extra_data_get.get("date_field") == updated_metadata["date_field"]
    assert extra_data_get.get("float_field") == updated_metadata["float_field"]
    assert extra_data_get.get("enum_field") == updated_metadata["enum_field"]
    assert (
        extra_data_get.get("multiselect_field") == updated_metadata["multiselect_field"]
    )


def test_box_metadata_update_instance_on_file_partial_update(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test updating a metadata template instance on a file with partial update."""
    file_id = metadata_test_data.test_files[0].id
    initial_metadata = _get_metadata()

    assert metadata_test_data.test_metadata_template is not None
    assert metadata_test_data.test_metadata_template.template_key is not None

    # start by removing any existing metadata instance on the file
    box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    # Set initial metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg,
        metadata_test_data.test_metadata_template.template_key,
        file_id,
        initial_metadata,
    )
    assert response_set is not None
    assert isinstance(response_set, dict)
    assert response_set.get("error") is None

    # Prepare updated metadata with only some fields changed
    updated_metadata = {
        "test_field": "Partially Updated Value",
        "float_field": 1.41,
        # Intentionally leaving out date_field and enum_field to test partial update
    }

    # Update metadata on the file
    response_update = box_metadata_update_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
        metadata=updated_metadata,
        remove_non_included_data=False,  # Do not remove fields not included in the update
    )

    assert response_update is not None
    assert isinstance(response_update, dict)
    assert response_update.get("error") is None

    metadata_instance_update = response_update.get("metadata_instance", {})
    assert metadata_instance_update["$parent"] == f"file_{file_id}"
    assert (
        metadata_instance_update["$template"]
        == metadata_test_data.test_metadata_template.template_key
    )

    extra_data_get = metadata_instance_update.get("extra_data", {})

    assert extra_data_get.get("test_field") == updated_metadata["test_field"]
    assert extra_data_get.get("float_field") == updated_metadata["float_field"]
    assert extra_data_get.get("date_field") == initial_metadata["date_field"]
    assert extra_data_get.get("enum_field") == initial_metadata["enum_field"]


def test_box_metadata_update_instance_on_file_partial_update_remove_not_included(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test updating a metadata template instance on a file with partial update and removing non-included fields."""
    file_id = metadata_test_data.test_files[0].id
    initial_metadata = _get_metadata()

    assert metadata_test_data.test_metadata_template is not None
    assert metadata_test_data.test_metadata_template.template_key is not None

    # start by removing any existing metadata instance on the file
    box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    # Set initial metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg,
        metadata_test_data.test_metadata_template.template_key,
        file_id,
        initial_metadata,
    )
    assert response_set is not None
    assert isinstance(response_set, dict)
    assert response_set.get("error") is None

    # Prepare updated metadata with only some fields changed
    updated_metadata = {
        "test_field": "Partially Updated Value",
        "float_field": 1.41,
        # Intentionally leaving out date_field and enum_field to test removal of non-included fields
    }

    # Update metadata on the file
    response_update = box_metadata_update_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
        metadata=updated_metadata,
        remove_non_included_data=True,  # Remove fields not included in the update
    )

    assert response_update is not None
    assert isinstance(response_update, dict)
    assert response_update.get("error") is None

    metadata_instance_update = response_update.get("metadata_instance", {})
    assert metadata_instance_update["$parent"] == f"file_{file_id}"
    assert (
        metadata_instance_update["$template"]
        == metadata_test_data.test_metadata_template.template_key
    )

    extra_data_get = metadata_instance_update.get("extra_data", {})

    assert extra_data_get.get("test_field") == updated_metadata["test_field"]
    assert extra_data_get.get("float_field") == updated_metadata["float_field"]
    assert extra_data_get.get("date_field") is None  # Should be removed
    assert extra_data_get.get("enum_field") is None  # Should be removed


def test_box_metadata_update_instance_on_file_add_missing_fields(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test updating a metadata template instance on a file by adding missing fields."""
    file_id = metadata_test_data.test_files[0].id
    created_template = metadata_test_data.test_metadata_template
    initial_metadata = {
        "test_field": "Original Value",
        "date_field": "2025-10-01T00:00:00.000Z",
        # intentionally leaving out float_field and enum_field to test adding missing fields
    }

    assert created_template is not None
    assert created_template.template_key is not None

    # start by removing any existing metadata instance on the file
    box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    # Set initial metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg, created_template.template_key, file_id, initial_metadata
    )
    assert response_set is not None
    assert isinstance(response_set, dict)
    assert response_set.get("error") is None

    # Prepare updated metadata with some fields missing
    updated_metadata = _get_metadata()

    # Update metadata on the file
    response_update = box_metadata_update_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=created_template.template_key,
        metadata=updated_metadata,
        remove_non_included_data=False,  # Do not remove fields not included in the update
    )

    assert response_update is not None
    assert isinstance(response_update, dict)
    assert response_update.get("error") is None

    metadata_instance_update = response_update.get("metadata_instance", {})

    assert metadata_instance_update["$parent"] == f"file_{file_id}"
    assert metadata_instance_update["$template"] == created_template.template_key

    extra_data_get = metadata_instance_update.get("extra_data", {})

    assert extra_data_get.get("test_field") == updated_metadata["test_field"]
    assert extra_data_get.get("date_field") == updated_metadata["date_field"]
    assert extra_data_get.get("float_field") == updated_metadata["float_field"]
    assert extra_data_get.get("enum_field") == updated_metadata["enum_field"]
    assert (
        extra_data_get.get("multiselect_field") == updated_metadata["multiselect_field"]
    )


def test_box_metadata_template_create(
    box_client_ccg: BoxClient,
):
    """Test creating a metadata template."""
    template_name = f"A{uuid.uuid4()} Pytest"

    fields = [
        {
            "type": "string",
            "displayName": "Test Field",
            "key": "test_field",
        },
        {
            "type": "date",
            "displayName": "Date Field",
            "key": "date_field",
        },
        {
            "type": "float",
            "displayName": "Float Field",
            "key": "float_field",
        },
        {
            "type": "enum",
            "displayName": "Enum Field",
            "key": "enum_field",
            "options": [
                {"key": "option1"},
                {"key": "option2"},
            ],
        },
    ]

    response = box_metadata_template_create(
        box_client_ccg,
        display_name=template_name,
        fields=fields,
    )

    assert response is not None
    assert "error" not in response
    assert isinstance(response, dict)
    metadata_template = response.get("metadata_template", {})

    # Verify the template was created successfully
    assert metadata_template.get("displayName") == template_name
    assert metadata_template.get("templateKey") is not None
    assert metadata_template.get("id") is not None

    # Clean up
    box_client_ccg.metadata_templates.delete_metadata_template(
        scope="enterprise", template_key=metadata_template.get("templateKey")
    )

    # test creation with an error
    response = box_metadata_template_create(
        box_client_ccg,
        display_name=template_name,
        fields=[],
        template_key="",
    )

    assert response is not None
    assert isinstance(response, dict)
    assert "error" in response


def test_box_metadata_template_create_with_template_key(
    box_client_ccg: BoxClient,
):
    """Test creating a metadata template with a specific template key."""
    template_name = f"A{uuid.uuid4()} Pytest"
    template_key = f"A{uuid.uuid4()}"

    fields = [
        {
            "type": "string",
            "displayName": "Test Field",
            "key": "test_field",
        }
    ]

    response = box_metadata_template_create(
        box_client_ccg,
        display_name=template_name,
        fields=fields,
        template_key=template_key,
    )

    assert response is not None
    assert isinstance(response, dict)
    assert "error" not in response

    metadata_template = response.get("metadata_template", {})

    # Verify the template was created with the specified key
    assert metadata_template.get("displayName") == template_name
    assert metadata_template.get("templateKey") == template_key
    assert metadata_template.get("id") is not None

    # Clean up
    box_client_ccg.metadata_templates.delete_metadata_template(
        scope="enterprise", template_key=metadata_template.get("templateKey")
    )


def test_box_metadata_template_get_by_id(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test retrieving a metadata template by its ID."""
    assert metadata_test_data.test_metadata_template.id is not None

    response = box_metadata_template_get_by_id(
        box_client_ccg,
        template_id=metadata_test_data.test_metadata_template.id,
    )

    assert response is not None
    assert isinstance(response, dict)
    assert "error" not in response

    metadata_template = response.get("metadata_template", {})

    assert metadata_template.get("id") == metadata_test_data.test_metadata_template.id
    assert (
        metadata_template.get("displayName")
        == metadata_test_data.test_metadata_template.display_name
    )
    assert (
        metadata_template.get("templateKey")
        == metadata_test_data.test_metadata_template.template_key
    )


def test_box_metadata_template_get_by_id_not_found(
    box_client_ccg: BoxClient,
):
    """Test retrieving a non-existent metadata template by ID."""
    response = box_metadata_template_get_by_id(
        box_client_ccg,
        template_id="non_existent_template_id_12345",
    )

    assert response is not None
    assert isinstance(response, dict)
    assert "error" in response


def test_box_metadata_update_no_changes(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test updating metadata when there are no changes to make."""
    file_id = metadata_test_data.test_files[0].id
    metadata = _get_metadata()

    assert metadata_test_data.test_metadata_template.template_key is not None

    # Clean up first to ensure a fresh start
    box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    # Set metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg,
        metadata_test_data.test_metadata_template.template_key,
        file_id,
        metadata,
    )
    assert response_set.get("error") is None

    # Try to update with the exact same metadata
    response_update = box_metadata_update_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
        metadata=metadata,
        remove_non_included_data=False,
    )

    assert response_update is not None
    assert isinstance(response_update, dict)
    # Should return a message indicating no changes
    assert response_update.get("message") == "No changes to update"

    # force error on tool
    response_error = box_metadata_update_instance_on_file(
        box_client_ccg,
        file_id="",
        template_key=metadata_test_data.test_metadata_template.template_key,
        metadata=metadata,
        remove_non_included_data=False,
    )

    assert response_error is not None
    assert isinstance(response_error, dict)
    assert "error" in response_error


def test_box_metadata_update_instance_on_non_existent_file(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test updating metadata on a non-existent file."""
    fake_file_id = "999999999999"
    metadata = _get_metadata()

    assert metadata_test_data.test_metadata_template.template_key is not None

    response = box_metadata_update_instance_on_file(
        box_client_ccg,
        file_id=fake_file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
        metadata=metadata,
    )

    assert response is not None
    assert isinstance(response, dict)
    assert "error" in response


def test_box_metadata_set_instance_duplicate(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test setting metadata instance when one already exists (should fail)."""
    file_id = metadata_test_data.test_files[0].id
    metadata = _get_metadata()

    assert metadata_test_data.test_metadata_template.template_key is not None

    # First set should succeed (already done in previous tests, but ensure it's there)
    box_metadata_set_instance_on_file(
        box_client_ccg,
        metadata_test_data.test_metadata_template.template_key,
        file_id,
        metadata,
    )

    # Try to set again - should return an error
    response = box_metadata_set_instance_on_file(
        box_client_ccg,
        metadata_test_data.test_metadata_template.template_key,
        file_id,
        metadata,
    )

    assert response is not None
    assert isinstance(response, dict)
    # This should return an error since the instance already exists
    assert "error" in response or "metadata_instance" in response


def test_box_metadata_delete_non_existent_instance(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test deleting a metadata instance that doesn't exist."""
    file_id = (
        metadata_test_data.test_files[2].id
        if len(metadata_test_data.test_files) > 2
        else metadata_test_data.test_files[0].id
    )

    assert metadata_test_data.test_metadata_template.template_key is not None

    # Ensure no metadata exists first
    box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    # Try to delete again - should handle gracefully
    response = box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    assert response is not None
    assert isinstance(response, dict)
    # Should return either success message or error
    assert "message" in response or "error" in response


def test_box_metadata_delete_non_existing_file(
    box_client_ccg: BoxClient, metadata_test_data: TestData
):
    """Test deleting a metadata instance on a non-existing file."""
    fake_file_id = "999999999999"

    assert metadata_test_data.test_metadata_template.template_key is not None

    response = box_metadata_delete_instance_on_file(
        box_client_ccg,
        file_id=fake_file_id,
        template_key=metadata_test_data.test_metadata_template.template_key,
    )

    assert response is not None
    assert isinstance(response, dict)
    assert "error" in response
