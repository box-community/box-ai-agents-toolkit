"""
Wrapper functions for Box Metadata Templates APIs.
See: https://developer.box.com/reference#metadata-templates
"""

from typing import Any, Dict, List, Optional

from box_sdk_gen import BoxClient, Metadata, BoxAPIError
from box_sdk_gen.managers.metadata_templates import (
    UpdateMetadataTemplateScope,
)
from box_sdk_gen.schemas.metadata_template import MetadataTemplate
from box_sdk_gen.schemas.metadata_templates import (
    MetadataTemplates,
)


def _box_metadata_template_create(
    client: BoxClient,
    # scope: str,
    display_name: str,
    *,
    template_key: Optional[str] = None,
    # hidden: Optional[bool] = False,
    fields: Optional[List[Dict[str, Any]]] = None,
    # copy_instance_on_item_copy: Optional[bool] = False,
) -> MetadataTemplate:
    """
    Create a new metadata template definition in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        # scope (str): The scope of the template ("enterprise" or "global").
        display_name (str): Human-readable name for the template.
        template_key (str, optional): Key to identify the template.
        # hidden (bool, optional): Whether the template is hidden.
        fields (List[Dict], optional): List of field definitions.
        # copy_instance_on_item_copy (bool, optional): Cascade policy for instances.

    Returns:
        MetadataTemplate: The created metadata template definition.
    """
    scope = "enterprise"  # Default scope, can be changed as needed
    return client.metadata_templates.create_metadata_template(
        scope=scope,
        display_name=display_name,
        template_key=template_key,
        hidden=False,
        fields=fields,
        copy_instance_on_item_copy=False,
    )


def _box_metadata_template_list(
    client: BoxClient,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> MetadataTemplates:
    """
    List metadata template definitions for a given scope.

    Args:
        client (BoxClient): An authenticated Box client.
        scope (str): The scope ("enterprise" or "global").
        marker (str, optional): Pagination marker.
        limit (int, optional): Max items per page.

    Returns:
        MetadataTemplates: A page of metadata template entries.
    """
    return client.metadata_templates.get_enterprise_metadata_templates(
        marker=marker, limit=limit
    )


def _box_metadata_template_update(
    client: BoxClient,
    scope: UpdateMetadataTemplateScope,
    template_key: str,
    request_body: List[Dict[str, Any]],
) -> MetadataTemplate:
    """
    Update a metadata template definition.
    """
    return client.metadata_templates.update_metadata_template(
        scope=scope, template_key=template_key, request_body=request_body
    )


def _box_metadata_template_delete(
    client: BoxClient,
    template_key: str,
) -> None:
    """
    Delete a metadata template definition.
    """
    scope = "enterprise"  # Default scope, can be changed as needed
    client.metadata_templates.delete_metadata_template(
        scope=scope, template_key=template_key
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
) -> Dict:
    """
    Retrieve a metadata template definition by scope and key.
    """
    try:
        return client.metadata_templates.get_metadata_template(
            scope="enterprise", template_key=template_key
        ).to_dict()
    except BoxAPIError as e:
        return {"error": e.message}


def box_metadata_template_get_by_id(
    client: BoxClient,
    template_id: str,
) -> MetadataTemplate:
    """
    Retrieve a metadata template definition by its unique ID.
    """
    return client.metadata_templates.get_metadata_template_by_id(template_id)


def box_metadata_template_get_by_name(
    client: BoxClient,
    display_name: str,
) -> Dict:
    """
    Find a metadata template by its display name within a given scope.

    Args:
        client (BoxClient): An authenticated Box client.
        display_name (str): The display name of the template to search for.

    Returns:
        Optional[MetadataTemplate]: The found metadata template or None if not found.
    """
    templates = _box_metadata_template_list(client)
    for template in templates.entries:
        if template.display_name == display_name:
            return template.to_dict()
    return {"message": "Template not found"}


def box_metadata_set_instance_on_file(
    client: BoxClient,
    template_key: str,
    file_id: str,
    metadata: Dict[str, Any],
) -> Metadata:
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
        Metadata: The created metadata instance on the file.
    """
    return client.file_metadata.create_file_metadata_by_id(
        file_id=file_id,
        scope="enterprise",
        template_key=template_key,
        request_body=metadata,
    )


def box_metadata_get_instance_on_file(
    client: BoxClient,
    file_id: str,
    template_key: str,
) -> Optional[Metadata]:
    """
    Get the metadata template instance associated with a specific file.

    Args:
        client (BoxClient): An authenticated Box client.
        file_id (str): The ID of the file to check.
        template_key (str): The key of the metadata template to retrieve.

    Returns:
        Optional[MetadataTemplate]: The metadata template instance or None if not found.
    """
    metadata = client.file_metadata.get_file_metadata_by_id(
        file_id=file_id, scope="enterprise", template_key=template_key
    )
    return metadata
