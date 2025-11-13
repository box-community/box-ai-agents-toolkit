# Tasks

Tools for creating and managing tasks on files in Box.

## Overview

Tasks allow you to assign work items to users for files. There are two types of tasks:
- **Review Tasks** - Assignees must approve or reject
- **Complete Tasks** - Assignees must mark as complete

## Task Types

### Review Task

Create a review task where assignees must approve or reject the file.

```python
from box_ai_agents_toolkit import box_task_review_create
from datetime import datetime, timedelta

due_date = datetime.now() + timedelta(days=7)
result = box_task_review_create(
    client,
    file_id="12345",
    due_at=due_date,
    message="Please review this document",
    requires_all_assignees_to_complete=False
)
print("Review task created:", result)
```

### Complete Task

Create a completion task where assignees must mark it as complete.

```python
from box_ai_agents_toolkit import box_task_complete_create
from datetime import datetime, timedelta

due_date = datetime.now() + timedelta(days=7)
result = box_task_complete_create(
    client,
    file_id="12345",
    due_at=due_date,
    message="Please complete this task",
    requires_all_assignees_to_complete=True
)
print("Complete task created:", result)
```

## Managing Tasks

### List Tasks for a File

```python
from box_ai_agents_toolkit import box_task_file_list

result = box_task_file_list(client, file_id="12345")
print("Tasks:", result)
```

### Get Task Details

```python
from box_ai_agents_toolkit import box_task_details

result = box_task_details(client, task_id="67890")
print("Task details:", result)
```

### Update Task

```python
from box_ai_agents_toolkit import box_task_update
from datetime import datetime, timedelta

new_due_date = datetime.now() + timedelta(days=14)
result = box_task_update(
    client,
    task_id="67890",
    due_at=new_due_date,
    message="Updated: Please review ASAP",
    requires_all_assignees_to_complete=True
)
print("Task updated:", result)
```

### Delete Task

```python
from box_ai_agents_toolkit import box_task_remove

result = box_task_remove(client, task_id="67890")
print("Task deleted:", result)
```

## Task Assignments

### Assign Task by User ID

```python
from box_ai_agents_toolkit import box_task_assign_by_user_id

result = box_task_assign_by_user_id(
    client,
    task_id="67890",
    user_id="11111"
)
print("Task assigned:", result)
```

### Assign Task by Email

```python
from box_ai_agents_toolkit import box_task_assign_by_email

result = box_task_assign_by_email(
    client,
    task_id="67890",
    email="user@example.com"
)
print("Task assigned:", result)
```

### List Task Assignments

```python
from box_ai_agents_toolkit import box_task_assignments_list

result = box_task_assignments_list(client, task_id="67890")
print("Assignments:", result)
```

### Get Assignment Details

```python
from box_ai_agents_toolkit import box_task_assignment_details

result = box_task_assignment_details(client, task_assignment_id="22222")
print("Assignment details:", result)
```

### Update Task Assignment

Complete or approve/reject a task assignment.

```python
from box_ai_agents_toolkit import box_task_assignment_update

# For review tasks: approve
result = box_task_assignment_update(
    client,
    task_assignment_id="22222",
    is_positive_outcome=True,
    message="Approved - looks good!"
)

# For review tasks: reject
result = box_task_assignment_update(
    client,
    task_assignment_id="22222",
    is_positive_outcome=False,
    message="Please revise section 3"
)

# For complete tasks: mark complete
result = box_task_assignment_update(
    client,
    task_assignment_id="22222",
    is_positive_outcome=True,
    message="Task completed"
)
print("Assignment updated:", result)
```

### Remove Task Assignment

```python
from box_ai_agents_toolkit import box_task_assignment_remove

result = box_task_assignment_remove(client, task_assignment_id="22222")
print("Assignment removed:", result)
```

## Parameters

### Task Parameters

- `file_id` - ID of the file to create task for
- `due_at` - DateTime when task is due (automatically converted to user's timezone)
- `message` - Description or instructions for the task
- `requires_all_assignees_to_complete` - If True, all assignees must complete; if False, any assignee can complete

### Assignment Update Parameters

- `is_positive_outcome` - For review tasks: True=approved, False=rejected; For complete tasks: True=completed
- `message` - Optional message with the update

## Related Modules

- `box_api_tasks.py` - Task operations
