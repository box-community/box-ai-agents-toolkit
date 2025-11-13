# User Management

Tools for managing and searching Box users.

## Get User Information

### Get Current User

Retrieve information about the currently authenticated user.

```python
from box_ai_agents_toolkit import box_user_get_current

user = box_user_get_current(client)
print("Current user info:", user)
```

### Get User by ID

Retrieve information about a specific user by their ID.

```python
from box_ai_agents_toolkit import box_user_get_by_id

user = box_user_get_by_id(client, user_id="123456")
print("User info:", user)
```

## List Users

### List Users with Pagination

List users in the enterprise with pagination support.

```python
from box_ai_agents_toolkit import box_user_list

users = box_user_list(client, limit=10)
print("Users:", users)
```

### List All Users

Retrieve all users in the enterprise.

```python
from box_ai_agents_toolkit import box_users_list

result = box_users_list(client)
print("All users:", result)
```

## Search Users

### Search by Email

Find users by their email address.

```python
from box_ai_agents_toolkit import box_users_search_by_email

result = box_users_search_by_email(client, email="user@example.com")
print("Users with this email:", result)
```

### Locate by Name

Find users by their name.

```python
from box_ai_agents_toolkit import box_users_locate_by_name

result = box_users_locate_by_name(client, name="Jane Doe")
print("Users with this name:", result)
```

### Search by Name or Email

Search for users by either name or email using a general query.

```python
from box_ai_agents_toolkit import box_users_search_by_name_or_email

result = box_users_search_by_name_or_email(client, query="Jane")
print("Users matching query:", result)
```

## Related Modules

- `box_api_users.py` - User management operations
