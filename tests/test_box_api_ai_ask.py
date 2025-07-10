from box_ai_agents_toolkit import (
    box_ai_ask_file_single,
    box_ai_ask_file_multi,
    box_ai_ask_hub,
    box_ai_extract_freeform,
)
from box_sdk_gen import BoxClient

FILE_A_ID = "1918161198980"
FILE_B_ID = "1918164583027"
HUB_ID = "370336300"


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
