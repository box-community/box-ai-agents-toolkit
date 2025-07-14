from typing import Any, Dict, List, Optional

from box_sdk_gen import (
    AiAgentReference,
    AiAgentReferenceTypeField,
    AiExtractStructuredResponse,
    AiItemAsk,
    AiItemAskTypeField,
    AiItemBase,
    AiItemBaseTypeField,
    AiResponse,
    AiResponseFull,
    BoxAPIError,
    BoxClient,
    CreateAiAskMode,
    CreateAiExtractStructuredFields,
    CreateAiExtractStructuredFieldsOptionsField,
    CreateAiExtractStructuredMetadataTemplate,
)


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
            type=AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )

    mode = CreateAiAskMode.SINGLE_ITEM_QA
    ai_item = AiItemAsk(id=file_id, type=AiItemAskTypeField.FILE)
    try:
        response: Optional[AiResponseFull] = client.ai.create_ai_ask(
            mode=mode, prompt=prompt, items=[ai_item], ai_agent=ai_agent
        )
        if response is None:
            return {"message": "No response from Box AI"}
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
            type=AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )

    mode = CreateAiAskMode.MULTIPLE_ITEM_QA
    ai_items = []
    for file_id in file_ids:
        ai_items.append(AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE))

    try:
        response: Optional[AiResponseFull] = client.ai.create_ai_ask(
            mode=mode, prompt=prompt, items=ai_items, ai_agent=ai_agent
        )
        if response is None:
            return {"message": "No response from Box AI"}
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
            type=AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )
    mode = CreateAiAskMode.SINGLE_ITEM_QA
    ai_item = AiItemAsk(id=hub_id, type=AiItemAskTypeField.HUBS)
    try:
        response: Optional[AiResponseFull] = client.ai.create_ai_ask(
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
            type=AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
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


def box_ai_extract_structured_using_fields(
    client: BoxClient,
    file_ids: List[str],
    fields: List[dict[str, Any]],
    ai_agent_id: Optional[str] = None,
) -> dict:
    """Extract information from one or more files using AI.
    Args:
        client (BoxClient): The Box client instance.
        file_ids (List[str]): A list of file IDs to extract information from, example: ["1234567890", "0987654321"].
        fields (List[dict[str, str]]): The fields to extract in a structured format.
                        example:[
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
            type=AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )
    ai_items = []
    for file_id in file_ids:
        ai_items.append(AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE))

    # grab the fields from the dict and convert into List[CreateAiExtractStructuredFields]
    # fields_list = fields.get("fields", [])
    structured_fields = []
    options = []
    for field in fields:
        field_options: Optional[List[Dict[str, Any]]] = field.get("options", None)
        if field_options is not None:
            for option in field_options:
                key_value = option.get("key")
                if key_value is not None:
                    options.append(
                        CreateAiExtractStructuredFieldsOptionsField(key=str(key_value))
                    )

        key_value = field.get("key")
        if key_value is None:
            return {"error": "Field key is required"}
        structured_fields.append(
            CreateAiExtractStructuredFields(
                key=str(key_value),
                description=field.get("description"),
                display_name=field.get("displayName"),
                prompt=field.get("prompt"),
                type=field.get("type"),
                options=options if options is not None and len(options) > 0 else None,
            )
        )

    try:
        response: AiExtractStructuredResponse = client.ai.create_ai_extract_structured(
            items=ai_items, fields=structured_fields, ai_agent=ai_agent
        )
        return response.to_dict()
    except BoxAPIError as e:
        return {"error": e.message}


def box_ai_extract_structured_enhanced_using_fields(
    client: BoxClient,
    file_ids: List[str],
    fields: List[dict[str, Any]],
) -> dict:
    """Extract information from one or more files using AI.
    This function is an enhanced version that uses a specific AI agent for structured extraction.
    Args:
        client (BoxClient): The Box client instance.
        file_ids (List[str]): A list of file IDs to extract information from, example: ["1234567890", "0987654321"].
        fields (List[dict[str, str]]): The fields to extract in a structured format.
                        example:[
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
    Returns:
        dict: The AI response containing the extracted information.
    """
    ai_agent_id = "enhanced_extract_agent"

    return box_ai_extract_structured_using_fields(
        client=client,
        file_ids=file_ids,
        fields=fields,
        ai_agent_id=ai_agent_id,
    )


def box_ai_extract_structured_using_template(
    client: BoxClient,
    file_ids: List[str],
    template_key: str,
    ai_agent_id: Optional[str] = None,
) -> dict:
    """Extract information from one or more files using AI with a metadata template.
    Args:
        client (BoxClient): The Box client instance.
        file_ids (List[str]): A list of file IDs to extract information from, example: ["1234567890", "0987654321"].
        template_key (str): The key of the metadata template to use for the extraction.
                            Example: "insurance_policy_template".
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
            type=AiAgentReferenceTypeField.AI_AGENT_ID, id=ai_agent_id
        )
    ai_items = []
    for file_id in file_ids:
        ai_items.append(AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE))

    metadata_template = CreateAiExtractStructuredMetadataTemplate(
        template_key=template_key, scope="enterprise"
    )
    try:
        response: AiExtractStructuredResponse = client.ai.create_ai_extract_structured(
            items=ai_items, metadata_template=metadata_template, ai_agent=ai_agent
        )
        return response.to_dict()
    except BoxAPIError as e:
        return {"error": e.message}


def box_ai_extract_structured_enhanced_using_template(
    client: BoxClient,
    file_ids: List[str],
    template_key: str,
) -> dict:
    """Extract information from one or more files using AI with a metadata template.
    This function is an enhanced version that uses a specific AI agent for structured extraction.
    Args:
        client (BoxClient): The Box client instance.
        file_ids (List[str]): A list of file IDs to extract information from, example: ["1234567890", "0987654321"].
        template_key (str): The key of the metadata template to use for the extraction.
                            Example: "insurance_policy_template".
    Returns:
        dict: The AI response containing the extracted information.
    """

    ai_agent_id = "enhanced_extract_agent"

    return box_ai_extract_structured_using_template(
        client=client,
        file_ids=file_ids,
        template_key=template_key,
        ai_agent_id=ai_agent_id,
    )
