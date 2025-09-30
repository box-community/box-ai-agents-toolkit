import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid

import pytest
from box_sdk_gen import (
    CreateFolderParent,
    File,
    FileReferenceV2025R0,
    Folder,
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
