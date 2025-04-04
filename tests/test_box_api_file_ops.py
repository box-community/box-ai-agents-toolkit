import os
import tempfile

from box_sdk_gen import BoxClient, UploadFileAttributes, UploadFileAttributesParentField


def test_box_upload_file(box_client_ccg: BoxClient):
    """Test uploading a file to Box"""
    # Test content
    test_content = "This is a test file created by the test_box_upload_file test."
    test_filename = "test_upload.txt"

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        # Upload to root folder
        with open(temp_file_path, "rb") as file:
            upload_attributes = UploadFileAttributes(
                name=test_filename, parent=UploadFileAttributesParentField(id="0")
            )
            upload_result = box_client_ccg.uploads.upload_file(upload_attributes, file)
            file_id = upload_result.entries[0].id

            # Verify file exists in Box
            file_info = box_client_ccg.files.get_file_by_id(file_id)
            assert file_info is not None
            assert file_info.name == test_filename

    finally:
        # Clean up - delete the test file from Box
        if "file_id" in locals():
            box_client_ccg.files.delete_file_by_id(file_id)

        # Delete local temp file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_box_download_file(box_client_ccg: BoxClient):
    """Test downloading a file from Box"""
    # First upload a file to test downloading
    test_content = "This is a test file for download testing."
    test_filename = "test_download.txt"

    # Upload to root folder
    upload_attributes = UploadFileAttributes(
        name=test_filename, parent=UploadFileAttributesParentField(id="0")
    )

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, "rb") as file:
            upload_result = box_client_ccg.uploads.upload_file(upload_attributes, file)
            file_id = upload_result.entries[0].id

        # Test downloading
        download_stream = box_client_ccg.downloads.download_file(file_id)
        # Use read() instead of trying to access .content
        downloaded_data = download_stream.read()
        downloaded_content = downloaded_data.decode("utf-8")
        assert downloaded_content == test_content

    finally:
        # Clean up - delete the test file from Box
        if "file_id" in locals():
            box_client_ccg.files.delete_file_by_id(file_id)

        # Delete local temp file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
