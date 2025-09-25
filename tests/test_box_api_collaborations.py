import uuid
from box_ai_agents_toolkit import (
    box_collaborations_list_by_file,
    box_collaborations_list_by_folder,
    box_collaboration_file_user_by_user_id,
    box_collaboration_file_user_by_user_login,
    box_collaboration_folder_user_by_user_id,
    box_collaboration_folder_user_by_user_login,
    box_collaboration_file_group_by_group_id,
    box_collaboration_folder_group_by_group_id,
    box_collaboration_delete,
    box_collaboration_update,
)
from box_sdk_gen import (
    BoxClient,
    CreateGroupMembershipUser,
    CreateGroupMembershipGroup,
    GroupFull,
)
from .conftest import TestData
import pytest


def _prep_test_group(box_client_ccg: BoxClient) -> GroupFull:
    def find_next_user(exclude_ids):
        return next(
            (
                user
                for user in all_users
                if user.id not in exclude_ids
                and user.login is not None
                and user.login.endswith("@boxdemo.com")
            ),
            None,
        )

    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users and len(all_users) > 0

    test_group_name = f"Test Group for box_collaboration {uuid.uuid4()}"
    test_group = box_client_ccg.groups.create_group(name=test_group_name)
    membership_group = CreateGroupMembershipGroup(id=test_group.id)

    # Add current user to group
    box_client_ccg.memberships.create_group_membership(
        group=membership_group, user=CreateGroupMembershipUser(id=user_me)
    )

    # Add two more users to group
    test_user_a = find_next_user({user_me})
    assert test_user_a is not None, "No suitable test user A found."
    box_client_ccg.memberships.create_group_membership(
        group=membership_group, user=CreateGroupMembershipUser(id=test_user_a.id)
    )

    test_user_b = find_next_user({user_me, test_user_a.id})
    assert test_user_b is not None, "No suitable test user B found."
    box_client_ccg.memberships.create_group_membership(
        group=membership_group, user=CreateGroupMembershipUser(id=test_user_b.id)
    )

    return test_group


@pytest.mark.order(index=10)
def test_box_collaborations_list_by_file_no_collaborations(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test file to work with
    assert collaborations_test_files.test_files is not None
    assert len(collaborations_test_files.test_files) > 0

    test_file = collaborations_test_files.test_files[0]
    result_collaborations = box_collaborations_list_by_file(
        client=box_client_ccg, file_id=test_file.id
    )

    collaborations = result_collaborations.get("collaborations", None)
    error = result_collaborations.get("error", None)
    message = result_collaborations.get("message", None)

    # expected result is no error, 0 collaborations and a message
    assert message == "No collaborations found for the specified file."
    assert collaborations is None or collaborations == []
    assert error is None, f"Error occurred: {error}"

    # Test invalid file id
    invalid_file_id = "1234567890"  # assuming this file ID does not exist
    result_collaborations = box_collaborations_list_by_file(
        client=box_client_ccg, file_id=invalid_file_id
    )

    collaborations = result_collaborations.get("collaborations", None)
    error = result_collaborations.get("error", None)
    message = result_collaborations.get("message", None)

    # expected result is an error and no collaborations
    assert collaborations is None or collaborations == []
    assert error is not None, "Expected error for invalid file ID."
    assert message is None, f"Unexpected message: {message}"


@pytest.mark.order(index=20)
def test_box_collaborations_list_by_folder_no_collaborations(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert collaborations_test_files.test_folder is not None
    assert collaborations_test_files.test_folder.id is not None

    test_folder = collaborations_test_files.test_folder
    result_collaborations = box_collaborations_list_by_folder(
        client=box_client_ccg, folder_id=test_folder.id
    )

    collaborations = result_collaborations.get("collaborations", None)
    error = result_collaborations.get("error", None)
    message = result_collaborations.get("message", None)

    # expected result is no error, 0 collaborations and a message
    assert message == "No collaborations found for the specified folder."
    assert collaborations is None or collaborations == []
    assert error is None, f"Error occurred: {error}"

    # Test invalid folder id
    invalid_folder_id = "1234567890"  # assuming this folder ID does not exist
    result_collaborations = box_collaborations_list_by_folder(
        client=box_client_ccg, folder_id=invalid_folder_id
    )

    collaborations = result_collaborations.get("collaborations", None)
    error = result_collaborations.get("error", None)
    message = result_collaborations.get("message", None)

    # expected result is an error and no collaborations
    assert collaborations is None or collaborations == []
    assert error is not None, "Expected error for invalid folder ID."
    assert message is None, f"Unexpected message: {message}"


@pytest.mark.order(index=30)
def test_box_collaboration_file_user_by_user_id(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test file to work with
    assert collaborations_test_files.test_files is not None
    assert len(collaborations_test_files.test_files) > 0

    test_file = collaborations_test_files.test_files[0]
    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None
    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com

    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_id = test_user.id

    result = box_collaboration_file_user_by_user_id(
        client=box_client_ccg,
        file_id=test_file.id,
        user_id=test_user_id,
        role="editor",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )

    collaboration = result.get("collaboration", None)
    error = result.get("error", None)

    # expected result is no error and a collaboration object
    assert collaboration is not None, "No collaboration returned."
    assert error is None, f"Error occurred: {error}"
    assert collaboration["accessible_by"]["id"] == test_user_id
    assert collaboration["role"] == "editor"

    # clean up by removing the collaboration
    try:
        box_client_ccg.user_collaborations.delete_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
    except Exception as e:
        print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")


@pytest.mark.order(index=40)
def test_box_collaboration_file_user_by_user_login(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test file to work with
    assert collaborations_test_files.test_files is not None
    assert len(collaborations_test_files.test_files) > 0

    test_file = collaborations_test_files.test_files[0]
    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None
    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com

    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_login = test_user.login
    assert test_user_login is not None, "No login found for test user."

    result = box_collaboration_file_user_by_user_login(
        client=box_client_ccg,
        file_id=test_file.id,
        user_login=test_user_login,
        role="editor",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )

    collaboration = result.get("collaboration", None)
    error = result.get("error", None)
    message = result.get("message", None)

    # expected result is no error and a collaboration object
    assert error is None, f"Error occurred: {error}"
    assert message is None, f"Unexpected message: {message}"
    assert collaboration is not None, "No collaboration returned."
    assert collaboration["accessible_by"]["login"] == test_user_login
    assert collaboration["role"] == "editor"

    # clean up by removing the collaboration
    try:
        box_client_ccg.user_collaborations.delete_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
    except Exception as e:
        print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")


@pytest.mark.order(index=50)
def test_box_collaborations_list_by_file_many_collaborations(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test file to work with
    assert collaborations_test_files.test_files is not None
    assert len(collaborations_test_files.test_files) > 0

    test_file = collaborations_test_files.test_files[0]
    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None
    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get all users that are not me and the email ends in @boxdemo.com
    test_users = [
        user
        for user in all_users
        if user.id != user_me
        and user.login is not None
        and user.login.endswith("@boxdemo.com")
    ]
    assert len(test_users) >= 3, "Not enough suitable test users found."

    # collaborate with each user
    for user in test_users:
        result = box_collaboration_file_user_by_user_id(
            client=box_client_ccg,
            file_id=test_file.id,
            user_id=user.id,
            role="editor",
            is_access_only=False,
            expires_at=None,
            notify=False,
        )
        collaboration = result.get("collaboration", None)
        error = result.get("error", None)
        # ignore error if user is already a collaborator
        # '400 User is already a collaborator' in error message
        if error and "400 User is already a collaborator" in error:
            continue
        # otherwise assert no error and collaboration is returned
        assert error is None, f"Error occurred for user {user.id}: {error}"
        assert collaboration is not None, (
            f"No collaboration returned for user {user.id}."
        )
        assert collaboration["accessible_by"]["id"] == user.id
        assert collaboration["role"] == "editor"

    # list collaborations
    result_collaborations = box_collaborations_list_by_file(
        client=box_client_ccg, file_id=test_file.id, limit=2
    )
    collaborations = result_collaborations.get("collaborations", None)
    error = result_collaborations.get("error", None)
    message = result_collaborations.get("message", None)

    # expected result is no error, multiple collaborations and no message
    assert message is None, f"Unexpected message: {message}"
    assert collaborations is not None and len(collaborations) >= len(test_users)
    assert error is None, f"Error occurred: {error}"

    # remove all collaborators except me
    for collaboration in collaborations:
        if (
            collaboration["accessible_by"]["id"] != user_me
            and collaboration["status"] == "accepted"
        ):
            try:
                box_client_ccg.user_collaborations.delete_collaboration_by_id(
                    collaboration_id=collaboration["id"]
                )
            except Exception as e:
                print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")

    # check that all collaborators except me are removed
    result_collaborations = box_collaborations_list_by_file(
        client=box_client_ccg, file_id=test_file.id
    )
    collaborations = result_collaborations.get("collaborations", None)
    error = result_collaborations.get("error", None)
    message = result_collaborations.get("message", None)

    # expected results are no error, no collaborations and a message saying no collaborations found
    assert message == "No collaborations found for the specified file."
    assert error is None, f"Error occurred: {error}"
    assert collaborations is None or collaborations == []


@pytest.mark.order(index=60)
def test_box_collaborations_list_by_folder_many_collaborations(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert collaborations_test_files.test_folder is not None
    assert collaborations_test_files.test_folder.id is not None

    test_folder = collaborations_test_files.test_folder
    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None
    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get all users that are not me and the email ends in @boxdemo.com
    test_users = [
        user
        for user in all_users
        if user.id != user_me
        and user.login is not None
        and user.login.endswith("@boxdemo.com")
    ]
    assert len(test_users) >= 3, "Not enough suitable test users found."

    # collaborate with each user
    for user in test_users:
        result = box_collaboration_folder_user_by_user_id(
            client=box_client_ccg,
            folder_id=test_folder.id,
            user_id=user.id,
            role="editor",
            is_access_only=False,
            expires_at=None,
            notify=False,
        )
        collaboration = result.get("collaboration", None)
        error = result.get("error", None)
        # ignore error if user is already a collaborator
        # '400 User is already a collaborator' in error message
        if error and "400 User is already a collaborator" in error:
            continue
        # otherwise assert no error and collaboration is returned
        assert error is None, f"Error occurred for user {user.id}: {error}"
        assert collaboration is not None, (
            f"No collaboration returned for user {user.id}."
        )
        assert collaboration["accessible_by"]["id"] == user.id
        assert collaboration["role"] == "editor"

    # list collaborations
    result_collaborations = box_collaborations_list_by_folder(
        client=box_client_ccg, folder_id=test_folder.id, limit=2
    )
    collaborations = result_collaborations.get("collaborations", None)
    error = result_collaborations.get("error", None)
    message = result_collaborations.get("message", None)

    # expected result is no error, multiple collaborations and no message
    assert error is None, f"Error occurred: {error}"
    assert message is None, f"Unexpected message: {message}"
    assert collaborations is not None and len(collaborations) >= len(test_users)

    # remove all collaborators except me
    for collaboration in collaborations:
        if (
            collaboration["accessible_by"]["id"] != user_me
            and collaboration["status"] == "accepted"
        ):
            try:
                box_client_ccg.user_collaborations.delete_collaboration_by_id(
                    collaboration_id=collaboration["id"]
                )
            except Exception as e:
                print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")

    # check that all collaborators except me are removed
    result_collaborations = box_collaborations_list_by_folder(
        client=box_client_ccg, folder_id=test_folder.id
    )

    error = result_collaborations.get("error", None)
    message = result_collaborations.get("message", None)
    collaborations = result_collaborations.get("collaborations", None)

    # expected results are no error, no collaborations and a message saying no collaborations found
    assert message == "No collaborations found for the specified folder."
    assert error is None, f"Error occurred: {error}"
    assert collaborations is None or collaborations == []


@pytest.mark.order(index=70)
def test_box_collaboration_folder_user_by_user_id(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert collaborations_test_files.test_folder is not None
    assert collaborations_test_files.test_folder.id is not None

    test_folder = collaborations_test_files.test_folder
    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None
    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com

    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_id = test_user.id

    result = box_collaboration_folder_user_by_user_id(
        client=box_client_ccg,
        folder_id=test_folder.id,
        user_id=test_user_id,
        role="editor",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )

    error = result.get("error", None)
    message = result.get("message", None)
    collaboration = result.get("collaboration", None)

    # expected result is no error and a collaboration object
    assert error is None, f"Error occurred: {error}"
    assert message is None, f"Unexpected message: {message}"
    assert collaboration is not None, "No collaboration returned."

    assert collaboration["accessible_by"]["id"] == test_user_id
    assert collaboration["role"] == "editor"

    # clean up by removing the collaboration
    try:
        box_client_ccg.user_collaborations.delete_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
    except Exception as e:
        print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")

    # test with invalid role
    result_invalid_role = box_collaboration_folder_user_by_user_id(
        client=box_client_ccg,
        folder_id=test_folder.id,
        user_id=test_user_id,
        role="invalid_role",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )

    error = result_invalid_role.get("error", None)
    message = result_invalid_role.get("message", None)
    collaboration = result_invalid_role.get("collaboration", None)

    # expected result is an error and no collaboration  object
    assert collaboration is None, "Expected no collaboration returned."
    assert error is not None, "Expected error for invalid role."
    assert message is None, f"Unexpected message: {message}"
    assert "Invalid role" in error, f"Unexpected error message: {error}"


@pytest.mark.order(index=80)
def test_box_collaboration_folder_user_by_user_login(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert collaborations_test_files.test_folder is not None
    assert collaborations_test_files.test_folder.id is not None

    test_folder = collaborations_test_files.test_folder
    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None
    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com

    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_login = test_user.login
    assert test_user_login is not None, "No login found for test user."

    result = box_collaboration_folder_user_by_user_login(
        client=box_client_ccg,
        folder_id=test_folder.id,
        user_login=test_user_login,
        role="editor",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )

    error = result.get("error", None)
    message = result.get("message", None)
    collaboration = result.get("collaboration", None)

    # expected result is no error and a collaboration object
    assert error is None, f"Error occurred: {error}"
    assert message is None, f"Unexpected message: {message}"
    assert collaboration is not None, "No collaboration returned."

    assert collaboration["accessible_by"]["login"] == test_user_login
    assert collaboration["role"] == "editor"

    # clean up by removing the collaboration
    try:
        box_client_ccg.user_collaborations.delete_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
    except Exception as e:
        print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")

    # test using an invalid role
    result_invalid_role = box_collaboration_folder_user_by_user_login(
        client=box_client_ccg,
        folder_id=test_folder.id,
        user_login=test_user_login,
        role="invalid_role",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )

    error = result_invalid_role.get("error", None)
    message = result_invalid_role.get("message", None)
    collaboration = result_invalid_role.get("collaboration", None)

    # expected result is an error and no collaboration  object
    assert collaboration is None, "Expected no collaboration returned."
    assert error is not None, "Expected error for invalid role."
    assert message is None, f"Unexpected message: {message}"
    assert "Invalid role" in error, f"Unexpected error message: {error}"


@pytest.mark.order(index=90)
def test_box_collaboration_file_group_by_group_id(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test file to work with
    assert collaborations_test_files.test_files is not None
    assert len(collaborations_test_files.test_files) > 0

    test_file = collaborations_test_files.test_files[0]

    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    test_group = _prep_test_group(box_client_ccg)
    assert test_group is not None
    assert test_group.id is not None

    result = box_collaboration_file_group_by_group_id(
        client=box_client_ccg,
        file_id=test_file.id,
        group_id=test_group.id,
        role="editor",
        expires_at=None,
        notify=False,
    )

    error = result.get("error", None)
    message = result.get("message", None)
    collaboration = result.get("collaboration", None)

    # expected result is no error and a collaboration object
    assert error is None, f"Error occurred: {error}"
    assert message is None, f"Unexpected message: {message}"
    assert collaboration is not None, "No collaboration returned."

    assert collaboration["accessible_by"]["id"] == test_group.id
    assert collaboration["role"] == "editor"

    # clean up by removing the collaboration
    try:
        box_client_ccg.user_collaborations.delete_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
    except Exception as e:
        print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")

    # clean up by removing the group
    try:
        box_client_ccg.groups.delete_group_by_id(group_id=test_group.id)
    except Exception as e:
        print(f"Error deleting group {test_group.id}: {str(e)}")


@pytest.mark.order(index=100)
def test_box_collaboration_folder_group_by_group_id(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test folder to work with
    assert collaborations_test_files.test_folder is not None
    assert collaborations_test_files.test_folder.id is not None

    test_folder = collaborations_test_files.test_folder

    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    test_group = _prep_test_group(box_client_ccg)
    assert test_group is not None
    assert test_group.id is not None

    result = box_collaboration_folder_group_by_group_id(
        client=box_client_ccg,
        folder_id=test_folder.id,
        group_id=test_group.id,
        role="editor",
        expires_at=None,
        notify=False,
    )

    error = result.get("error", None)
    message = result.get("message", None)
    collaboration = result.get("collaboration", None)

    # expected result is no error and a collaboration object
    assert error is None, f"Error occurred: {error}"
    assert message is None, f"Unexpected message: {message}"
    assert collaboration is not None, "No collaboration returned."

    assert collaboration["accessible_by"]["id"] == test_group.id
    assert collaboration["role"] == "editor"

    # test using an invalid role
    result_invalid_role = box_collaboration_folder_group_by_group_id(
        client=box_client_ccg,
        folder_id=test_folder.id,
        group_id=test_group.id,
        role="invalid_role",
        expires_at=None,
        notify=False,
    )

    error = result_invalid_role.get("error", None)
    message = result_invalid_role.get("message", None)
    collaboration_invalid_role = result_invalid_role.get("collaboration", None)

    # expected result is an error and no collaboration  object
    assert collaboration_invalid_role is None, "Expected no collaboration returned."
    assert error is not None, "Expected error for invalid role."
    assert message is None, f"Unexpected message: {message}"
    assert "Invalid role" in error, f"Unexpected error message: {error}"

    # clean up by removing the collaboration
    try:
        box_client_ccg.user_collaborations.delete_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
    except Exception as e:
        print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")

    # clean up by removing the group
    try:
        box_client_ccg.groups.delete_group_by_id(group_id=test_group.id)
    except Exception as e:
        print(f"Error deleting group {test_group.id}: {str(e)}")


@pytest.mark.order(index=110)
def test_box_collaboration_delete(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test file to work with
    assert collaborations_test_files.test_files is not None
    assert len(collaborations_test_files.test_files) > 0

    test_file = collaborations_test_files.test_files[0]

    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com

    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_id = test_user.id

    result = box_collaboration_file_user_by_user_id(
        client=box_client_ccg,
        file_id=test_file.id,
        user_id=test_user_id,
        role="editor",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )

    collaboration = result.get("collaboration", None)
    error = result.get("error", None)

    # expected result is no error and a collaboration object
    assert collaboration is not None, "No collaboration returned."
    assert error is None, f"Error occurred: {error}"
    assert collaboration["accessible_by"]["id"] == test_user_id
    assert collaboration["role"] == "editor"

    # now delete the collaboration using the box_collaboration_delete function
    delete_result = box_collaboration_delete(
        client=box_client_ccg, collaboration_id=collaboration["id"]
    )
    delete_error = delete_result.get("error", None)
    delete_message = delete_result.get("message", None)

    # expected result is no error and a success message
    assert delete_error is None, f"Error occurred during delete: {delete_error}"
    assert (
        delete_message == f"Collaboration {collaboration['id']} deleted successfully."
    ), f"Unexpected message: {delete_message}"

    # verify the collaboration is deleted by attempting to get it
    try:
        box_client_ccg.user_collaborations.get_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
        assert False, "Collaboration still exists after deletion."
    except Exception as e:
        # expected exception since the collaboration should not exist
        assert "404" in str(e), f"Unexpected error when verifying deletion: {str(e)}"

    # clean up by removing the collaboration if it still exists
    try:
        box_client_ccg.user_collaborations.delete_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
    except Exception:
        pass  # ignore errors here since we expect it to be deleted already


@pytest.mark.order(index=120)
def test_box_collaboration_update(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    # Ensure we have a test file to work with
    assert collaborations_test_files.test_files is not None
    assert len(collaborations_test_files.test_files) > 0

    test_file = collaborations_test_files.test_files[0]

    user_me = box_client_ccg.users.get_user_me().id
    assert user_me is not None

    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    # Get the first user that is not me and the email ends in @boxdemo.com

    test_user = next(
        (
            user
            for user in all_users
            if user.id != user_me
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_id = test_user.id

    result = box_collaboration_file_user_by_user_id(
        client=box_client_ccg,
        file_id=test_file.id,
        user_id=test_user_id,
        role="editor",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )

    error = result.get("error", None)
    message = result.get("message", None)
    collaboration = result.get("collaboration", None)

    # expected result is no error and a collaboration object
    assert error is None, f"Error occurred: {error}"
    assert message is None, f"Unexpected message: {message}"
    assert collaboration is not None, "No collaboration returned."

    assert collaboration["accessible_by"]["id"] == test_user_id
    assert collaboration["role"] == "editor"

    # now update the collaboration using the box_collaboration_update function
    update_result = box_collaboration_update(
        client=box_client_ccg,
        collaboration_id=collaboration["id"],
        role="viewer",
    )
    update_error = update_result.get("error", None)
    update_message = update_result.get("message", None)
    updated_collaboration = update_result.get("collaboration", None)

    # expected result is no error and an updated collaboration object
    assert update_error is None, f"Error occurred during update: {update_error}"
    assert update_message is None, f"Unexpected message: {update_message}"
    assert updated_collaboration is not None, "No updated collaboration returned."
    assert updated_collaboration["id"] == collaboration["id"]
    assert updated_collaboration["role"] == "viewer"

    # clean up by removing the collaboration
    try:
        box_client_ccg.user_collaborations.delete_collaboration_by_id(
            collaboration_id=collaboration["id"]
        )
    except Exception as e:
        print(f"Error deleting collaboration {collaboration['id']}: {str(e)}")

    # test using an invalid status
    result_invalid_status = box_collaboration_update(
        client=box_client_ccg,
        collaboration_id=collaboration["id"],
        role="editor",
        status="invalid_status",
    )
    error = result_invalid_status.get("error", None)
    message = result_invalid_status.get("message", None)
    collaboration_invalid_status = result_invalid_status.get("collaboration", None)
    # expected result is an error and no collaboration  object
    assert collaboration_invalid_status is None, "Expected no collaboration returned."
    assert error is not None, "Expected error for invalid status."
    assert message is None, f"Unexpected message: {message}"
    assert "Invalid status" in error, f"Unexpected error message: {error}"


@pytest.mark.order(index=130)
def test_box_collaboration_invalid_file_all_file_methods(
    box_client_ccg: BoxClient, collaborations_test_files: TestData
):
    invalid_file_id = "1234567890"  # assuming this file ID does not exist

    # Test list by file
    list_result = box_collaborations_list_by_file(
        client=box_client_ccg, file_id=invalid_file_id
    )
    list_error = list_result.get("error", None)
    assert list_error is not None, "Expected error for invalid file ID in list_by_file."

    # Test create collaboration by user ID
    create_user_id_result = box_collaboration_file_user_by_user_id(
        client=box_client_ccg,
        file_id=invalid_file_id,
        user_id="12345",  # arbitrary user ID
        role="editor",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )
    create_user_id_error = create_user_id_result.get("error", None)
    assert create_user_id_error is not None, (
        "Expected error for invalid file ID in create by user ID."
    )

    # Test create collaboration delete
    delete_result = box_collaboration_delete(
        client=box_client_ccg,
        collaboration_id="12345",  # arbitrary collaboration ID
    )
    delete_error = delete_result.get("error", None)
    assert delete_error is not None, (
        "Expected error for invalid collaboration ID in delete."
    )

    # Test update collaboration
    update_result = box_collaboration_update(
        client=box_client_ccg,
        collaboration_id="12345",  # arbitrary collaboration ID
        role="viewer",
    )
    update_error = update_result.get("error", None)
    assert update_error is not None, (
        "Expected error for invalid collaboration ID in update."
    )

    # Test using invalid role for create and update
    create_invalid_role_result = box_collaboration_file_user_by_user_id(
        client=box_client_ccg,
        file_id=invalid_file_id,
        user_id="12345",  # arbitrary user ID
        role="invalid_role",
        is_access_only=False,
        expires_at=None,
        notify=False,
    )
    create_invalid_role_error = create_invalid_role_result.get("error", None)
    assert create_invalid_role_error is not None, (
        "Expected error for invalid role in create collaboration."
    )

    update_invalid_role_result = box_collaboration_update(
        client=box_client_ccg,
        collaboration_id="12345",  # arbitrary collaboration ID
        role="invalid_role",
    )
    update_invalid_role_error = update_invalid_role_result.get("error", None)
    assert update_invalid_role_error is not None, (
        "Expected error for invalid role in update collaboration."
    )
