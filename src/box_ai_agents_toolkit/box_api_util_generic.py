import logging
from typing import Optional
from zoneinfo import ZoneInfo

from box_sdk_gen import (
    BoxAPIError,
    BoxClient,
    DataSanitizer,
)

logging.basicConfig(level=logging.INFO)


def log_box_api_error(e: BoxAPIError) -> None:
    """Log details of a BoxAPIError."""
    data_sanitizer = DataSanitizer()
    logging.error(f"Box API Error: {e.response_info.print(data_sanitizer)}")


def log_generic_error(e: Exception) -> None:
    """Log details of a generic exception."""
    logging.error(f"An error occurred: {str(e)}")


def current_user_timezone(client: BoxClient) -> Optional[ZoneInfo]:
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
