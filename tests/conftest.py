import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest
from box_sdk_gen import (
    AiStudioAgentAsk,
    AiStudioAgentExtract,
    AiStudioAgentTextGen,
    CreateFolderParent,
    CreateMetadataTemplateFields,
    File,
    FileReferenceV2025R0,
    Folder,
    MetadataTemplate,
    UploadFileAttributes,
    UploadFileAttributesParentField,
)
from dotenv import load_dotenv

from src.box_ai_agents_toolkit import (
    BoxClient,
    get_ccg_client,
)

# @pytest.fixture
# def box_client_auth() -> BoxClient:
#     return get_oauth_client()


@pytest.fixture(scope="module")
def box_client_ccg() -> BoxClient:
    load_dotenv()
    return get_ccg_client()


@dataclass
class TestData:
    test_folder: Folder
    test_files: Optional[list[File]] = None
    test_hub_id: Optional[str] = None
    test_template_key: Optional[str] = None
    test_metadata_template: Optional[MetadataTemplate] = None
    test_ai_agent_id: Optional[str] = None


@pytest.fixture(scope="module")
def docgen_test_files(box_client_ccg: BoxClient):
    # create temporary folder
    folder_name = f"Pytest DocGen Template  {datetime.now().isoformat()}"
    parent = CreateFolderParent(id="0")  # root folder
    folder = box_client_ccg.folders.create_folder(folder_name, parent=parent)

    test_data = TestData(
        test_folder=folder,
    )

    # upload test files
    test_data_path = Path(__file__).parent.joinpath("test_data").joinpath("DocGen")

    if not test_data_path.exists():
        current_path = Path(__file__).parent
        raise FileNotFoundError(
            f"Test data path {test_data_path} does not exist in {current_path}."
        )

    for file_path in test_data_path.glob("*.docx"):
        with file_path.open("rb") as f:
            file_name = file_path.name
            file_attributes = UploadFileAttributes(
                name=file_name,
                parent=UploadFileAttributesParentField(id=folder.id),
            )
            uploaded_file = box_client_ccg.uploads.upload_file(
                attributes=file_attributes,
                file_file_name=f"{file_name}_{datetime.now().isoformat()}",
                file=f,
            )
            if not test_data.test_files:
                test_data.test_files = []
            if uploaded_file.entries:
                test_data.test_files.append(uploaded_file.entries[0])

    # yield the data for the test
    yield test_data

    # clean up temporary folder
    box_client_ccg.folders.delete_folder_by_id(folder.id, recursive=True)


@pytest.fixture(scope="module")
def docgen_test_templates(box_client_ccg: BoxClient, docgen_test_files: TestData):
    """
    Fixture to create and return a list of Doc Gen templates for testing.
    """
    if not docgen_test_files.test_files:
        pytest.skip("No test files available for Doc Gen template creation.")

    # Convert all test files into templates
    for file in docgen_test_files.test_files:
        box_client_ccg.docgen_template.create_docgen_template_v2025_r0(
            FileReferenceV2025R0(id=file.id)
        )

    # it takes a few seconds for the templates to list the tags
    time.sleep(5)

    yield docgen_test_files


@pytest.fixture(scope="module")
def text_extract_test_files(box_client_ccg: BoxClient):
    # create temporary folder
    folder_name = f"Pytest Text Extract  {datetime.now().isoformat()}"
    parent = CreateFolderParent(id="0")  # root folder
    folder = box_client_ccg.folders.create_folder(folder_name, parent=parent)

    test_data = TestData(
        test_folder=folder,
    )

    test_data_path = Path(__file__).parent.joinpath("test_data").joinpath("TextExtract")

    if not test_data_path.exists():
        current_path = Path(__file__).parent
        raise FileNotFoundError(
            f"Test data path {test_data_path} does not exist in {current_path}."
        )

    for file_path in test_data_path.glob("*.*"):
        with file_path.open("rb") as f:
            file_name = file_path.name
            file_attributes = UploadFileAttributes(
                name=file_name,
                parent=UploadFileAttributesParentField(id=folder.id),
            )
            uploaded_file = box_client_ccg.uploads.upload_file(
                attributes=file_attributes,
                file_file_name=f"{file_name}_{datetime.now().isoformat()}",
                file=f,
            )
            if not test_data.test_files:
                test_data.test_files = []
            if uploaded_file.entries:
                test_data.test_files.append(uploaded_file.entries[0])

    # yield the data for the test
    yield test_data

    # clean up temporary folder
    box_client_ccg.folders.delete_folder_by_id(folder.id, recursive=True)


@pytest.fixture(scope="module")
def collaborations_test_files(box_client_ccg: BoxClient):
    # create temporary folder
    folder_name = f"Pytest Collaborations  {uuid.uuid4()}"
    parent = CreateFolderParent(id="0")  # root folder
    folder = box_client_ccg.folders.create_folder(folder_name, parent=parent)

    test_data = TestData(
        test_folder=folder,
    )

    test_data_path = (
        Path(__file__).parent.joinpath("test_data").joinpath("Collaborations")
    )

    if not test_data_path.exists():
        current_path = Path(__file__).parent
        raise FileNotFoundError(
            f"Test data path {test_data_path} does not exist in {current_path}."
        )

    for file_path in test_data_path.glob("*.*"):
        with file_path.open("rb") as f:
            file_name = file_path.name
            file_attributes = UploadFileAttributes(
                name=file_name,
                parent=UploadFileAttributesParentField(id=folder.id),
            )
            uploaded_file = box_client_ccg.uploads.upload_file(
                attributes=file_attributes,
                file_file_name=f"{file_name}_{datetime.now().isoformat()}",
                file=f,
            )
            if not test_data.test_files:
                test_data.test_files = []
            if uploaded_file.entries:
                test_data.test_files.append(uploaded_file.entries[0])

    # yield the data for the test
    yield test_data

    # clean up temporary folder
    box_client_ccg.folders.delete_folder_by_id(folder.id, recursive=True)


@pytest.fixture(scope="module")
def shared_link_test_files(box_client_ccg: BoxClient):
    # create temporary folder
    folder_name = f"Pytest Shared Links  {uuid.uuid4()}"
    parent = CreateFolderParent(id="0")  # root folder
    folder = box_client_ccg.folders.create_folder(folder_name, parent=parent)

    test_data = TestData(
        test_folder=folder,
    )

    test_data_path = (
        Path(__file__).parent.joinpath("test_data").joinpath("Collaborations")
    )

    if not test_data_path.exists():
        current_path = Path(__file__).parent
        raise FileNotFoundError(
            f"Test data path {test_data_path} does not exist in {current_path}."
        )

    for file_path in test_data_path.glob("*.*"):
        with file_path.open("rb") as f:
            file_name = file_path.name
            file_attributes = UploadFileAttributes(
                name=file_name,
                parent=UploadFileAttributesParentField(id=folder.id),
            )
            uploaded_file = box_client_ccg.uploads.upload_file(
                attributes=file_attributes,
                file_file_name=f"{file_name}_{datetime.now().isoformat()}",
                file=f,
            )
            if not test_data.test_files:
                test_data.test_files = []
            if uploaded_file.entries:
                test_data.test_files.append(uploaded_file.entries[0])

    # yield the data for the test
    yield test_data

    # clean up temporary folder
    box_client_ccg.folders.delete_folder_by_id(folder.id, recursive=True)


@pytest.fixture(scope="module")
def web_link_test_data(box_client_ccg: BoxClient):
    # create temporary folder
    folder_name = f"Pytest Web Links  {uuid.uuid4()}"
    parent = CreateFolderParent(id="0")  # root folder
    folder = box_client_ccg.folders.create_folder(folder_name, parent=parent)

    test_data = TestData(
        test_folder=folder,
    )

    # yield the data for the test
    yield test_data

    # clean up temporary folder
    box_client_ccg.folders.delete_folder_by_id(folder.id, recursive=True)


@pytest.fixture(scope="module")
def tasks_test_data(box_client_ccg: BoxClient):
    # create temporary folder
    folder_name = f"{uuid.uuid4()} Tasks Pytest"
    parent = CreateFolderParent(id="0")  # root folder
    folder = box_client_ccg.folders.create_folder(folder_name, parent=parent)

    test_data = TestData(
        test_folder=folder,
    )

    test_data_path = Path(__file__).parent.joinpath("test_data").joinpath("Tasks")

    if not test_data_path.exists():
        current_path = Path(__file__).parent
        raise FileNotFoundError(
            f"Test data path {test_data_path} does not exist in {current_path}."
        )

    for file_path in test_data_path.glob("*.*"):
        with file_path.open("rb") as f:
            file_name = file_path.name
            file_attributes = UploadFileAttributes(
                name=file_name,
                parent=UploadFileAttributesParentField(id=folder.id),
            )
            uploaded_file = box_client_ccg.uploads.upload_file(
                attributes=file_attributes,
                file_file_name=f"{file_name}_{datetime.now().isoformat()}",
                file=f,
            )
            if not test_data.test_files:
                test_data.test_files = []
            if uploaded_file.entries:
                test_data.test_files.append(uploaded_file.entries[0])

    # yield the data for the test
    yield test_data

    # clean up temporary folder
    box_client_ccg.folders.delete_folder_by_id(folder.id, recursive=True)


@pytest.fixture(scope="module")
def ai_test_data(box_client_ccg: BoxClient):
    # create temporary folder
    folder_name = f"{uuid.uuid4()} AI Pytest"
    parent = CreateFolderParent(id="0")  # root folder
    folder = box_client_ccg.folders.create_folder(folder_name, parent=parent)

    test_data = TestData(
        test_folder=folder,
    )

    # upload test files
    test_data_path = Path(__file__).parent.joinpath("test_data").joinpath("AI")

    if not test_data_path.exists():
        current_path = Path(__file__).parent
        raise FileNotFoundError(
            f"Test data path {test_data_path} does not exist in {current_path}."
        )

    for file_path in test_data_path.glob("*.*"):
        with file_path.open("rb") as f:
            file_name = file_path.name
            file_attributes = UploadFileAttributes(
                name=file_name,
                parent=UploadFileAttributesParentField(id=folder.id),
            )
            uploaded_file = box_client_ccg.uploads.upload_file(
                attributes=file_attributes,
                file_file_name=f"{file_name}_{datetime.now().isoformat()}",
                file=f,
            )
            if not test_data.test_files:
                test_data.test_files = []
            if uploaded_file.entries:
                test_data.test_files.append(uploaded_file.entries[0])

    # create temporary hub
    hub_name = f"{uuid.uuid4()} Pytest"
    hub = box_client_ccg.hubs.create_hub_v2025_r0(hub_name, description="Pytest Hub")

    test_data.test_hub_id = hub.id

    # create a test ai agent
    ai_agent_name = f"{uuid.uuid4()} Pytest AI Agent"

    ask_agent = AiStudioAgentAsk(
        access_state="enabled",
        description="ASK AI Agent for Pytest",
    )
    text_gen_agent = AiStudioAgentTextGen(
        access_state="enabled",
        description="Text Generation AI Agent for Pytest",
    )
    extract_agent = AiStudioAgentExtract(
        access_state="enabled",
        description="Text Extraction AI Agent for Pytest",
    )

    ai_agent = box_client_ccg.ai_studio.create_ai_agent(
        name=ai_agent_name,
        access_state="enabled",
        ask=ask_agent,
        text_gen=text_gen_agent,
        extract=extract_agent,
    )
    test_data.test_ai_agent_id = ai_agent.id

    # create test metadata template

    # assert metadata.get("name") is not None
    # assert metadata.get("number") is not None
    # assert metadata.get("effectiveDate") is not None
    # assert metadata.get("paymentTerms") is not None

    template_name = f"{uuid.uuid4()}"
    template = box_client_ccg.metadata_templates.create_metadata_template(
        scope="enterprise",
        display_name=template_name,
        template_key=f"A{template_name}",
        fields=[
            CreateMetadataTemplateFields(
                type="string",
                key="name",
                display_name="Name",
            ),
            CreateMetadataTemplateFields(
                type="string",
                key="number",
                display_name="Number",
            ),
            CreateMetadataTemplateFields(
                type="date",
                key="effectiveDate",
                display_name="Effective Date",
            ),
            CreateMetadataTemplateFields(
                type="string",
                key="paymentTerms",
                display_name="Payment Terms",
            ),
        ],
    )

    test_data.test_template_key = template.template_key

    # yield the data for the test
    yield test_data

    # delete test ai agent
    box_client_ccg.ai_studio.delete_ai_agent_by_id(test_data.test_ai_agent_id)

    # delete metadata template
    box_client_ccg.metadata_templates.delete_metadata_template(
        scope="enterprise", template_key=template.template_key
    )

    # clean up temporary hub
    box_client_ccg.hubs.delete_hub_by_id_v2025_r0(hub.id)

    # clean up temporary folder
    box_client_ccg.folders.delete_folder_by_id(folder.id, recursive=True)


@pytest.fixture(scope="module")
def metadata_test_data(box_client_ccg: BoxClient):
    # create temporary folder
    folder_name = f"{uuid.uuid4()} Metadata Pytest"
    parent = CreateFolderParent(id="0")  # root folder
    folder = box_client_ccg.folders.create_folder(folder_name, parent=parent)

    test_data = TestData(
        test_folder=folder,
    )

    # upload test files
    test_data_path = Path(__file__).parent.joinpath("test_data").joinpath("AI")

    if not test_data_path.exists():
        current_path = Path(__file__).parent
        raise FileNotFoundError(
            f"Test data path {test_data_path} does not exist in {current_path}."
        )

    for file_path in test_data_path.glob("*.*"):
        with file_path.open("rb") as f:
            file_name = file_path.name
            file_attributes = UploadFileAttributes(
                name=file_name,
                parent=UploadFileAttributesParentField(id=folder.id),
            )
            uploaded_file = box_client_ccg.uploads.upload_file(
                attributes=file_attributes,
                file_file_name=f"{file_name}_{datetime.now().isoformat()}",
                file=f,
            )
            if not test_data.test_files:
                test_data.test_files = []
            if uploaded_file.entries:
                test_data.test_files.append(uploaded_file.entries[0])

    # create test metadata template

    template_name = f"{uuid.uuid4()}"
    fields = []

    field_text = {
        "type": "string",
        "displayName": "Test Field",
        "key": "test_field",
    }
    fields.append(field_text)

    field_date = {
        "type": "date",
        "displayName": "Date Field",
        "key": "date_field",
    }
    fields.append(field_date)

    field_float = {
        "type": "float",
        "displayName": "Float Field",
        "key": "float_field",
    }
    fields.append(field_float)

    field_enum = {
        "type": "enum",
        "displayName": "Enum Field",
        "key": "enum_field",
        "options": [
            {"key": "option1"},
            {"key": "option2"},
        ],
    }
    fields.append(field_enum)

    field_multiselect = {
        "type": "multiSelect",
        "displayName": "Multiselect Field",
        "key": "multiselect_field",
        "options": [
            {"key": "option1"},
            {"key": "option2"},
        ],
    }
    fields.append(field_multiselect)

    template = box_client_ccg.metadata_templates.create_metadata_template(
        scope="enterprise",
        display_name=template_name,
        template_key=f"A{template_name}",
        fields=fields,
    )

    test_data.test_template_key = template.template_key
    test_data.test_metadata_template = template

    # yield the data for the test
    yield test_data

    # delete metadata template
    box_client_ccg.metadata_templates.delete_metadata_template(
        scope="enterprise", template_key=template.template_key
    )

    # clean up temporary folder
    box_client_ccg.folders.delete_folder_by_id(folder.id, recursive=True)
