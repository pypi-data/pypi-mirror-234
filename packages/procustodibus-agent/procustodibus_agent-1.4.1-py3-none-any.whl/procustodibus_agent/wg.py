# -*- coding: utf-8 -*-
"""WireGuard utilities."""

from base64 import b64decode, b64encode
from hashlib import sha256
from subprocess import PIPE, run  # noqa: S404


def run_wg_set(cnf, args):
    """Runs `wg set` command.

    Arguments:
        cnf (Config): Config object.
        args: Command arguments.
    """
    run([cnf.wg, "set", *args])  # noqa: S603 S607


def run_wg_show(cnf):
    """Runs `wg show` command.

    Arguments:
        cnf (Config): Config object.

    Returns:
        str: Output of `wg show` command.
    """
    result = run([cnf.wg, "show", "all", "dump"], stdout=PIPE)  # noqa: S603 S607
    return result.stdout.decode("utf-8")


def parse_wg_show(s):
    """Parses `wg show` command output into a dict.

    Raises:
        ValueError: Output can't be parsed.

    Arguments:
        s (str): Output of `wg show` command.

    Returns:
        dict: Output of `wg show` command as a dict.
    """
    result = {}

    for line in s.splitlines():
        fields = line.split()
        len_fields = len(fields)

        if len_fields == 0:
            pass
        elif len_fields == 5:
            _add_interface(result, fields)
        elif len_fields == 9:
            _add_peer(result, fields)
        else:
            raise ValueError("can't parse line from wg show", line)

    return result


def filter_wg_show(data, cnf):
    """Removes configured elements from parsed output of `wg show`.

    Arguments:
        data (dict): Dict parsed from `wg show` command.
        cnf (Config): Config object.

    Returns:
        dict: Same dict with some items removed.
    """
    for interface in cnf.unmanaged_interfaces:
        data.pop(interface, None)
    if cnf.redact_secrets:
        data = remove_secrets_from_wg_show(data)
    return data


def remove_secrets_from_wg_show(data):
    """Removes secrets from parsed output of `wg show`.

    Arguments:
        data (dict): Dict parsed from `wg show` command.

    Returns:
        dict: Same dict with secret items removed.
    """
    for interface in data.values():
        del interface["private_key"]
        for peer in interface["peers"].values():
            del peer["preshared_key"]
    return data


def _add_interface(result, fields):
    """Adds the the specified interface fields to the result.

    Arguments:
        result (dict): Result dict.
        fields (list): List of field values.
    """
    interface, private, public, port, fwmark = fields
    result[interface] = {
        "private_key": private if private != "(none)" else "",
        "public_key": public if public != "(none)" else "",
        "listen_port": int(port),
        "fwmark": int(fwmark, 0) if fwmark != "off" else 0,
        "peers": {},
    }


def _add_peer(result, fields):
    """Adds the the specified peer fields to the result.

    Arguments:
        result (dict): Result dict.
        fields (list): List of field values.
    """
    interface, public, preshared, endpoint, ips, handshake, rx, tx, keepalive = fields
    result[interface]["peers"][public] = {
        "preshared_key": preshared if preshared != "(none)" else "",
        "preshared_key_hash": _hash_preshared_key(preshared),
        "endpoint": endpoint if endpoint != "(none)" else "",
        "allowed_ips": ips.split(",") if ips != "(none)" else [],
        "latest_handshake": int(handshake),
        "transfer_rx": int(rx),
        "transfer_tx": int(tx),
        "persistent_keepalive": int(keepalive) if keepalive != "off" else 0,
    }


def _hash_preshared_key(key):
    """Hashes the specified key.

    Arguments:
        key (str): Base64-encoded key to hash.

    Returns:
        str: Hash of raw key bytes as base64 string.
    """
    if not key or key == "(none)":
        return ""
    return b64encode(sha256(b64decode(key.encode())).digest()).decode()
