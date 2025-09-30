import pytest
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

FILE_A_ID = "1918161198980"  # Policy
FILE_B_ID = "1918164583027"  # Claim
HUB_ID = "370336300"
TEMPLATE_KEY = "acmePolicy"  # Example template key for structured extraction


def test_box_ai_ask_file(box_client_ccg: BoxClient):
    """Test the box_ai_ask_file function."""
    response = box_ai_ask_file_single(
        client=box_client_ccg,
        file_id=FILE_A_ID,
        prompt="What is the title of this file?",
    )
    assert isinstance(response, dict)
    assert "error" not in response
    assert "answer" in response
    assert isinstance(response["answer"], str)

    # test with a non existing file
    response = box_ai_ask_file_single(
        client=box_client_ccg,
        file_id="non_existing_file_id",
        prompt="What is the title of this file?",
    )
    assert isinstance(response, dict)
    assert "error" in response

    # test with an empty prompt
    response = box_ai_ask_file_single(
        client=box_client_ccg,
        file_id=FILE_A_ID,
        prompt="",
    )
    assert isinstance(response, dict)
    assert "error" in response


def test_box_ai_ask_file_multi(box_client_ccg: BoxClient):
    """Test the box_ai_ask_file_multi function."""
    response = box_ai_ask_file_multi(
        client=box_client_ccg,
        file_ids=[FILE_A_ID, FILE_B_ID],
        prompt="What is the title of these files?",
    )
    assert isinstance(response, dict)
    assert "error" not in response
    assert "answer" in response
    assert isinstance(response["answer"], str)

    # test with an empty file_ids list
    response = box_ai_ask_file_multi(
        client=box_client_ccg,
        file_ids=[],
        prompt="What is the title of these files?",
    )
    assert isinstance(response, dict)
    assert "error" in response

    # test with duplicated items in file_ids
    response = box_ai_ask_file_multi(
        client=box_client_ccg,
        file_ids=[FILE_A_ID] * 21,
        prompt="What is the title of these files?",
    )
    assert isinstance(response, dict)
    assert "error" in response


def test_box_ai_ask_hub(box_client_ccg: BoxClient):
    """Test the box_ai_ask_hub function."""
    response = box_ai_ask_hub(
        client=box_client_ccg,
        hub_id=HUB_ID,
        prompt="What is the title of this hub?",
    )
    assert isinstance(response, dict)
    assert "error" not in response
    assert "answer" or "message" in response


def test_box_ai_extract_freeform(box_client_ccg: BoxClient):
    """Test the box_ai_extract_freeform function."""
    prompt = "name, policy number, address, claim number, date reported"
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=[FILE_A_ID, FILE_B_ID],
        prompt=prompt,
    )
    assert isinstance(response, dict)
    assert "error" not in response
    assert "answer" in response
    # assert each field is present in the answer from the prompt
    for field in prompt.split(", "):
        assert field in response["answer"]

    # test with an empty file_ids list
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=[],
        prompt=prompt,
    )
    assert isinstance(response, dict)
    assert "error" in response

    prompt = "name, policy number, address"
    # test single file extraction
    response = box_ai_extract_freeform(
        client=box_client_ccg,
        file_ids=[FILE_A_ID],
        prompt=prompt,
    )
    assert isinstance(response, dict)
    assert "error" not in response
    assert "answer" in response
    for field in prompt.split(", "):
        assert field in response["answer"]


def test_box_ai_extract_structured(box_client_ccg: BoxClient):
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
        file_ids=[FILE_A_ID],
        fields=fields,
    )
    assert isinstance(response, dict)
    assert "error" not in response
    metadata = response.get("answer", {})

    # check if fields exits in metadata
    assert metadata.get("name") is not None
    assert metadata.get("number") is not None
    assert metadata.get("effectiveDate") is not None
    assert metadata.get("paymentTerms") is not None
    assert metadata.get("coverageTypes") is not None


def test_box_ai_extract_structured_using_template(box_client_ccg: BoxClient):
    """Test the box_ai_extract_structured_using_template function."""
    response = box_ai_extract_structured_using_template(
        client=box_client_ccg,
        file_ids=[FILE_A_ID],
        template_key=TEMPLATE_KEY,
    )
    assert isinstance(response, dict)
    assert "error" not in response
    metadata = response.get("answer", {})

    # check if fields exits in metadata
    assert metadata.get("name") is not None
    assert metadata.get("number") is not None
    assert metadata.get("effectiveDate") is not None
    assert metadata.get("paymentTerms") is not None


@pytest.mark.skip(
    reason="Skipping enhanced structured extraction tests since API is broken"
)
def test_box_ai_extract_structured_enhanced_using_fields(box_client_ccg: BoxClient):
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
        file_ids=[FILE_A_ID],
        fields=fields,
    )
    assert isinstance(response, dict)
    assert "error" not in response
    assert response["ai_agent_info"]["models"][0]["name"] == "google__gemini_2_5_pro"
    metadata = response.get("answer", {})

    # check if fields exits in metadata
    assert metadata.get("name") is not None
    assert metadata.get("number") is not None


@pytest.mark.skip(
    reason="Skipping enhanced structured extraction tests since API is broken"
)
def test_box_ai_extract_structured_enhanced_using_template(box_client_ccg: BoxClient):
    """Test the box_ai_extract_structured_enhanced_using_template function."""
    response = box_ai_extract_structured_enhanced_using_template(
        client=box_client_ccg,
        file_ids=[FILE_A_ID],
        template_key=TEMPLATE_KEY,
    )
    assert isinstance(response, dict)
    assert "error" not in response
    assert response["ai_agent_info"]["models"][0]["name"] == "google__gemini_2_5_pro"
    metadata = response.get("answer", {})

    # check if fields exits in metadata
    assert metadata.get("name") is not None
    assert metadata.get("number") is not None
    assert metadata.get("effectiveDate") is not None
    assert metadata.get("paymentTerms") is not None
