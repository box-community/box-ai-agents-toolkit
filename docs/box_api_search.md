# Search

Tools for searching Box content and locating files and folders.

## Search for Content

Search across your Box content using keywords and filters.

```python
from box_ai_agents_toolkit import box_search

results = box_search(client, query="contract", limit=10, content_types=["name", "description"])
print("Search results:", results)
```

### Parameters

- `client`: Authenticated Box client
- `query`: Search query string
- `limit`: Maximum number of results to return
- `content_types`: List of content types to search (e.g., "name", "description", "file_content")

## Locate Folder by Name

Find a specific folder by name within a parent folder.

```python
from box_ai_agents_toolkit import box_locate_folder_by_name

folder = box_locate_folder_by_name(client, folder_name="Documents", parent_folder_id="0")
print("Found folder:", folder)
```

### Parameters

- `client`: Authenticated Box client
- `folder_name`: Name of the folder to find
- `parent_folder_id`: ID of the parent folder to search within

## Related Modules

- `box_api_search.py` - Search operations
