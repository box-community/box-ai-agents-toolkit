import logging
from box_sdk_gen import (
    BoxAPIError,
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
