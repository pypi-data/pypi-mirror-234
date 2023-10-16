# -*- coding: utf-8 -*-
"""Agent logic."""
from io import StringIO
from logging import getLogger
from time import sleep

from procustodibus_agent import __version__ as version
from procustodibus_agent.api import ping_api
from procustodibus_agent.connectivity import check_connectivity
from procustodibus_agent.executor import execute_desired
from procustodibus_agent.ip_route import annotate_wg_show_with_ip_address_show
from procustodibus_agent.resolve_hostname import apply_endpoint_hostnames
from procustodibus_agent.wg import filter_wg_show, parse_wg_show, run_wg_show
from procustodibus_agent.wg_cnf import annotate_wg_show_with_wg_cnf


def is_connection_good(cnf, message="Checking connectivity", expect_error=False):
    """Runs connectivity check and logs result.

    Arguments:
        cnf (Config): Config object.
        message (str): Message to log (defaults to 'Checking connectivity').
        expect_error (bool): True if error expected (defaults to False).

    Returns:
        bool: True if connection is good.
    """
    buffer = StringIO()
    # print to buffer
    print(message, file=buffer)  # noqa: T201

    error = check_connectivity(cnf, buffer)
    if error:
        if not expect_error:
            getLogger(__name__).error(buffer.getvalue())
        return False

    getLogger(__name__).info(buffer.getvalue())
    return True


def ping_loop(cnf):
    """Pings continuously as specified by looping configuration.

    Arguments:
        cnf (Config): Config object.
    """
    good = is_connection_good(cnf, message=f"Starting agent {version}")

    while cnf.loop:
        if good:
            try:
                ping(cnf)
            except Exception:
                getLogger(__name__).exception("ping failed")
                good = is_connection_good(cnf)
            sleep(cnf.loop)
        else:
            sleep(cnf.loop)
            good = is_connection_good(cnf, expect_error=True)


def ping(cnf):
    """Gathers wg info and pings api, executing desired changes from response.

    Arguments:
        cnf (Config): Config object.
    """
    interfaces = interrogate(cnf)
    response = ping_api(cnf, interfaces)
    executed = execute_desired(cnf, interfaces, response.get("data"))

    if executed:
        # notify api of changes
        interfaces = interrogate(cnf)
        ping_api(cnf, interfaces, executed)
    else:
        # check for endpoint dns updates
        apply_endpoint_hostnames(cnf, interfaces)


def interrogate(cnf):
    """Extracts interface dict from wg show and wg config.

    Arguments:
        cnf (Config): Config object.

    Returns:
        dict: Interface info parsed from wg etc.
    """
    interfaces = filter_wg_show(parse_wg_show(run_wg_show(cnf)), cnf)
    interfaces = annotate_wg_show_with_wg_cnf(cnf, interfaces)
    interfaces = annotate_wg_show_with_ip_address_show(interfaces)
    return interfaces
