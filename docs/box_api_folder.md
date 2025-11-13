# Folders

Tools for managing Box folders.

## Overview

This module provides comprehensive folder management capabilities including creating, reading, updating, and deleting folders.

## List Folder Contents

```python
from box_ai_agents_toolkit import box_folder_list_content

contents = box_folder_list_content(client, folder_id="0")
print("Folder contents:", contents)
```

## Create Folder

```python
from box_ai_agents_toolkit import box_create_folder

folder = box_create_folder(client, name="New Folder", parent_id="0")
print("Created folder:", folder)
```

### Parameters

- `name` - Name of the new folder
- `parent_id` - ID of the parent folder (use "0" for root folder)

## Update Folder

Update folder properties like name and description.

```python
from box_ai_agents_toolkit import box_update_folder

updated_folder = box_update_folder(
    client,
    folder_id="12345",
    name="Updated Name",
    description="New description"
)
print("Updated folder:", updated_folder)
```

### Parameters

- `folder_id` - ID of the folder to update
- `name` - New name for the folder (optional)
- `description` - New description for the folder (optional)

## Delete Folder

Delete a folder from Box.

```python
from box_ai_agents_toolkit import box_delete_folder

box_delete_folder(client, folder_id="12345")
print("Folder deleted")
```

## Related Operations

- See [Files](box_api_file.md) for file operations within folders
- See [Search](box_api_search.md) for finding folders by name
- See [Collaborations](box_api_collaborations.md) for sharing folders

## Related Modules

- `box_api_folder.py` - Folder operations
