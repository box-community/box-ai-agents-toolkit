# Collaborations

Tools for managing collaborations on files and folders in Box.

## Overview

Collaborations allow you to share files and folders with users or groups, assigning them specific roles and permissions. You can create collaborations with users (by ID or email) or groups, and manage them throughout their lifecycle.

## Available Roles

- `editor` - Can view, download, upload, edit, delete, and manage collaborators
- `viewer` - Can view and download
- `previewer` - Can view only (no download)
- `uploader` - Can upload to folders only
- `viewer_uploader` - Can view and upload
- `co-owner` - Full access like owner

## File Collaborations

### Create Collaboration with User by ID

```python
from box_ai_agents_toolkit import box_collaboration_file_user_by_user_id

result = box_collaboration_file_user_by_user_id(
    client,
    file_id="12345",
    user_id="67890",
    role="editor",
    is_access_only=False,
    notify=True
)
print("Collaboration created:", result)
```

### Create Collaboration with User by Email

```python
from box_ai_agents_toolkit import box_collaboration_file_user_by_user_login

result = box_collaboration_file_user_by_user_login(
    client,
    file_id="12345",
    user_login="user@example.com",
    role="viewer",
    notify=True
)
print("Collaboration created:", result)
```

### Create Collaboration with Group

```python
from box_ai_agents_toolkit import box_collaboration_file_group_by_group_id

result = box_collaboration_file_group_by_group_id(
    client,
    file_id="12345",
    group_id="98765",
    role="editor",
    notify=True
)
print("Collaboration created:", result)
```

### List File Collaborations

```python
from box_ai_agents_toolkit import box_collaborations_list_by_file

result = box_collaborations_list_by_file(client, file_id="12345", limit=100)
print("File collaborations:", result)
```

## Folder Collaborations

### Create Collaboration with User by ID

```python
from box_ai_agents_toolkit import box_collaboration_folder_user_by_user_id

result = box_collaboration_folder_user_by_user_id(
    client,
    folder_id="12345",
    user_id="67890",
    role="editor",
    can_view_path=True,
    notify=True
)
print("Collaboration created:", result)
```

### Create Collaboration with User by Email

```python
from box_ai_agents_toolkit import box_collaboration_folder_user_by_user_login

result = box_collaboration_folder_user_by_user_login(
    client,
    folder_id="12345",
    user_login="user@example.com",
    role="viewer",
    can_view_path=True,
    notify=True
)
print("Collaboration created:", result)
```

### Create Collaboration with Group

```python
from box_ai_agents_toolkit import box_collaboration_folder_group_by_group_id

result = box_collaboration_folder_group_by_group_id(
    client,
    folder_id="12345",
    group_id="98765",
    role="editor",
    can_view_path=True,
    notify=True
)
print("Collaboration created:", result)
```

### List Folder Collaborations

```python
from box_ai_agents_toolkit import box_collaborations_list_by_folder

result = box_collaborations_list_by_folder(client, folder_id="12345", limit=100)
print("Folder collaborations:", result)
```

## Manage Collaborations

### Update Collaboration

```python
from box_ai_agents_toolkit import box_collaboration_update

result = box_collaboration_update(
    client,
    collaboration_id="11111",
    role="viewer",
    status="accepted",
    can_view_path=False
)
print("Collaboration updated:", result)
```

### Delete Collaboration

```python
from box_ai_agents_toolkit import box_collaboration_delete

result = box_collaboration_delete(client, collaboration_id="11111")
print("Collaboration deleted:", result)
```

## Parameters

### Common Parameters

- `is_access_only` - If true, collaborators have access to shared items but won't see them in "All Files"
- `can_view_path` - If true, collaborators can view the path to the root folder (folders only)
- `expires_at` - DateTime when the collaboration expires
- `notify` - Whether to send email notification to the collaborator

## Related Modules

- `box_api_collaborations.py` - Collaboration operations
