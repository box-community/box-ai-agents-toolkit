# Web Links

Tools for creating and managing web link bookmarks in Box.

## Overview

Web links in Box are bookmarks to external URLs that you can store, organize, and share just like files and folders.

## Create Web Link

```python
from box_ai_agents_toolkit import box_web_link_create

result = box_web_link_create(
    client,
    url="https://www.example.com",
    parent_folder_id="0",
    name="Example Website",
    description="A link to example.com"
)
print("Web link created:", result)
```

### Parameters

- `url` - The URL of the web link
- `parent_folder_id` - ID of the folder to store the web link in
- `name` - Optional name for the web link
- `description` - Optional description

## Get Web Link

Retrieve details of a web link by its ID.

```python
from box_ai_agents_toolkit import box_web_link_get_by_id

result = box_web_link_get_by_id(client, web_link_id="12345")
print("Web link details:", result)
```

## Update Web Link

Update properties of an existing web link.

```python
from box_ai_agents_toolkit import box_web_link_update_by_id

result = box_web_link_update_by_id(
    client,
    web_link_id="12345",
    url="https://www.newexample.com",
    parent_folder_id="67890",
    name="Updated Name",
    description="Updated description"
)
print("Web link updated:", result)
```

### Parameters

- `web_link_id` - ID of the web link to update
- `url` - New URL (optional)
- `parent_folder_id` - New parent folder ID to move the web link (optional)
- `name` - New name (optional)
- `description` - New description (optional)

## Delete Web Link

Delete a web link from Box.

```python
from box_ai_agents_toolkit import box_web_link_delete_by_id

result = box_web_link_delete_by_id(client, web_link_id="12345")
print("Web link deleted:", result)
```

## Use Cases

Web links are useful for:
- Creating bookmarks to frequently accessed websites
- Organizing external resources alongside Box content
- Sharing external URLs with collaborators through Box
- Building content collections that mix files and web resources

## Related Modules

- `box_api_weblink.py` - Web link operations
- See also: [Shared Links](box_api_shared_links.md) for sharing web links
