import pytest
from box_sdk_gen import BoxClient

from box_ai_agents_toolkit import (
    box_docgen_template_create,
    box_docgen_template_delete,
    box_docgen_template_get_by_id,
    box_docgen_template_get_by_name,
    box_docgen_template_list,
    box_docgen_template_list_tags,
)

from .conftest import TestData


def test_box_docgen_template_create(
    box_client_ccg: BoxClient, docgen_test_files: TestData
):
    """
    Test creating a Box Doc Gen template.
    """
    # Ensure we have a test file to work with
    if not docgen_test_files.test_files:
        pytest.skip("No test files available for Doc Gen template creation.")

    # Use the first test file
    file_id = docgen_test_files.test_files[0].id

    # Create the Doc Gen template
    template = box_docgen_template_create(box_client_ccg, file_id)

    # Check if the template creation was successful
    assert (
        "error" not in template
    ), f"Error creating Doc Gen template: {template['error']}"
    assert "file" in template, "Template file not found in the response."
    assert "id" in template["file"], "Template file ID not found in the response."
    assert template["file"]["id"] is not None, "Template file ID should not be None."
    # Verify that the template ID matches the file ID
    assert template["file"]["id"] == file_id, "Template ID does not match the file ID."

    # create template for an existing template file does not return error...
    existing_template = box_docgen_template_create(box_client_ccg, file_id)
    assert (
        "error" not in existing_template
    ), f"Error creating Doc Gen template for existing template: {existing_template['error']}"

    # test with an invalid file ID
    invalid_file_id = "1234567890"
    error_response = box_docgen_template_create(box_client_ccg, invalid_file_id)
    assert "error" in error_response, "Expected an error response for invalid file ID."


def test_box_docgen_template_list(
    box_client_ccg: BoxClient, docgen_test_templates: TestData
):
    # Check the list of templates to ensure the created template is listed
    templates = box_docgen_template_list(box_client_ccg)
    assert isinstance(templates, list), "Templates should be returned as a list."
    assert len(templates) > 0, "Template list should not be empty."

    # Check if the test templates exist in the returned list
    assert isinstance(
        docgen_test_templates.test_files, list
    ), "Test files should be a list."

    assert docgen_test_templates.test_files[0].id in [
        template["file"]["id"] for template in templates
    ], "Test template file ID should be in the list of templates."


def test_box_docgen_template_get_by_id(
    box_client_ccg: BoxClient, docgen_test_templates: TestData
):
    """
    Test retrieving a Box Doc Gen template by ID.
    """
    if not docgen_test_templates.test_files:
        pytest.skip("No test files available for Doc Gen template retrieval.")

    # Use the first test file's ID
    file_id = docgen_test_templates.test_files[0].id

    # Retrieve the template by ID
    template = box_docgen_template_get_by_id(box_client_ccg, file_id)

    # Check if the retrieval was successful
    assert (
        "error" not in template
    ), f"Error retrieving Doc Gen template: {template['error']}"
    assert "file" in template, "Template file not found in the response."
    assert "id" in template["file"], "Template file ID not found in the response."
    assert (
        template["file"]["id"] == file_id
    ), "Retrieved template ID does not match the file ID."


def test_box_docgen_template_get_by_name(
    box_client_ccg: BoxClient, docgen_test_templates: TestData
):
    """
    Test retrieving a Box Doc Gen template by name.
    """
    if not docgen_test_templates.test_files:
        pytest.skip("No test files available for Doc Gen template retrieval by name.")

    # Use the first test file's name
    template_name = docgen_test_templates.test_files[0].name
    if not template_name:
        pytest.skip("Test file does not have a name for Doc Gen template retrieval.")

    # Retrieve the template by name
    template = box_docgen_template_get_by_name(box_client_ccg, template_name)

    # Check if the retrieval was successful
    assert (
        "error" not in template
    ), f"Error retrieving Doc Gen template by name: {template['error']}"
    assert "file_name" in template, "Template file name not found in the response."
    assert "file" in template, "Template file not found in the response."
    assert "id" in template["file"], "Template file ID not found in the response."
    assert (
        template["file_name"] == template_name
    ), "Retrieved template name does not match the expected name."
    assert (
        template["file"]["id"] == docgen_test_templates.test_files[0].id
    ), "Retrieved template ID does not match the expected file ID."


def test_box_docgen_template_delete(
    box_client_ccg: BoxClient, docgen_test_templates: TestData
):
    """
    Test deleting a Box Doc Gen template.
    """
    if not docgen_test_templates.test_files:
        pytest.skip("No test files available for Doc Gen template deletion.")

    # Use the first test file's ID
    file_id = docgen_test_templates.test_files[2].id

    # Delete the template by ID
    response = box_docgen_template_delete(box_client_ccg, file_id)

    # Check if the deletion was successful
    assert (
        "error" not in response
    ), f"Error deleting Doc Gen template: {response['error']}"
    assert (
        response["message"] == "Template deleted successfully."
    ), "Unexpected message after deleting the template."

    # Verify that the template no longer exists
    deleted_template = box_docgen_template_get_by_id(box_client_ccg, file_id)
    assert "error" in deleted_template, "Template should not exist after deletion."


def test_box_docgen_template_list_tags(
    box_client_ccg: BoxClient, docgen_test_templates: TestData
):
    """
    Test listing tags for a Box Doc Gen template.
    """
    if not docgen_test_templates.test_files:
        pytest.skip("No test files available for Doc Gen template tag listing.")

    # Use the first test file's ID
    file_id = docgen_test_templates.test_files[0].id

    # List tags for the template
    tags = box_docgen_template_list_tags(box_client_ccg, file_id)

    # Check if the tags are returned as a list
    assert isinstance(tags, list), "Tags should be returned as a list."

    # assert no error in response
    assert (
        "error" not in tags[0]
    ), f"Error listing tags for Doc Gen template: {tags[0]['error']}"
    assert len(tags) > 0, "Tags list should not be empty."
    assert all(
        "tag_content" in tag for tag in tags
    ), "Each tag should have a 'tag_content' key."
