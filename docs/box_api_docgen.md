# Document Generation (DocGen)

Tools for creating and managing document generation templates and jobs in Box.

## Template Management

### Mark a File as a DocGen Template

```python
from box_ai_agents_toolkit import box_docgen_template_create

template = box_docgen_template_create(client, file_id="template_file_id")
print("Created DocGen Template:", template)
```

### List DocGen Templates

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

### Delete a DocGen Template

```python
from box_ai_agents_toolkit import box_docgen_template_delete

box_docgen_template_delete(client, template_id="template_file_id")
print("Template deleted")
```

### List Template Tags and Jobs

```python
from box_ai_agents_toolkit import box_docgen_template_list_tags, box_docgen_template_list_jobs

tags = box_docgen_template_list_tags(client, template_id="template_file_id", template_version_id='v1', marker='m', limit=5)
jobs = box_docgen_template_list_jobs(client, template_id="template_file_id", marker='m2', limit=3)
print("Template tags:", tags)
print("Template jobs:", jobs)
```

## Document Generation

### Create a Document Generation Batch

Generate multiple documents from a template with different data inputs.

```python
from box_ai_agents_toolkit import box_docgen_create_batch

data_input = [
    {"generated_file_name": "file1", "user_input": {"a": "b"}},
    {"generated_file_name": "file2", "user_input": {"x": "y"}}
]
batch = box_docgen_create_batch(
    client=client,
    docgen_template_id="template_file_id",
    destination_folder_id="dest_folder_id",
    output_type="pdf",
    document_generation_data=data_input
)
print("Batch job created:", batch)
```

### Create Single Document from User Input

Generate a single document from a template with custom data.

```python
from box_ai_agents_toolkit import box_docgen_create_single_file_from_user_input

result = box_docgen_create_single_file_from_user_input(
    client=client,
    docgen_template_id="template_file_id",
    destination_folder_id="dest_folder_id",
    user_input={"name": "John Doe", "date": "2024-01-01"},
    generated_file_name="Generated Document",
    output_type="pdf"
)
print("Single document created:", result)
```

## Job Management

### Get DocGen Job by ID

```python
from box_ai_agents_toolkit import box_docgen_get_job_by_id

job = box_docgen_get_job_by_id(client, job_id="job123")
print("Job details:", job)
```

### List DocGen Jobs

```python
from box_ai_agents_toolkit import box_docgen_list_jobs

jobs = box_docgen_list_jobs(client, marker="m", limit=10)
print("DocGen jobs:", jobs)
```

### List Jobs by Batch

```python
from box_ai_agents_toolkit import box_docgen_list_jobs_by_batch

batch_jobs = box_docgen_list_jobs_by_batch(client, batch_id="batch123", marker="m", limit=5)
print("Batch jobs:", batch_jobs)
```

## Related Modules

- `box_api_docgen.py` - Document generation operations
- `box_api_docgen_template.py` - Template management
