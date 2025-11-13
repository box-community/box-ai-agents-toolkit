# Group Management

Tools for managing and searching Box groups.

## Search for Groups

Search for groups in the enterprise using a filter term.

```python
from box_ai_agents_toolkit import box_groups_search

result = box_groups_search(client, filter_term="Finance", limit=100)
print("Groups:", result)
```

### Parameters

- `client`: Authenticated Box client
- `filter_term`: Search term to filter groups
- `limit`: Maximum number of groups to return (default: 100)

## List Groups by User

Retrieve all groups that a specific user belongs to.

```python
from box_ai_agents_toolkit import box_groups_list_by_user

result = box_groups_list_by_user(client, user_id="123456")
print("User's groups:", result)
```

### Parameters

- `client`: Authenticated Box client
- `user_id`: ID of the user

## List Group Members

Retrieve all members of a specific group.

```python
from box_ai_agents_toolkit import box_groups_list_members

result = box_groups_list_members(client, group_id="654321")
print("Group members:", result)
```

### Parameters

- `client`: Authenticated Box client
- `group_id`: ID of the group

## Related Modules

- `box_api_groups.py` - Group management operations
