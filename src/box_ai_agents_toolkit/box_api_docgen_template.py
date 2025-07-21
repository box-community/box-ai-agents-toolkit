"""
Wrapper functions for Box Doc Gen Template APIs.
See: https://developer.box.com/reference/v2025.0/
"""

from typing import Any, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    DocGenJobsV2025R0,
    DocGenTagsV2025R0,
    DocGenTemplateV2025R0,
    FileReferenceV2025R0,
)


def box_docgen_template_create(
    client: BoxClient,
    file_id: str,
) -> dict[str, Any]:
    """
    Mark a file as a Box Doc Gen template.

    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to mark as template.

    Returns:
        dict[str, Any]: Metadata of the created template.
    """
    try:
        docgen_template = client.docgen_template.create_docgen_template_v2025_r0(
            FileReferenceV2025R0(id=file_id)
        )
        return docgen_template.to_dict()
    except BoxAPIError as e:
        return {"error": e.message}


def box_docgen_template_list(
    client: BoxClient,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict[str, Any] | list[dict[str, Any]]:
    """
    List all Box Doc Gen templates accessible to the user.

    Args:
        client (BoxClient): Authenticated Box client.
        marker (str, optional): Pagination marker.
        limit (int, optional): Max items per page.

    Returns:
        dict[str, Any] | list[dict[str, Any]]: A list of template metadata or an error message.
    """
    try:
        template_list = client.docgen_template.get_docgen_templates_v2025_r0(
            marker=marker, limit=limit
        )
        if template_list.entries is None:
            return {"message": "No templates found."}

        # Convert entries to a list of dictionaries
        return_list = [
            template_list.entries[i].to_dict()
            for i in range(len(template_list.entries))
        ]
        return return_list
    except BoxAPIError as e:
        return {"error": e.message}


def box_docgen_template_delete(
    client: BoxClient,
    template_id: str,
) -> None:
    """
    Un mark a file as a Box Doc Gen template.

    Args:
        client (BoxClient): Authenticated Box client.
        template_id (str): ID of the template to delete.
    """
    client.docgen_template.delete_docgen_template_by_id_v2025_r0(template_id)


def box_docgen_template_get_by_id(
    client: BoxClient,
    template_id: str,
) -> DocGenTemplateV2025R0:
    """
    Retrieve details of a specific Box Doc Gen template.

    Args:
        client (BoxClient): Authenticated Box client.
        template_id (str): ID of the template.

    Returns:
        DocGenTemplateV2025R0: Detailed template metadata.
    """
    return client.docgen_template.get_docgen_template_by_id_v2025_r0(template_id)


def box_docgen_template_list_tags(
    client: BoxClient,
    template_id: str,
    template_version_id: Optional[str] = None,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> DocGenTagsV2025R0:
    """
    List all tags for a Box Doc Gen template.

    Args:
        client (BoxClient): Authenticated Box client.
        template_id (str): ID of the template.
        template_version_id (str, optional): Specific version ID.
        marker (str, optional): Pagination marker.
        limit (int, optional): Max items per page.

    Returns:
        DocGenTagsV2025R0: A page of tags.
    """
    return client.docgen_template.get_docgen_template_tags_v2025_r0(
        template_id,
        template_version_id=template_version_id,
        marker=marker,
        limit=limit,
    )


def box_docgen_template_list_jobs(
    client: BoxClient,
    template_id: str,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> DocGenJobsV2025R0:
    """
    List Doc Gen jobs that used a specific template.

    Args:
        client (BoxClient): Authenticated Box client.
        template_id (str): ID of the template.
        marker (str, optional): Pagination marker.
        limit (int, optional): Max items per page.

    Returns:
        DocGenJobsV2025R0: A page of Doc Gen jobs for the template.
    """
    return client.docgen_template.get_docgen_template_job_by_id_v2025_r0(
        template_id, marker=marker, limit=limit
    )
