# OAuth Callback Handler

Internal module for handling OAuth authentication callbacks.

## Overview

This module provides the callback server functionality used during OAuth authentication. It's automatically used by the authentication module and typically doesn't need to be called directly by users.

## Usage

This module is used internally when you call `get_oauth_client()`. The authentication flow:

1. Opens a browser window for user to authenticate
2. Starts a local callback server to receive the authorization code
3. Exchanges the code for access tokens
4. Returns an authenticated client

## Related Documentation

For user-facing authentication, see [Authentication](box_authentication.md).

## Related Modules

- `box_auth_callback.py` - OAuth callback server
- `box_authentication.py` - Main authentication module
