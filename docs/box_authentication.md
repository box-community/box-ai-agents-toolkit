# Authentication

The Box AI Agents Toolkit supports two authentication methods: OAuth 2.0 and Client Credentials Grant (CCG).

## CCG Authentication

CCG authentication is recommended for server-side applications and automated workflows.

### Configuration

Create a `.env` file with your CCG credentials:

```yaml
BOX_CLIENT_ID = "your client id"
BOX_CLIENT_SECRET = "your client secret"
BOX_SUBJECT_TYPE = "user/enterprise"
BOX_SUBJECT_ID = "user id/enterprise id"
```

### Usage

```python
from box_ai_agents_toolkit import get_ccg_client

client = get_ccg_client()
```

## OAuth Authentication

OAuth authentication is recommended for applications that need to act on behalf of a user.

### Configuration

Create a `.env` file with your OAuth credentials:

```yaml
BOX_CLIENT_ID = "your client id"
BOX_CLIENT_SECRET = "your client secret"
BOX_REDIRECT_URL = "http://localhost:8000/callback"
```

### Usage

```python
from box_ai_agents_toolkit import get_oauth_client

client = get_oauth_client()
```

The OAuth flow will open a browser window for user authentication and handle the callback automatically.

## Related Modules

- `box_authentication.py` - Core authentication implementation
- `box_auth_callback.py` - OAuth callback handler
