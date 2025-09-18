# Box AI Agents Toolkit

A Python library for building AI agents for Box. This toolkit provides functionalities for authenticating with Box using OAuth and CCG, interacting with Box files and folders, managing document generation operations, and handling metadata templates.

## Features

- **Authentication**: Authenticate with Box using OAuth or CCG.
- **Box API Interactions**: Interact with Box files and folders.
- **File Upload & Download**: Easily upload files to and download files from Box.
- **Folder Management**: Create, update, delete, and list folder contents.
- **Search**: Search for content and locate folders by name.
- **Document Generation (DocGen)**: Create and manage document generation jobs and templates.
- **Metadata Templates**: Create and retrieve metadata templates by key, ID, or name.
- **Metadata Instances**: Set, get, update, and delete metadata instances on files.
- **AI Capabilities**: 
  - Ask AI questions about single or multiple files
  - Ask AI questions about Box hubs
  - Extract information using freeform prompts
  - Extract structured information using fields or templates
  - Enhanced extraction capabilities with improved formatting

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

**List Folder Contents:**

```python
from box_ai_agents_toolkit import box_folder_list_content

contents = box_folder_list_content(client, folder_id="0")
print("Folder contents:", contents)
```

**Create a Folder:**

```python
from box_ai_agents_toolkit import box_create_folder

folder = box_create_folder(client, name="New Folder", parent_id="0")
print("Created folder:", folder)
```

**Update a Folder:**

```python
from box_ai_agents_toolkit import box_update_folder

updated_folder = box_update_folder(client, folder_id="12345", name="Updated Name", description="New description")
print("Updated folder:", updated_folder)
```

**Delete a Folder:**

```python
from box_ai_agents_toolkit import box_delete_folder

box_delete_folder(client, folder_id="12345")
print("Folder deleted")
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

#### Search

**Search for Content:**

```python
from box_ai_agents_toolkit import box_search

results = box_search(client, query="contract", limit=10, content_types=["name", "description"])
print("Search results:", results)
```

**Locate Folder by Name:**

```python
from box_ai_agents_toolkit import box_locate_folder_by_name

folder = box_locate_folder_by_name(client, folder_name="Documents", parent_folder_id="0")
print("Found folder:", folder)
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

**Retrieve a DocGen Template by Name:**

```python
from box_ai_agents_toolkit import box_docgen_template_get_by_name

template_details = box_docgen_template_get_by_name(client, template_name="My Template")
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
batch = box_docgen_create_batch(
    client=client,
    docgen_template_id="template_file_id",
    destination_folder_id="dest_folder_id",
    output_type="pdf",
    document_generation_data=data_input
)
print("Batch job created:", batch)
```

**Create Single Document from User Input:**

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

**Get DocGen Job by ID:**

```python
from box_ai_agents_toolkit import box_docgen_get_job_by_id

job = box_docgen_get_job_by_id(client, job_id="job123")
print("Job details:", job)
```

**List DocGen Jobs:**

```python
from box_ai_agents_toolkit import box_docgen_list_jobs

jobs = box_docgen_list_jobs(client, marker="m", limit=10)
print("DocGen jobs:", jobs)
```

**List Jobs by Batch:**

```python
from box_ai_agents_toolkit import box_docgen_list_jobs_by_batch

batch_jobs = box_docgen_list_jobs_by_batch(client, batch_id="batch123", marker="m", limit=5)
print("Batch jobs:", batch_jobs)
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

**Retrieve a Metadata Template by Key:**

```python
from box_ai_agents_toolkit import box_metadata_template_get_by_key

template = box_metadata_template_get_by_key(client, scope="enterprise", template_key="tmpl1")
print("Metadata Template Details:", template)
```

**Retrieve a Metadata Template by ID:**

```python
from box_ai_agents_toolkit import box_metadata_template_get_by_id

template = box_metadata_template_get_by_id(client, template_id="12345")
print("Metadata Template Details:", template)
```

**Retrieve a Metadata Template by Name:**

```python
from box_ai_agents_toolkit import box_metadata_template_get_by_name

template = box_metadata_template_get_by_name(client, template_name="My Template", scope="enterprise")
print("Metadata Template Details:", template)
```

#### Metadata Instances on Files

**Set Metadata Instance on File:**

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

**Get Metadata Instance on File:**

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

**Update Metadata Instance on File:**

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

**Delete Metadata Instance on File:**

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

### AI Capabilities

**Ask AI a Question about a Single File:**

```python
from box_ai_agents_toolkit import box_ai_ask_file_single

response = box_ai_ask_file_single(client, file_id="12345", prompt="What is this file about?")
print("AI Response:", response)
```

**Ask AI a Question about Multiple Files:**

```python
from box_ai_agents_toolkit import box_ai_ask_file_multi

file_ids = ["12345", "67890"]
response = box_ai_ask_file_multi(client, file_ids=file_ids, prompt="Compare these files")
print("AI Response:", response)
```

**Ask AI a Question about a Box Hub:**

```python
from box_ai_agents_toolkit import box_ai_ask_hub

response = box_ai_ask_hub(client, hubs_id="12345", prompt="What is the current policy on parental leave?")
print("AI Response:", response)
```

**Extract Information from Files using AI (Freeform):**

```python
from box_ai_agents_toolkit import box_ai_extract_freeform

response = box_ai_extract_freeform(client, file_id="12345", prompt="Extract date, name, and contract number from this file.")
print("AI Extract Response:", response)
```

**Extract Structured Information using Fields:**

```python
from box_ai_agents_toolkit import box_ai_extract_structured_using_fields

fields = [
    {"key": "contract_date", "type": "date", "description": "The contract signing date"},
    {"key": "parties", "type": "array", "description": "Names of contracting parties"}
]
response = box_ai_extract_structured_using_fields(client, file_id="12345", fields=fields)
print("Structured Extract Response:", response)
```

**Extract Enhanced Structured Information using Fields:**

```python
from box_ai_agents_toolkit import box_ai_extract_structured_enhanced_using_fields

fields = [
    {"key": "contract_date", "type": "date", "description": "The contract signing date"},
    {"key": "parties", "type": "array", "description": "Names of contracting parties"}
]
response = box_ai_extract_structured_enhanced_using_fields(client, file_id="12345", fields=fields)
print("Enhanced Structured Extract Response:", response)
```

**Extract Structured Information using Template:**

```python
from box_ai_agents_toolkit import box_ai_extract_structured_using_template

response = box_ai_extract_structured_using_template(client, file_id="12345", template_key="contract_template")
print("Template-based Extract Response:", response)
```

**Extract Enhanced Structured Information using Template:**

```python
from box_ai_agents_toolkit import box_ai_extract_structured_enhanced_using_template

response = box_ai_extract_structured_enhanced_using_template(client, file_id="12345", template_key="contract_template")
print("Enhanced Template-based Extract Response:", response)
```

### User Management

**Get Current User Info:**

```python
from box_ai_agents_toolkit import box_user_get_current

user = box_user_get_current(client)
print("Current user info:", user)
```

**Get User by ID:**

```python
from box_ai_agents_toolkit import box_user_get_by_id

user = box_user_get_by_id(client, user_id="123456")
print("User info:", user)
```

**List Users:**

```python
from box_ai_agents_toolkit import box_user_list

users = box_user_list(client, limit=10)
print("Users:", users)
```

**List All Users:**

```python
from box_ai_agents_toolkit import box_users_list

result = box_users_list(client)
print("All users:", result)
```

**Search Users by Email:**

```python
from box_ai_agents_toolkit import box_users_search_by_email

result = box_users_search_by_email(client, email="user@example.com")
print("Users with this email:", result)
```

**Locate Users by Name:**

```python
from box_ai_agents_toolkit import box_users_locate_by_name

result = box_users_locate_by_name(client, name="Jane Doe")
print("Users with this name:", result)
```

**Search Users by Name or Email:**

```python
from box_ai_agents_toolkit import box_users_search_by_name_or_email

result = box_users_search_by_name_or_email(client, query="Jane")
print("Users matching query:", result)
```

### Group Management

**Search for Groups:**

```python
from box_ai_agents_toolkit import box_groups_search

result = box_groups_search(client, filter_term="Finance", limit=100)
print("Groups:", result)
```

**List Groups for a Specific User:**

```python
from box_ai_agents_toolkit import box_groups_list_by_user

result = box_groups_list_by_user(client, user_id="123456")
print("User's groups:", result)
```

**List Members of a Group:**

```python
from box_ai_agents_toolkit import box_groups_list_members

result = box_groups_list_members(client, group_id="654321")
print("Group members:", result)
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

### Linting and Code Quality

To run the linter:

```sh
ruff check
```

To format code:

```sh
ruff format
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## Contact

For questions or issues, open an issue on the [GitHub repository](https://github.com/box-community/box-ai-agents-toolkit/issues).