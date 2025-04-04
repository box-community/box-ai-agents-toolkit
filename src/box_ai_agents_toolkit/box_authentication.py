import os
import uuid

from box_sdk_gen import (
    BoxCCGAuth,
    BoxClient,
    BoxOAuth,
    CCGConfig,
    FileWithInMemoryCacheTokenStorage,
    GetAuthorizeUrlOptions,
    OAuthConfig,
)

from .box_auth_callback import callback_handle_request, open_browser

# Environment variables
CLIENT_ID = os.getenv("BOX_CLIENT_ID")
CLIENT_SECRET = os.getenv("BOX_CLIENT_SECRET")
# CCG
SUBJECT_TYPE = os.getenv("BOX_SUBJECT_TYPE")
SUBJECT_ID = os.getenv("BOX_SUBJECT_ID")
# OAuth
REDIRECT_URL = os.environ.get("BOX_REDIRECT_URL", "http://localhost:8000/callback")


def get_auth_config() -> OAuthConfig:
    return OAuthConfig(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_storage=FileWithInMemoryCacheTokenStorage(".auth.oauth"),
    )


def get_ccg_config() -> CCGConfig:
    if SUBJECT_TYPE == "enterprise":
        enterprise_id = SUBJECT_ID
        user_id = None
    else:
        enterprise_id = None
        user_id = SUBJECT_ID

    return CCGConfig(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        enterprise_id=enterprise_id,
        user_id=user_id,
        token_storage=FileWithInMemoryCacheTokenStorage(".auth.ccg"),
    )


def get_ccg_client() -> BoxClient:
    conf = get_ccg_config()
    auth = BoxCCGAuth(conf)
    return add_extra_header_to_box_client(BoxClient(auth))


def get_oauth_client() -> BoxClient:
    conf = get_auth_config()
    auth = BoxOAuth(conf)
    return add_extra_header_to_box_client(BoxClient(auth))


def add_extra_header_to_box_client(box_client: BoxClient) -> BoxClient:
    """
    Add extra headers to the Box client.

    Args:
        box_client (BoxClient): A Box client object.
        header (Dict[str, str]): A dictionary of extra headers to add to the Box client.

    Returns:
        BoxClient: A Box client object with the extra headers added.
    """
    header = {"x-box-ai-library": "mcp-server-box"}
    return box_client.with_extra_headers(extra_headers=header)


def authorize_app() -> bool:
    conf = get_auth_config()
    auth = BoxOAuth(conf)

    state = str(uuid.uuid4())
    options = GetAuthorizeUrlOptions(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URL,
        state=state,
    )
    auth_url = auth.get_authorize_url(options=options)
    open_browser(auth_url)
    hostname = REDIRECT_URL.split(":")[1].replace("/", "")
    port = REDIRECT_URL.split(":")[2].split("/")[0]
    callback_handle_request(auth, hostname, int(port), state)

    access_token = auth.token_storage.get()
    if not access_token:
        return False

    return True
