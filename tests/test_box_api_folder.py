from src.box_ai_agents_toolkit import box_folder_items_list
from tests.conftest import BoxClient


def test_box_folder_items_list(box_client_ccg: BoxClient):
    FOLDER_ID = "334525105465"
    result = box_folder_items_list(box_client_ccg, FOLDER_ID, is_recursive=True)
    assert "folder_items" in result or "message" in result
    if "folder_items" in result:
        assert isinstance(result["folder_items"], list)
        for item in result["folder_items"]:
            assert "id" in item
            assert "type" in item
            assert "name" in item
    if "message" in result:
        assert result["message"] == "No items found in folder."
