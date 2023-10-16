# -*- coding: utf-8 -*-
"""Executor utilities."""

from logging import getLogger
from pathlib import Path
from re import match, search
from subprocess import PIPE, STDOUT, CompletedProcess, run  # noqa: S404
from tempfile import NamedTemporaryFile

from procustodibus_agent.resolve_hostname import split_endpoint_address_and_port
from procustodibus_agent.wg_cnf import (
    delete_wg_cnf,
    find_wg_cnf_path,
    rename_wg_cnf,
    update_wg_cnf,
)


def execute_desired(cnf, interfaces, data):
    """Executes desired changes from API.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.

    Returns:
        list: Executed changes.
    """
    data = normalize_data(data)
    if not data:
        return []

    shut_down_interfaces(cnf, interfaces, data)
    delete_interfaces(cnf, interfaces, data)
    delete_endpoints(cnf, interfaces, data)
    update_interfaces(cnf, interfaces, data)
    update_routings(cnf, interfaces, data)
    update_endpoints(cnf, interfaces, data)
    create_interfaces(cnf, interfaces, data)
    create_routings(cnf, interfaces, data)
    create_endpoints(cnf, interfaces, data)
    rename_interfaces(cnf, interfaces, data)
    start_up_interfaces(cnf, interfaces, data)
    update_down_scripts(cnf, interfaces, data)

    return aggregate_executed_results(data)


def normalize_data(data):
    """Removes invalid desired change objects.

    And ensures they contain a fow core properties:
        type (str): Change type (eg 'desired_routings').
        id (str): Change ID (eg 'ABC123').
        attributes (dict): Properties to change.
        key (str): Log key to identify change (eg 'desired_interfaces ABC123').
        interface (str): Name of wg interface (eg 'wg0').
        results (list): List of change results (to append to).

    Arguments:
        data (list): List of desired change objects.

    Returns:
        list: Normalized list of desired change objects.
    """
    normalized = []

    for x in data:
        if (
            x.get("type")
            and x.get("id")
            and x.get("attributes")
            and (x["attributes"].get("name") or x["attributes"].get("interface"))
        ):
            x["key"] = f"{x['type']} {x['id']}"
            x["interface"] = x["attributes"].get("interface") or x["attributes"].get(
                "name"
            )
            x["results"] = []
            normalized.append(x)

    return normalized


def aggregate_executed_results(data):
    """Extracts result output from processed list of desired change objects.

    Arguments:
        data (list): Processed list of desired change objects.

    Returns:
        list: Flattened list of executed result output.
    """
    return [x for x in [executed_result(x) for x in data] if x]


def executed_result(change):
    """Extracts result output from a processed desired change object.

    Arguments:
        change (dict): Processed desired change object.

    Returns:
        list: Executed result output.
    """
    results = change["results"]
    output = []

    if next((x for x in results if x.returncode), None):
        output.append(f"fail {change['key']}")
    elif results:
        output.append(f"success {change['key']}")

    for x in results:
        if x.stdout:
            output.append(x.stdout)

    return "\n".join(output)


def shut_down_interfaces(cnf, interfaces, data):
    """Shuts down interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_shut_down_interface(interfaces, x):
            shut_down_interface(cnf, interfaces, x)


def delete_interfaces(cnf, interfaces, data):
    """Deletes existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_delete_interface(interfaces, x):
            delete_interface(cnf, interfaces, x)


def delete_endpoints(cnf, interfaces, data):
    """Deletes existing peers for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_delete_endpoint(interfaces, x):
            delete_endpoint(cnf, interfaces, x)


def update_interfaces(cnf, interfaces, data):
    """Updates existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_update_interface(interfaces, x):
            update_interface(cnf, interfaces, x)


def update_routings(cnf, interfaces, data):
    """Updates the routing info of existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_update_routing(interfaces, x):
            update_routing(cnf, interfaces, x)


def update_endpoints(cnf, interfaces, data):
    """Updates existing peers for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_update_endpoint(interfaces, x):
            update_endpoint(cnf, interfaces, x)


def create_interfaces(cnf, interfaces, data):
    """Creates new interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_create_interface(interfaces, x):
            create_interface(cnf, interfaces, x)


def create_routings(cnf, interfaces, data):
    """Creates the routing info for new interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_create_routing(interfaces, x):
            create_routing(cnf, interfaces, x)


def create_endpoints(cnf, interfaces, data):
    """Creates new peers for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_create_endpoint(interfaces, x):
            create_endpoint(cnf, interfaces, x)


def rename_interfaces(cnf, interfaces, data):
    """Renames existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_rename_interface(interfaces, x):
            rename_interface(cnf, interfaces, x)


# simpler for now to keep this logic together rather than subdivide it more functions
def start_up_interfaces(cnf, interfaces, data):  # noqa: CCR001
    """Starts up new or existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    desired_interfaces = {
        x["interface"]: x for x in data if x["type"] == "desired_interfaces"
    }

    to_start = {}
    for x in data:
        if _is_start_up_interface(interfaces, x):
            changes = to_start.get(x["interface"])
            if changes:
                changes.append(x)
            else:
                to_start[x["interface"]] = [x]

    for name, changes in to_start.items():
        desired = desired_interfaces.get(name)
        desired_up = desired and desired["attributes"].get("up")
        desired_down = desired and desired["attributes"].get("up") is False
        if not desired_down and (desired_up or interfaces.get(name)):
            start_up_interface(cnf, interfaces, name, changes)


def update_down_scripts(cnf, interfaces, data):
    """Updates the down scripts of existing interfaces for desired change objects.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        data (list): List of desired change objects.
    """
    for x in data:
        if _is_update_down_script(interfaces, x):
            update_down_script(cnf, interfaces, x)


def shut_down_interface(cnf, interfaces, change):
    """Shuts down an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    results = change["results"]
    name = change["interface"]
    # remove to signal to other steps that the interface is down
    interface = interfaces.pop(name, {})
    manager = interface.get("manager") or cnf.manager

    # start back up at end if renaming and was previously up
    if (
        interface
        and change["attributes"].get("rename")
        and change["attributes"].get("up") is not False
    ):
        change["attributes"]["up"] = True

    if manager == "systemd":
        results.append(_cmd("systemctl", "stop", f"wg-quick@{name}.service"))
        results.append(_cmd("systemctl", "disable", f"wg-quick@{name}.service"))
    else:
        results.append(_cmd(cnf.wg_quick, "down", name))


def delete_interface(cnf, interfaces, change):
    """Deletes an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    results = change["results"]
    name = change["interface"]
    description = f"rm {find_wg_cnf_path(cnf, name)}"
    results.append(_as_cmd(description, lambda: delete_wg_cnf(cnf, name)))


def delete_endpoint(cnf, interfaces, change):
    """Deletes an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)
    pk = change["attributes"].get("public_key")
    peer = interface["peers"].get(pk) if interface else None

    if peer:
        results.append(_cmd(cnf.wg, "set", name, "peer", pk, "remove"))
        _delete_endpoint_routes(interface, peer, change)

    if find_wg_cnf_path(cnf, name).exists():
        results.append(_update_wg_cnf_as_cmd(cnf, name, {}, [change["attributes"]]))
    else:
        results.append(CompletedProcess([], 0))


# simpler to keep this logic together rather than subdivide it more functions
def _delete_endpoint_routes(interface, peer, change):  # noqa: CCR001
    """Deletes an existing peer from a desired change object.

    Arguments:
        interface (dict): Interface info parsed from wg etc.
        peer (dict): Peer info parsed from wg etc.
        change (dict): Desired change object.
    """
    table = interface.get("table") or "auto"
    if table == "off":
        return

    allowed_ips = peer.get("allowed_ips") or []
    default_route = _uses_default_route(allowed_ips)

    if table != "auto" or not default_route:
        name = change["interface"]
        results = change["results"]
        for x in allowed_ips:
            _update_route("del", x, name, table, results)
    else:
        change["restart"] = True


def update_interface(cnf, interfaces, change):
    """Updates an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    to_set = {k: change["attributes"].get(k) for k in ["id", "description"]}
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)

    _update_interface_private_key(cnf, interface, change, name, to_set, results)

    port = change["attributes"].get("listen_port") or change["attributes"].get("port")
    if port is not None and port != interface.get("listen_port"):
        to_set["port"] = port
        results.append(_cmd(cnf.wg, "set", name, "listen-port", str(port)))

    fwmark = change["attributes"].get("fwmark")
    if fwmark is not None and fwmark != interface.get("fwmark"):
        to_set["fwmark"] = fwmark
        change["restart"] = True

    results.append(_update_wg_cnf_as_cmd(cnf, name, to_set))


def _update_interface_private_key(cnf, interface, change, name, to_set, results):
    """Updates the private key of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    pk = change["attributes"].get("private_key")
    if pk is not None and pk != interface.get("private_key"):
        to_set["private_key"] = pk
        if pk:
            with NamedTemporaryFile(mode="w", buffering=1) as f:
                f.write(pk)
                f.write("\n")
                results.append(_cmd(cnf.wg, "set", name, "private-key", f.name))
        else:
            results.append(_cmd(cnf.wg, "set", name, "private-key", "/dev/null"))


def update_routing(cnf, interfaces, change):
    """Updates the routing info for an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    to_set = {}
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)

    _update_routing_address(cnf, interface, change, name, to_set, results)
    _update_routing_dns(cnf, interface, change, name, to_set, results)
    _update_routing_mtu(cnf, interface, change, name, to_set, results)
    _update_routing_table(cnf, interface, change, name, to_set, results)
    _update_routing_scripts(cnf, interface, change, name, to_set, results)

    results.append(_update_wg_cnf_as_cmd(cnf, name, to_set))


# simpler to keep this logic together rather than subdivide it more functions
def _update_routing_address(  # noqa: CCR001
    cnf, interface, change, name, to_set, results
):
    """Updates the address list of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    new_addresses = change["attributes"].get("address")
    old_addresses = interface.get("address") or []
    if new_addresses is not None:
        for x in old_addresses:
            if x not in new_addresses:
                to_set["address"] = new_addresses
                family = calculate_ip_family(x)
                results.append(
                    _cmd("ip", f"-{family}", "address", "del", x, "dev", name)
                )
        for x in new_addresses:
            if x not in old_addresses:
                to_set["address"] = new_addresses
                family = calculate_ip_family(x)
                results.append(
                    _cmd("ip", f"-{family}", "address", "add", x, "dev", name)
                )


def _update_routing_dns(cnf, interface, change, name, to_set, results):
    """Updates the DNS list of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    dns = change["attributes"].get("dns")
    search = change["attributes"].get("search")
    if dns is None or search is None or (dns + search) == interface.get("dns"):
        return

    to_set["dns"] = dns
    to_set["search"] = search

    resolvconf_name = f"{resolvconf_interface_prefix()}{name}"
    results.append(_cmd("resolvconf", "-d", resolvconf_name, "-f"))
    resolvconf_input = []

    if dns:
        resolvconf_input.append(f"nameserver {','.join(dns)}\n")
    if search:
        resolvconf_input.append(f"search {','.join(search)}\n")
    if resolvconf_input:
        results.append(
            _cmd(
                "resolvconf",
                "-a",
                resolvconf_name,
                "-m",
                "0",
                "-x",
                stdin="".join(resolvconf_input),
            )
        )


def _update_routing_mtu(cnf, interface, change, name, to_set, results):
    """Updates the MTU of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    mtu = change["attributes"].get("mtu")
    if mtu is not None and mtu != interface.get("mtu"):
        to_set["mtu"] = mtu
        if mtu == 0:
            change["restart"] = True
        else:
            results.append(
                _cmd("ip", "link", "set", "mtu", str(mtu), "up", "dev", name)
            )


def _update_routing_table(cnf, interface, change, name, to_set, results):
    """Updates the routing table of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    table = change["attributes"].get("table")
    if table is not None and table != interface.get("table"):
        to_set["table"] = table
        # update_endpoint() needs to know the table to add routes to
        interface["new_table"] = table or "auto"
        change["restart"] = True


def _update_routing_scripts(cnf, interface, change, name, to_set, results):
    """Updates the scripts of an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interface (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        to_set (dict): Dict of interface properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    for key in ["pre_up", "post_up", "save_config"]:
        value = change["attributes"].get(key)
        if value is not None and value != interface.get(key):
            to_set[key] = value
            if key != "save_config":
                change["restart"] = True


# TODO: refactor into smaller functions
def update_endpoint(cnf, interfaces, change):  # noqa: CCR001
    """Updates an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    to_set = {k: change["attributes"].get(k) for k in ["id", "name", "public_key"]}
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)
    pk = change["attributes"].get("public_key")
    peer = interface["peers"].get(pk) or {}

    old_table = interface.get("table") or "auto"
    new_table = interface.get("new_table") or old_table
    not_auto_table = old_table != "auto" and new_table != "auto"

    new_allowed_ips = change["attributes"].get("allowed_ips")
    old_allowed_ips = peer.get("allowed_ips") or []
    default_route = _uses_default_route(old_allowed_ips) or _uses_default_route(
        new_allowed_ips
    )
    allowed_ips_different = new_allowed_ips is not None and set(
        old_allowed_ips
    ).symmetric_difference(new_allowed_ips)

    if not_auto_table or not default_route or not allowed_ips_different:
        _update_endpoint_preshared_key(cnf, peer, change, name, pk, to_set, results)
        if allowed_ips_different:
            _update_endpoint_allowed_ips(
                cnf,
                old_allowed_ips,
                new_allowed_ips,
                name,
                pk,
                old_table,
                new_table,
                to_set,
                results,
            )
        _update_endpoint_address(cnf, peer, change, name, pk, to_set, results)

        keepalive = change["attributes"].get("keepalive")
        if keepalive is not None and keepalive != peer.get("persistent_keepalive"):
            to_set["keepalive"] = keepalive
            _wg_set_peer(cnf, name, pk, "persistent-keepalive", str(keepalive), results)

    else:
        to_set = change["attributes"]
        change["restart"] = True

    results.append(_update_wg_cnf_as_cmd(cnf, name, {}, [to_set]))


def _uses_default_route(ips):
    """True if the specified AllowedIPs list should override the default route.

    Arguments:
        ips (list): AllowedIPs list (eg ['0.0.0.0/0, ::/0']).

    Returns:
        boolean: True if should override the default route.
    """
    if ips:
        for ip in ips:
            if "/0" in ip:
                return True
    return False


# simpler to keep this logic together rather than subdivide it more functions
def _update_endpoint_preshared_key(  # noqa: CFQ002
    cnf, peer, change, name, pk, to_set, results
):
    """Updates the preshared key of an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        peer (dict): Peer info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        pk (str): Peer public key (eg 'ABC...123=').
        to_set (dict): Dict of peer properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    shared = change["attributes"].get("preshared_key")
    if shared is not None and shared != peer.get("preshared_key"):
        if shared and shared != "off":
            to_set["preshared_key"] = shared
            with NamedTemporaryFile(mode="w", buffering=1) as f:
                f.write(shared)
                f.write("\n")
                _wg_set_peer(cnf, name, pk, "preshared-key", f.name, results)
        else:
            to_set["preshared_key"] = ""
            _wg_set_peer(cnf, name, pk, "preshared-key", "/dev/null", results)


# simpler to keep this logic together rather than subdivide it more functions
def _update_endpoint_allowed_ips(  # noqa: CCR001, CFQ002
    cnf,
    old_allowed_ips,
    new_allowed_ips,
    name,
    pk,
    old_table,
    new_table,
    to_set,
    results,
):
    """Updates the allowed IPs list an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        old_allowed_ips (list): Old list of AllowedIPs.
        new_allowed_ips (list): New list of AllowedIPs.
        name (str): Interface name (eg 'wg0').
        pk (str): Peer public key (eg 'ABC...123=').
        old_table (str): Old route table name (eg 'auto').
        new_table (str): New route table name (eg 'off').
        to_set (dict): Dict of peer properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    to_set["allowed_ips"] = new_allowed_ips
    _wg_set_peer(cnf, name, pk, "allowed-ips", ",".join(new_allowed_ips), results)

    if old_table != "off":
        for x in old_allowed_ips:
            if x not in new_allowed_ips:
                _update_route("del", x, name, old_table, results)

    if new_table != "off":
        for x in new_allowed_ips:
            if x not in old_allowed_ips:
                _update_route("add", x, name, new_table, results)


def _update_route(action, to, dev, table, results):
    """Adds or removes the specified route.

    Arguments:
        action (str): "add" or "del".
        to (str): IP address or CIDR (eg '10.0.0.0/24').
        dev (str): Interface name (eg 'wg0').
        table (str): Route table name (eg 'auto').
        results (list): List of completed proccess objects (to add to).
    """
    family = calculate_ip_family(to)

    args = ["ip", f"-{family}", "route", action, to, "dev", dev]
    if table != "auto":
        args += ["table", table]

    results.append(_cmd(*args))


# simpler to keep this logic together rather than subdivide it more functions
def _update_endpoint_address(  # noqa: CCR001, CFQ002
    cnf, peer, change, name, pk, to_set, results
):
    """Updates the endpoint address an existing peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        peer (dict): Peer info parsed from wg etc.
        change (dict): Desired change object.
        name (str): Interface name (eg 'wg0').
        pk (str): Peer public key (eg 'ABC...123=').
        to_set (dict): Dict of peer properties to set (to add to).
        results (list): List of completed proccess objects (to add to).
    """
    endpoint = change["attributes"].get("endpoint")
    if endpoint is None:
        return

    old_endpoint = peer.get("endpoint") or ""
    old_hostname = peer.get("hostname") or ""
    if old_hostname:
        old_ip, old_port = split_endpoint_address_and_port(old_endpoint)
        old_endpoint = (
            f"{old_hostname}:{old_port}" if old_port != 51820 else old_hostname
        )

    if endpoint != old_endpoint:
        to_set["endpoint"] = endpoint
        if endpoint:
            _wg_set_peer(cnf, name, pk, "endpoint", endpoint, results)


def _wg_set_peer(cnf, name, pk, setting, value, results):
    """Sets the specified wg setting for the specified peer.

    Arguments:
        cnf (Config): Config object.
        name (str): Interface name (eg 'wg0').
        pk (str): Peer public key.
        setting (str): Setting name (eg 'allowed-ips').
        value (str): Setting value (eg '10.0.0.1/24,fc00:0:0:1::/64').
        results (list): List to append the results of the command to.
    """
    results.append(_cmd(cnf.wg, "set", name, "peer", pk, setting, value))


def create_interface(cnf, interfaces, change):
    """Sets up a new interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    change["restart"] = True
    results = change["results"]
    name = change["interface"]
    to_set = change["attributes"]
    results.append(_update_wg_cnf_as_cmd(cnf, name, to_set))


def create_routing(cnf, interfaces, change):
    """Sets up the routing info for a new interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    create_interface(cnf, interfaces, change)


def create_endpoint(cnf, interfaces, change):
    """Sets up a new peer from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    change["restart"] = True
    results = change["results"]
    name = change["interface"]
    to_set = change["attributes"]
    results.append(_update_wg_cnf_as_cmd(cnf, name, {}, [to_set]))


def rename_interface(cnf, interfaces, change):
    """Renames an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    results = change["results"]
    old_name = change["interface"]
    old_path = find_wg_cnf_path(cnf, old_name)
    new_name = change["attributes"].get("rename")

    if not new_name or new_name == old_name:
        update_interface(cnf, interfaces, change)
    elif old_path.exists():
        change["interface"] = new_name
        change["restart"] = True
        results.append(
            _as_cmd(
                f"mv {old_path} {find_wg_cnf_path(cnf, new_name)}",
                lambda: rename_wg_cnf(cnf, old_name, new_name),
            )
        )
    else:
        change["interface"] = new_name
        create_interface(cnf, interfaces, change)


def start_up_interface(cnf, interfaces, name, changes):
    """Starts up a new or existing interface for a list of desired changes.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        name (str): Interface name to start up (eg `wg0`).
        changes (list): List of desired change objects.
    """
    results = []
    interface = interfaces.get(name) or {}
    manager = interface.get("manager") or cnf.manager

    if manager == "systemd":
        # stop first, and ignore shutdown output/errors
        _cmd("systemctl", "stop", f"wg-quick@{name}.service")
        results.append(_cmd("systemctl", "start", f"wg-quick@{name}.service"))
        results.append(_cmd("systemctl", "enable", f"wg-quick@{name}.service"))
    else:
        # stop first, and ignore shutdown output/errors
        _cmd(cnf.wg_quick, "down", name)
        results.append(_cmd(cnf.wg_quick, "up", name))

    for x in changes:
        x["results"].extend(results)


def update_down_script(cnf, interfaces, change):
    """Updates the routing info for an existing interface from a desired change object.

    Arguments:
        cnf (Config): Config object.
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.
    """
    to_set = {}
    results = change["results"]
    name = change["interface"]
    interface = interfaces.get(name)

    for key in ["pre_down", "post_down"]:
        value = change["attributes"].get(key)
        if value is not None and value != interface.get(key):
            to_set[key] = value

    results.append(_update_wg_cnf_as_cmd(cnf, name, to_set))


def _cmd(*args, stdin=None):
    """Executes a command with the specified arguments.

    Arguments:
        *args (list): Command arguments.
        stdin (str): Optional command input.

    Returns:
        Completed process object.
    """
    try:
        if stdin:
            completed = run(  # noqa: S603 S607
                args,
                input=stdin,
                stdout=PIPE,
                stderr=STDOUT,
                timeout=30,
                universal_newlines=True,
            )
        else:
            completed = run(  # noqa: S603 S607
                args, stdout=PIPE, stderr=STDOUT, timeout=30, universal_newlines=True
            )
    except Exception as e:
        completed = CompletedProcess([], 1, stdout=str(e))

    output = " ".join(args)
    if completed.stdout:
        output = f"{output}\n{completed.stdout}"

    if completed.returncode:
        getLogger(__name__).warning("err # %s", output)
    else:
        getLogger(__name__).info("ok  # %s", output)

    return completed


def _as_cmd(description, function):
    """Runs the specified function and returns a CompletedProcess object as the result.

    Arguments:
        description (str): Command description (eg 'update config file').
        function (lambda): Zero-argument function to run.

    Returns:
        Completed process object.
    """
    try:
        function()
        getLogger(__name__).info("ok  # %s", description)
        return CompletedProcess([], 0)
    except Exception as e:
        getLogger(__name__).warning("err # %s", description, exc_info=True)
        return CompletedProcess([], 1, stdout=str(e))


def _update_wg_cnf_as_cmd(cnf, name, interface, peers=None):
    """Updates the cnf file for the specified interface with the specified properties.

    Arguments:
        cnf (Config): Config object.
        name (str): Name of interface to update (eg 'wg0').
        interface (dict): Properties of interface to update.
        peers (list): List of dicts with peer properties to update.

    Returns:
        Completed process object.
    """
    description = f"procustodibus_agent setconf {name} {find_wg_cnf_path(cnf, name)}"
    return _as_cmd(description, lambda: update_wg_cnf(cnf, name, interface, peers))


def _is_shut_down_interface(interfaces, change):
    """Checks if the specified change object should shut down an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should shut down an interface.
    """
    return (
        change["type"] == "desired_interfaces"
        and interfaces.get(change["interface"])
        and (
            change["attributes"].get("up") is False
            or change["attributes"].get("delete")
            or change["attributes"].get("rename")
        )
    )


def _is_delete_interface(interfaces, change):
    """Checks if the specified change object should delete an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should delete an interface
    """
    return change["type"] == "desired_interfaces" and change["attributes"].get("delete")


def _is_delete_endpoint(interfaces, change):
    """Checks if the specified change object should delete a peer.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should delete a peer.
    """
    return change["type"] == "desired_endpoints" and change["attributes"].get("delete")


def _is_update_interface(interfaces, change):
    """Checks if the specified change object should update an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should update an interface.
    """
    return (
        change["type"] == "desired_interfaces"
        and not change["attributes"].get("delete")
        and interfaces.get(change["interface"])
    )


def _is_update_routing(interfaces, change):
    """Checks if the specified change object should update the routing for an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should update the routing.
    """
    return change["type"] == "desired_routings" and interfaces.get(change["interface"])


def _is_update_endpoint(interfaces, change):
    """Checks if the specified change object should update a peer.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should update a peer.
    """
    return (
        change["type"] == "desired_endpoints"
        and not change["attributes"].get("delete")
        and interfaces.get(change["interface"])
    )


def _is_create_interface(interfaces, change):
    """Checks if the specified change object should create an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should create an interface.
    """
    return (
        change["type"] == "desired_interfaces"
        and not change["attributes"].get("delete")
        and not change["attributes"].get("rename")
        and not interfaces.get(change["interface"])
    )


def _is_create_routing(interfaces, change):
    """Checks if the specified change object should create the routing for an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should create the routing.
    """
    return change["type"] == "desired_routings" and not interfaces.get(
        change["interface"]
    )


def _is_create_endpoint(interfaces, change):
    """Checks if the specified change object should create a peer.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should create a peer.
    """
    return (
        change["type"] == "desired_endpoints"
        and not change["attributes"].get("delete")
        and not interfaces.get(change["interface"])
    )


def _is_rename_interface(interfaces, change):
    """Checks if the specified change object should rename an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should rename an interface.
    """
    return (
        change["type"] == "desired_interfaces"
        and not change["attributes"].get("delete")
        and change["attributes"].get("rename")
    )


def _is_start_up_interface(interfaces, change):
    """Checks if the specified change object should start up an interface.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should start up an interface.
    """
    return (
        change.get("restart")
        or change["attributes"].get("restart")
        or (
            change["type"] == "desired_interfaces"
            and change["attributes"].get("up")
            and not change["attributes"].get("delete")
            and not interfaces.get(change["interface"])
        )
    )


def _is_update_down_script(interfaces, change):
    """Checks if the specified change object should update the down scripts.

    Arguments:
        interfaces (dict): Interface info parsed from wg etc.
        change (dict): Desired change object.

    Returns:
        boolean: True if should update the down scripts.
    """
    return change["type"] == "desired_routings" and interfaces.get(change["interface"])


def calculate_ip_family(address):
    """Determines whether the specified IP address is IPv4 or IPv6.

    Arguments:
        address (str): IP address (eg 'fc00:0:0:1::').

    Returns:
        int: 4 or 6.
    """
    return 6 if search(r":.*:", address) else 4


def resolvconf_interface_prefix(file="/etc/resolvconf/interface-order"):
    """Returns the prefix to append to an interface name for resolvconf commands.

    Arguments:
        file (str): Resolvconf interface-order file path to check.

    Returns:
        str: Prefix (eg 'tun') or blank ('').
    """
    path = Path(file)
    if path.exists():
        with open(path) as f:
            for line in f:
                interface_match = match(r"([A-Za-z0-9-]+)\*", line)
                if interface_match:
                    return interface_match[1]
    return ""
