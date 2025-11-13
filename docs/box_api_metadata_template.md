# Metadata Templates

Tools for creating and managing metadata templates and instances in Box.

## Template Management

### Create a Metadata Template

```python
from box_ai_agents_toolkit import box_metadata_template_create

template = box_metadata_template_create(
    client,
    scope="enterprise",
    display_name="My Template",
    template_key="tmpl1",
    hidden=True,
    fields=[{"key": "a", "type": "string"}],
    copy_instance_on_item_copy=False,
)
print("Created Metadata Template:", template)
```

### Get Template by Key

```python
from box_ai_agents_toolkit import box_metadata_template_get_by_key

template = box_metadata_template_get_by_key(client, scope="enterprise", template_key="tmpl1")
print("Metadata Template Details:", template)
```

### Get Template by ID

```python
from box_ai_agents_toolkit import box_metadata_template_get_by_id

template = box_metadata_template_get_by_id(client, template_id="12345")
print("Metadata Template Details:", template)
```

### Get Template by Name

```python
from box_ai_agents_toolkit import box_metadata_template_get_by_name

template = box_metadata_template_get_by_name(client, template_name="My Template", scope="enterprise")
print("Metadata Template Details:", template)
```

## Metadata Instances on Files

### Set Metadata Instance

Apply metadata to a file using a template.

```python
from box_ai_agents_toolkit import box_metadata_set_instance_on_file

metadata = {"field1": "value1", "field2": "value2"}
result = box_metadata_set_instance_on_file(
    client,
    file_id="12345",
    scope="enterprise",
    template_key="tmpl1",
    metadata=metadata
)
print("Metadata set:", result)
```

### Get Metadata Instance

Retrieve metadata from a file.

```python
from box_ai_agents_toolkit import box_metadata_get_instance_on_file

metadata = box_metadata_get_instance_on_file(
    client,
    file_id="12345",
    scope="enterprise",
    template_key="tmpl1"
)
print("File metadata:", metadata)
```

### Update Metadata Instance

Update existing metadata on a file using JSON Patch operations.

```python
from box_ai_agents_toolkit import box_metadata_update_instance_on_file

updates = [
    {"op": "replace", "path": "/field1", "value": "new_value1"},
    {"op": "add", "path": "/field3", "value": "value3"}
]
result = box_metadata_update_instance_on_file(
    client,
    file_id="12345",
    scope="enterprise",
    template_key="tmpl1",
    request_body=updates
)
print("Metadata updated:", result)
```

### Delete Metadata Instance

Remove metadata from a file.

```python
from box_ai_agents_toolkit import box_metadata_delete_instance_on_file

box_metadata_delete_instance_on_file(
    client,
    file_id="12345",
    scope="enterprise",
    template_key="tmpl1"
)
print("Metadata instance deleted")
```

## Related Modules

- `box_api_metadata_template.py` - Metadata template operations
