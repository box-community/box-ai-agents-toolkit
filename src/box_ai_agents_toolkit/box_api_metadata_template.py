"""
Wrapper functions for Box Metadata Templates APIs.
See: https://developer.box.com/reference#metadata-templates
"""
from typing import Any, Dict, List, Optional

from box_sdk_gen import BoxClient
from box_sdk_gen.managers.metadata_templates import (
    DeleteMetadataTemplateScope,
    GetMetadataTemplateScope,
    UpdateMetadataTemplateScope,
)
from box_sdk_gen.schemas.metadata_template import MetadataTemplate
from box_sdk_gen.schemas.metadata_templates import MetadataTemplates


def box_metadata_template_create(
    client: BoxClient,
    scope: str,
    display_name: str,
    *,
    template_key: Optional[str] = None,
    hidden: Optional[bool] = None,
    fields: Optional[List[Dict[str, Any]]] = None,
    copy_instance_on_item_copy: Optional[bool] = None,
) -> MetadataTemplate:
    """
    Create a new metadata template definition in Box.

    Args:
        client (BoxClient): An authenticated Box client.
        scope (str): The scope of the template ("enterprise" or "global").
        display_name (str): Human-readable name for the template.
        template_key (str, optional): Key to identify the template.
        hidden (bool, optional): Whether the template is hidden.
        fields (List[Dict], optional): List of field definitions.
        copy_instance_on_item_copy (bool, optional): Cascade policy for instances.

    Returns:
        MetadataTemplate: The created metadata template definition.
    """
    return client.metadata_templates.create_metadata_template(
        scope=scope,
        display_name=display_name,
        template_key=template_key,
        hidden=hidden,
        fields=fields,
        copy_instance_on_item_copy=copy_instance_on_item_copy,
    )


def box_metadata_template_list(
    client: BoxClient,
    scope: str,
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
    scope_lower = scope.lower()
    if scope_lower == GetMetadataTemplateScope.ENTERPRISE.value:
        return client.metadata_templates.get_enterprise_metadata_templates(
            marker=marker, limit=limit
        )
    if scope_lower == GetMetadataTemplateScope.GLOBAL.value:
        return client.metadata_templates.get_global_metadata_templates(
            marker=marker, limit=limit
        )
    raise ValueError(f"Invalid scope '{scope}'. Must be 'enterprise' or 'global'.")


def box_metadata_template_get(
    client: BoxClient,
    scope: GetMetadataTemplateScope,
    template_key: str,
) -> MetadataTemplate:
    """
    Retrieve a metadata template definition by scope and key.
    """
    return client.metadata_templates.get_metadata_template(scope, template_key)


def box_metadata_template_get_by_id(
    client: BoxClient,
    template_id: str,
) -> MetadataTemplate:
    """
    Retrieve a metadata template definition by its unique ID.
    """
    return client.metadata_templates.get_metadata_template_by_id(template_id)


def box_metadata_template_update(
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


def box_metadata_template_delete(
    client: BoxClient,
    scope: DeleteMetadataTemplateScope,
    template_key: str,
) -> None:
    """
    Delete a metadata template definition.
    """
    client.metadata_templates.delete_metadata_template(scope, template_key)


def box_metadata_template_list_by_instance_id(
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