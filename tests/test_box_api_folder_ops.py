import uuid

from box_sdk_gen import BoxClient, CreateFolderParent, UpdateFolderByIdParent


def test_folder_lifecycle(box_client_ccg: BoxClient):
    """Test creating, updating, and deleting a folder in Box"""
    # Generate unique folder names to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    test_folder_name = f"test_folder_{unique_id}"
    updated_folder_name = f"updated_folder_{unique_id}"

    try:
        # 1. Create a test folder in root directory
        new_folder = box_client_ccg.folders.create_folder(
            name=test_folder_name,
            parent=CreateFolderParent(id="0"),  # Root folder
        )

        # Verify folder was created
        assert new_folder is not None
        assert new_folder.name == test_folder_name
        folder_id = new_folder.id

        # 2. Update the folder name
        updated_folder = box_client_ccg.folders.update_folder_by_id(
            folder_id=folder_id,
            name=updated_folder_name,
            description="This is a test folder for API testing",
        )

        # Verify folder was updated
        assert updated_folder is not None
        assert updated_folder.name == updated_folder_name
        assert updated_folder.description == "This is a test folder for API testing"

        # 3. Create a subfolder
        subfolder_name = f"subfolder_{unique_id}"
        subfolder = box_client_ccg.folders.create_folder(
            name=subfolder_name, parent=CreateFolderParent(id=folder_id)
        )

        # Verify subfolder was created
        assert subfolder is not None
        assert subfolder.name == subfolder_name

        # 4. List folder contents
        folder_items = box_client_ccg.folders.get_folder_items(folder_id)
        # Verify the subfolder is in the folder contents
        found_subfolder = False
        for item in folder_items.entries:
            if item.id == subfolder.id and item.name == subfolder_name:
                found_subfolder = True
                break
        assert found_subfolder

    finally:
        # Clean up - delete the test folder (and all sub folders recursively)
        if "folder_id" in locals():
            box_client_ccg.folders.delete_folder_by_id(folder_id, recursive=True)


def test_folder_management_with_moves(box_client_ccg: BoxClient):
    """Test folder moving operations in Box"""
    # Generate unique folder names to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    parent_folder_name = f"parent_folder_{unique_id}"
    child_folder_name = f"child_folder_{unique_id}"

    try:
        # 1. Create two test folders in root directory
        parent_folder = box_client_ccg.folders.create_folder(
            name=parent_folder_name,
            parent=CreateFolderParent(id="0"),  # Root folder
        )

        child_folder = box_client_ccg.folders.create_folder(
            name=child_folder_name,
            parent=CreateFolderParent(id="0"),  # Root folder
        )

        parent_id = parent_folder.id
        child_id = child_folder.id

        # 2. Move child folder into parent folder
        moved_folder = box_client_ccg.folders.update_folder_by_id(
            folder_id=child_id, parent=UpdateFolderByIdParent(id=parent_id)
        )

        # 3. Verify the move worked
        assert moved_folder is not None
        assert moved_folder.parent.id == parent_id

        # 4. List parent folder contents to confirm child is there
        parent_items = box_client_ccg.folders.get_folder_items(parent_id)
        found_child = False
        for item in parent_items.entries:
            if item.id == child_id:
                found_child = True
                break
        assert found_child

    finally:
        # Clean up - delete the test folders
        if "parent_id" in locals():
            box_client_ccg.folders.delete_folder_by_id(parent_id, recursive=True)
        # Only try to delete child directly if it wasn't moved successfully
        if "child_id" in locals() and "found_child" in locals() and not found_child:
            box_client_ccg.folders.delete_folder_by_id(child_id)
