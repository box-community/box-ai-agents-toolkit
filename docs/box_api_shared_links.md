# Shared Links

Tools for creating and managing shared links for files, folders, and web links in Box.

## Overview

Shared links provide a way to share Box content with people who may not have Box accounts. You can control access levels, set passwords, expiration dates, and permissions.

## Access Levels

- `open` - Anyone with the link can access
- `company` - Only people in your company can access
- `collaborators` - Only people who are collaborators can access

## File Shared Links

### Create or Update Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_file_create_or_update

result = box_shared_link_file_create_or_update(
    client,
    file_id="12345",
    access="company",
    can_download=True,
    can_preview=True,
    can_edit=False,
    password="SecurePass123!",
    vanity_name="my-contract"
)
print("Shared link:", result)
```

### Get Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_file_get

result = box_shared_link_file_get(client, file_id="12345")
print("Shared link:", result)
```

### Remove Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_file_remove

result = box_shared_link_file_remove(client, file_id="12345")
print("Result:", result)
```

### Find File by Shared Link URL

```python
from box_ai_agents_toolkit import box_shared_link_file_find_by_shared_link_url

result = box_shared_link_file_find_by_shared_link_url(
    client,
    shared_link_url="https://app.box.com/s/abc123",
    password="SecurePass123!"
)
print("File details:", result)
```

## Folder Shared Links

### Create or Update Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_folder_create_or_update

result = box_shared_link_folder_create_or_update(
    client,
    folder_id="12345",
    access="company",
    can_download=True,
    can_preview=True,
    can_edit=False
)
print("Shared link:", result)
```

### Get Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_folder_get

result = box_shared_link_folder_get(client, folder_id="12345")
print("Shared link:", result)
```

### Remove Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_folder_remove

result = box_shared_link_folder_remove(client, folder_id="12345")
print("Result:", result)
```

### Find Folder by Shared Link URL

```python
from box_ai_agents_toolkit import box_shared_link_folder_find_by_shared_link_url

result = box_shared_link_folder_find_by_shared_link_url(
    client,
    shared_link_url="https://app.box.com/s/abc123"
)
print("Folder details:", result)
```

## Web Link Shared Links

### Create or Update Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_web_link_create_or_update

result = box_shared_link_web_link_create_or_update(
    client,
    web_link_id="12345",
    access="company",
    password="SecurePass123!"
)
print("Shared link:", result)
```

### Get Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_web_link_get

result = box_shared_link_web_link_get(client, web_link_id="12345")
print("Shared link:", result)
```

### Remove Shared Link

```python
from box_ai_agents_toolkit import box_shared_link_web_link_remove

result = box_shared_link_web_link_remove(client, web_link_id="12345")
print("Result:", result)
```

### Find Web Link by Shared Link URL

```python
from box_ai_agents_toolkit import box_shared_link_web_link_find_by_shared_link_url

result = box_shared_link_web_link_find_by_shared_link_url(
    client,
    shared_link_url="https://app.box.com/s/abc123"
)
print("Web link details:", result)
```

## Parameters

### Common Parameters

- `access` - Access level: "open", "company", or "collaborators"
- `can_download` - Allow downloads (default: True)
- `can_preview` - Allow preview (default: True)
- `can_edit` - Allow editing (default: False)
- `password` - Password protection (must be 8+ characters with number, uppercase, or special character)
- `vanity_name` - Custom URL slug for the shared link
- `unshared_at` - DateTime when the link should expire

## Related Modules

- `box_api_shared_links.py` - Shared link operations
