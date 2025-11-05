"""
Wrapper functions for Box Metadata Templates APIs.
See: https://developer.box.com/reference#metadata-templates
"""

from typing import Any, Dict, List, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    CreateFileMetadataByIdScope,
    CreateMetadataTemplateFields,
    CreateMetadataTemplateFieldsOptionsField,
    CreateMetadataTemplateFieldsTypeField,
    DeleteFileMetadataByIdScope,
    DeleteMetadataTemplateScope,
    GetFileMetadataByIdScope,
    GetMetadataTemplateScope,
    MetadataTemplate,
    MetadataTemplates,
    UpdateFileMetadataByIdScope,
)


def _box_metadata_template_create(
    client: BoxClient,
    display_name: str,
    fields: List[CreateMetadataTemplateFields] | None = None,
    copy_instance_on_item_copy: bool | None = None,
    template_key: Optional[str] = None,
) -> MetadataTemplate:
    """
    Create a new metadata template definition in Box.
    Args:
        client (BoxClient): An authenticated Box client.
        display_name (str): Human-readable name for the template.
        template_key (str, optional): Key to identify the template.
        fields (List[CreateMetadataTemplateFields], optional): List of field definitions.
    Returns:
        MetadataTemplate: The created metadata template definition.
    """
    return client.metadata_templates.create_metadata_template(
        scope="enterprise",  # Default scope
        display_name=display_name,
        fields=fields,
        copy_instance_on_item_copy=copy_instance_on_item_copy or False,
        template_key=template_key,
    )


def box_metadata_template_create(
    client: BoxClient,
    display_name: str,
    fields: List[Dict[str, Any]],
    *,
    template_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new metadata template definition in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        display_name (str): Human-readable name for the template.
        template_key (str, optional): Key to identify the template.
        fields (List[Dict], optional): List of field definitions.
        Example:{"displayName": "Customer",
                "fields": [
                    {
                    "type": "string",
                    "key": "name",
                    "displayName": "Name",
                    "description": "The customer name",
                    "hidden": false
                    },
                    {
                    "type": "date",
                    "key": "last_contacted_at",
                    "displayName": "Last Contacted At",
                    "description": "When this customer was last contacted at",
                    "hidden": false
                    },
                    {
                    "key": "totalAmount",
                    "type": "float",
                    "description": "Final amount paid",
                    "displayName": "Total Amount"
                    },
                    {
                    "type": "enum",
                    "key": "industry",
                    "displayName": "Industry",
                    "options": [
                        {"key": "Technology"},
                        {"key": "Healthcare"},
                        {"key": "Legal"}
                    ]
                    },
                    {
                    "type": "multiSelect",
                    "key": "role",
                    "displayName": "Contact Role",
                    "options": [
                        {"key": "Developer"},
                        {"key": "Business Owner"},
                        {"key": "Marketing"},
                        {"key": "Legal"},
                        {"key": "Sales"}
                    ]
                    }
                ]
                }

    Returns:
        Dict[str, Any]: The created metadata template definition or error message.
    """
    metadata_template_fields: List[CreateMetadataTemplateFields] = []

    for field in fields:
        options: List[CreateMetadataTemplateFieldsOptionsField] = []
        if "options" in field:
            for option in field["options"]:
                options.append(
                    CreateMetadataTemplateFieldsOptionsField(
                        key=option["key"],
                    )
                )
        type = CreateMetadataTemplateFieldsTypeField(field["type"])

        metadata_template_fields.append(
            CreateMetadataTemplateFields(
                type=type,
                key=field.get("key"),
                display_name=field.get("displayName"),
                description=field.get("description", None),
                hidden=field.get("hidden", False),
                options=options if options else None,
            )
        )
    try:
        response = _box_metadata_template_create(
            client=client,
            display_name=display_name,
            fields=metadata_template_fields,
            template_key=template_key,
        )
        return {"metadata_template": response.to_dict()}
    except BoxAPIError as e:
        return {"error": e.message}


def box_metadata_template_list(
    client: BoxClient,
    limit: Optional[int] = 1000,
) -> Dict[str, Any]:
    """
    List metadata template definitions for a given scope.

    Args:
        client (BoxClient): An authenticated Box client.
        limit (int, optional): Max items per page.

    Returns:
        Dict[str, Any]: List of metadata template definitions or error message.
    """

    marker = None

    try:
        templates = client.metadata_templates.get_enterprise_metadata_templates(
            limit=limit
        )
        if templates.entries is None:
            return {"message": "No templates found"}
        else:
            result = [template.to_dict() for template in templates.entries]

        if templates.next_marker:
            marker = templates.next_marker
            while marker:
                templates = client.metadata_templates.get_enterprise_metadata_templates(
                    limit=limit, marker=marker
                )
                if templates.entries:
                    result.extend(
                        [template.to_dict() for template in templates.entries]
                    )
                marker = templates.next_marker

    except BoxAPIError as e:
        return {"error": e.message}

    return {"metadata_templates": result}


# def _box_metadata_template_update(
#     client: BoxClient,
#     scope: UpdateMetadataTemplateScope,
#     template_key: str,
#     request_body: List[Dict[str, Any]],
# ) -> MetadataTemplate:
#     """
#     Update a metadata template definition.
#     """
#     formalize_request_body: List[UpdateMetadataTemplateRequestBody]=[]
#     for item in request_body:
#         formalize_request_body.append(
#             UpdateMetadataTemplateRequestBody(
#                 op=item["op"],
#                 path=item["path"],
#                 value=item.get("value"),
#             )
#         )
#     return client.metadata_templates.update_metadata_template(
#         scope=scope, template_key=template_key, request_body=request_body
#     )


def _box_metadata_template_delete(
    client: BoxClient,
    template_key: str,
) -> None:
    """
    Delete a metadata template definition.
    """
    client.metadata_templates.delete_metadata_template(
        scope=DeleteMetadataTemplateScope.ENTERPRISE, template_key=template_key
    )


def _box_metadata_template_list_by_instance_id(
    client: BoxClient,
    metadata_instance_id: str,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> MetadataTemplates:
    """
    List metadata template definitions associated with a specific metadata instance.
    """
    return client.metadata_templates.get_metadata_templates_by_instance_id(
        metadata_instance_id, marker=marker, limit=limit
    )


def box_metadata_template_get_by_key(
    client: BoxClient,
    template_key: str,
) -> Dict[str, Any]:
    """
    Retrieve a metadata template definition by scope and key.
    """
    try:
        response = client.metadata_templates.get_metadata_template(
            scope=GetMetadataTemplateScope.ENTERPRISE, template_key=template_key
        )
        return {"metadata_template": response.to_dict()}
    except BoxAPIError as e:
        return {"error": e.message}


def box_metadata_template_get_by_id(
    client: BoxClient,
    template_id: str,
) -> Dict[str, Any]:
    """
    Retrieve a metadata template definition by its unique ID.
    """
    try:
        response = client.metadata_templates.get_metadata_template_by_id(template_id)
        return {"metadata_template": response.to_dict()}
    except BoxAPIError as e:
        return {"error": e.message}


def box_metadata_template_get_by_name(
    client: BoxClient,
    display_name: str,
) -> Dict[str, Any]:
    """
    Find a metadata template by its display name within a given scope.

    Args:
        client (BoxClient): An authenticated Box client.
        display_name (str): The display name of the template to search for.

    Returns:
        Dict[str, Any]: The metadata template definition or a not found message.
    """
    templates = box_metadata_template_list(client).get("metadata_templates", None)
    if templates is None:
        return {"message": "No templates found"}

    for template in templates:
        if template["displayName"].lower() == display_name.lower():
            return {"metadata_template": template}
    return {"message": "Template not found"}


def box_metadata_set_instance_on_file(
    client: BoxClient,
    template_key: str,
    file_id: str,
    metadata: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Set a metadata template instance on a specific file.

    Args:
        client (BoxClient): An authenticated Box client.
        template_key (str): The key of the metadata template to set.
        file_id (str): The ID of the file to set the metadata on.
        metadata (Dict[str, Any]): The metadata instance to set, as a dictionary.
        Metadata example:
        {'test_field': 'Test Value', 'date_field': '2023-10-01T00:00:00.000Z', 'float_field': 3.14, 'enum_field': 'option1', 'multiselect_field': ['option1', 'option2']}

    Returns:
        Dict[str, Any]: The created metadata instance on the file.
    """
    try:
        resp = client.file_metadata.create_file_metadata_by_id(
            file_id=file_id,
            scope=CreateFileMetadataByIdScope(GetFileMetadataByIdScope.ENTERPRISE),
            template_key=template_key,
            request_body=metadata,
        )
        return {"metadata_instance": resp.to_dict()}
    except BoxAPIError as e:
        return {"error": e.message}


def box_metadata_get_instance_on_file(
    client: BoxClient,
    file_id: str,
    template_key: str,
) -> Dict[str, Any]:
    """
    Get the metadata template instance associated with a specific file.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to check.
        template_key (str): The key of the metadata template to retrieve.

    Returns:
        Dict[str, Any]: The metadata template instance or None if not found.
    """
    try:
        resp = client.file_metadata.get_file_metadata_by_id(
            file_id=file_id,
            scope=GetFileMetadataByIdScope.ENTERPRISE,
            template_key=template_key,
        )
        return {"metadata_instance": resp.to_dict()}
    except BoxAPIError as e:
        return {"error": e.message}


def box_metadata_update_instance_on_file(
    client: BoxClient,
    file_id: str,
    template_key: str,
    metadata: Dict[str, Any],
    remove_non_included_data: bool = False,
) -> Dict[str, Any]:
    """
    Update the metadata template instance associated with a specific file.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to update metadata on.
        template_key (str): The key of the metadata template to update.
        metadata (Dict[str, Any]): The updated metadata instance.
        remove_non_included_data (bool): If True, remove data from fields not included in the metadata.

    Returns:
        Dict[str, Any]: The updated metadata instance or error message.
    """
    # Read existing metadata instance
    existing_metadata = box_metadata_get_instance_on_file(
        client, file_id=file_id, template_key=template_key
    )
    if "error" in existing_metadata:
        return existing_metadata
    existing_metadata = existing_metadata.get("metadata_instance", {})
    existing_extra_data = existing_metadata.get("extra_data", {})
    # Compare each field and update only if necessary
    # each field in metadata should be a key-value pair
    # with an additional property 'operation' to indicate the operation
    # supported operations are 'replace', 'add', 'remove'
    request_body = []
    for key, value in metadata.items():
        if key in existing_extra_data:
            if value != existing_extra_data[key]:
                request_body.append(
                    {"op": "replace", "path": f"/{key}", "value": value}
                )
        else:
            request_body.append({"op": "add", "path": f"/{key}", "value": value})

    # If there are fields to remove, add them to the request body
    if remove_non_included_data:
        for key in existing_extra_data:
            if key not in metadata:
                request_body.append({"op": "remove", "path": f"/{key}"})

    if not request_body:
        return {"message": "No changes to update"}

    try:
        resp = client.file_metadata.update_file_metadata_by_id(
            file_id=file_id,
            scope=UpdateFileMetadataByIdScope.ENTERPRISE,
            template_key=template_key,
            request_body=request_body,
        )
        return {"metadata_instance": resp.to_dict()}
    except BoxAPIError as e:
        return {"error": e.message}


def box_metadata_delete_instance_on_file(
    client: BoxClient,
    file_id: str,
    template_key: str,
) -> Dict[str, Any]:
    """
    Delete the metadata template instance associated with a specific file.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to delete metadata from.
        template_key (str): The key of the metadata template to delete.

    Returns:
        Dict[str, Any]: Confirmation of deletion or error message.
    """
    try:
        client.file_metadata.delete_file_metadata_by_id(
            file_id=file_id,
            scope=DeleteFileMetadataByIdScope.ENTERPRISE,
            template_key=template_key,
        )
        return {"message": "Metadata instance deleted successfully"}
    except BoxAPIError as e:
        return {"error": e.message}
