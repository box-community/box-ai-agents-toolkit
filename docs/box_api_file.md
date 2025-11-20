# Files and Folders

Tools for managing Box files and folders.

## File Operations

### Get File Information

Retrieves information about a file in Box.

```python
from box_ai_agents_toolkit import box_file_info

file_info = box_file_info(client, file_id="12345")
print("File info:", file_info)
```

### Extract Text from File

Extracts text from a file in Box. The result can be markdown or plain text. If a markdown representation is available, it will be preferred. Otherwise, extracted text representation will be used as a fallback.

```python
from box_ai_agents_toolkit import box_file_text_extract

text = box_file_text_extract(client, file_id="12345")
print("Extracted text:", text)
```

### Download a File

Downloads a file from Box and optionally saves it locally.

```python
from box_ai_agents_toolkit import box_file_download

path_saved, file_content, mime_type = box_file_download(
    client,
    file_id="12345",
    save_file=True,
    save_path="/path/to/save"  # optional
)
print("File saved to:", path_saved)
print("MIME type:", mime_type)
```

### Upload a File

Uploads content as a file to Box.

```python
from box_ai_agents_toolkit import box_file_upload

result = box_file_upload(
    client,
    content="This is file content",  # str or bytes
    file_name="test_upload.txt",
    parent_folder_id="0"
)
print("Uploaded file info:", result)
```

### Get File Thumbnail URL

Retrieves the thumbnail URL of a file from Box.

```python
from box_ai_agents_toolkit import box_file_thumbnail_url

result = box_file_thumbnail_url(
    client,
    file_id="12345",
    extension="png",  # "png" or "jpg"
    min_height=100,
    max_width=200
)
print("Thumbnail URL:", result)
```

### Download File Thumbnail

Downloads the thumbnail image of a file from Box.

```python
from box_ai_agents_toolkit import box_file_thumbnail_download

result = box_file_thumbnail_download(
    client,
    file_id="12345",
    extension="png",
    min_height=100,
    max_width=200
)
print("Thumbnail content (bytes):", result)
```

### Copy a File

Copies a file to a specified folder in Box.

```python
from box_ai_agents_toolkit import box_file_copy

result = box_file_copy(
    client,
    file_id="12345",
    destination_folder_id="67890",
    new_name="copy_of_file.txt",  # optional
    version_number=1  # optional
)
print("Copied file info:", result)
```

### Move a File

Moves a file to a specified folder in Box.

```python
from box_ai_agents_toolkit import box_file_move

result = box_file_move(
    client,
    file_id="12345",
    destination_folder_id="67890"
)
print("Moved file info:", result)
```

### Rename a File

Renames a file in Box.

```python
from box_ai_agents_toolkit import box_file_rename

result = box_file_rename(
    client,
    file_id="12345",
    new_name="new_filename.txt"
)
print("Renamed file info:", result)
```

### Delete a File

Deletes a file from Box.

```python
from box_ai_agents_toolkit import box_file_delete

result = box_file_delete(client, file_id="12345")
print("Result:", result)
```

### Set File Description

Sets the description of a file in Box.

```python
from box_ai_agents_toolkit import box_file_set_description

result = box_file_set_description(
    client,
    file_id="12345",
    description="This is my file description"
)
print("Updated file info:", result)
```

### File Retention and Lock Operations

#### Set Retention Date

Sets the retention date of a file in Box. This date cannot be shortened once set on a file.

```python
from box_ai_agents_toolkit import box_file_retention_date_set
from datetime import datetime

retention_date = datetime(2025, 12, 31)
result = box_file_retention_date_set(
    client,
    file_id="12345",
    retention_date=retention_date
)
print("Updated file info:", result)
```

#### Clear Retention Date

Clears the retention date of a file in Box.

```python
from box_ai_agents_toolkit import box_file_retention_date_clear

result = box_file_retention_date_clear(client, file_id="12345")
print("Updated file info:", result)
```

#### Lock a File

Defines a lock on a file. This prevents the file from being moved, renamed, or otherwise changed by anyone other than the user who created the lock.

```python
from box_ai_agents_toolkit import box_file_lock
from datetime import datetime

lock_expires_at = datetime(2025, 12, 31)
result = box_file_lock(
    client,
    file_id="12345",
    lock_expires_at=lock_expires_at,  # optional
    is_download_prevented=False  # optional
)
print("Locked file info:", result)
```

#### Unlock a File

Removes a lock from a file.

```python
from box_ai_agents_toolkit import box_file_unlock

result = box_file_unlock(client, file_id="12345")
print("Unlocked file info:", result)
```

### File Download Permissions

#### Allow Download (Open)

Allows anyone with access to the file to download it.

```python
from box_ai_agents_toolkit import box_file_set_download_open

result = box_file_set_download_open(client, file_id="12345")
print("Updated file info:", result)
```

#### Allow Download (Company Only)

Sets a file to be downloadable by company members only. This removes the download option for external users with viewer or editor roles.

```python
from box_ai_agents_toolkit import box_file_set_download_company

result = box_file_set_download_company(client, file_id="12345")
print("Updated file info:", result)
```

#### Reset Download Permissions

Resets the download permissions of a file to the default behavior based on collaboration roles.

```python
from box_ai_agents_toolkit import box_file_set_download_reset

result = box_file_set_download_reset(client, file_id="12345")
print("Updated file info:", result)
```

### File Tags

#### List Tags

Lists the tags associated with a file in Box.

```python
from box_ai_agents_toolkit import box_file_tag_list

result = box_file_tag_list(client, file_id="12345")
print("Tags:", result)
```

#### Add Tag

Adds a tag to a file in Box.

```python
from box_ai_agents_toolkit import box_file_tag_add

result = box_file_tag_add(
    client,
    file_id="12345",
    tag="important"
)
print("Updated file info:", result)
```

#### Remove Tag

Removes a tag from a file in Box.

```python
from box_ai_agents_toolkit import box_file_tag_remove

result = box_file_tag_remove(
    client,
    file_id="12345",
    tag="important"
)
print("Updated file info:", result)
```

## Related Modules

- `box_api_file.py` - Core file operations, thumbnails, locking, tags, and download permissions
- `box_api_file_transfer.py` - File upload and download operations
- `box_api_file_representation.py` - File text extraction and representation handling
