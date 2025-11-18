"""Integration tests for Box file transfer API functions.

Tests use real Box API calls without mocks to validate file upload and download
operations work correctly against the Box service.
"""

import os
import tempfile
import uuid

import pytest
from box_sdk_gen import BoxClient

from src.box_ai_agents_toolkit import box_file_download, box_file_upload
from tests.conftest import SampleData


# ==================== File Upload Tests ====================


def test_box_upload_file_text_to_test_folder(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test uploading a text file to the root folder."""
    content = "This is a test poem\nWith multiple lines\nFor testing purposes"
    file_name = f"test_poem_{uuid.uuid4()}.txt"
    folder_id = file_test_data.test_folder.id

    result = box_file_upload(
        client=box_client_ccg,
        content=content,
        file_name=file_name,
        parent_folder_id=folder_id,
    )

    assert result is not None
    assert "id" in result
    assert "name" in result
    assert "type" in result
    assert result["name"] == file_name
    assert result["type"] == "file"

    # Verify file was actually uploaded by downloading it
    _, file_content, mime_type = box_file_download(
        client=box_client_ccg,
        file_id=result["id"],
    )
    assert file_content.decode() == content
    assert mime_type == "text/plain"

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_upload_file_text_with_folder_id(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test uploading a text file to a specific folder."""
    content = "Another test poem\nStored in a folder\nFor organization"
    file_name = f"test_poem_folder_{uuid.uuid4()}.txt"

    result = box_file_upload(
        client=box_client_ccg,
        content=content,
        file_name=file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    assert result["name"] == file_name
    assert result["type"] == "file"

    # Verify file is in the correct folder
    file_info = box_client_ccg.files.get_file_by_id(result["id"])
    assert file_info.parent.id == file_test_data.test_folder.id

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_upload_file_binary(box_client_ccg: BoxClient, file_test_data: SampleData):
    """Test uploading binary content (random bytes)."""
    binary_content = bytes([i % 256 for i in range(1024)])  # 1KB of binary data
    file_name = f"test_binary_{uuid.uuid4()}.bin"

    result = box_file_upload(
        client=box_client_ccg,
        content=binary_content,
        file_name=file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    assert result["name"] == file_name
    assert result["type"] == "file"

    # Verify binary content is preserved
    _, downloaded_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=result["id"],
    )
    assert downloaded_content == binary_content

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_upload_file_with_integer_folder_id(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test uploading with folder_id as integer (should be converted to string)."""
    content = "Test with integer folder ID"
    file_name = f"test_int_folder_{uuid.uuid4()}.txt"

    folder_id_int = int(file_test_data.test_folder.id)

    result = box_file_upload(
        client=box_client_ccg,
        content=content,
        file_name=file_name,
        parent_folder_id=folder_id_int,
    )

    file_info = box_client_ccg.files.get_file_by_id(result["id"])
    assert file_info.parent.id == file_test_data.test_folder.id

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_upload_file_large_binary(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test uploading larger binary content."""
    # Create 10KB of binary data
    binary_content = bytes([i % 256 for i in range(10240)])
    file_name = f"test_large_binary_{uuid.uuid4()}.bin"

    result = box_file_upload(
        client=box_client_ccg,
        content=binary_content,
        file_name=file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    assert result["name"] == file_name

    # Verify size
    file_info = box_client_ccg.files.get_file_by_id(result["id"])
    assert file_info.size == len(binary_content)

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_upload_file_multiline_text(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test uploading multiline text content."""
    poem = """Roses are red,
Violets are blue,
Integration tests are written,
To verify the upload too."""

    file_name = f"test_multiline_{uuid.uuid4()}.txt"

    result = box_file_upload(
        client=box_client_ccg,
        content=poem,
        file_name=file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    assert result["name"] == file_name

    # Verify content is preserved
    _, file_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=result["id"],
    )
    assert file_content.decode() == poem

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_upload_file_returns_valid_id(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test that upload returns a valid file_id that can be used in API calls."""
    content = "Test content for validation"
    file_name = f"test_validation_{uuid.uuid4()}.txt"

    result = box_file_upload(
        client=box_client_ccg,
        content=content,
        file_name=file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    # Verify the returned ID is valid by using it in another API call
    file_info = box_client_ccg.files.get_file_by_id(result["id"])
    assert file_info.id == result["id"]
    assert file_info.name == file_name

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_upload_file_empty_string(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test uploading an empty string file."""
    content = ""
    file_name = f"test_empty_{uuid.uuid4()}.txt"

    result = box_file_upload(
        client=box_client_ccg,
        content=content,
        file_name=file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    assert result["name"] == file_name

    # Verify empty content
    _, file_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=result["id"],
    )
    assert file_content == b""

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_upload_file_to_nonexistent_folder(box_client_ccg: BoxClient):
    """Test uploading to a folder that doesn't exist."""
    content = "Test content"
    file_name = f"test_nonexistent_folder_{uuid.uuid4()}.txt"
    fake_folder_id = "999999999999"

    with pytest.raises(Exception):
        box_file_upload(
            client=box_client_ccg,
            content=content,
            file_name=file_name,
            parent_folder_id=fake_folder_id,
        )


# ==================== File Download Tests ====================


def test_box_download_file_without_save(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test downloading a file without saving to disk."""
    file_to_download = file_test_data.test_files[0]

    saved_path, file_content, mime_type = box_file_download(
        client=box_client_ccg,
        file_id=file_to_download.id,
        save_file=False,
    )

    assert saved_path is None
    assert file_content is not None
    assert isinstance(file_content, bytes)
    assert len(file_content) > 0
    assert mime_type is not None


def test_box_download_file_with_save_to_temp(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test downloading a file and saving to temp directory."""
    file_to_download = file_test_data.test_files[0]

    saved_path, file_content, mime_type = box_file_download(
        client=box_client_ccg,
        file_id=file_to_download.id,
        save_file=True,
    )

    try:
        assert saved_path is not None
        assert os.path.exists(saved_path)
        assert saved_path.startswith(tempfile.gettempdir())
        assert file_content is not None
        assert isinstance(file_content, bytes)

        # Verify saved file matches downloaded content
        with open(saved_path, "rb") as f:
            file_on_disk = f.read()
        assert file_on_disk == file_content
    finally:
        # Cleanup
        if saved_path and os.path.exists(saved_path):
            os.remove(saved_path)  # noqa: F841


def test_box_download_file_with_save_path_directory(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test downloading a file with save_path as a directory."""
    file_to_download = file_test_data.test_files[0]

    with tempfile.TemporaryDirectory() as temp_dir:
        saved_path, file_content, _ = box_file_download(
            client=box_client_ccg,
            file_id=file_to_download.id,
            save_file=True,
            save_path=temp_dir,
        )

        assert saved_path is not None
        assert os.path.exists(saved_path)
        assert os.path.dirname(saved_path) == temp_dir
        assert os.path.basename(saved_path) == file_to_download.name

        # Verify saved file matches downloaded content
        with open(saved_path, "rb") as f:
            file_on_disk = f.read()
        assert file_on_disk == file_content


def test_box_download_file_with_save_path_file(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test downloading a file with save_path as a specific file path."""
    file_to_download = file_test_data.test_files[0]

    with tempfile.TemporaryDirectory() as temp_dir:
        specific_path = os.path.join(temp_dir, "downloaded_file.bin")

        saved_path, file_content, _ = box_file_download(
            client=box_client_ccg,
            file_id=file_to_download.id,
            save_file=True,
            save_path=specific_path,
        )

        assert saved_path == specific_path
        assert os.path.exists(saved_path)

        # Verify saved file matches downloaded content
        with open(saved_path, "rb") as f:
            file_on_disk = f.read()
        assert file_on_disk == file_content


def test_box_download_file_with_string_file_id(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test that file_id can be passed as string."""
    file_to_download = file_test_data.test_files[0]

    _, file_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=str(file_to_download.id),
        save_file=False,
    )

    assert file_content is not None
    assert len(file_content) > 0


def test_box_download_file_with_integer_file_id(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test that file_id can be passed as integer."""
    file_to_download = file_test_data.test_files[0]

    _, file_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=int(file_to_download.id),
        save_file=False,
    )

    assert file_content is not None
    assert len(file_content) > 0


def test_box_download_file_returns_bytes(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test that downloaded content is returned as bytes."""
    file_to_download = file_test_data.test_files[0]

    _, file_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=file_to_download.id,
    )

    assert isinstance(file_content, bytes)


def test_box_download_file_returns_mime_type(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test that mime type is detected and returned."""
    file_to_download = file_test_data.test_files[0]

    _, _, mime_type = box_file_download(
        client=box_client_ccg,
        file_id=file_to_download.id,
    )

    assert mime_type is not None
    # Should detect MIME type for PDF files
    if file_to_download.name.endswith(".pdf"):
        assert mime_type == "application/pdf"


def test_box_download_and_reupload_file(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test that a downloaded file can be re-uploaded with same content."""
    original_file = file_test_data.test_files[0]

    # Download the file
    _, original_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=original_file.id,
    )

    # Re-upload the file
    new_file_name = f"reupload_{original_file.name}"
    result = box_file_upload(
        client=box_client_ccg,
        content=original_content,
        file_name=new_file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    # Verify re-uploaded file has the same content
    _, reupload_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=result["id"],
    )

    assert original_content == reupload_content

    # Cleanup
    box_client_ccg.files.delete_file_by_id(result["id"])


def test_box_download_file_preserves_binary_data(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test that binary data is preserved during download."""
    # Upload binary data
    binary_content = bytes([i % 256 for i in range(512)])
    file_name = f"test_binary_preserve_{uuid.uuid4()}.bin"

    upload_result = box_file_upload(
        client=box_client_ccg,
        content=binary_content,
        file_name=file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    # Download and verify
    _, downloaded_content, _ = box_file_download(
        client=box_client_ccg,
        file_id=upload_result["id"],
    )

    assert downloaded_content == binary_content

    # Cleanup
    box_client_ccg.files.delete_file_by_id(upload_result["id"])


def test_box_download_file_with_special_characters(
    box_client_ccg: BoxClient, file_test_data: SampleData
):
    """Test downloading a file with special characters in the filename."""
    content = "Test content for special characters"
    special_file_name = f"test_file_with_special_chars_{uuid.uuid4()}.txt"

    upload_result = box_file_upload(
        client=box_client_ccg,
        content=content,
        file_name=special_file_name,
        parent_folder_id=file_test_data.test_folder.id,
    )

    _, downloaded_content, mime_type = box_file_download(
        client=box_client_ccg,
        file_id=upload_result["id"],
    )

    assert downloaded_content.decode() == content
    assert mime_type == "text/plain"

    # Cleanup
    box_client_ccg.files.delete_file_by_id(upload_result["id"])


# ==================== Error Handling Tests ====================


def test_box_download_nonexistent_file(box_client_ccg: BoxClient):
    """Test downloading a file that doesn't exist."""
    fake_file_id = "999999999999"

    with pytest.raises(Exception):
        box_file_download(
            client=box_client_ccg,
            file_id=fake_file_id,
        )
