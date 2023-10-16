# -*- coding: utf-8 -*-
"""Connectivity test."""
import os
import sys
from re import search
from socket import gethostbyname

from requests import RequestException

from procustodibus_agent import DOCS_URL
from procustodibus_agent.api import (
    get_health_info,
    get_host_info,
    raise_unless_has_cnf,
    setup_api,
)
from procustodibus_agent.wg import parse_wg_show, run_wg_show


def check_connectivity(cnf, output=None):
    """Runs all connectivity checks and outputs issues.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to (defaults to stdout).

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    if not output:
        output = sys.stdout

    try:
        raise_unless_has_cnf(cnf)
    except Exception as e:
        # print to stdout or designated file
        print(str(e), file=output)  # noqa: T201
        return 1

    exit_code = (
        check_wg(cnf, output)
        + check_dns(cnf, output)
        + check_health(cnf, output)
        + check_host(cnf, output)
    )

    if exit_code:
        # print to stdout or designated file
        print(  # noqa: T201
            "Issues encountered; "
            "see {}/guide/agents/troubleshoot/ to fix".format(DOCS_URL),
            file=output,
        )
    else:
        # print to stdout or designated file
        print("All systems go :)", file=output)  # noqa: T201

    return exit_code


def check_wg(cnf, output):
    """Checks that wireguard is available and configured with at least one interface.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    try:
        interfaces = parse_wg_show(run_wg_show(cnf))
    except OSError as e:
        _bad("no wg executable found ({})".format(e), output)
        return 2

    if interfaces:
        _good("{} wireguard interfaces found".format(len(interfaces)), output)
        return 0
    else:
        _bad("no wireguard interfaces found", output)
        return 0


def check_dns(cnf, output):
    """Checks that the local DNS resolver can resolve api.procustodib.us.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    hostname = _get_hostname(cnf.api)
    try:
        address = gethostbyname(hostname)
        _good("{} is pro custodibus ip address".format(address), output)
        return 0
    except OSError as e:
        _bad("cannot lookup ip address for {} ({})".format(hostname, e), output)
        return 4


def check_health(cnf, output):
    """Checks connectivity to and the health of the Pro Custodibus API.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    try:
        errors = [x["error"] for x in get_health_info(cnf) if not x["healthy"]]
    except RequestException as e:
        errors = ["server unavailable ({})".format(e)]

    if errors:
        for error in errors:
            _bad("unhealthy pro custodibus api: {}".format(error), output)
        return 8
    else:
        _good("healthy pro custodibus api", output)
        return 0


def check_host(cnf, output):
    """Checks that the agent can access the configured host through the API.

    Arguments:
        cnf (Config): Config object.
        output (IOBase): Output stream to write issues to.

    Returns:
        int: 0 if no issues, positive number if issues.
    """
    try:
        _setup_if_available(cnf)
    except (RequestException, ValueError) as e:
        _bad("cannot set up access to api ({})".format(e), output)
        return 16

    try:
        host = get_host_info(cnf)
        name = host["data"][0]["attributes"]["name"]
        _good("can access host record on api for {}".format(name), output)
        return 0
    except (RequestException, ValueError) as e:
        _bad("cannot access host record on api ({})".format(e), output)
        return 16


def _setup_if_available(cnf):
    """Sets up new agent credentials if setup code is available.

    Arguments:
        cnf (Config): Config object.
    """
    if type(cnf.setup) is dict or os.path.exists(cnf.setup):
        setup_api(cnf)


def _good(message, output):
    """Prints the specified "good" message to the specified output stream.

    Arguments:
        message (str): Message to print.
        output (IOBase): Output stream to write to.
    """
    # print to stdout or designated file
    print(f"... {message} ...", file=output)  # noqa: T201


def _bad(message, output):
    """Prints the specified "bad" message to the specified output stream.

    Arguments:
        message (str): Message to print.
        output (IOBase): Output stream to write to.
    """
    # print to stdout or designated file
    print(f"!!! {message} !!!", file=output)  # noqa: T201


def _get_hostname(url):
    """Extracts the hostname from the specified URL.

    Arguments:
        url (str): URL (eg 'http://test.example.com:8080').

    Returns:
        str: Hostname (eg 'test.example.com').
    """
    match = search(r"(?<=://)[^:/]+", url)
    return match.group(0) if match else None
