"""
Wrapper functions for Box Doc Gen (document generation) APIs.
See: https://developer.box.com/reference/v2025.0/
"""
from typing import Any, Dict, List, Optional, Union

from box_sdk_gen import (
    BoxClient,
    CreateDocgenBatchV2025R0DestinationFolder,
    DocGenBatchBaseV2025R0,
    DocGenDocumentGenerationDataV2025R0,
    DocGenJobsFullV2025R0,
    DocGenJobsV2025R0,
    DocGenJobV2025R0,
    FileReferenceV2025R0,
)


def box_docgen_get_job_by_id(
    client: BoxClient,
    job_id: str,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> DocGenJobV2025R0:
    """
    Retrieve a Box Doc Gen job by its ID.

    Args:
        client (BoxClient): Authenticated Box client.
        job_id (str): ID of the Doc Gen job.
        marker (str, optional): Pagination marker (unused for single job).
        limit (int, optional): Pagination limit (unused for single job).

    Returns:
        DocGenJobV2025R0: Details of the specified Doc Gen job.
    """
    # marker and limit are not used for this endpoint, but included for signature consistency
    return client.docgen.get_docgen_job_by_id_v2025_r0(job_id)


def box_docgen_list_jobs(
    client: BoxClient,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> DocGenJobsFullV2025R0:
    """
    List all Box Doc Gen jobs for the current user.

    Args:
        client (BoxClient): Authenticated Box client.
        marker (str, optional): Pagination marker.
        limit (int, optional): Maximum number of items to return.

    Returns:
        DocGenJobsFullV2025R0: A page of Doc Gen job entries.
    """
    return client.docgen.get_docgen_jobs_v2025_r0(marker=marker, limit=limit)


def box_docgen_list_jobs_by_batch(
    client: BoxClient,
    batch_id: str,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> DocGenJobsV2025R0:
    """
    List Doc Gen jobs in a specific batch.

    Args:
        client (BoxClient): Authenticated Box client.
        batch_id (str): ID of the Doc Gen batch.
        marker (str, optional): Pagination marker.
        limit (int, optional): Maximum number of items to return.

    Returns:
        DocGenJobsV2025R0: A list of Doc Gen jobs in the batch.
    """
    return client.docgen.get_docgen_batch_job_by_id_v2025_r0(
        batch_id=batch_id, marker=marker, limit=limit
    )


def box_docgen_create_batch(
    client: BoxClient,
    file_id: str,
    input_source: str,
    destination_folder_id: str,
    output_type: str,
    document_generation_data: List[Dict[str, Any]],
) -> DocGenBatchBaseV2025R0:
    """
    Create a new Box Doc Gen batch to generate documents from a template.

    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file (template) to use.
        input_source (str): Source of input (e.g., "api").
        destination_folder_id (str): ID of the folder to save generated docs.
        output_type (str): Desired output file type (e.g., "pdf").
        document_generation_data (List[Dict]):
            List of dicts with keys:
                - "generated_file_name" (str)
                - "user_input" (Dict[str, Any])

    Returns:
        DocGenBatchBaseV2025R0: Information about the created batch job.
    """
    # Prepare SDK model instances
    file_ref = FileReferenceV2025R0(id=file_id)
    dest_folder = CreateDocgenBatchV2025R0DestinationFolder(id=destination_folder_id)
    data_items: List[DocGenDocumentGenerationDataV2025R0] = []
    for item in document_generation_data:
        data_items.append(
            DocGenDocumentGenerationDataV2025R0(
                generated_file_name=item.get("generated_file_name"),
                user_input=item.get("user_input"),
            )
        )
    return client.docgen.create_docgen_batch_v2025_r0(
        file=file_ref,
        input_source=input_source,
        destination_folder=dest_folder,
        output_type=output_type,
        document_generation_data=data_items,
    )
  
def box_docgen_create_batch_from_user_input(
    client: BoxClient,
    file_id: str,
    destination_folder_id: str,
    user_input: Union[str, Dict[str, Any], List[Dict[str, Any]]],
    generated_file_name: Optional[str] = None,
    output_type: str = "pdf",
) -> DocGenBatchBaseV2025R0:
    """
    Parse a raw user_input string (JSON or key-value pairs) into the required
    document_generation_data list and invoke box_docgen_create_batch.

    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the template file in Box.
        destination_folder_id (str): ID of the folder to save generated docs.
        user_input (str): JSON string or key-value pairs (e.g. 'key1: val1, key2: val2').
        generated_file_name (str, optional): Base name for generated documents.
            Defaults to 'DocGen Output' if None.
        output_type (str): Output file type (e.g. 'pdf').

    Returns:
        DocGenBatchBaseV2025R0: Information about the created batch job.
    """
    import json
    import re

    # Default generated file name
    gen_name = generated_file_name or "DocGen Output"
    # If user_input already provided as dict or list, build document_generation_data directly
    if isinstance(user_input, dict):
        doc_data_list = [{"generated_file_name": gen_name, "user_input": user_input}]
        return box_docgen_create_batch(
            client=client,
            file_id=file_id,
            input_source="api",
            destination_folder_id=destination_folder_id,
            output_type=output_type,
            document_generation_data=doc_data_list,
        )
    if isinstance(user_input, list):
        doc_data_list = []
        for item in user_input:
            if not isinstance(item, dict):
                raise ValueError("List items in user_input must be dicts")
            doc_data_list.append({"generated_file_name": gen_name, "user_input": item})
        return box_docgen_create_batch(
            client=client,
            file_id=file_id,
            input_source="api",
            destination_folder_id=destination_folder_id,
            output_type=output_type,
            document_generation_data=doc_data_list,
        )

    # Attempt JSON parsing first
    try:
        parsed = json.loads(user_input)
        if isinstance(parsed, list):
            doc_data_list = parsed
        elif isinstance(parsed, dict):
            doc_data_list = [{"generated_file_name": gen_name, "user_input": parsed}]
        else:
            raise ValueError("Parsed JSON is not a list or dict")
    except json.JSONDecodeError:
        # Fallback: parse key-value pairs
        kv: Dict[str, Any] = {}
        # split on commas, semicolons, or newlines
        parts = re.split(r"[;,\n]+", user_input)
        for part in parts:
            if ":" in part:
                key, val = part.split(":", 1)
            elif "=" in part:
                key, val = part.split("=", 1)
            elif " - " in part:
                key, val = part.split(" - ", 1)
            else:
                continue
            k = key.strip().lower().replace(" ", "_")
            v = val.strip()
            if k and v:
                kv[k] = v
        if not kv:
            raise ValueError(
                f"Invalid user_input format: '{user_input}'. Provide JSON or key-value pairs."
            )
        doc_data_list = [{"generated_file_name": gen_name, "user_input": kv}]

    # Delegate to core batch creation
    return box_docgen_create_batch(
        client=client,
        file_id=file_id,
        input_source="api",
        destination_folder_id=destination_folder_id,
        output_type=output_type,
        document_generation_data=doc_data_list,
    )