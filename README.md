# Box AI Agents Toolkit

A Python library for building AI agents for Box. This toolkit provides functionalities for authenticating with Box using OAuth and CCG, interacting with Box files and folders, managing document generation operations, and handling metadata templates.

## Features

- **Authentication**: Authenticate with Box using OAuth or CCG.
- **Box API Interactions**: Interact with Box files and folders.
- **File Upload & Download**: Easily upload files to and download files from Box.
- **Document Generation (DocGen)**: Create and manage document generation jobs and templates.
- **Metadata Templates**: Create, list, update, and delete metadata templates.
- **AI Capabilities**: Ask AI questions about files or Box hubs and extract information from file contents.

## Installation

To install the toolkit, run:

```sh
pip install box-ai-agents-toolkit
```

## Usage

### Authentication

#### CCG Authentication

Create a `.env` file with:

```yaml
BOX_CLIENT_ID = "your client id"
BOX_CLIENT_SECRET = "your client secret"
BOX_SUBJECT_TYPE = "user/enterprise"
BOX_SUBJECT_ID = "user id/enterprise id"
```

Then authenticate:

```python
from box_ai_agents_toolkit import get_ccg_client

client = get_ccg_client()
```

#### OAuth Authentication

Create a `.env` file with:

```yaml
BOX_CLIENT_ID = "your client id"
BOX_CLIENT_SECRET = "your client secret"
BOX_REDIRECT_URL = "http://localhost:8000/callback"
```

Then authenticate:

```python
from box_ai_agents_toolkit import get_oauth_client

client = get_oauth_client()
```

### Box API Interactions

#### Files and Folders

**Get File by ID:**

```python
from box_ai_agents_toolkit import box_file_get_by_id

file = box_file_get_by_id(client, file_id="12345")
```

**Extract Text from File:**

```python
from box_ai_agents_toolkit import box_file_text_extract

text = box_file_text_extract(client, file_id="12345")
```

#### File Upload & Download

**Upload a File:**

```python
from box_ai_agents_toolkit import box_upload_file

content = "This is a test file content."
result = box_upload_file(client, content, file_name="test_upload.txt", folder_id="0")
print("Uploaded File Info:", result)
```

**Download a File:**

```python
from box_ai_agents_toolkit import box_file_download

path_saved, file_content, mime_type = box_file_download(client, file_id="12345", save_file=True)
print("File saved to:", path_saved)
```

### Document Generation (DocGen)

**Mark a File as a DocGen Template:**

```python
from box_ai_agents_toolkit import box_docgen_template_create

template = box_docgen_template_create(client, file_id="template_file_id")
print("Created DocGen Template:", template)
```

**List DocGen Templates:**

```python
from box_ai_agents_toolkit import box_docgen_template_list

templates = box_docgen_template_list(client, marker='x', limit=10)
print("DocGen Templates:", templates)
```

**Delete a DocGen Template:**

```python
from box_ai_agents_toolkit import box_docgen_template_delete

box_docgen_template_delete(client, template_id="template_file_id")
print("Template deleted")
```

**Retrieve a DocGen Template by ID:**

```python
from box_ai_agents_toolkit import box_docgen_template_get_by_id

template_details = box_docgen_template_get_by_id(client, template_id="template_file_id")
print("Template details:", template_details)
```

**List Template Tags and Jobs:**

```python
from box_ai_agents_toolkit import box_docgen_template_list_tags, box_docgen_template_list_jobs

tags = box_docgen_template_list_tags(client, template_id="template_file_id", template_version_id='v1', marker='m', limit=5)
jobs = box_docgen_template_list_jobs(client, template_id="template_file_id", marker='m2', limit=3)
print("Template tags:", tags)
print("Template jobs:", jobs)
```

**Create a Document Generation Batch:**

```python
from box_ai_agents_toolkit import box_docgen_create_batch

data_input = [
    {"generated_file_name": "file1", "user_input": {"a": "b"}},
    {"generated_file_name": "file2", "user_input": {"x": "y"}}
]
batch = box_docgen_create_batch(client, file_id="f1", input_source="api", destination_folder_id="dest", output_type="pdf", document_generation_data=data_input)
print("Batch job created:", batch)
```

Alternatively, you can create a batch from raw user input:

```python
from box_ai_agents_toolkit import box_docgen_create_batch_from_user_input

batch = box_docgen_create_batch_from_user_input(client, file_id="f1", destination_folder_id="dest", user_input='{"key":"value"}', generated_file_name="Output File", output_type="pdf")
print("Batch job created from user input:", batch)
```

### Metadata Templates

**Create a Metadata Template:**

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

**List Metadata Templates:**

```python
from box_ai_agents_toolkit import box_metadata_template_list

templates = box_metadata_template_list(client, scope="enterprise", marker="m", limit=5)
print("Metadata Templates:", templates)
```

**Retrieve a Metadata Template:**

```python
from box_ai_agents_toolkit import box_metadata_template_get

template = box_metadata_template_get(client, scope="enterprise", template_key="tmpl1")
print("Metadata Template Details:", template)
```

**Update a Metadata Template:**

```python
from box_ai_agents_toolkit import box_metadata_template_update

updated_template = box_metadata_template_update(client, scope="global", template_key="tmpl1", request_body=[{"op": "replace", "path": "/displayName", "value": "New Name"}])
print("Updated Metadata Template:", updated_template)
```

**Delete a Metadata Template:**

```python
from box_ai_agents_toolkit import box_metadata_template_delete

box_metadata_template_delete(client, scope="enterprise", template_key="tmpl1")
print("Metadata Template deleted")
```

**List Metadata Templates by Instance ID:**

```python
from box_ai_agents_toolkit import box_metadata_template_list_by_instance_id

templates = box_metadata_template_list_by_instance_id(client, metadata_instance_id="inst1", marker="a", limit=3)
print("Templates by Instance ID:", templates)
```

### AI Capabilities

**Ask AI a Question about a File:**

```python
from box_ai_agents_toolkit import box_file_ai_ask

response = box_file_ai_ask(client, file_id="12345", prompt="What is this file about?")
print("AI Response:", response)
```

**Ask AI a Question about a Box Hub:**

```python
from box_ai_agents_toolkit import box_hubs_ai_ask

response = box_hubs_ai_ask(client, hubs_id="12345", prompt="What is the current policy on parental leave?")
print("AI Response:", response)
```

**Extract Information from a File using AI:**

```python
from box_ai_agents_toolkit import box_file_ai_extract

response = box_file_ai_extract(client, file_id="12345", prompt="Extract date, name, and contract number from this file.")
print("AI Extract Response:", response)
```

## Development

### Setting Up

1. Clone the repository:
    ```sh
    git clone https://github.com/box-community/box-ai-agents-toolkit.git
    cd box-ai-agents-toolkit
    ```

2. Install dependencies:
    ```sh
    pip install -e .[dev]
    ```

### Running Tests

To run the tests, use:

```sh
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## Contact

For questions or issues, open an issue on the [GitHub repository](https://github.com/box-community/box-ai-agents-toolkit/issues).