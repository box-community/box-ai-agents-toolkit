from typing import List

from box_sdk_gen import (
    BoxClient,
    File,
    Folder,
    SearchForContentContentTypes,
    SearchForContentType,
)


def box_search(
    client: BoxClient,
    query: str,
    file_extensions: List[str] | None = None,
    content_types: List[SearchForContentContentTypes] | None = None,
    ancestor_folder_ids: List[str] | None = None,
) -> List[File]:
    # content_types: List[SearchForContentContentTypes] = [
    #     SearchForContentContentTypes.NAME,
    #     SearchForContentContentTypes.DESCRIPTION,
    #     # SearchForContentContentTypes.FILE_CONTENT,
    #     SearchForContentContentTypes.COMMENTS,
    #     SearchForContentContentTypes.TAG,
    # ]
    type = [
        SearchForContentType.FILE,
    ]
    fields: List[str] = ["id", "name", "type", "size", "description"]

    search_results = client.search.search_for_content(
        query=query,
        file_extensions=file_extensions,
        ancestor_folder_ids=ancestor_folder_ids,
        content_types=content_types,
        type=type,
        fields=fields,
    )
    return search_results.entries


def box_locate_folder_by_name(
    client: BoxClient, folder_name: str, parent_folder_id: str = "0"
) -> List[Folder]:
    type = [
        SearchForContentType.FOLDER,
    ]
    fields: List[str] = ["id", "name", "type"]

    content_types: List[SearchForContentContentTypes] = [
        SearchForContentContentTypes.NAME,
    ]

    search_results = client.search.search_for_content(
        query=folder_name,
        # file_extensions=file_extensions,
        ancestor_folder_ids=parent_folder_id,
        content_types=content_types,
        type=type,
        fields=fields,
    )
    return search_results.entries
