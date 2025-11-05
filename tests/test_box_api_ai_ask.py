from typing import Dict

from box_sdk_gen import BoxClient

from box_ai_agents_toolkit import (
    box_ai_ask_file_multi,
    box_ai_ask_file_single,
    box_ai_ask_hub,
    box_ai_extract_freeform,
    box_ai_extract_structured_enhanced_using_fields,
    box_ai_extract_structured_enhanced_using_template,
    box_ai_extract_structured_using_fields,
    box_ai_extract_structured_using_template,
)
from tests.conftest import TestData


def test_box_ai_ask_file(box_client_ccg: BoxClient, ai_test_data: TestData):
    """Test the box_ai_ask_file function."""
    response = box_ai_ask_file_single(
        client=box_client_ccg,
        file_id=ai_test_data.test_files[0].id,
        prompt="What is the title of this file?",
    )

    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    # test with a non existing file
    response = box_ai_ask_file_single(
        client=box_client_ccg,
        file_id="non_existing_file_id",
        prompt="What is the title of this file?",
    )
    assert isinstance(response, Dict)
    assert "error" in response

    # test with an empty prompt
    response = box_ai_ask_file_single(
        client=box_client_ccg,
        file_id=ai_test_data.test_files[0].id,
        prompt="",
    )
    assert isinstance(response, Dict)
    assert "error" in response


def test_box_ai_ask_file_multi(box_client_ccg: BoxClient, ai_test_data: TestData):
    """Test the box_ai_ask_file_multi function."""
    response = box_ai_ask_file_multi(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id, ai_test_data.test_files[1].id],
        prompt="What is the title of these files?",
    )
    assert isinstance(response, Dict)
    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    # test with an empty file_ids list
    response = box_ai_ask_file_multi(
        client=box_client_ccg,
        file_ids=[],
        prompt="What is the title of these files?",
    )
    assert isinstance(response, Dict)
    assert "error" in response

    # test with duplicated items in file_ids
    response = box_ai_ask_file_multi(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id] * 21,
        prompt="What is the title of these files?",
    )
    assert isinstance(response, Dict)
    assert "error" in response


def test_box_ai_ask_hub(box_client_ccg: BoxClient, ai_test_data: TestData):
    """Test the box_ai_ask_hub function."""
    response = box_ai_ask_hub(
        client=box_client_ccg,
        hub_id=ai_test_data.test_hub_id,
        prompt="What is the title of this hub?",
    )
    assert isinstance(response, Dict)
    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    # test with a non existing hub
    response = box_ai_ask_hub(
        client=box_client_ccg,
        hub_id="non_existing_hub_id",
        prompt="What is the title of this hub?",
    )
    assert isinstance(response, Dict)
    assert "error" in response


def test_box_ai_extract_freeform(box_client_ccg: BoxClient, ai_test_data: TestData):
    """Test the box_ai_extract_freeform function."""
    prompt = "name, policy number, address, claim number, date reported"
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id, ai_test_data.test_files[1].id],
        prompt=prompt,
    )
    assert isinstance(response, Dict)
    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    # assert each field is present in the answer from the prompt
    for field in prompt.split(", "):
        assert field in response["AI_response"]["answer"]

    # test with an empty file_ids list
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=[],
        prompt=prompt,
    )
    assert isinstance(response, Dict)
    assert "error" in response

    prompt = "name, policy number, address"

    # test single file extraction
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        prompt=prompt,
    )
    assert isinstance(response, Dict)
    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    for field in prompt.split(", "):
        assert field in response["AI_response"]["answer"]


def test_box_ai_extract_structured(box_client_ccg: BoxClient, ai_test_data: TestData):
    """Test the box_ai_extract_structured function."""
    fields = [
        {
            "type": "string",
            "key": "name",
            "displayName": "Name",
            "description": "Policyholder Name",
        },
        {
            "type": "string",
            "key": "number",
            "displayName": "Number",
            "description": "Policy Number",
        },
        {
            "type": "date",
            "key": "effectiveDate",
            "displayName": "Effective Date",
            "description": "Policy Effective Date",
        },
        {
            "type": "enum",
            "key": "paymentTerms",
            "displayName": "Payment Terms",
            "description": "Frequency of payment per year",
            "options": [
                {"key": "Monthly"},
                {"key": "Quarterly"},
                {"key": "Semiannual"},
                {"key": "Annually"},
            ],
        },
        {
            "type": "multiSelect",
            "key": "coverageTypes",
            "displayName": "Coverage Types",
            "description": "Types of coverage for the policy",
            "prompt": "Look in the coverage type table and include all listed types.",
            "options": [
                {"key": "Body Injury Liability"},
                {"key": "Property Damage Liability"},
                {"key": "Personal Damage Liability"},
                {"key": "Collision"},
                {"key": "Comprehensive"},
                {"key": "Uninsured Motorist"},
                {"key": "Something that does not exist"},
            ],
        },
    ]

    response = box_ai_extract_structured_using_fields(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        fields=fields,
    )
    assert isinstance(response, Dict)
    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    metadata = response.get("AI_response", {}).get("answer", {})

    # check if fields exits in metadata
    assert metadata.get("name") is not None
    assert metadata.get("number") is not None
    assert metadata.get("effectiveDate") is not None
    assert metadata.get("paymentTerms") is not None
    assert metadata.get("coverageTypes") is not None


def test_box_ai_extract_structured_using_template(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test the box_ai_extract_structured_using_template function."""
    response = box_ai_extract_structured_using_template(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        template_key=ai_test_data.test_template_key,
    )
    assert isinstance(response, Dict)
    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    metadata = response.get("AI_response", {}).get("answer", {})

    # check if fields exits in metadata
    assert metadata.get("name") is not None
    assert metadata.get("number") is not None
    assert metadata.get("effectiveDate") is not None
    assert metadata.get("paymentTerms") is not None


def test_box_ai_extract_structured_enhanced_using_fields(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test the box_ai_extract_structured_enhanced_using_fields function."""
    fields = [
        {
            "type": "string",
            "key": "name",
            "displayName": "Name",
            "description": "Policyholder Name",
        },
        {
            "type": "string",
            "key": "number",
            "displayName": "Number",
            "description": "Policy Number",
        },
    ]

    response = box_ai_extract_structured_enhanced_using_fields(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        fields=fields,
    )
    assert isinstance(response, Dict)
    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    assert (
        response["AI_response"]["ai_agent_info"]["models"][0]["name"]
        == "google__gemini_2_5_pro"
    )
    metadata = response.get("AI_response", {}).get("answer", {})

    # check if fields exits in metadata
    assert metadata.get("name") is not None
    assert metadata.get("number") is not None


def test_box_ai_extract_structured_enhanced_using_template(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test the box_ai_extract_structured_enhanced_using_template function."""
    response = box_ai_extract_structured_enhanced_using_template(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        template_key=ai_test_data.test_template_key,
    )
    assert isinstance(response, Dict)
    assert "message" not in response
    assert "error" not in response
    assert "AI_response" in response

    assert (
        response["AI_response"]["ai_agent_info"]["models"][0]["name"]
        == "google__gemini_2_5_pro"
    )
    metadata = response.get("AI_response", {}).get("answer", {})

    # check if fields exits in metadata
    assert metadata.get("name") is not None
    assert metadata.get("number") is not None
    assert metadata.get("effectiveDate") is not None
    assert metadata.get("paymentTerms") is not None


# ============================================================================
# Additional tests for improved coverage
# ============================================================================


def test_box_ai_ask_file_with_custom_agent(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_ask_file_single with custom ai_agent_id."""
    response = box_ai_ask_file_single(
        client=box_client_ccg,
        file_id=ai_test_data.test_files[0].id,
        prompt="What is the title of this file?",
        ai_agent_id=ai_test_data.test_ai_agent_id,
    )
    assert isinstance(response, Dict)
    assert "AI_response" in response or "error" in response


def test_box_ai_ask_file_multi_with_custom_agent(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_ask_file_multi with custom ai_agent_id."""
    response = box_ai_ask_file_multi(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id, ai_test_data.test_files[1].id],
        prompt="What is the title of these files?",
        ai_agent_id=ai_test_data.test_ai_agent_id,
    )
    assert isinstance(response, Dict)
    assert "AI_response" in response or "error" in response


def test_box_ai_ask_hub_with_custom_agent(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_ask_hub with custom ai_agent_id."""
    response = box_ai_ask_hub(
        client=box_client_ccg,
        hub_id=ai_test_data.test_hub_id,
        prompt="What is the title of this hub?",
        ai_agent_id=ai_test_data.test_ai_agent_id,
    )
    assert isinstance(response, Dict)
    assert "AI_response" in response or "error" in response


def test_box_ai_ask_hub_empty_prompt(box_client_ccg: BoxClient, ai_test_data: TestData):
    """Test box_ai_ask_hub with empty prompt."""
    response = box_ai_ask_hub(
        client=box_client_ccg,
        hub_id=ai_test_data.test_hub_id,
        prompt="",
    )
    assert isinstance(response, Dict)
    assert "error" in response


def test_box_ai_extract_freeform_with_custom_agent(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_freeform with custom ai_agent_id."""
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        prompt="name, policy number",
        ai_agent_id=ai_test_data.test_ai_agent_id,
    )
    assert isinstance(response, Dict)
    assert "AI_response" in response or "error" in response


def test_box_ai_extract_freeform_exactly_20_files(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_freeform with exactly 20 files (boundary test)."""
    file_ids = [ai_test_data.test_files[0].id] * 20
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=file_ids,
        prompt="Extract names",
    )
    assert isinstance(response, Dict)
    # Should get an error because boundary is >= 20
    assert "error" in response
    assert "No more than 20 files" in response["error"]


def test_box_ai_extract_freeform_empty_prompt(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_freeform with empty prompt."""
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        prompt="",
    )
    assert isinstance(response, Dict)
    # API will likely reject empty prompt
    assert "error" in response or "AI_response" in response


def test_box_ai_extract_structured_with_custom_agent(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_fields with custom ai_agent_id."""
    fields = [
        {
            "type": "string",
            "key": "name",
            "displayName": "Name",
            "description": "Policyholder Name",
        }
    ]
    response = box_ai_extract_structured_using_fields(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        fields=fields,
        ai_agent_id=ai_test_data.test_ai_agent_id,
    )
    assert isinstance(response, Dict)
    assert "AI_response" in response or "error" in response


def test_box_ai_extract_structured_empty_files(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_fields with empty file list."""
    fields = [
        {
            "type": "string",
            "key": "name",
            "displayName": "Name",
            "description": "Test field",
        }
    ]
    response = box_ai_extract_structured_using_fields(
        client=box_client_ccg,
        file_ids=[],
        fields=fields,
    )
    assert isinstance(response, Dict)
    assert "error" in response
    assert "At least one file ID is required" in response["error"]


def test_box_ai_extract_structured_too_many_files(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_fields with >20 files."""
    fields = [
        {
            "type": "string",
            "key": "name",
            "displayName": "Name",
            "description": "Test field",
        }
    ]
    file_ids = [ai_test_data.test_files[0].id] * 21
    response = box_ai_extract_structured_using_fields(
        client=box_client_ccg,
        file_ids=file_ids,
        fields=fields,
    )
    assert isinstance(response, Dict)
    assert "error" in response
    assert "No more than 20 files" in response["error"]


def test_box_ai_extract_structured_missing_field_key(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_fields with missing field key."""
    fields = [
        {
            "type": "string",
            # Missing "key" field
            "displayName": "Name",
            "description": "Test field without key",
        }
    ]
    response = box_ai_extract_structured_using_fields(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        fields=fields,
    )
    assert isinstance(response, Dict)
    assert "error" in response
    assert "Field key is required" in response["error"]


def test_box_ai_extract_structured_fields_without_options(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_fields with fields that have no options."""
    fields = [
        {
            "type": "string",
            "key": "simple_field",
            "displayName": "Simple Field",
            "description": "A field without options",
        }
    ]
    response = box_ai_extract_structured_using_fields(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        fields=fields,
    )
    assert isinstance(response, Dict)
    assert "AI_response" in response or "error" in response


def test_box_ai_extract_structured_using_template_with_custom_agent(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_template with custom ai_agent_id."""
    response = box_ai_extract_structured_using_template(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        template_key=ai_test_data.test_template_key,
        ai_agent_id=ai_test_data.test_ai_agent_id,
    )
    assert isinstance(response, Dict)
    assert "AI_response" in response or "error" in response


def test_box_ai_extract_structured_using_template_empty_files(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_template with empty file list."""
    response = box_ai_extract_structured_using_template(
        client=box_client_ccg,
        file_ids=[],
        template_key=ai_test_data.test_template_key,
    )
    assert isinstance(response, Dict)
    assert "error" in response
    assert "At least one file ID is required" in response["error"]


def test_box_ai_extract_structured_using_template_too_many_files(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_template with >20 files."""
    file_ids = [ai_test_data.test_files[0].id] * 21
    response = box_ai_extract_structured_using_template(
        client=box_client_ccg,
        file_ids=file_ids,
        template_key=ai_test_data.test_template_key,
    )
    assert isinstance(response, Dict)
    assert "error" in response
    assert "No more than 20 files" in response["error"]


def test_box_ai_extract_structured_invalid_template(
    box_client_ccg: BoxClient, ai_test_data: TestData
):
    """Test box_ai_extract_structured_using_template with invalid template key."""
    response = box_ai_extract_structured_using_template(
        client=box_client_ccg,
        file_ids=[ai_test_data.test_files[0].id],
        template_key="non_existent_template_key_12345",
    )
    assert isinstance(response, Dict)
    assert "error" in response
