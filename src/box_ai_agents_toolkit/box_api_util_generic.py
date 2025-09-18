import logging
from typing import Any, Dict, List, Optional
from box_sdk_gen import (
    BoxAPIError,
    DataSanitizer,
    BoxClient,
)

logging.basicConfig(level=logging.INFO)


def log_box_api_error(e: BoxAPIError) -> None:
    """Log details of a BoxAPIError."""
    data_sanitizer = DataSanitizer()
    logging.error(f"Box API Error: {e.response_info.print(data_sanitizer)}")
