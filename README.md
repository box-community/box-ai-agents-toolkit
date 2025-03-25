# Box AI Agents Toolkit

A Python library for building AI agents for Box. This toolkit provides functionalities for authenticating with Box using OAuth and CCG, interacting with Box files and folders, and utilizing AI capabilities provided by Box.

## Features

- **Authentication**: Authenticate with Box using OAuth and CCG.
- **Box API Interactions**: Interact with Box files and folders.
- **AI Capabilities**: Utilize AI capabilities provided by Box.

## Installation

To install the toolkit, use the following command:

```sh
pip install box-ai-agents-toolkit
```

## Usage

### Authentication

#### CCG Authentication

Create a `.env` file with the following:
```yaml
BOX_CLIENT_ID = "your client id"
BOX_CLIENT_SECRET = "your client secret"
BOX_SUBJECT_TYPE = "user/enterprise"
BOX_SUBJECT_ID = "user id/enterprise id"
```

```python
from box_ai_agents_toolkit import get_ccg_client

client = get_ccg_client()
```

#### OAuth Authentication

Create a `.env` file with the following:
```yaml
BOX_CLIENT_ID = "your client id"
BOX_CLIENT_SECRET = "your client secret"
BOX_REDIRECT_URL = "http://localhost:8000/callback"
```

```python
from box_ai_agents_toolkit import get_oauth_client

client = get_oauth_client()
```

### Box API Interactions

#### Get File by ID

```python
from box_ai_agents_toolkit import box_file_get_by_id

file = box_file_get_by_id(client, file_id="12345")
```

#### Extract Text from File

```python
from box_ai_agents_toolkit import box_file_text_extract

text = box_file_text_extract(client, file_id="12345")
```

### AI Capabilities

#### Ask AI a Question about a File

```python
from box_ai_agents_toolkit import box_file_ai_ask

response = box_file_ai_ask(client, file_id="12345", prompt="What is this file about?")
```

#### Extract Information from a File using AI

```python
from box_ai_agents_toolkit import box_file_ai_extract

response = box_file_ai_extract(client, file_id="12345", prompt="Extract date, name, contract number from this file.")
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

To run the tests, use the following command:

```sh
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome!

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/box-community/box-ai-agents-toolkit/issues).