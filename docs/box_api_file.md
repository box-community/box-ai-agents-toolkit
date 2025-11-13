# Files and Folders

Tools for managing Box files and folders.

## File Operations

### Get File by ID

```python
from box_ai_agents_toolkit import box_file_get_by_id

file = box_file_get_by_id(client, file_id="12345")
```

### Extract Text from File

```python
from box_ai_agents_toolkit import box_file_text_extract

text = box_file_text_extract(client, file_id="12345")
```

### Upload a File

```python
from box_ai_agents_toolkit import box_upload_file

content = "This is a test file content."
result = box_upload_file(client, content, file_name="test_upload.txt", folder_id="0")
print("Uploaded File Info:", result)
```

### Download a File

```python
from box_ai_agents_toolkit import box_file_download

path_saved, file_content, mime_type = box_file_download(client, file_id="12345", save_file=True)
print("File saved to:", path_saved)
```

## Folder Operations

### List Folder Contents

```python
from box_ai_agents_toolkit import box_folder_list_content

contents = box_folder_list_content(client, folder_id="0")
print("Folder contents:", contents)
```

### Create a Folder

```python
from box_ai_agents_toolkit import box_create_folder

folder = box_create_folder(client, name="New Folder", parent_id="0")
print("Created folder:", folder)
```

### Update a Folder

```python
from box_ai_agents_toolkit import box_update_folder

updated_folder = box_update_folder(client, folder_id="12345", name="Updated Name", description="New description")
print("Updated folder:", updated_folder)
```

### Delete a Folder

```python
from box_ai_agents_toolkit import box_delete_folder

box_delete_folder(client, folder_id="12345")
print("Folder deleted")
```

## Related Modules

- `box_api_file.py` - File operations
- `box_api_folder.py` - Folder operations
