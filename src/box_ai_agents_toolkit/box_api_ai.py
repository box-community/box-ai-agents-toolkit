import json
from typing import Dict, Iterable

from box_sdk_gen import (
    AiAgentAsk,
    AiAgentAskTypeField,
    AiAgentBasicTextTool,
    AiAgentExtract,
    AiAgentExtractTypeField,
    AiAgentLongTextTool,
    AiExtractResponse,
    AiItemBase,
    AiItemBaseTypeField,
    AiResponse,
    AiResponseFull,
    BoxClient,
    CreateAiAskMode,
    CreateAiExtractStructuredFields,
    CreateAiExtractStructuredFieldsOptionsField,
)

from src.box_ai_agents_toolkit.box_api_file import box_file_get_by_id
from src.box_ai_agents_toolkit.box_api_util_classes import BoxFileExtended


def box_file_ai_ask(
    client: BoxClient, file_id: str, prompt: str, ai_agent: AiAgentAsk = None
) -> Dict:
    mode = CreateAiAskMode.SINGLE_ITEM_QA
    ai_item = AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE)
    response: AiResponseFull = client.ai.create_ai_ask(
        mode=mode, prompt=prompt, items=[ai_item], ai_agent=ai_agent
    )
    return response.to_dict()


def box_file_ai_extract(
    client: BoxClient, file_id: str, prompt: str, ai_agent: AiAgentAsk = None
) -> dict:
    ai_item = AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE)
    response: AiResponse = client.ai.create_ai_extract(
        prompt=prompt, items=[ai_item], ai_agent=ai_agent
    )
    return response.to_dict()


def box_file_ai_extract_structured(
    client: BoxClient, file_id: str, fields_json_str: str
) -> Dict:
    ai_item = AiItemBase(id=file_id, type=AiItemBaseTypeField.FILE)
    fields_list = json.loads(fields_json_str)
    ai_fields = []
    options = []
    for field in fields_list:
        field_options = field.get("options")
        if field_options is not None:
            for option in field.get("options"):
                options.append(
                    CreateAiExtractStructuredFieldsOptionsField(key=option.get("key"))
                )

        ai_fields.append(
            CreateAiExtractStructuredFields(
                key=field.get("key"),
                description=field.get("description"),
                display_name=field.get("display_name"),
                prompt=field.get("prompt"),
                type=field.get("type"),
                options=options if options is not None and len(options) > 0 else None,
            )
        )
    response: AiExtractResponse = client.ai.create_ai_extract_structured(
        items=[ai_item], fields=ai_fields
    )
    return response.to_dict()


def box_folder_ai_ask(
    client: BoxClient,
    folder_id: str,
    prompt: str,
    is_recursive: bool = False,
    by_pass_text_extraction: bool = False,
) -> Iterable[BoxFileExtended]:
    # folder items iterator
    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "file":
            file = box_file_get_by_id(client=client, file_id=item.id)
            if not by_pass_text_extraction:
                ai_response = box_file_ai_ask(
                    client=client, file_id=item.id, prompt=prompt
                )
            else:
                ai_response = {}
            yield BoxFileExtended(
                file=file, text_representation=None, ai_response=ai_response
            )
        elif item.type == "folder" and is_recursive:
            yield from box_folder_ai_ask(
                client=client,
                folder_id=item.id,
                prompt=prompt,
                is_recursive=is_recursive,
                by_pass_text_extraction=by_pass_text_extraction,
            )


def box_folder_ai_extract(
    client: BoxClient,
    folder_id: str,
    prompt: str,
    is_recursive: bool = False,
    by_pass_text_extraction: bool = False,
) -> Iterable[BoxFileExtended]:
    # folder items iterator
    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "file":
            file = box_file_get_by_id(client=client, file_id=item.id)
            if not by_pass_text_extraction:
                ai_response: Dict = box_file_ai_extract(
                    client=client, file_id=item.id, prompt=prompt
                )
            else:
                ai_response = {}
            yield BoxFileExtended(file=file, ai_response=ai_response)
        elif item.type == "folder" and is_recursive:
            yield from box_folder_ai_extract(
                client=client,
                folder_id=item.id,
                prompt=prompt,
                is_recursive=is_recursive,
                by_pass_text_extraction=by_pass_text_extraction,
            )


def box_folder_ai_extract_structured(
    client: BoxClient,
    folder_id: str,
    fields_json_str: str,
    is_recursive: bool = False,
    by_pass_text_extraction: bool = False,
) -> Iterable[BoxFileExtended]:
    # folder items iterator
    for item in client.folders.get_folder_items(folder_id).entries:
        if item.type == "file":
            file = box_file_get_by_id(client=client, file_id=item.id)
            if not by_pass_text_extraction:
                ai_response: Dict = box_file_ai_extract_structured(
                    client=client, file_id=item.id, fields_json_str=fields_json_str
                )
            else:
                ai_response = {}
            yield BoxFileExtended(file=file, ai_response=ai_response)
        elif item.type == "folder" and is_recursive:
            yield from box_folder_ai_extract_structured(
                client=client,
                folder_id=item.id,
                fields_json_str=fields_json_str,
                is_recursive=is_recursive,
                by_pass_text_extraction=by_pass_text_extraction,
            )


def box_claude_ai_agent_ask() -> AiAgentAsk:
    return AiAgentAsk(
        type=AiAgentAskTypeField.AI_AGENT_ASK,
        long_text=AiAgentLongTextTool(
            model="aws__claude_3_7_sonnet",
        ),
        basic_text=AiAgentBasicTextTool(
            model="aws__claude_3_7_sonnet",
        ),
        long_text_multi=AiAgentLongTextTool(
            model="aws__claude_3_7_sonnet",
        ),
        basic_text_multi=AiAgentBasicTextTool(
            model="aws__claude_3_7_sonnet",
        ),
    )


def box_claude_ai_agent_extract() -> AiAgentExtract:
    return AiAgentExtract(
        type=AiAgentExtractTypeField.AI_AGENT_EXTRACT,
        long_text=AiAgentLongTextTool(
            model="aws__claude_3_7_sonnet",
        ),
        basic_text=AiAgentBasicTextTool(
            model="aws__claude_3_7_sonnet",
        ),
    )
