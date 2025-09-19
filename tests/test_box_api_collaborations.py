from box_ai_agents_toolkit import (
    box_collaborations_list_by_file,
    box_collaboration_file_user_by_user_id,
    box_collaboration_file_user_by_user_login,
)
from box_sdk_gen import BoxClient
from .conftest import TestData
import pytest


@pytest.mark.order(index=1)
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


@pytest.mark.order(index=2)
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


@pytest.mark.order(index=3)
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


@pytest.mark.order(index=4)
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
