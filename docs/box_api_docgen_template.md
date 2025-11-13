# Document Generation Templates

Tools for managing Box document generation templates.

## Overview

Document generation templates are the foundation for creating documents from structured data. This module handles template creation, retrieval, and management.

## Template Management

### Create DocGen Template

Mark a Box file as a document generation template.

```python
from box_ai_agents_toolkit import box_docgen_template_create

template = box_docgen_template_create(client, file_id="template_file_id")
print("Created DocGen Template:", template)
```

### List Templates

```python
from box_ai_agents_toolkit import box_docgen_template_list

templates = box_docgen_template_list(client, marker='x', limit=10)
print("DocGen Templates:", templates)
```

### Get Template by ID

```python
from box_ai_agents_toolkit import box_docgen_template_get_by_id

template_details = box_docgen_template_get_by_id(client, template_id="template_file_id")
print("Template details:", template_details)
```

### Get Template by Name

```python
from box_ai_agents_toolkit import box_docgen_template_get_by_name

template_details = box_docgen_template_get_by_name(client, template_name="My Template")
print("Template details:", template_details)
```

### Delete Template

```python
from box_ai_agents_toolkit import box_docgen_template_delete

box_docgen_template_delete(client, template_id="template_file_id")
print("Template deleted")
```

## Template Metadata

### List Template Tags

Get all tags (fields) available in a template.

```python
from box_ai_agents_toolkit import box_docgen_template_list_tags

tags = box_docgen_template_list_tags(
    client,
    template_id="template_file_id",
    template_version_id='v1',
    marker='m',
    limit=5
)
print("Template tags:", tags)
```

### List Template Jobs

Get all generation jobs created from a template.

```python
from box_ai_agents_toolkit import box_docgen_template_list_jobs

jobs = box_docgen_template_list_jobs(
    client,
    template_id="template_file_id",
    marker='m2',
    limit=3
)
print("Template jobs:", jobs)
```

## Related Operations

For actually generating documents from templates, see [Document Generation](box_api_docgen.md).

## Related Modules

- `box_api_docgen_template.py` - Template management
- `box_api_docgen.py` - Document generation operations
