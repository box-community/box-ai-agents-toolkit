import pytest
from box_sdk_gen import BoxClient

from box_ai_agents_toolkit import (
    box_docgen_template_create,
    box_docgen_template_list,
)

from .conftest import DocGenTestData


def test_box_docgen_template_create(
    box_client_ccg: BoxClient, docgen_test_data: DocGenTestData
):
    """
    Test creating a Box Doc Gen template.
    """
    # Ensure we have a test file to work with
    if not docgen_test_data.docgen_test_files:
        pytest.skip("No test files available for Doc Gen template creation.")

    # Use the first test file
    file_id = docgen_test_data.docgen_test_files[0].id

    # Create the Doc Gen template
    template = box_docgen_template_create(box_client_ccg, file_id)

    # Check if the template creation was successful
    assert "error" not in template, (
        f"Error creating Doc Gen template: {template['error']}"
    )
    assert "file" in template, "Template file not found in the response."
    assert "id" in template["file"], "Template file ID not found in the response."
    assert template["file"]["id"] is not None, "Template file ID should not be None."
    # Verify that the template ID matches the file ID
    assert template["file"]["id"] == file_id, "Template ID does not match the file ID."

    # create template for an existing template file does not return error...
    existing_template = box_docgen_template_create(box_client_ccg, file_id)
    assert "error" not in existing_template, (
        f"Error creating Doc Gen template for existing template: {existing_template['error']}"
    )

    # test with an invalid file ID
    invalid_file_id = "1234567890"
    error_response = box_docgen_template_create(box_client_ccg, invalid_file_id)
    assert "error" in error_response, "Expected an error response for invalid file ID."

    # Check the list of templates to ensure the created template is listed
    templates = box_docgen_template_list(box_client_ccg)
    assert isinstance(templates, list), "Templates should be returned as a list."
    assert len(templates) > 0, "Template list should not be empty."

    # Check if each file in the test data exists in the template list
    file_ids = {file.id for file in docgen_test_data.docgen_test_files}
    for template in templates:
        assert "file" in template, "Template entry should contain file metadata."
        assert "id" in template["file"], "Template file metadata should contain an ID."
        assert template["file"]["id"] in file_ids, (
            f"Template file ID {template['file']['id']} not found in test data files."
        )
