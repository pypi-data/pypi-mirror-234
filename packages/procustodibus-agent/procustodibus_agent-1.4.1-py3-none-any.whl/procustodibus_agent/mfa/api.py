# -*- coding: utf-8 -*-
"""MFA API utilities."""

import requests
from requests import Request

from procustodibus_agent.api import (
    API_TIMEOUT,
    encode_base64_web,
    raise_unless_has_cnf,
    send_with_session,
)
from procustodibus_agent.cnf import Cnf


def check_mfa_api(cnf, endpoint):
    """Checks if MFA for specified endpoint has expired.

    Arguments:
        cnf (Config): Config object.
        endpoint (str): Endpoint ID.

    Returns:
        str: OK, EXPIRED, UPDATING, or UNKNOWN.
    """
    if cnf is None:
        cnf = Cnf()
    response = requests.get(
        f"{cnf.api}/endpoints/{endpoint}/psk-rotation", timeout=API_TIMEOUT
    )
    response.raise_for_status()
    return response.text


def list_mfa_api(cnf):
    """Lists MFA state for all endpoints of the configured host.

    Arguments:
        cnf (Config): Config object.

    Returns:
        Response: Response json.
    """
    raise_unless_has_cnf(cnf)

    request = Request(
        "GET",
        f"{cnf.api}/endpoints",
        params={"included": "connection", "max": 1000},
    )

    response = send_with_session(cnf, request)
    return response.json()


def do_mfa_api(cnf, endpoint, user, token):
    """Synchorizes the MFA key of the specified endpoint.

    Arguments:
        cnf (Config): Config object.
        endpoint (str): Endpoint ID.
        user (str): User ID.
        token (str): Session token.

    Returns:
        Response: Response json.
    """
    url = f"{cnf.api}/endpoints/{endpoint}/psk-synchronize"
    authn = f"X-Custos user=^{user}, session=^{token}"

    response = requests.post(url, headers={"authorization": authn}, timeout=API_TIMEOUT)
    response.raise_for_status()
    return response.json()


def login_api_with_password(cnf, user, password, secondary_code=None):
    """Authenticates with specified username and password.

    Arguments:
        cnf (Config): Config object.
        user (str): User ID.
        password (str): Password.
        secondary_code (str): Optional secondary verification code.

    Returns:
        str: Session token.
    """
    raise_unless_has_cnf(cnf)

    url = f"{cnf.api}/sessions"
    password = encode_base64_web(password.encode("utf-8"))
    if secondary_code:
        code = encode_base64_web(secondary_code.encode("utf-8"))
        authn = f"X-Custos user=^{user}, password={password}, secondary_code={code}"
    else:
        authn = f"X-Custos user=^{user}, password={password}"

    response = requests.post(url, headers={"authorization": authn}, timeout=API_TIMEOUT)
    response.raise_for_status()
    return response.json()["data"][0]["attributes"]["token"]
