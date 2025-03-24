import pytest
from dotenv import load_dotenv
from box_sdk_gen import BoxClient
from src.box_ai_agents_toolkit import (
    get_ccg_client,
    # get_oauth_client,
)

load_dotenv()

# @pytest.fixture
# def box_client_auth() -> BoxClient:
#     return get_oauth_client()


@pytest.fixture
def box_client_ccg() -> BoxClient:
    return get_ccg_client()
