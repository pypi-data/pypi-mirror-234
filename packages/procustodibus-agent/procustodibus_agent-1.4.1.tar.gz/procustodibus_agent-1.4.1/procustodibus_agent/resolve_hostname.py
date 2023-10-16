# -*- coding: utf-8 -*-
"""Utilities for updating endpoints with resolved hostnames."""

from contextlib import suppress
from logging import getLogger
from re import fullmatch
from socket import AF_INET, AF_INET6, IPPROTO_UDP, SOCK_DGRAM, gaierror, getaddrinfo

from procustodibus_agent.wg import run_wg_set


def apply_endpoint_hostnames(cnf, interfaces):
    """Updates the endpoints of the specified peers if configured with a hostname.

    Arguments:
        cnf (Cnf): Config object.
        interfaces (dict): Interfaces data.
    """
    resolve = cnf.resolve_hostnames
    if resolve == "once":
        return

    for name, interface in interfaces.items():
        for pubkey, peer in interface.get("peers", {}).items():
            hostname = peer.get("hostname")
            endpoint = peer.get("endpoint")
            apply_endpoint_hostname(cnf, name, pubkey, hostname, resolve, endpoint)


def apply_endpoint_hostname(cnf, name, pubkey, hostname, family, endpoint):
    """Updates the specified peer's endpoint using the specified hostname.

    Arguments:
        cnf (Cnf): Config object.
        name (str): Interface name (eg 'wg0').
        pubkey (str): Peer public key.
        hostname (str): Hostname to use (eg 'foo.example.com').
        family (str): Preferred address family ('ipv4' or 'ipv6' or 'auto').
        endpoint (str): Existing endpoint (eg '10.10.10.10:51820').
    """
    if not name or not pubkey or not hostname or not endpoint:
        return

    family = get_address_family(family)
    address, port = split_endpoint_address_and_port(endpoint)
    addresses = lookup_addresses(hostname, family, port)

    if not addresses:
        message = "hostname resolution failed: {}".format(hostname)
        getLogger(__name__).warning(message)
    elif address not in addresses:
        set_endpoint_address(cnf, name, pubkey, addresses[0], port)


def set_endpoint_address(cnf, name, pubkey, address, port):
    """Runs the `wg set` command to set the endpoint of the specified peer.

    Arguments:
        cnf (Cnf): Config object.
        name (str): Interface name (eg 'wg0').
        pubkey (str): Peer public key.
        address (str): Endpoint IP address (eg '10.10.10.10').
        port (int): Endpoint port (eg 51820).
    """
    if address.find(":") >= 0:
        endpoint = "[{}]:{}".format(address, port)
    else:
        endpoint = "{}:{}".format(address, port)

    run_wg_set(cnf, [name, "peer", pubkey, "endpoint", endpoint])


def get_address_family(family):
    """Returns address family number for IP address type.

    Arguments:
        family: Address family number (AF_INET or AF_INET6)
            or string ('ipv4' or 'ipv6').

    Returns:
        Address family number.
    """
    if family == "ipv4":
        return AF_INET
    if family == "ipv6":
        return AF_INET6
    elif isinstance(family, str):
        return 0
    return family or 0


def split_endpoint_address_and_port(endpoint):
    """Splits the specified endpoint into IP address and port.

    Arguments:
        endpoint (str): IP address and port (eg '[fc00:0:0:1::]:51820').

    Returns:
        Tuple of string IP address and integer port number.
    """
    if not endpoint:
        return "", 51820

    ipv6 = fullmatch(r"\[([^\]]+)\]:(\d+)", endpoint)
    if ipv6:
        return ipv6[1], int(ipv6[2])

    ipv4 = endpoint.split(":")
    if len(ipv4) == 2:
        with suppress(ValueError):
            return ipv4[0], int(ipv4[1])

    return ipv4[0], 51820


def lookup_addresses(hostname, family=0, port=None):
    """Looks up the DNS entries for the specified hostname.

    Arguments:
        hostname (str): Hostname to lookup (eg 'foo.example.com').
        family (int): Address family (AF_NET or AF_NET6), defaults to 0 (any).
        port (int): Port number, defaults to None (any).

    Returns:
        list: List of string IP addresses.
    """
    try:
        info = getaddrinfo(hostname, port, family, SOCK_DGRAM, IPPROTO_UDP)
        return [x[4][0] for x in info]
    except gaierror:
        return []
