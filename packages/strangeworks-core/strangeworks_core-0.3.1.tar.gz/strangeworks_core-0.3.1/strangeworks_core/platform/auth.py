"""auth.py."""
from typing import Callable
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException

from strangeworks_core.errors.error import StrangeworksError

SDK_AUTH_URL = "users/token"
PRODUCT_AUTH_URL = "product/token"


def get_token(api_key: str, base_url: str, auth_url: str) -> str:
    """Obtain a bearer token using an API key."""
    auth_url = urljoin(base_url, auth_url)
    try:
        res = requests.post(auth_url, json={"key": api_key})
        if res.status_code != 200:
            raise StrangeworksError.authentication_error(
                message="Unable to exchange api key for bearer token"
            )
        payload = res.json()
        auth_token = payload.get("accessToken")
        return auth_token

    except RequestException:
        raise StrangeworksError.authentication_error(
            message="Unable to obtain bearer token using api key."
        )


def get_sdk_authenticator(base_url: str) -> Callable[[str], str]:
    """Convenience wrapper for generating an SDK authenticator."""
    return get_authenticator(base_url=base_url, auth_url=SDK_AUTH_URL)


def get_product_authenticator(base_url: str) -> Callable[[str], str]:
    """Convenience wrapper for generating an product/service authenticator."""
    return get_authenticator(base_url=base_url, auth_url=PRODUCT_AUTH_URL)


def get_authenticator(
    base_url: str,
    auth_url: str,
) -> Callable[[str], str]:
    """Generate a user authenticator function.

    Returns a Callable which is configured to use the given url to exchange api keys
    for user authentication tokens from the platform.

    Parameters
    ----------
    base_url: str
        URL for the Strangeworks platform.

    Return
    ------
    str
        The JWT token
    """
    url = urljoin(base_url, auth_url)

    def auth_fn(api_key: str) -> str:
        try:
            res = requests.post(url, json={"key": api_key})
            if res.status_code != 200:
                raise StrangeworksError.authentication_error(
                    message="Unable to exchange api key for bearer token"
                )
            payload = res.json()
            auth_token = payload.get("accessToken")
            return auth_token
        except RequestException:
            raise StrangeworksError.authentication_error(
                message="Unable to obtain bearer token using api key."
            )

    return auth_fn
