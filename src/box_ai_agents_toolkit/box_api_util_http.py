import requests

from box_ai_agents_toolkit import BoxClient, BoxSDKError


def _do_request(box_client: BoxClient, url: str):
    """
    Performs a GET request to a Box API endpoint using the provided Box client.

    This is an internal helper function and should not be called directly.

    Args:
        box_client (BoxClient): An authenticated Box client object.
        url (str): The URL of the Box API endpoint to make the request to.

    Returns:
        bytes: The content of the response from the Box API.

    Raises:
        BoxSDKError: If an error occurs while retrieving the access token.
        requests.exceptions.RequestException: If the request fails (e.g., network error,
                                             4XX or 5XX status code).
    """
    try:
        access_token = box_client.auth.retrieve_token().access_token
        resp = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
        resp.raise_for_status()
        return resp.content
    except BoxSDKError as e:
        raise BoxSDKError(f"Failed to retrieve access token: {e.message}")
    except requests.HTTPError as e:
        raise requests.HTTPError(
            f"Request failed: {e.response.text if e.response else str(e)}"
        )
