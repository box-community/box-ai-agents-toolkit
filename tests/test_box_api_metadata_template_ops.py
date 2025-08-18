import datetime
from typing import Any, Dict

import pytest

from src.box_ai_agents_toolkit.box_api_metadata_template import (
    BoxClient,
    MetadataTemplate,
    MetadataTemplates,
    _box_metadata_template_create,
    _box_metadata_template_delete,
    box_metadata_delete_instance_on_file,
    box_metadata_get_instance_on_file,
    box_metadata_set_instance_on_file,
    box_metadata_template_get_by_key,
    box_metadata_template_get_by_name,
    box_metadata_template_list,
    box_metadata_update_instance_on_file,
)


@pytest.fixture
def template_name():
    """Generate a unique template name for testing."""
    return f"Pytest Template {datetime.datetime.now().isoformat()}"


@pytest.fixture
def created_template(box_client_ccg: BoxClient, template_name: str):
    """Create a metadata template for testing and clean up afterward."""
    fields = []

    field_text = {
        "type": "string",
        "displayName": "Test Field",
        "key": "test_field",
    }
    fields.append(field_text)

    field_date = {
        "type": "date",
        "displayName": "Date Field",
        "key": "date_field",
    }
    fields.append(field_date)

    field_float = {
        "type": "float",
        "displayName": "Float Field",
        "key": "float_field",
    }
    fields.append(field_float)

    field_enum = {
        "type": "enum",
        "displayName": "Enum Field",
        "key": "enum_field",
        "options": [
            {"key": "option1"},
            {"key": "option2"},
        ],
    }
    fields.append(field_enum)

    field_multiselect = {
        "type": "multiSelect",
        "displayName": "Multiselect Field",
        "key": "multiselect_field",
        "options": [
            {"key": "option1"},
            {"key": "option2"},
        ],
    }
    fields.append(field_multiselect)

    template = _box_metadata_template_create(
        box_client_ccg, display_name=template_name, fields=fields
    )

    yield template
    # Cleanup
    try:
        if template.template_key is not None:
            _box_metadata_template_delete(
                box_client_ccg, template_key=template.template_key
            )
    except Exception:
        pass  # Template might already be deleted


# @pytest.fixture
def get_metadata() -> Dict[str, Any]:
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
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test finding a metadata template by display name."""

    assert created_template.display_name is not None
    response = box_metadata_template_get_by_name(
        box_client_ccg, display_name=created_template.display_name
    )
    assert response is not None
    assert response.get("displayName") == created_template.display_name
    assert response.get("templateKey") is not None
    assert response.get("id") is not None

    # test finding a non-existent template
    response_non_existent = box_metadata_template_get_by_name(
        box_client_ccg, display_name="Non Existent Template"
    )
    assert response_non_existent is not None
    assert isinstance(response_non_existent, dict)
    assert response_non_existent.get("message") == "Template not found"

    # Test with an existing template but different case
    response_case_insensitive = box_metadata_template_get_by_name(
        box_client_ccg, display_name=created_template.display_name.upper()
    )
    assert response_case_insensitive is not None
    assert response_case_insensitive.get("displayName") == created_template.display_name
    assert response_case_insensitive.get("templateKey") == created_template.template_key
    assert response_case_insensitive.get("id") == created_template.id


def test_box_metadata_template_get_by_key(
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test retrieving a metadata template by its key."""
    assert created_template.template_key is not None, "template_key must not be None"
    response = box_metadata_template_get_by_key(
        box_client_ccg, template_key=created_template.template_key
    )
    assert response is not None
    assert isinstance(response, dict)
    assert response.get("displayName") == created_template.display_name
    assert response.get("templateKey") == created_template.template_key
    assert response.get("id") == created_template.id

    # Test retrieving a non-existent template
    response_non_existent = box_metadata_template_get_by_key(
        box_client_ccg, template_key="non_existent_template_key"
    )
    assert response_non_existent is not None
    assert isinstance(response_non_existent, dict)

    # The response should contain 404
    assert "error" in response_non_existent
    assert "404" in response_non_existent["error"]


def test_box_metadata_template_list(
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test listing metadata templates."""
    response: MetadataTemplates = box_metadata_template_list(box_client_ccg)
    assert response is not None
    assert response.entries is not None and len(response.entries) > 0
    # Check it the template created shows up on the list
    assert any(
        template.template_key == created_template.template_key
        for template in response.entries
    )


def test_box_metadata_set_get_instance_on_file(
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test setting a metadata template instance on a file."""
    file_id = "1918361187949"  # Replace with a valid file ID for testing
    metadata = get_metadata()

    if created_template.template_key is None:
        pytest.skip("Template key is None, cannot set metadata on file.")

    # Set metadata on the file
    response = box_metadata_set_instance_on_file(
        box_client_ccg, created_template.template_key, file_id, metadata
    )

    assert response is not None
    assert isinstance(response, dict)
    assert response["$parent"] == f"file_{file_id}"
    assert response["$template"] == created_template.template_key
    extra_data = response.get("extra_data", {})
    assert extra_data.get("test_field") == metadata["test_field"]
    assert extra_data.get("date_field") == metadata["date_field"]
    assert extra_data.get("float_field") == metadata["float_field"]
    assert extra_data.get("enum_field") == metadata["enum_field"]
    assert extra_data.get("multiselect_field") == metadata["multiselect_field"]

    response_get = box_metadata_get_instance_on_file(
        box_client_ccg, file_id=file_id, template_key=created_template.template_key
    )
    assert response_get is not None
    assert isinstance(response_get, dict)
    assert response_get["$parent"] == f"file_{file_id}"
    assert response_get["$template"] == created_template.template_key
    extra_data_get = response_get.get("extra_data", {})
    assert extra_data_get.get("test_field") == metadata["test_field"]
    assert extra_data_get.get("date_field") == metadata["date_field"]
    assert extra_data_get.get("float_field") == metadata["float_field"]
    assert extra_data_get.get("enum_field") == metadata["enum_field"]
    assert extra_data_get.get("multiselect_field") == metadata["multiselect_field"]


def test_box_metadata_delete_instance_on_file(
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test deleting a metadata template instance on a file."""
    file_id = "1918361187949"  # Replace with a valid file ID for testing
    metadata = get_metadata()
    if created_template.template_key is None:
        pytest.skip("Template key is None, cannot set metadata on file.")
    # Set metadata on the file
    response = box_metadata_set_instance_on_file(
        box_client_ccg, created_template.template_key, file_id, metadata
    )
    assert response is not None

    # Now delete the metadata instance
    response_delete = box_metadata_delete_instance_on_file(
        box_client_ccg, file_id=file_id, template_key=created_template.template_key
    )
    assert response_delete is not None  # Assuming delete returns None on success
    assert isinstance(response_delete, dict)
    assert response_delete.get("message") == "Metadata instance deleted successfully"

    # Verify that the metadata instance is deleted
    response_get = box_metadata_get_instance_on_file(
        box_client_ccg, file_id=file_id, template_key=created_template.template_key
    )
    assert response_get is not None
    assert isinstance(response_get, dict)
    assert response_get.get("error") is not None
    # Error contains a 404
    assert "404" in response_get["error"]


def test_box_metadata_update_instance_on_file_full_update(
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test updating a metadata template instance on a file."""
    file_id = "1918361187949"  # Replace with a valid file ID for testing
    initial_metadata = get_metadata()

    assert created_template is not None
    assert created_template.template_key is not None
    # Set initial metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg, created_template.template_key, file_id, initial_metadata
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
        template_key=created_template.template_key,
        metadata=updated_metadata,
        remove_non_included_data=True,
    )

    assert response_update is not None
    assert isinstance(response_update, dict)
    assert response_update.get("error") is None

    extra_data_get = response_update.get("extra_data", {})

    assert extra_data_get.get("test_field") == updated_metadata["test_field"]
    assert extra_data_get.get("date_field") == updated_metadata["date_field"]
    assert extra_data_get.get("float_field") == updated_metadata["float_field"]
    assert extra_data_get.get("enum_field") == updated_metadata["enum_field"]
    assert (
        extra_data_get.get("multiselect_field") == updated_metadata["multiselect_field"]
    )


def test_box_metadata_update_instance_on_file_partial_update(
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test updating a metadata template instance on a file with partial update."""
    file_id = "1918361187949"  # Replace with a valid file ID for testing
    initial_metadata = get_metadata()

    assert created_template is not None
    assert created_template.template_key is not None
    # Set initial metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg, created_template.template_key, file_id, initial_metadata
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
        template_key=created_template.template_key,
        metadata=updated_metadata,
        remove_non_included_data=False,  # Do not remove fields not included in the update
    )

    assert response_update is not None
    assert isinstance(response_update, dict)
    assert response_update.get("error") is None

    extra_data_get = response_update.get("extra_data", {})

    assert extra_data_get.get("test_field") == updated_metadata["test_field"]
    assert extra_data_get.get("float_field") == updated_metadata["float_field"]
    assert extra_data_get.get("date_field") == initial_metadata["date_field"]
    assert extra_data_get.get("enum_field") == initial_metadata["enum_field"]


def test_box_metadata_update_instance_on_file_partial_update_remove_not_included(
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test updating a metadata template instance on a file with partial update and removing non-included fields."""
    file_id = "1918361187949"  # Replace with a valid file ID for testing
    initial_metadata = get_metadata()

    assert created_template is not None
    assert created_template.template_key is not None
    # Set initial metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg, created_template.template_key, file_id, initial_metadata
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
        template_key=created_template.template_key,
        metadata=updated_metadata,
        remove_non_included_data=True,  # Remove fields not included in the update
    )

    assert response_update is not None
    assert isinstance(response_update, dict)
    assert response_update.get("error") is None

    extra_data_get = response_update.get("extra_data", {})

    assert extra_data_get.get("test_field") == updated_metadata["test_field"]
    assert extra_data_get.get("float_field") == updated_metadata["float_field"]
    assert extra_data_get.get("date_field") is None  # Should be removed
    assert extra_data_get.get("enum_field") is None  # Should be removed


def test_box_metadata_update_instance_on_file_add_missing_fields(
    box_client_ccg: BoxClient, created_template: MetadataTemplate
):
    """Test updating a metadata template instance on a file by adding missing fields."""
    file_id = "1918361187949"  # Replace with a valid file ID for testing
    initial_metadata = {
        "test_field": "Original Value",
        "date_field": "2025-10-01T00:00:00.000Z",
        # intentionally leaving out float_field and enum_field to test adding missing fields
    }

    assert created_template is not None
    assert created_template.template_key is not None
    # Set initial metadata on the file
    response_set = box_metadata_set_instance_on_file(
        box_client_ccg, created_template.template_key, file_id, initial_metadata
    )
    assert response_set is not None
    assert isinstance(response_set, dict)
    assert response_set.get("error") is None

    # Prepare updated metadata with some fields missing
    updated_metadata = get_metadata()

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

    extra_data_get = response_update.get("extra_data", {})

    assert extra_data_get.get("test_field") == updated_metadata["test_field"]
    assert extra_data_get.get("date_field") == updated_metadata["date_field"]
    assert extra_data_get.get("float_field") == updated_metadata["float_field"]
    assert extra_data_get.get("enum_field") == updated_metadata["enum_field"]
    assert (
        extra_data_get.get("multiselect_field") == updated_metadata["multiselect_field"]
    )


@pytest.mark.skip(reason="Delete Pytest leftovers")
def test_delete_all_pytest_templates(box_client_ccg: BoxClient):
    # list all templates that start with "Pytest Template"
    templates = box_metadata_template_list(box_client_ccg)

    if templates.entries is not None:
        for template in templates.entries:
            if (
                template.display_name is not None
                and template.display_name.startswith("Pytest Template")
                and template.template_key is not None
            ):
                try:
                    if template.template_key is not None:
                        _box_metadata_template_delete(
                            box_client_ccg, template_key=template.template_key
                        )
                except Exception as e:
                    print(f"Failed to delete template {template.display_name}: {e}")
