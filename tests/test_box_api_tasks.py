from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from box_sdk_gen import (
    BoxClient,
    CreateCollaborationAccessibleBy,
    CreateCollaborationAccessibleByTypeField,
    CreateCollaborationItem,
    CreateCollaborationItemTypeField,
    CreateCollaborationRole,
)

from box_ai_agents_toolkit import (
    box_task_assign_by_email,
    box_task_assign_by_user_id,
    box_task_assignment_details,
    box_task_assignment_remove,
    box_task_assignment_update,
    box_task_assignments_list,
    box_task_complete_create,
    box_task_details,
    box_task_file_list,
    box_task_remove,
    box_task_review_create,
    box_task_update,
)
from box_ai_agents_toolkit.box_api_tasks import _current_user_timezone

from .conftest import TestData


def test_box_task_review_create(box_client_ccg: BoxClient, tasks_test_data: TestData):
    """Test creating a review task for a file."""
    # Ensure we have test files
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]
    due_date = datetime.now() + timedelta(days=7)
    message = "Please review this file"

    # Create review task
    result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        due_at=due_date,
        message=message,
        requires_all_assignees_to_complete=False,
    )

    # Verify task was created successfully
    assert "task" in result
    assert "error" not in result
    assert result["task"]["message"] == message
    assert result["task"]["item"]["id"] == test_file.id
    assert result["task"]["action"] == "review"
    assert result["task"]["completion_rule"] == "any_assignee"


def test_box_task_review_create_all_assignees(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test creating a review task requiring all assignees to complete."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]
    message = "Critical review required"

    # Create review task requiring all assignees
    result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message=message,
        requires_all_assignees_to_complete=True,
    )

    # Verify task was created with correct completion rule
    assert "task" in result
    assert result["task"]["completion_rule"] == "all_assignees"


def test_box_task_complete_create(box_client_ccg: BoxClient, tasks_test_data: TestData):
    """Test creating a complete task for a file."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]
    due_date = datetime.now() + timedelta(days=3)
    message = "Please complete this task"

    # Create complete task
    result = box_task_complete_create(
        client=box_client_ccg,
        file_id=test_file.id,
        due_at=due_date,
        message=message,
        requires_all_assignees_to_complete=False,
    )

    # Verify task was created successfully
    assert "task" in result
    assert "error" not in result
    assert result["task"]["message"] == message
    assert result["task"]["item"]["id"] == test_file.id
    assert result["task"]["action"] == "complete"
    assert result["task"]["completion_rule"] == "any_assignee"


def test_box_tasks_file_list_with_tasks(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test listing tasks for a file that has tasks."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task first
    create_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Test task for listing",
    )
    assert "task" in create_result

    # List tasks for the file
    result = box_task_file_list(
        client=box_client_ccg,
        file_id=test_file.id,
    )

    # Verify tasks were listed
    assert "tasks" in result
    assert "error" not in result
    assert len(result["tasks"]) > 0
    assert any(task["id"] == create_result["task"]["id"] for task in result["tasks"])


def test_box_tasks_file_list_no_tasks(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test listing tasks for a file that has no tasks."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 1

    # Use a file that definitely has no tasks by finding one without any
    test_file = None
    for file in tasks_test_data.test_files:
        tasks_result = box_task_file_list(
            client=box_client_ccg,
            file_id=file.id,
        )
        if (
            "message" in tasks_result
            and tasks_result["message"] == "No tasks found for the specified file."
        ):
            test_file = file
            break

    # If all files have tasks, skip this test or use the last file and clean it
    if test_file is None:
        test_file = tasks_test_data.test_files[-1]
        # Clean up any existing tasks on this file
        tasks_result = box_task_file_list(
            client=box_client_ccg,
            file_id=test_file.id,
        )
        if "tasks" in tasks_result:
            for task in tasks_result["tasks"]:
                box_task_remove(client=box_client_ccg, task_id=task["id"])

    # List tasks for the file
    result = box_task_file_list(
        client=box_client_ccg,
        file_id=test_file.id,
    )

    # Verify the response shows no tasks
    assert "message" in result
    assert result["message"] == "No tasks found for the specified file."
    assert "error" not in result


def test_box_task_details(box_client_ccg: BoxClient, tasks_test_data: TestData):
    """Test retrieving details of a specific task."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]
    message = "Test task for details"

    # Create a task
    create_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message=message,
    )
    assert "task" in create_result
    task_id = create_result["task"]["id"]

    # Get task details
    result = box_task_details(
        client=box_client_ccg,
        task_id=task_id,
    )

    # Verify task details
    assert "task" in result
    assert "error" not in result
    assert result["task"]["id"] == task_id
    assert result["task"]["message"] == message


def test_box_task_update(box_client_ccg: BoxClient, tasks_test_data: TestData):
    """Test updating a task."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]
    original_message = "Original task message"

    # Create a task
    create_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message=original_message,
    )
    assert "task" in create_result
    task_id = create_result["task"]["id"]

    # Update the task
    updated_message = "Updated task message"
    new_due_date = datetime.now() + timedelta(days=14)
    result = box_task_update(
        client=box_client_ccg,
        task_id=task_id,
        message=updated_message,
        due_at=new_due_date,
        requires_all_assignees_to_complete=True,
    )

    # Verify update
    assert "task" in result
    assert "error" not in result
    assert result["task"]["id"] == task_id
    assert result["task"]["message"] == updated_message
    assert result["task"]["completion_rule"] == "all_assignees"


def test_box_task_remove(box_client_ccg: BoxClient, tasks_test_data: TestData):
    """Test removing a task."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task
    create_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task to be deleted",
    )
    assert "task" in create_result
    task_id = create_result["task"]["id"]

    # Remove the task
    result = box_task_remove(
        client=box_client_ccg,
        task_id=task_id,
    )

    # Verify removal
    assert "message" in result
    assert result["message"] == "Task removed successfully."
    assert "error" not in result

    # Verify task is actually deleted by trying to get details
    details_result = box_task_details(
        client=box_client_ccg,
        task_id=task_id,
    )
    assert "error" in details_result


def test_box_task_details_invalid_id(box_client_ccg: BoxClient):
    """Test retrieving details for a non-existent task."""
    invalid_task_id = "999999999"

    result = box_task_details(
        client=box_client_ccg,
        task_id=invalid_task_id,
    )

    # Verify error is returned
    assert "error" in result
    assert "task" not in result


def test_box_task_update_invalid_id(box_client_ccg: BoxClient):
    """Test updating a non-existent task."""
    invalid_task_id = "999999999"

    result = box_task_update(
        client=box_client_ccg,
        task_id=invalid_task_id,
        message="This should fail",
    )

    # Verify error is returned
    assert "error" in result
    assert "task" not in result


def test_box_task_remove_invalid_id(box_client_ccg: BoxClient):
    """Test removing a non-existent task."""
    invalid_task_id = "999999999"

    result = box_task_remove(
        client=box_client_ccg,
        task_id=invalid_task_id,
    )

    # Verify error is returned
    assert "error" in result
    assert (
        "message" not in result or result.get("message") != "Task removed successfully."
    )


def test_box_task_review_create_invalid_file_id(box_client_ccg: BoxClient):
    """Test creating a task for a non-existent file."""
    invalid_file_id = "999999999"

    result = box_task_review_create(
        client=box_client_ccg,
        file_id=invalid_file_id,
        message="This should fail",
    )

    # Verify error is returned
    assert "error" in result
    assert "task" not in result


def test_box_tasks_file_list_invalid_file_id(box_client_ccg: BoxClient):
    """Test listing tasks for a non-existent file."""
    invalid_file_id = "999999999"

    result = box_task_file_list(
        client=box_client_ccg,
        file_id=invalid_file_id,
    )

    # Verify error is returned
    assert "error" in result


def test_current_user_timezone_invalid(box_client_ccg: BoxClient):
    """Test that invalid timezone strings are handled gracefully."""
    # Mock the user response to return an invalid timezone
    mock_user = MagicMock()
    mock_user.timezone = "Invalid/Timezone/String"

    with patch.object(box_client_ccg.users, "get_user_me", return_value=mock_user):
        result = _current_user_timezone(box_client_ccg)

        # Should fall back to UTC when timezone is invalid
        assert result is not None
        assert str(result) == "UTC"


def test_current_user_timezone_valid(box_client_ccg: BoxClient):
    """Test that valid timezone strings are properly converted."""
    # Mock the user response to return a valid timezone
    mock_user = MagicMock()
    mock_user.timezone = "America/New_York"

    with patch.object(box_client_ccg.users, "get_user_me", return_value=mock_user):
        result = _current_user_timezone(box_client_ccg)

        # Should return the ZoneInfo object for America/New_York
        assert result is not None
        assert str(result) == "America/New_York"


def test_current_user_timezone_none(box_client_ccg: BoxClient):
    """Test that None timezone is handled gracefully."""
    # Mock the user response to return None for timezone
    mock_user = MagicMock()
    mock_user.timezone = None

    with patch.object(box_client_ccg.users, "get_user_me", return_value=mock_user):
        result = _current_user_timezone(box_client_ccg)

        # Should return None when user has no timezone set
        assert result is None


def test_task_create_with_timezone(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test creating a task with a naive datetime gets user's timezone applied."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a naive datetime (no timezone)
    naive_due_date = datetime(2025, 12, 31, 17, 0, 0)

    # Mock the user timezone to be America/New_York
    mock_user = MagicMock()
    mock_user.timezone = "America/New_York"

    with patch.object(box_client_ccg.users, "get_user_me", return_value=mock_user):
        result = box_task_review_create(
            client=box_client_ccg,
            file_id=test_file.id,
            due_at=naive_due_date,
            message="Task with timezone test",
        )

    # Verify task was created successfully
    assert "task" in result
    assert "error" not in result
    assert result["task"]["message"] == "Task with timezone test"
    # The due_at should be set with timezone information
    assert "due_at" in result["task"]


def test_task_create_with_invalid_timezone(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test creating a task when user has invalid timezone falls back to UTC."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a naive datetime (no timezone)
    naive_due_date = datetime(2025, 12, 31, 17, 0, 0)

    # Mock the user timezone to be invalid
    mock_user = MagicMock()
    mock_user.timezone = "Invalid/Bogus/Timezone"

    with patch.object(box_client_ccg.users, "get_user_me", return_value=mock_user):
        result = box_task_review_create(
            client=box_client_ccg,
            file_id=test_file.id,
            due_at=naive_due_date,
            message="Task with invalid timezone test",
        )

    # Verify task was created successfully despite invalid timezone
    # The function should fall back to UTC and still create the task
    assert "task" in result
    assert "error" not in result
    assert result["task"]["message"] == "Task with invalid timezone test"
    # The due_at should be set (with UTC as fallback)
    assert "due_at" in result["task"]


def test_box_task_assignments_list_with_assignments(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test listing assignments for a task that has assignments."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task for assignment listing test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user to assign task to
    current_user = box_client_ccg.users.get_user_me()

    # Assign task to current user
    assignment_result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=current_user.id,
    )
    assert "assignment" in assignment_result

    # List assignments for the task
    result = box_task_assignments_list(
        client=box_client_ccg,
        task_id=task_id,
    )

    # Verify assignments were listed
    assert "assignments" in result
    assert "error" not in result
    assert len(result["assignments"]) > 0
    assert any(
        assignment["id"] == assignment_result["assignment"]["id"]
        for assignment in result["assignments"]
    )


def test_box_task_assignments_list_no_assignments(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test listing assignments for a task that has no assignments."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task without any assignments
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task without assignments",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # List assignments for the task
    result = box_task_assignments_list(
        client=box_client_ccg,
        task_id=task_id,
    )

    # Verify the response shows no assignments
    assert "message" in result
    assert result["message"] == "No assignments found for the specified task."
    assert "error" not in result


def test_box_task_assignment_details(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test retrieving details of a specific task assignment."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task for assignment details test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user
    current_user = box_client_ccg.users.get_user_me()

    # Assign task to current user
    assignment_result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=current_user.id,
    )
    assert "assignment" in assignment_result
    assignment_id = assignment_result["assignment"]["id"]

    # Get assignment details
    result = box_task_assignment_details(
        client=box_client_ccg,
        task_assignment_id=assignment_id,
    )

    # Verify assignment details
    assert "assignment" in result
    assert "error" not in result
    assert result["assignment"]["id"] == assignment_id
    assert result["assignment"]["assigned_to"]["id"] == current_user.id


def test_box_task_assign_by_user_id(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test assigning a task to a user by user ID."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task for user ID assignment test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user
    current_user = box_client_ccg.users.get_user_me()

    # Assign task to current user
    result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=current_user.id,
    )

    # Verify assignment was created
    assert "assignment" in result
    assert "error" not in result
    assert result["assignment"]["assigned_to"]["id"] == current_user.id
    assert result["assignment"]["assigned_to"]["type"] == "user"


def test_box_task_assign_by_email(box_client_ccg: BoxClient, tasks_test_data: TestData):
    """Test assigning a task to a user by email."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task for email assignment test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user's email
    current_user = box_client_ccg.users.get_user_me()
    user_email = current_user.login
    assert user_email is not None, "User must have a login email"

    # Assign task to current user by email
    result = box_task_assign_by_email(
        client=box_client_ccg,
        task_id=task_id,
        email=user_email,
    )

    # Verify assignment was created
    assert "assignment" in result
    assert "error" not in result
    assert result["assignment"]["assigned_to"]["login"] == user_email
    assert result["assignment"]["assigned_to"]["type"] == "user"


def test_box_task_assignment_update_review_approved(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test updating a review task assignment to approved state."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a review task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Review task for approval test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user
    current_user = box_client_ccg.users.get_user_me()

    # Assign task to current user
    assignment_result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=current_user.id,
    )
    assert "assignment" in assignment_result
    assignment_id = assignment_result["assignment"]["id"]

    # Update assignment to approved
    result = box_task_assignment_update(
        client=box_client_ccg,
        task_assignment_id=assignment_id,
        message="Approved after review",
        is_positive_outcome=True,
    )

    # Verify update
    assert "task assignment" in result
    assert "error" not in result
    assert result["task assignment"]["resolution_state"] == "approved"
    assert result["task assignment"]["message"] == "Approved after review"


def test_box_task_assignment_update_review_rejected(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test updating a review task assignment to rejected state."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a review task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Review task for rejection test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user
    current_user = box_client_ccg.users.get_user_me()

    # Assign task to current user
    assignment_result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=current_user.id,
    )
    assert "assignment" in assignment_result
    assignment_id = assignment_result["assignment"]["id"]

    # Update assignment to rejected
    result = box_task_assignment_update(
        client=box_client_ccg,
        task_assignment_id=assignment_id,
        message="Rejected after review",
        is_positive_outcome=False,
    )

    # Verify update
    assert "task assignment" in result
    assert "error" not in result
    assert result["task assignment"]["resolution_state"] == "rejected"
    assert result["task assignment"]["message"] == "Rejected after review"


def test_box_task_assignment_update_complete_completed(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test updating a complete task assignment to completed state."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a complete task
    task_result = box_task_complete_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Complete task for completion test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user
    current_user = box_client_ccg.users.get_user_me()

    # Assign task to current user
    assignment_result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=current_user.id,
    )
    assert "assignment" in assignment_result
    assignment_id = assignment_result["assignment"]["id"]

    # Update assignment to completed
    result = box_task_assignment_update(
        client=box_client_ccg,
        task_assignment_id=assignment_id,
        message="Task completed",
        is_positive_outcome=True,
    )

    # Verify update
    assert "task assignment" in result
    assert "error" not in result
    assert result["task assignment"]["resolution_state"] == "completed"
    assert result["task assignment"]["message"] == "Task completed"


def test_box_task_assignment_update_complete_incomplete(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test updating a complete task assignment to incomplete state."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a complete task
    task_result = box_task_complete_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Complete task for incomplete test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user
    current_user = box_client_ccg.users.get_user_me()

    # Assign task to current user
    assignment_result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=current_user.id,
    )
    assert "assignment" in assignment_result
    assignment_id = assignment_result["assignment"]["id"]

    # Update assignment to incomplete
    result = box_task_assignment_update(
        client=box_client_ccg,
        task_assignment_id=assignment_id,
        message="Task still in progress",
        is_positive_outcome=False,
    )

    # Expect a message indicating an update to the assignment of this type implies the change to positive outcome
    # Example
    # {"message": "Any update to this task must change its state must be a positive outcome (complete)."}
    assert "message" in result

    assert "error" not in result


def test_box_task_assignment_remove(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test removing a task assignment."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task for assignment removal test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    # Get current user
    current_user = box_client_ccg.users.get_user_me()

    # Assign task to current user
    assignment_result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=current_user.id,
    )
    assert "assignment" in assignment_result
    assignment_id = assignment_result["assignment"]["id"]

    # We can't delete the only assignee of a task, so create a second assignment

    # Get the first user that is not me and the email ends in @boxdemo.com
    all_users = box_client_ccg.users.get_users().entries
    assert all_users is not None and len(all_users) > 0

    test_user = next(
        (
            user
            for user in all_users
            if user.id != current_user.id
            and user.login is not None
            and user.login.endswith("@boxdemo.com")
        ),
        None,
    )
    assert test_user is not None, "No suitable test user found."
    test_user_id = test_user.id

    # First we need to collaborate with the user to assign the task
    item = CreateCollaborationItem(
        type=CreateCollaborationItemTypeField.FILE,
        id=test_file.id,
    )
    accessible_by = CreateCollaborationAccessibleBy(
        id=test_user_id, type=CreateCollaborationAccessibleByTypeField.USER
    )
    box_client_ccg.user_collaborations.create_collaboration(
        item=item,
        accessible_by=accessible_by,
        role=CreateCollaborationRole.EDITOR,
    )

    # Now assign the task to the second user
    second_assignment_result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=test_user_id,
    )
    assert "assignment" in second_assignment_result
    second_assignment_id = second_assignment_result["assignment"]["id"]
    assert second_assignment_id != assignment_id

    # Remove the assignment
    result = box_task_assignment_remove(
        client=box_client_ccg,
        task_assignment_id=assignment_id,
    )

    # Verify removal
    assert "message" in result
    assert result["message"] == "Task assignment removed successfully."
    assert "error" not in result

    # Verify assignment is actually deleted by trying to get details
    details_result = box_task_assignment_details(
        client=box_client_ccg,
        task_assignment_id=assignment_id,
    )
    assert "error" in details_result


def test_box_task_assignments_list_invalid_task_id(box_client_ccg: BoxClient):
    """Test listing assignments for a non-existent task."""
    invalid_task_id = "999999999"

    result = box_task_assignments_list(
        client=box_client_ccg,
        task_id=invalid_task_id,
    )

    # Verify error is returned
    assert "error" in result


def test_box_task_assignment_details_invalid_id(box_client_ccg: BoxClient):
    """Test retrieving details for a non-existent task assignment."""
    invalid_assignment_id = "999999999"

    result = box_task_assignment_details(
        client=box_client_ccg,
        task_assignment_id=invalid_assignment_id,
    )

    # Verify error is returned
    assert "error" in result
    assert "assignment" not in result


def test_box_task_assign_by_user_id_invalid_task_id(box_client_ccg: BoxClient):
    """Test assigning a non-existent task."""
    invalid_task_id = "999999999"

    # Get current user
    current_user = box_client_ccg.users.get_user_me()

    result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=invalid_task_id,
        user_id=current_user.id,
    )

    # Verify error is returned
    assert "error" in result
    assert "assignment" not in result


def test_box_task_assign_by_user_id_invalid_user_id(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test assigning a task to a non-existent user."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task for invalid user test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    invalid_user_id = "999999999"

    result = box_task_assign_by_user_id(
        client=box_client_ccg,
        task_id=task_id,
        user_id=invalid_user_id,
    )

    # Verify error is returned
    assert "error" in result
    assert "assignment" not in result


def test_box_task_assign_by_email_invalid_email(
    box_client_ccg: BoxClient, tasks_test_data: TestData
):
    """Test assigning a task to a non-existent email."""
    assert tasks_test_data.test_files is not None
    assert len(tasks_test_data.test_files) > 0

    test_file = tasks_test_data.test_files[0]

    # Create a task
    task_result = box_task_review_create(
        client=box_client_ccg,
        file_id=test_file.id,
        message="Task for invalid email test",
    )
    assert "task" in task_result
    task_id = task_result["task"]["id"]

    invalid_email = "nonexistent@invalid-domain-12345.com"

    result = box_task_assign_by_email(
        client=box_client_ccg,
        task_id=task_id,
        email=invalid_email,
    )

    # Verify error is returned
    assert "error" in result
    assert "assignment" not in result


def test_box_task_assignment_update_invalid_id(box_client_ccg: BoxClient):
    """Test updating a non-existent task assignment."""
    invalid_assignment_id = "999999999"

    result = box_task_assignment_update(
        client=box_client_ccg,
        task_assignment_id=invalid_assignment_id,
        message="This should fail",
        is_positive_outcome=True,
    )

    # Verify error is returned
    assert "error" in result
    assert "task assignment" not in result


def test_box_task_assignment_remove_invalid_id(box_client_ccg: BoxClient):
    """Test removing a non-existent task assignment."""
    invalid_assignment_id = "999999999"

    result = box_task_assignment_remove(
        client=box_client_ccg,
        task_assignment_id=invalid_assignment_id,
    )

    # Verify error is returned
    assert "error" in result
    assert (
        "message" not in result
        or result.get("message") != "Task assignment removed successfully."
    )
