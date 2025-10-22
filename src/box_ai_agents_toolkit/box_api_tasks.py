from datetime import datetime as DateTime
from datetime import timezone
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    CreateTaskAction,
    CreateTaskAssignmentAssignTo,
    CreateTaskAssignmentTask,
    CreateTaskAssignmentTaskTypeField,
    CreateTaskCompletionRule,
    CreateTaskItem,
    CreateTaskItemTypeField,
    UpdateTaskAssignmentByIdResolutionState,
    UpdateTaskByIdCompletionRule,
)

from .box_api_util_generic import log_box_api_error


def _current_user_timezone(client: BoxClient) -> Optional[ZoneInfo]:
    """
    Helper function to get the current user's timezone.
    Args:
        client (BoxClient): Authenticated Box client.
    Returns:
        Optional[ZoneInfo]: Timezone of the current user or None if not available.
    """

    user = client.users.get_user_me()
    if user.timezone:
        # Convert IANA timezone string (e.g., 'America/New_York') to ZoneInfo object
        try:
            return ZoneInfo(user.timezone)
        except Exception:
            # If timezone string is invalid, fall back to UTC
            return ZoneInfo("UTC")
    return None


def _task_create(
    client: BoxClient,
    file_id: str,
    action: CreateTaskAction,
    due_at: Optional[DateTime] = None,
    message: Optional[str] = None,
    requires_all_assignees_to_complete: bool = False,
) -> Dict[str, Any]:
    """
    Helper function to create a task in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to create the task for.
        action (CreateTaskAction): The action for the task.
        due_at (Optional[DateTime]): Due date for the task.
        message (Optional[str]): Message or description for the task.
        requires_all_assignees_to_complete: bool = False: Whether all assignees must complete the task.
    Returns:
        Dict[str, Any]: Dictionary containing created task details or error message.
    """
    if requires_all_assignees_to_complete:
        completion_rule = CreateTaskCompletionRule.ALL_ASSIGNEES
    else:
        completion_rule = CreateTaskCompletionRule.ANY_ASSIGNEE

    item = CreateTaskItem(id=file_id, type=CreateTaskItemTypeField.FILE)
    if due_at is not None:
        # If datetime is naive (no timezone), add user's timezone or UTC
        if due_at.tzinfo is None:
            user_tz = _current_user_timezone(client)
            if user_tz is not None:
                due_at = due_at.replace(tzinfo=user_tz)
            else:
                due_at = due_at.replace(tzinfo=timezone.utc)
    try:
        task = client.tasks.create_task(
            item=item,
            action=action,
            due_at=due_at,
            message=message,
            completion_rule=completion_rule,
        )
        return {"task": task.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_file_list(
    client: BoxClient,
    file_id: str,
) -> Dict[str, Any]:
    """
    List all tasks associated with a specific file in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to list tasks for.
    Returns:
        Dict[str, Any]: Dictionary containing list of tasks or error or empty message.
    """
    try:
        tasks = client.tasks.get_file_tasks(file_id=file_id)
        if tasks.entries is None or len(tasks.entries) == 0:
            return {"message": "No tasks found for the specified file."}
        return {"tasks": [task.to_dict() for task in tasks.entries]}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_details(
    client: BoxClient,
    task_id: str,
) -> Dict[str, Any]:
    """
    Retrieve details of a specific task in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        task_id (str): ID of the task to retrieve details for.
    Returns:
        Dict[str, Any]: Dictionary containing task details or error message.
    """
    try:
        task = client.tasks.get_task_by_id(task_id=task_id)
        return {"task": task.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_review_create(
    client: BoxClient,
    file_id: str,
    due_at: Optional[DateTime] = None,
    message: Optional[str] = None,
    requires_all_assignees_to_complete: bool = False,
) -> Dict[str, Any]:
    """
    Create a new task for a specific file in Box of review type.
    This means the assignee needs to review the file, and output a approve or reject action.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to create the task for.
        due_at (Optional[DateTime]): Due date for the task.
        message (Optional[str]): Message or description for the task.
        requires_all_assignees_to_complete: bool = False: Whether all assignees must complete the task.
    Returns:
        Dict[str, Any]: Dictionary containing created task details or error message.
    """

    action = CreateTaskAction.REVIEW

    return _task_create(
        client=client,
        file_id=file_id,
        action=action,
        due_at=due_at,
        message=message,
        requires_all_assignees_to_complete=requires_all_assignees_to_complete,
    )


def box_task_complete_create(
    client: BoxClient,
    file_id: str,
    due_at: Optional[DateTime] = None,
    message: Optional[str] = None,
    requires_all_assignees_to_complete: bool = False,
) -> Dict[str, Any]:
    """
    Create a new task for a specific file in Box of completion type.
    This means the assignee needs to mark the task as complete once done.
    Args:
        client (BoxClient): Authenticated Box client.
        file_id (str): ID of the file to create the task for.
        due_at (Optional[DateTime]): Due date for the task.
        message (Optional[str]): Message or description for the task.
        requires_all_assignees_to_complete: bool = False: Whether all assignees must complete the task.
    Returns:
        Dict[str, Any]: Dictionary containing created task details or error message.
    """

    action = CreateTaskAction.COMPLETE

    return _task_create(
        client=client,
        file_id=file_id,
        action=action,
        due_at=due_at,
        message=message,
        requires_all_assignees_to_complete=requires_all_assignees_to_complete,
    )


def box_task_remove(
    client: BoxClient,
    task_id: str,
) -> Dict[str, Any]:
    """
    Remove a specific task in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        task_id (str): ID of the task to remove.
    Returns:
        Dict[str, Any]: Dictionary indicating success or containing error message.
    """
    try:
        client.tasks.delete_task_by_id(task_id=task_id)
        return {"message": "Task removed successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_update(
    client: BoxClient,
    task_id: str,
    due_at: Optional[DateTime] = None,
    message: Optional[str] = None,
    requires_all_assignees_to_complete: bool = False,
) -> Dict[str, Any]:
    """
    Update a specific task in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        task_id (str): ID of the task to update.
        due_at (Optional[DateTime]): New due date for the task.
        message (Optional[str]): New message or description for the task.
    Returns:
        Dict[str, Any]: Dictionary containing updated task details or error message.
    """
    if requires_all_assignees_to_complete:
        completion_rule = UpdateTaskByIdCompletionRule.ALL_ASSIGNEES
    else:
        completion_rule = UpdateTaskByIdCompletionRule.ANY_ASSIGNEE

    if due_at is not None:
        # If datetime is naive (no timezone), add user's timezone or UTC
        if due_at.tzinfo is None:
            user_tz = _current_user_timezone(client)
            if user_tz is not None:
                due_at = due_at.replace(tzinfo=user_tz)
            else:
                due_at = due_at.replace(tzinfo=timezone.utc)

    try:
        task = client.tasks.update_task_by_id(
            task_id=task_id,
            due_at=due_at,
            message=message,
            completion_rule=completion_rule,
        )
        return {"task": task.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_assignments_list(
    client: BoxClient,
    task_id: str,
) -> Dict[str, Any]:
    """
    List all assignments associated with a specific task in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        task_id (str): ID of the task to list assignments for.
    Returns:
        Dict[str, Any]: Dictionary containing list of assignments or error or empty message.
    """
    try:
        assignments = client.task_assignments.get_task_assignments(task_id=task_id)
        if assignments.entries is None or len(assignments.entries) == 0:
            return {"message": "No assignments found for the specified task."}
        return {
            "assignments": [assignment.to_dict() for assignment in assignments.entries]
        }
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_assignment_details(
    client: BoxClient,
    task_assignment_id: str,
) -> Dict[str, Any]:
    """
    Retrieve details of a specific task assignment in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        task_assignment_id (str): ID of the task assignment to retrieve details for.
    Returns:
        Dict[str, Any]: Dictionary containing task assignment details or error message.
    """
    try:
        assignment = client.task_assignments.get_task_assignment_by_id(
            task_assignment_id=task_assignment_id
        )
        return {"assignment": assignment.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_assign_by_user_id(
    client: BoxClient,
    task_id: str,
    user_id: str,
) -> Dict[str, Any]:
    """
    Assign a task to a user by their user ID in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        task_id (str): ID of the task to assign.
        user_id (str): ID of the user to assign the task to.
    Returns:
        Dict[str, Any]: Dictionary containing created task assignment details or error message.
    """

    task = CreateTaskAssignmentTask(
        id=task_id, type=CreateTaskAssignmentTaskTypeField.TASK
    )
    assign_to = CreateTaskAssignmentAssignTo(id=user_id)
    try:
        assignment = client.task_assignments.create_task_assignment(
            task=task,
            assign_to=assign_to,
        )
        return {"assignment": assignment.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_assign_by_email(
    client: BoxClient,
    task_id: str,
    email: str,
) -> Dict[str, Any]:
    """
    Assign a task to a user by their email in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        task_id (str): ID of the task to assign.
        email (str): Email of the user to assign the task to.
    Returns:
        Dict[str, Any]: Dictionary containing created task assignment details or error message.
    """

    task = CreateTaskAssignmentTask(
        id=task_id, type=CreateTaskAssignmentTaskTypeField.TASK
    )
    assign_to = CreateTaskAssignmentAssignTo(login=email)
    try:
        assignment = client.task_assignments.create_task_assignment(
            task=task,
            assign_to=assign_to,
        )
        return {"assignment": assignment.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_assignment_remove(
    client: BoxClient,
    task_assignment_id: str,
) -> Dict[str, Any]:
    """
    Remove a specific task assignment in Box.
    Args:
        client (BoxClient): Authenticated Box client.
        task_assignment_id (str): ID of the task assignment to remove.
    Returns:
        Dict[str, Any]: Dictionary indicating success or containing error message.
    """
    try:
        client.task_assignments.delete_task_assignment_by_id(
            task_assignment_id=task_assignment_id
        )
        return {"message": "Task assignment removed successfully."}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}


def box_task_assignment_update(
    client: BoxClient,
    task_assignment_id: str,
    is_positive_outcome: bool,
    message: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Updates a task assignment to mark it as complete or review outcome.

    Args:
        client (BoxClient): Authenticated Box client.
        task_assignment_id (str): ID of the task assignment to update.
        message (Optional[str]): Message or description for the task assignment update. None means no change
        is_positive_outcome (Optional[bool]):
            For review tasks: True for approved, False for rejected.
            For complete tasks: True for completed, False for incomplete.
            None means no change.
    Returns:
        Dict[str, Any]: Dictionary containing updated task assignment details or error message.
    """

    try:
        # get the task assignment details
        task_assignment = client.task_assignments.get_task_assignment_by_id(
            task_assignment_id=task_assignment_id
        )

        if not task_assignment or not task_assignment.item:
            return {"error": "Task assignment not found."}

        # get the file id from the task assignment
        file_id = task_assignment.item.id

        # list all tasks for the file
        file_tasks = client.tasks.get_file_tasks(file_id=file_id).entries
        if not file_tasks:
            return {"error": "No tasks found for the associated file."}

        task_action = None

        for task in file_tasks:
            if (
                not task.task_assignment_collection
                or not task.task_assignment_collection.entries
                or len(task.task_assignment_collection.entries) == 0
            ):
                continue

            for task_assignment in task.task_assignment_collection.entries:
                if task_assignment.id == task_assignment_id:
                    task_action = task.action
                    break
        if task_action is None:
            return {"error": "Unable to identify type of task (Complete/Review)."}

        resolution_state = None

        match task_action:
            case CreateTaskAction.COMPLETE:
                # complete task
                match is_positive_outcome:
                    case False:
                        resolution_state = (
                            UpdateTaskAssignmentByIdResolutionState.INCOMPLETE
                        )
                    case True:
                        resolution_state = (
                            UpdateTaskAssignmentByIdResolutionState.COMPLETED
                        )

            case CreateTaskAction.REVIEW:
                match is_positive_outcome:
                    case False:
                        resolution_state = (
                            UpdateTaskAssignmentByIdResolutionState.REJECTED
                        )
                    case True:
                        resolution_state = (
                            UpdateTaskAssignmentByIdResolutionState.APPROVED
                        )

        if (
            task_action == CreateTaskAction.COMPLETE
            and resolution_state == UpdateTaskAssignmentByIdResolutionState.INCOMPLETE
        ):
            # For complete tasks, Box API does not allow marking as incomplete via update.
            return {
                "message": "Any update to this task's state must be a positive outcome (complete)."
            }

        task_assignment = client.task_assignments.update_task_assignment_by_id(
            task_assignment_id=task_assignment_id,
            message=message,
            resolution_state=resolution_state,
        )
        return {"task assignment": task_assignment.to_dict()}
    except BoxAPIError as e:
        log_box_api_error(e)
        return {"error": e.message}
