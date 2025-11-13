# AI Capabilities

Tools for leveraging Box AI to ask questions and extract information from files.

## Ask AI Questions

### Ask About a Single File

Ask Box AI questions about the content of a specific file.

```python
from box_ai_agents_toolkit import box_ai_ask_file_single

response = box_ai_ask_file_single(client, file_id="12345", prompt="What is this file about?")
print("AI Response:", response)
```

### Ask About Multiple Files

Ask Box AI questions that span across multiple files.

```python
from box_ai_agents_toolkit import box_ai_ask_file_multi

file_ids = ["12345", "67890"]
response = box_ai_ask_file_multi(client, file_ids=file_ids, prompt="Compare these files")
print("AI Response:", response)
```

### Ask About a Box Hub

Query Box AI about content within a Box Hub.

```python
from box_ai_agents_toolkit import box_ai_ask_hub

response = box_ai_ask_hub(client, hubs_id="12345", prompt="What is the current policy on parental leave?")
print("AI Response:", response)
```

## Extract Information

### Freeform Extraction

Extract information from files using natural language prompts.

```python
from box_ai_agents_toolkit import box_ai_extract_freeform

response = box_ai_extract_freeform(client, file_id="12345", prompt="Extract date, name, and contract number from this file.")
print("AI Extract Response:", response)
```

### Structured Extraction with Fields

Extract structured information by defining specific fields.

```python
from box_ai_agents_toolkit import box_ai_extract_structured_using_fields

fields = [
    {"key": "contract_date", "type": "date", "description": "The contract signing date"},
    {"key": "parties", "type": "array", "description": "Names of contracting parties"}
]
response = box_ai_extract_structured_using_fields(client, file_id="12345", fields=fields)
print("Structured Extract Response:", response)
```

### Enhanced Structured Extraction with Fields

Use enhanced extraction capabilities with improved formatting.

```python
from box_ai_agents_toolkit import box_ai_extract_structured_enhanced_using_fields

fields = [
    {"key": "contract_date", "type": "date", "description": "The contract signing date"},
    {"key": "parties", "type": "array", "description": "Names of contracting parties"}
]
response = box_ai_extract_structured_enhanced_using_fields(client, file_id="12345", fields=fields)
print("Enhanced Structured Extract Response:", response)
```

### Structured Extraction with Template

Extract information using a predefined metadata template.

```python
from box_ai_agents_toolkit import box_ai_extract_structured_using_template

response = box_ai_extract_structured_using_template(client, file_id="12345", template_key="contract_template")
print("Template-based Extract Response:", response)
```

### Enhanced Structured Extraction with Template

Use enhanced extraction with a metadata template.

```python
from box_ai_agents_toolkit import box_ai_extract_structured_enhanced_using_template

response = box_ai_extract_structured_enhanced_using_template(client, file_id="12345", template_key="contract_template")
print("Enhanced Template-based Extract Response:", response)
```

## Related Modules

- `box_api_ai.py` - Box AI operations
