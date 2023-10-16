# -*- coding: utf-8 -*-
"""Utilities for manipulating wq conf ini."""

from contextlib import suppress
from pathlib import Path
from re import match, sub

from inflection import underscore

from procustodibus_agent import APP_URL
from procustodibus_agent import __version__ as version
from procustodibus_agent.api import format_datetime
from procustodibus_agent.cnf import (
    WIREGUARD_SPLITTABLE,
    find_ini_section_with_line,
    load_ini,
    load_ini_lines,
    replace_ini_line_value,
    save_ini_lines,
)


def annotate_wg_show_with_wg_cnf(cnf, interfaces):
    """Annotates parsed output of `wg show` with wg config.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Dict parsed from `wg show` command.

    Returns:
        dict: Same dict with additional properties.
    """
    for name, properties in interfaces.items():
        _annotate_interface(cnf, name, properties)
    return interfaces


def find_wg_cnf_path(cnf, name):
    """Returns path to ini file for specified wg interface.

    Arguments:
        cnf (Config): Config object.
        name (str): Interface name (eg 'wg0').

    Returns:
        Path: Path to ini file (eg '/etc/wireguard/wg0.conf').
    """
    directory = cnf.wg_cnf_dir or "/etc/wireguard"
    return Path(directory, f"{name}.conf")


def _annotate_interface(cnf, name, properties):
    """Annotates specified dict with wg config for specified interface.

    Arguments:
        cnf (Config): Config object.
        name (str): Interface name (eg 'wg0').
        properties (dict): Dict of interface properties.

    Returns:
        dict: Same dict with additional properties.
    """
    path = find_wg_cnf_path(cnf, name)
    try:
        if not path.exists():
            return properties
    except PermissionError:
        return properties

    ini = load_ini(path, WIREGUARD_SPLITTABLE)
    interface = ini.get("interface")
    if not interface:
        return properties

    _annotate_interface_properties(properties, interface[0])
    _annotate_interface_peers(properties, ini)
    return properties


# keep conversion of all interface values together in same function
# even if it makes cognitive-complexity high
def _annotate_interface_properties(properties, ini):  # noqa: CCR001
    """Annotates specified interface properties from specified wg config.

    Arguments:
        properties (dict): Dict of interface properties.
        ini (dict): Dict of interface config from wg ini.

    Returns:
        dict: Same dict with additional properties.
    """
    # string properties
    for key in ["table"]:
        values = ini.get(key)
        if values:
            properties[key] = values[0]

    # integer properties
    for key in ["mtu"]:
        values = ini.get(key)
        if values:
            with suppress(ValueError):
                properties[key] = int(values[0])

    # boolean properties
    for key in ["save_config"]:
        values = ini.get(key)
        if values:
            properties[key] = values[0] == "true"

    # list properties
    for key in ["address", "dns", "pre_up", "post_up", "pre_down", "post_down"]:
        values = ini.get(key)
        if values:
            properties[key] = values

    return properties


def _annotate_interface_peers(interface, ini):
    """Annotates specified interface peers from specified wg config.

    Arguments:
        interface (dict): Dict of interface properties.
        ini (dict): Dict of full config from wg ini.

    Returns:
        dict: Same dict with additional properties.
    """
    peers = {p["public_key"][0]: p for p in ini.get("peer", []) if p.get("public_key")}
    for name, properties in interface.get("peers", {}).items():
        peer = peers.get(name)
        if peer:
            _annotate_peer_properties(properties, peer)
    return interface


def _annotate_peer_properties(properties, ini):
    """Annotates specified peer properties from specified wg config.

    Arguments:
        properties (dict): Dict of peer properties.
        ini (dict): Dict of peer config from wg ini.

    Returns:
        dict: Same dict with additional properties.
    """
    endpoint = ini.get("endpoint")
    if endpoint and match("[A-Za-z]", endpoint[0]):
        properties["hostname"] = sub(":.*", "", endpoint[0])

    return properties


def delete_wg_cnf(cnf, name):
    """Deletes the cnf file for the specified interface with the specified name.

    Arguments:
        cnf (Config): Config object.
        name (str): Interface name (eg 'wg0').
    """
    path = find_wg_cnf_path(cnf, name)
    if path.exists():
        path.unlink()


def rename_wg_cnf(cnf, old_name, new_name):
    """Renames the cnf file for the specified interface to the specified new name.

    Arguments:
        cnf (Config): Config object.
        old_name (str): Existing name (eg 'wg0').
        new_name (str): New name (eg 'wg100').
    """
    path = find_wg_cnf_path(cnf, old_name)
    if path.exists():
        path.rename(find_wg_cnf_path(cnf, new_name))


def update_wg_cnf(cnf, name, interface, peers=None):
    """Updates the cnf file for the specified interface with the specified properties.

    Arguments:
        cnf (Config): Config object.
        name (str): Name of interface to update (eg 'wg0').
        interface (dict): Properties of interface to update.
        peers (list): List of dicts with peer properties to update.

    Raises:
        ValueError: Cnf file for the interface cannot be written.
    """
    if not interface and not peers:
        return

    chmod = None
    path = find_wg_cnf_path(cnf, name)
    if path.exists():
        sections = load_ini_lines(path)
    elif interface.get("private_key"):
        sections = [_stub_wg_cnf_interface_section(cnf, interface)]
        chmod = 0o640
    else:
        raise ValueError(f"{path} does not exist and private key not available")

    section = _find_wg_cnf_interface_section(cnf, interface, path, sections)
    _update_wg_cnf_interface_section(section, interface)
    _update_wg_cnf_routing_section(section, interface)
    _update_wg_cnf_peer_sections(cnf, sections, peers)

    save_ini_lines(path, sections, chmod)


def _find_wg_cnf_interface_section(cnf, interface, path, sections):
    """Finds the interface section within the list of sections.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Properties of interface to update.
        path (str): Path to cnf file.
        sections (list): List of list of lines.

    Returns:
        list: List of lines in interface section.

    Raises:
        ValueError: Interface section cannot be found or stubbed.
    """
    section = find_ini_section_with_line(sections, "[Interface]")
    if section:
        return section

    if interface.get("private_key"):
        section = _stub_wg_cnf_interface_section(cnf, interface)
        sections.append(section)
        return section
    else:
        raise ValueError(
            f"{path} does not contain an existing interface definition "
            "and private key not available"
        )


def _stub_wg_cnf_interface_section(cnf, interface):
    """Generates lines for the interface section of a new cnf file.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Properties of interface.

    Returns:
        list: List of lines for new cnf file.
    """
    identifier = interface.get("id")
    description = interface.get("description")
    url = f"{APP_URL}/interfaces/{identifier}" if identifier else ""

    if description and url:
        description = f"{description} ({url})"
    else:
        description = description or url

    return [
        f"# generated {format_datetime()} by procustodibus-agent {version}",
        f"# {description}",
        "[Interface]",
        f"PrivateKey = {interface['private_key']}",
    ]


def _update_wg_cnf_interface_section(lines, interface):
    """Updates the lines of the interface section of a cnf file.

    Arguments:
        lines (list): List of lines in interface section.
        interface (dict): Core properties of interface to update.
    """
    pk = interface.get("private_key")
    if pk:
        replace_ini_line_value(lines, "PrivateKey", pk)

    _update_wg_cnf_number_line(lines, interface, "ListenPort", ["listen_port", "port"])
    _update_wg_cnf_number_line(lines, interface, "FwMark", ["fw_mark", "fwmark"])


def _update_wg_cnf_routing_section(lines, interface):
    """Updates the lines of the interface section of a cnf file with routing info.

    Arguments:
        lines (list): List of lines in interface section.
        interface (dict): Routing properties of interface to update.
    """
    _update_wg_cnf_list_line(lines, interface, "Address")

    dns = interface.get("dns")
    search = interface.get("search")
    if dns is not None and search is not None:
        dns = dns + search
    elif search is not None:
        dns = search
    if dns == []:
        replace_ini_line_value(lines, "DNS", None)
    elif dns:
        replace_ini_line_value(lines, "DNS", dns)

    _update_wg_cnf_number_line(lines, interface, "MTU")
    _update_wg_cnf_text_auto_line(lines, interface, "Table")

    for key in ["PreUp", "PostUp", "PreDown", "PostDown"]:
        _update_wg_cnf_list_line(lines, interface, key)

    _update_wg_cnf_boolean_line(lines, interface, "SaveConfig")


# keep top-level logic for updating peer sections together
# even if it makes cognitive-complexity high
def _update_wg_cnf_peer_sections(cnf, sections, peers):  # noqa: CCR001
    """Updates the lines of the peer sections of a cnf file.

    Arguments:
        cnf (Config): Config object.
        sections (list): List of list of lines.
        peers (list): List of dicts with peer properties to update.
    """
    for peer in peers or []:
        pk = peer["public_key"]
        section = find_ini_section_with_line(sections, f"PublicKey = {pk}")
        if peer.get("delete"):
            if section:
                sections.remove(section)
        else:
            if not section:
                section = _stub_wg_cnf_peer_section(cnf, peer)
                sections.append(section)
            _update_wg_cnf_peer_section(section, peer)


def _stub_wg_cnf_peer_section(cnf, peer):
    """Generates lines for a new peer section of a cnf file.

    Arguments:
        cnf (Config): Config object.
        peer (dict): Properties of the peer.

    Returns:
        list: List of lines for new peer.
    """
    identifier = peer.get("id")
    name = peer.get("name")
    url = f"{APP_URL}/endpoints/{identifier}" if identifier else ""

    if name and url:
        description = f"{name} ({url})"
    else:
        description = name or url

    return [
        "",
        f"# {description}",
        "[Peer]",
        f"PublicKey = {peer['public_key']}",
    ]


def _update_wg_cnf_peer_section(lines, peer):
    """Updates the lines of a peer section in a cnf file.

    Arguments:
        lines (list): Existing list of lines in the peer section.
        peer (dict): Properties of the peer to update.
    """
    _update_wg_cnf_text_off_line(lines, peer, "PresharedKey")
    _update_wg_cnf_list_line(lines, peer, "AllowedIPs", ["allowed_ips"])
    _update_wg_cnf_text_line(lines, peer, "Endpoint")
    _update_wg_cnf_number_line(
        lines, peer, "PersistentKeepalive", ["persistent_keepalive", "keepalive"]
    )


def _update_wg_cnf_list_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, [[]], ini_key, src_keys)


def _update_wg_cnf_text_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, [""], ini_key, src_keys)


def _update_wg_cnf_text_auto_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, ["", "auto"], ini_key, src_keys)


def _update_wg_cnf_text_off_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, ["", "off"], ini_key, src_keys)


def _update_wg_cnf_number_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, [0, "0", "off"], ini_key, src_keys)


def _update_wg_cnf_boolean_line(lines, src, ini_key, src_keys=None):
    _update_wg_cnf_line(lines, src, [False, "", "false"], ini_key, src_keys)


def _update_wg_cnf_line(lines, src, empty_values, ini_key, src_keys=None):
    """Updates a line with the specified key from the specified src dict.

    Arguments:
        lines (list): Existing list of lines.
        src (dict): Source dict from which to update the value.
        empty_values (list): Values that should result in removing the line
            instead of updating it.
        ini_key (str): Key in lines to update (eg 'ListenPort').
        src_keys (list): Src keys to check (eg ['listen_port', 'port']).
    """
    if not src_keys:
        src_keys = [underscore(ini_key)]

    value = None
    for x in src_keys:
        value = src.get(x)
        if value is not None:
            break

    if value in empty_values:
        replace_ini_line_value(lines, ini_key, None)
    elif value is True:
        replace_ini_line_value(lines, ini_key, "true")
    elif value:
        replace_ini_line_value(lines, ini_key, value)
