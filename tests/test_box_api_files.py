from src.box_ai_agents_toolkit.box_api_file import (
    box_file_info,
    box_file_thumbnail_url,
    box_file_thumbnail_download,
)
from tests.conftest import BoxClient, SampleData


def test_box_file_info(box_client_ccg: BoxClient, file_test_data: SampleData) -> None:
    file_id = file_test_data.test_files[0].id
    info = box_file_info(box_client_ccg, file_id)
    assert info is not None
    assert "error" not in info

    assert "file_info" in info
    assert info["file_info"]["id"] == file_id


def test_box_file_thumbnail_url(
    box_client_ccg: BoxClient, file_test_data: SampleData
) -> None:
    file_id = file_test_data.test_files[0].id
    thumbnail_url = box_file_thumbnail_url(box_client_ccg, file_id)
    assert thumbnail_url is not None
    assert "error" not in thumbnail_url
    assert "thumbnail_url" in thumbnail_url


def test_box_file_thumbnail_download(
    box_client_ccg: BoxClient, file_test_data: SampleData
) -> None:
    file_id = file_test_data.test_files[0].id
    download_result = box_file_thumbnail_download(
        box_client_ccg,
        file_id,
    )
    assert download_result is not None
    assert "error" not in download_result
