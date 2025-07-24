"""
Wrapper functions for Box Doc Gen (document generation) APIs.
See: https://developer.box.com/reference/v2025.0/
"""

from typing import Any, Dict, List, Optional

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    CreateDocgenBatchV2025R0DestinationFolder,
    DocGenDocumentGenerationDataV2025R0,
    FileReferenceV2025R0,
)


def box_docgen_create_batch(
    client: BoxClient,
    docgen_template_id: str,
    destination_folder_id: str,
    document_generation_data: List[Dict[str, Any]],
    output_type: str = "pdf",
) -> dict[str, Any]:
    """
    Create a new Box Doc Gen batch to generate documents from a template.

    Args:
        client (BoxClient): Authenticated Box client.
        docgen_template_id (str): ID of the Doc Gen template.
        destination_folder_id (str): ID of the folder to save the generated document.
        document_generation_data (List[Dict[str, Any]]): Data for document generation.
        example:
            [
                {
                    "generated_file_name": "Image test",
                    "user_input": {
                        "order": {
                            "id": "12305",
                            "date": "18-08-2023",
                            "products": [
                                {
                                    "id": 1,
                                    "name": "A4 Papers",
                                    "type": "non-fragile",
                                    "quantity": 100,
                                    "price": 29,
                                    "amount": 2900
                                },
                            ]
                        }
                    }
                },
            ]
        output_type (str): Output file type (only, "pdf" or "docx").

    Returns:
        dict[str, Any]: Response containing batch creation status and details.
        If successful, contains a message with batch ID.
        If an error occurs, contains an "error" key with the error message.
    """
    # Prepare SDK model instances
    file_ref = FileReferenceV2025R0(id=docgen_template_id)
    dest_folder = CreateDocgenBatchV2025R0DestinationFolder(id=destination_folder_id)
    data_items: List[DocGenDocumentGenerationDataV2025R0] = []
    for item in document_generation_data:
        generated_file_name = item.get("generated_file_name")
        if not isinstance(generated_file_name, str):
            return {"error": "generated_file_name must be a string and cannot be None"}
        user_input = item.get("user_input")
        if not isinstance(user_input, dict):
            return {"error": "user_input must be a dict and cannot be None"}
        data_items.append(
            DocGenDocumentGenerationDataV2025R0(
                generated_file_name=generated_file_name,
                user_input=user_input,
            )
        )
    try:
        docgen_batch = client.docgen.create_docgen_batch_v2025_r0(
            file=file_ref,
            input_source="api",
            destination_folder=dest_folder,
            output_type=output_type,
            document_generation_data=data_items,
        )
        return {"message": f"Batch created successfully with id {docgen_batch.id}"}
    except BoxAPIError as e:
        return {"error": e.message}


def box_docgen_create_single_file_from_user_input(
    client: BoxClient,
    docgen_template_id: str,
    destination_folder_id: str,
    user_input: dict[str, Any],
    generated_file_name: Optional[str] = None,
    output_type: str = "pdf",
) -> dict[str, Any]:
    """
    Create a single document from a Doc Gen template using user input.

    Args:
        client (BoxClient): Authenticated Box client.
        docgen_template_id (str): ID of the Doc Gen template.
        destination_folder_id (str): ID of the folder to save the generated document.
        user_input (dict[str, Any]): User input data for document generation.
        example:
        example:
            {
                "user_input": {
                    "order": {
                        "id": "12305",
                        "date": "18-08-2023",
                        "products": [
                            {
                                "id": 1,
                                "name": "A4 Papers",
                                "type": "non-fragile",
                                "quantity": 100,
                                "price": 29,
                                "amount": 2900
                            },
                        ]
                    }
                }
            }
        generated_file_name (Optional[str]): Name for the generated document file.
        output_type (str): Output file type (only, "pdf" or "docx").

    Returns:
        dict[str, Any]: Information about the created batch job.
    """

    # Default generated file name
    try:
        docgen_template_file = client.files.get_file_by_id(docgen_template_id)
    except BoxAPIError as e:
        return {"error": f"Failed to retrieve template file: {e.message}"}

    gen_name = generated_file_name or docgen_template_file.name

    doc_data_list = [{"generated_file_name": gen_name, "user_input": user_input}]
    return box_docgen_create_batch(
        client=client,
        docgen_template_id=docgen_template_id,
        destination_folder_id=destination_folder_id,
        output_type=output_type,
        document_generation_data=doc_data_list,
    )


def box_docgen_list_jobs_by_batch(
    client: BoxClient,
    batch_id: str,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    """
    List Doc Gen jobs in a specific batch.

    Args:
        client (BoxClient): Authenticated Box client.
        batch_id (str): ID of the Doc Gen batch.
        marker (str, optional): Pagination marker.
        limit (int, optional): Maximum number of items to return.

    Returns:
        list[dict[str, Any]]: A list of Doc Gen jobs in the batch.
    """
    try:
        docgen_batch_jobs_list = client.docgen.get_docgen_batch_job_by_id_v2025_r0(
            batch_id=batch_id, marker=marker, limit=limit
        )
        docgen_batch_jobs = (
            [job.to_dict() for job in docgen_batch_jobs_list.entries]
            if docgen_batch_jobs_list.entries
            else []
        )
        if len(docgen_batch_jobs) == 0:
            return [{"message": "No jobs found in the specified batch."}]
        return docgen_batch_jobs
    except BoxAPIError as e:
        return [{"error": e.message}]


def box_docgen_get_job_by_id(
    client: BoxClient,
    job_id: str,
) -> dict[str, Any]:
    """
    Retrieve a Box Doc Gen job by its ID.

    Args:
        client (BoxClient): Authenticated Box client.
        job_id (str): ID of the Doc Gen job.

    Returns:
        dict[str, Any]: Details of the specified Doc Gen job.
    """
    # marker and limit are not used for this endpoint, but included for signature consistency
    try:
        docgen_job = client.docgen.get_docgen_job_by_id_v2025_r0(job_id)
        return docgen_job.to_dict() if docgen_job else {"error": "Job not found."}
    except BoxAPIError as e:
        return {"error": f"Failed to retrieve job: {e.message}"}


def box_docgen_list_jobs(
    client: BoxClient,
    marker: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    """
    List all Box Doc Gen jobs for the current user.

    Args:
        client (BoxClient): Authenticated Box client.
        marker (str, optional): Pagination marker.
        limit (int, optional): Maximum number of items to return.

    Returns:
        list[dict[str, Any]]: A list of Doc Gen jobs.
    """
    try:
        docgen_jobs_list = client.docgen.get_docgen_jobs_v2025_r0(
            marker=marker, limit=limit
        )
        docgen_jobs = (
            [job.to_dict() for job in docgen_jobs_list.entries]
            if docgen_jobs_list.entries
            else []
        )
        return docgen_jobs if docgen_jobs else [{"message": "No jobs found."}]
    except BoxAPIError as e:
        return [{"error": e.message}]
