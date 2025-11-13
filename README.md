# Box AI Agents Toolkit

A Python library for building AI agents for Box. This toolkit provides functionalities for authenticating with Box using OAuth and CCG, interacting with Box files and folders, managing document generation operations, and handling metadata templates.

## Features

- **Authentication**: Authenticate with Box using OAuth or CCG
- **Box API Interactions**: Interact with Box files and folders
- **File Upload & Download**: Easily upload files to and download files from Box
- **Folder Management**: Create, update, delete, and list folder contents
- **Search**: Search for content and locate folders by name
- **Document Generation (DocGen)**: Create and manage document generation jobs and templates
- **Metadata Templates**: Create and retrieve metadata templates and instances
- **AI Capabilities**: Ask questions and extract information from files using Box AI
- **User & Group Management**: Manage and search for Box users and groups
- **Collaborations**: Share files and folders with users and groups
- **Shared Links**: Create and manage shared links for files, folders, and web links
- **Tasks**: Create and manage tasks on files
- **Web Links**: Create and manage web link bookmarks

## Installation

### For End Users

Install the toolkit using pip:

```sh
pip install box-ai-agents-toolkit
```

Or using uv (faster):

```sh
uv pip install box-ai-agents-toolkit
```

### For Contributors and Developers

#### 1. Install uv

`uv` is an extremely fast Python package installer and resolver. Install it for your platform:

**macOS:**
```sh
brew install uv
```

**Linux:**
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Windows (wget):**
```sh
wget -qO- https://astral.sh/uv/install.sh | sh
```

#### 2. Clone and Install

```sh
# Clone the repository
git clone https://github.com/box-community/box-ai-agents-toolkit.git
cd box-ai-agents-toolkit

# Install dependencies (recommended)
uv sync


```

## Quick Start

### Authentication

```python
from box_ai_agents_toolkit import get_ccg_client

# Authenticate using CCG
client = get_ccg_client()
```

For detailed authentication options, see [Authentication Documentation](docs/box_authentication.md).

### Basic File Operations

```python
from box_ai_agents_toolkit import box_file_get_by_id, box_upload_file

# Get a file
file = box_file_get_by_id(client, file_id="12345")

# Upload a file
result = box_upload_file(client, content="Hello World", file_name="test.txt", folder_id="0")
```

## API Reference

Complete documentation organized by Python module:

| Module | Description | Documentation |
|--------|-------------|---------------|
| **Core Operations** |
| `box_authentication.py` | OAuth and CCG authentication | [Authentication](docs/box_authentication.md) |
| `box_auth_callback.py` | OAuth callback handler (internal) | [OAuth Callback](docs/box_auth_callback.md) |
| `box_api_file.py` | File operations (upload, download, get, extract text) | [Files](docs/box_api_file.md) |
| `box_api_folder.py` | Folder operations (create, update, delete, list) | [Folders](docs/box_api_folder.md) |
| `box_api_search.py` | Search content and locate folders | [Search](docs/box_api_search.md) |
| **Collaboration & Sharing** |
| `box_api_collaborations.py` | Manage collaborations on files and folders | [Collaborations](docs/box_api_collaborations.md) |
| `box_api_shared_links.py` | Create and manage shared links | [Shared Links](docs/box_api_shared_links.md) |
| **Content Management** |
| `box_api_tasks.py` | Create and manage tasks on files | [Tasks](docs/box_api_tasks.md) |
| `box_api_weblink.py` | Create and manage web link bookmarks | [Web Links](docs/box_api_weblink.md) |
| **Document Generation** |
| `box_api_docgen.py` | Generate documents from templates | [DocGen](docs/box_api_docgen.md) |
| `box_api_docgen_template.py` | Manage document generation templates | [DocGen Templates](docs/box_api_docgen_template.md) |
| **Metadata** |
| `box_api_metadata_template.py` | Manage metadata templates and instances | [Metadata](docs/box_api_metadata_template.md) |
| **AI Capabilities** |
| `box_api_ai.py` | Ask questions and extract information using Box AI | [AI](docs/box_api_ai.md) |
| **User & Group Management** |
| `box_api_users.py` | Manage and search users | [Users](docs/box_api_users.md) |
| `box_api_groups.py` | Manage and search groups | [Groups](docs/box_api_groups.md) |
| **Utilities (Internal)** |
| `box_api_util_classes.py` | Utility classes | [Util Classes](docs/box_api_util_classes.md) |
| `box_api_util_generic.py` | Generic utilities | [Util Generic](docs/box_api_util_generic.md) |
| `box_api_util_http.py` | HTTP utilities | [Util HTTP](docs/box_api_util_http.md) |

## Development

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
