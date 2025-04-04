import pytest
from dotenv import load_dotenv

from src.box_ai_agents_toolkit import (
    BoxClient,
    get_ccg_client,
    # get_oauth_client,
)

# @pytest.fixture
# def box_client_auth() -> BoxClient:
#     return get_oauth_client()


@pytest.fixture
def box_client_ccg() -> BoxClient:
    load_dotenv()
    return get_ccg_client()
