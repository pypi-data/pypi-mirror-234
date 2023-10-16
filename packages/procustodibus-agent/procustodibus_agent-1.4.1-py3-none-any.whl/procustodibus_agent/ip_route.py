# -*- coding: utf-8 -*-
"""Routing and addressing utilities."""

from ipaddress import IPv4Address, IPv4Interface
from json import loads
from platform import system
from re import fullmatch, sub
from subprocess import PIPE, run  # noqa: S404


def run_ip_address_show(device):
    """Runs `ip address show` command for specified device.

    Arguments:
        device (str): Device name (eg 'wg0').

    Returns:
        dict: Parsed JSON from `ip --json address show` command.
    """
    args = ["ip", "--json", "address", "show", "dev", device]
    result = run(args, stdout=PIPE)  # noqa: S603 S607
    output = result.stdout.decode("utf-8")
    return loads(output)[0] if fullmatch(r"\[\{.*\}\]\s*", output) else {}


def run_ifconfig(device):
    """Runs `ifconfig` command for specified device.

    Arguments:
        device (str): Device name (eg 'wg0').

    Returns:
        list: Lines from `ifconfig` command.
    """
    args = ["ifconfig", device]
    result = run(args, stdout=PIPE)  # noqa: S603 S607
    output = result.stdout.decode("utf-8")
    return [x.strip() for x in output.split("\n")]


def annotate_wg_show_with_ip_address_show(interfaces):
    """Annotates parsed output of `wg show` with output of `ip address show`.

    Arguments:
        interfaces (dict): Dict parsed from `wg show` command.

    Returns:
        dict: Same dict with additional properties.
    """
    for name, properties in interfaces.items():
        _annotate_interface(name, properties)
    return interfaces


def _annotate_interface(name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    if system() == "Linux":
        _annotate_interface_with_ip_address_show(name, properties)
    else:
        _annotate_interface_with_ifconfig(name, properties)
    return properties


def _annotate_interface_with_ip_address_show(name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    info = run_ip_address_show(name)
    if info:
        properties["address"] = [_format_address_info(a) for a in info["addr_info"]]
    return properties


def _format_address_info(info):
    """Formats the addr_info object from `ip address show` as a CIDR.

    Arguments:
        info (dict): addr_info object.

    Returns:
        string: CIDR.
    """
    return "{}/{}".format(info["local"], info["prefixlen"])


def _annotate_interface_with_ifconfig(name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    addresses = list(filter(None, [_parse_inet_address(x) for x in run_ifconfig(name)]))
    if addresses:
        properties["address"] = addresses
    return properties


def _parse_inet_address(line):
    """Parses the inet or inet6 address out of the specified ifconfig output line.

    Arguments:
        line (str): ifconfig output line (eg 'inet6 ffc0:: prefixlen 64').

    Returns:
        str: CIDR or empty string (eg 'ffc0::/64').
    """
    if not line.startswith("inet"):
        return ""

    parts = line.split()
    if len(parts) < 4:
        return ""
    elif parts[2] == "-->" and len(parts) >= 6:
        del parts[2:4]

    return _format_inet_address_parts(parts)


def _format_inet_address_parts(parts):
    """Formats the specified ifconfig output tokens as a CIDR.

    Arguments:
        parts (list): ifconfig output tokens
            (eg ['inet6', 'ffc0::', 'prefixlen', '64']).

    Returns:
        str: CIDR or empty string (eg 'ffc0::/64').
    """
    if parts[1] == "addr:":
        return _strip_interface_id(parts[2])
    elif parts[1].startswith("addr:"):
        ip = parts[1][5:]
        mask = parts[3][5:] if parts[3].startswith("Mask:") else 32
        return str(IPv4Interface((ip, mask)))
    elif parts[2] == "prefixlen":
        ip = _strip_interface_id(parts[1])
        mask = parts[3]
        return f"{ip}/{mask}"
    elif parts[2] == "netmask":
        ip = _strip_interface_id(parts[1])
        mask = str(IPv4Address(int(parts[3], 16)))
        return str(IPv4Interface((ip, mask)))
    return ""


def _strip_interface_id(ip):
    """Strips the interface number or name from the specified IP address.

    Arguments:
        ip (str): IP address (eg 'fe80::169d:99ff:fe7f:8c67%utun0').

    Returns:
        str: IP address (eg 'fe80::169d:99ff:fe7f:8c67').
    """
    return sub(r"%[^/]*", "", ip)
