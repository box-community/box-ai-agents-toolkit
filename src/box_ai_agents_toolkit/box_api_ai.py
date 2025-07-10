import json
from typing import Dict, Iterable, List, Optional

from box_sdk_gen import (
    BoxAPIError,
    AiAgentAsk,
    AiAgentAskTypeField,
    AiAgentBasicTextTool,
    AiAgentExtract,
    AiAgentExtractTypeField,
    AiAgentLongTextTool,
    AiExtractResponse,
    AiItemAskTypeField,
    AiItemBase,
    AiItemBaseTypeField,
    AiResponse,
    AiResponseFull,
    BoxClient,
    CreateAiAskMode,
    CreateAiExtractStructuredFields,
    CreateAiExtractStructuredFieldsOptionsField,
    AiAgentReference,
    AiAgentReferenceTypeField,
)

from box_ai_agents_toolkit.box_api_file import box_file_get_by_id
from box_ai_agents_toolkit.box_api_util_classes import BoxFileExtended


def box_ai_ask_file_single(
    client: BoxClient, file_id: str, prompt: str, ai_agent_id: Optional[str] = None
) -> Dict:
    """Ask a question about a file using AI.
    Args:
        client (BoxClient): The Box client instance.
        file_id (str): The ID of the file to ask about, example: "1234567890".
        prompt (str): The question to ask.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for the question. If None, the default AI agent will be used.

    Returns:
        Dict: The AI response containing the answer to the question.
    """
    ai_agent = None
    if ai_agent_id is not None:
        ai_agent = AiAgentReference(
            AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )

    mode = CreateAiAskMode.SINGLE_ITEM_QA
    ai_item = AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE)
    try:
        response: AiResponseFull = client.ai.create_ai_ask(
            mode=mode, prompt=prompt, items=[ai_item], ai_agent=ai_agent
        )
        return response.to_dict()
    except BoxAPIError as e:
        return {"error": e.message}


def box_ai_ask_file_multi(
    client: BoxClient,
    file_ids: List[str],
    prompt: str,
    ai_agent_id: Optional[str] = None,
) -> Dict:
    """Ask a question about multiple files using AI.
    Args:
        client (BoxClient): The Box client instance.
        file_ids (List[str]): A list of file IDs to ask about, example: ["1234567890", "0987654321"].
        prompt (str): The question to ask.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for the question. If None, the default AI agent will be used.
    Returns:
        Dict: The AI response containing the answers to the questions for each file.
    """
    ai_agent = None
    if ai_agent_id is not None:
        ai_agent = AiAgentReference(
            AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )

    mode = CreateAiAskMode.MULTIPLE_ITEM_QA
    ai_items = []
    for file_id in file_ids:
        ai_items.append(AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE))

    try:
        response: AiResponseFull = client.ai.create_ai_ask(
            mode=mode, prompt=prompt, items=ai_items, ai_agent=ai_agent
        )
        return response.to_dict()
    except BoxAPIError as e:
        return {"error": e.message}


def box_ai_ask_hub(
    client: BoxClient,
    hub_id: str,
    prompt: str,
    ai_agent_id: Optional[str] = None,
) -> Dict:
    """Ask a question about a hub using AI.
    Args:
        client (BoxClient): The Box client instance.
        hub_id (str): The ID of the hub to ask about, example: "1234567890".
        prompt (str): The question to ask.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for the question. If None, the default AI agent will be used.
    Returns:
        Dict: The AI response containing the answer to the question.
    """
    ai_agent = None
    if ai_agent_id is not None:
        ai_agent = AiAgentReference(
            AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )
    mode = CreateAiAskMode.SINGLE_ITEM_QA
    ai_item = AiItemBase(id=hub_id, type=AiItemAskTypeField.HUBS)
    try:
        response: AiResponseFull = client.ai.create_ai_ask(
            mode=mode, prompt=prompt, items=[ai_item], ai_agent=ai_agent
        )
        if response is None:
            return {"message": "No response from Box AI"}
        return response.to_dict()
    except BoxAPIError as e:
        return {"error": e.message}


def box_ai_extract_freeform(
    client: BoxClient,
    file_ids: List[str],
    prompt: str,
    ai_agent_id: Optional[str] = None,
) -> dict:
    """Extract information from one or more files using AI.
    Args:
        client (BoxClient): The Box client instance.
        file_ids (List[str]): A list of file IDs to extract information from, example: ["1234567890", "0987654321"].
        prompt (str): The fields to extract.
        ai_agent_id (Optional[str]): The ID of the AI agent to use for the extraction. If None, the default AI agent will be used.
    Returns:
        dict: The AI response containing the extracted information.
    """
    if len(file_ids) == 0:
        return {"error": "At least one file ID is required"}
    if len(file_ids) >= 20:
        return {"error": "No more than 20 files can be processed at once"}

    ai_agent = None
    if ai_agent_id is not None:
        ai_agent = AiAgentReference(
            AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )
    ai_items = []
    for file_id in file_ids:
        ai_items.append(AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE))
    try:
        response: AiResponse = client.ai.create_ai_extract(
            prompt=prompt, items=ai_items, ai_agent=ai_agent
        )
        return response.to_dict()
    except BoxAPIError as e:
        return {"error": e.message}
