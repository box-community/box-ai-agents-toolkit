import pytest
from datetime import datetime
import time
from box_sdk_gen import BoxClient

from box_ai_agents_toolkit import (
    # box_docgen_template_list_tags,
    box_docgen_create_batch,
    box_docgen_create_single_file_from_user_input,
)
from .conftest import DocGenTestData


def test_box_docgen_create_batch(
    box_client_ccg: BoxClient, docgen_test_templates: DocGenTestData
):
    """
    Test creating a Box Doc Gen batch.
    """
    # Ensure we have a test template to work with
    if not docgen_test_templates.docgen_test_files:
        pytest.skip("No test templates available for Doc Gen batch creation.")

    # Use the first test template
    template_file_id = docgen_test_templates.docgen_test_files[0].id

    # Define the destination folder ID and output type
    destination_folder_id = docgen_test_templates.docgen_test_folder.id

    destination_file_name = f"{docgen_test_templates.docgen_test_files[0].name}_generated_{datetime.now().isoformat()}.pdf"
    output_type = "pdf"

    # Read tags from template file
    # template_tags = box_docgen_template_list_tags(
    #     box_client_ccg, template_id=template_file_id
    # )

    sample_user_input = {
        "script": {
            "title": "Sample Document",
            "author": "Test Author",
            "genre": "Fiction",
            "date_written": "2023-01-01",
        }
    }

    # Create the Doc Gen batch
    batch = box_docgen_create_batch(
        client=box_client_ccg,
        docgen_template_id=template_file_id,
        destination_folder_id=destination_folder_id,
        output_type=output_type,
        document_generation_data=[
            {
                "generated_file_name": destination_file_name,
                "user_input": sample_user_input,
            }
        ],
    )

    # Check if the batch creation was successful
    assert "error" not in batch, f"Error creating Doc Gen batch: {batch['error']}"
    assert "message" in batch, "Batch creation did not return a success message"
    assert "Batch created successfully" in batch["message"], (
        "Batch creation message is incorrect"
    )


def test_box_docgen_create_single_file_from_user_input(
    box_client_ccg: BoxClient, docgen_test_templates: DocGenTestData
):
    """
    Test creating a single document from a Doc Gen template using user input.
    """
    # Ensure we have a test template to work with
    if not docgen_test_templates.docgen_test_files:
        pytest.skip("No test templates available for single file creation.")

    # Use the first test template
    template_file_id = docgen_test_templates.docgen_test_files[0].id

    # Define the destination folder ID and output type
    destination_folder_id = docgen_test_templates.docgen_test_folder.id
    output_type = "pdf"

    sample_user_input = {
        "script": {
            "title": "Sample Document",
            "author": "Test Author",
            "genre": "Fiction",
            "date_written": "2023-01-01",
        }
    }

    # Create the document from the template
    result = box_docgen_create_single_file_from_user_input(
        client=box_client_ccg,
        docgen_template_id=template_file_id,
        destination_folder_id=destination_folder_id,
        user_input=sample_user_input,
        output_type=output_type,
    )

    # Check if the document creation was successful
    assert "error" not in result, f"Error creating document: {result['error']}"
    assert "message" in result, "Document creation did not return a success message"
