# -*- coding: utf-8 -*-
"""Config utilities."""

import logging
import logging.config
import os
import sys
from os import environ
from pathlib import Path
from re import IGNORECASE, compile, fullmatch, match, split, sub

from inflection import underscore

from procustodibus_agent import DEFAULT_API_URL

DEFAULT_WG_CNF_DIRS = [
    "/opt/homebrew/etc/wireguard",
    "/usr/local/etc/wireguard",
    "/etc/wireguard",
]
DEFAULT_CNF_DIRS = [
    ".",
    "/usr/local/etc/procustodibus",
    "/etc/procustodibus",
] + DEFAULT_WG_CNF_DIRS
DEFAULT_LOGGING_FORMAT = "%(asctime)s %(name)s %(levelname)s: %(message)s"
DEFAULT_LOGGING_LEVEL = "WARNING"

PROCUSTODIBUS_SPLITTABLE = {
    "unmanaged_interfaces": ",",
}
WIREGUARD_SPLITTABLE = {
    "address": ",",
    "allowed_ips": ",",
    "dns": ",",
    "post_down": ";",
    "post_up": ";",
    "pre_down": ";",
    "pre_up": ";",
}


# simpler to keep logic in same function even if it makes cognitive-complexity high
def init_log(root_level="", cnf=None):  # noqa: CCR001
    """Initializes python logging.

    Arguments:
        root_level (str): Root logging level. Defaults to 'WARNING'.
        cnf (str): Path to Python logging configuration file.
    """
    if not root_level:
        root_level = environ.get("PROCUSTODIBUS_LOGGING_LEVEL")

    if cnf and os.path.exists(cnf):
        logging.config.fileConfig(cnf)
        if root_level:
            logging.getLogger().setLevel(root_level.upper())
        logging.getLogger(__name__).debug("init logging configuration from %s", cnf)

    else:
        _setup_default_logging(
            environ.get("PROCUSTODIBUS_LOGGING_FORMAT") or DEFAULT_LOGGING_FORMAT,
            root_level.upper() if root_level else DEFAULT_LOGGING_LEVEL,
        )
        if root_level:
            logging.getLogger(__name__).debug("init logging at %s", root_level)


def _setup_default_logging(log_format, log_level):
    """Sets up logging if no logging config file specified.

    Arguments:
        log_format (str): Log format.
        log_level (str): Log level.
    """
    logging.basicConfig(format=log_format, level=log_level, stream=sys.stdout)


def find_default_cnf():
    """Finds the path to an existing config file.

    Returns:
        str: Path to an existing config file, or blank.
    """
    path = environ.get("PROCUSTODIBUS_CONF")
    if path:
        return path

    for directory in DEFAULT_CNF_DIRS:
        path = f"{directory}/procustodibus.conf"
        if os.path.exists(path):
            return path

    return ""


def load_cnf(cnf_file):
    """Loads the specified procustodibus config file.

    Normalizes keys and values.

    Arguments:
        cnf_file (str): Path to config file, or blank.

    Returns:
        dict: Loaded config settings (dict of strings to normalized values).
    """
    return ini_to_dict(load_ini(cnf_file, PROCUSTODIBUS_SPLITTABLE))


def load_ini(ini_file, splittable=None):
    """Loads the specified ini config file.

    Converts section and key names to snake_case; splits and trims values.

    Arguments:
        ini_file (str): Path to config file, or blank.
        splittable (dict): Optional dict of key names whose values to split.

    Returns:
        dict: Loaded ini settings (dict of strings to list of dicts).
    """
    result = {}
    if not ini_file:
        return result

    section = {}
    _add_ini_value(result, "preface", section)
    if not splittable:
        splittable = {}

    with open(ini_file) as f:
        for line in f:
            line = sub("#.*", "", line).strip()
            section_match = fullmatch(r"\s*\[([^\]]+)\]\s*", line)
            if section_match:
                section_name = underscore(section_match[1])
                section = {}
                _add_ini_value(result, section_name, section)
            elif line:
                _add_ini_line(section, line, splittable)

    return result


def _add_ini_line(section, line, splittable):
    """Parses the specified key=value line and adds it to the specified dict.

    Trims key and value, and converts key to snake_case.

    Splits value by splitter char if key found in splittable dict.

    Arguments:
        section (dict): Dict to add parsed line to.
        line (str): Line to parse (eg 'DNS = 10.0.0.1, wg').
        splittable (dict): Dict of snake_case keys to splitter characters.
    """
    parts = line.split("=", maxsplit=1)
    if len(parts) < 2:
        parts.append("true")

    # snake_case keys
    # with special-case for IP to convert AllowedIPs to allowed_ips
    key = underscore(sub("IP", "Ip", parts[0].strip()))
    splitter = splittable.get(key)
    if splitter:
        value = [x.strip() for x in parts[1].split(splitter)]
    else:
        value = parts[1].strip()

    _add_ini_value(section, key, value)


def _add_ini_value(container, key, value):
    """Adds specified ini value to list of values in specified dict.

    Arguments:
        container (dict): Dict to add value to.
        key (str): Key under which to add value.
        value: Value to add (string or list of strings).
    """
    existing = container.setdefault(key, [])
    if isinstance(value, list):
        existing.extend(value)
    else:
        existing.append(value)


# simpler to keep logic in same function
# even if it makes cognitive-complexity high
def load_ini_lines(ini_file):  # noqa: CCR001
    """Loads the specified ini config file as a list of lines in a list of sections.

    Includes comments, whitespace, and section headers as-is in lines. The first
    section (index 0) may be a "preface" section, before the first named section.

    Arguments:
        ini_file (str): Path to config file, or blank.

    Returns:
        list: List of list of lines.
    """
    result = []
    if not ini_file:
        return result

    section = []

    with open(ini_file) as f:
        for line in f:
            section_match = match(r"\s*\[([^\]]+)\]", line)
            if section_match:
                if section:
                    result.append(section)
                section = []
            section.append(line.rstrip("\n"))

    if section:
        result.append(section)
    return result


def save_ini_lines(ini_file, sections, chmod=None):
    """Saves the specified ini config file from a list of lines in a list of sections.

    Arguments:
        ini_file (str): Path to config file.
        sections (list): List of list of lines.
        chmod (int): Optional octal mode value to set on file.
    """
    with open(ini_file, "w") as f:
        for lines in sections:
            for line in lines:
                # print to file
                print(line, file=f)  # noqa: T201

    if chmod:
        ini_file.chmod(chmod)


def find_ini_section_with_line(sections, line):
    """Finds the specified section of lines containing the specified line start.

    Arguments:
        sections (list): List of list of lines.
        line (str): Line start to find.

    Returns:
        list: List of lines or None.
    """
    for section in sections:
        for x in section:
            if x.startswith(line):
                return section
    return None


# splitting up this function would make the logic harder to follow
# even if it makes cognitive-complexity high
def replace_ini_line_value(lines, key, value):  # noqa: CCR001
    """Replaces the specified key in the specified list with the specified value.

    Replaces all lines with the matched key; or if the key is not found, appends
    to the list. If the value is itself a list, adds a separate line for each value.

    If the value is None or an empty list ([]), simply removes all lines with
    the matched key.

    Arguments:
        lines (list): List of lines.
        key (str): Key to match (eg 'AllowedIPs').
        value: Value to replace (eg ['0.0.0.0/0', '::/0']).
    """
    re = compile(rf"\s*{key.lower()}\s*=", IGNORECASE)
    empty = value is None or value == []
    found = False

    i = 0
    while i < len(lines):
        if match(re, lines[i]):
            if found or empty:
                del lines[i]
                i -= 1
            else:
                found = True
                if isinstance(value, list):
                    lines[i] = f"{key} = {value[0]}"
                    for v in value[1:]:
                        i += 1
                        lines.insert(i, f"{key} = {v}")
                else:
                    lines[i] = f"{key} = {value}"
        i += 1

    if not found and not empty:
        append_ini_line_value(lines, key, value)


def append_ini_line_value(lines, key, value):
    """Appends the specified key=value pair to the specified list.

    If the value is itself a list, adds a separate line for each value.

    Arguments:
        lines (list): List of lines.
        key (str): Key to append (eg 'AllowedIPs').
        value: Value to append (eg ['0.0.0.0/0', '::/0']).
    """
    i = len(lines)
    while i > 0 and fullmatch(r"#.*|\s*", lines[i - 1]):
        i -= 1

    if isinstance(value, list):
        for v in value:
            lines.insert(i, f"{key} = {v}")
            i += 1
    else:
        lines.insert(i, f"{key} = {value}")


def ini_to_dict(ini):
    """Normalizes property values in the specified dict.

    Drops empty sections, selects first value of non-known-list properties,
    coerces known boolean and number properties.

    Arguments:
        ini (dict): Dict to convert.

    Returns:
        dict: Loaded config settings (dict of strings to normalized values).
    """
    root = {}

    for section_name, section in ini.items():
        src = section[0]
        if src:
            segments = section_name.split(".")
            dst = _create_dict_by_path(root, segments)
            _normalize_cnf_section(src, dst)

    return root


def _normalize_cnf_section(src, dst):
    """Normalizes the property values of the specified config section.

    Copies normalized values from src dict to dst dict.

    Arguments:
        src (dict): Source config section.
        dst (dict): Destination config section.
    """
    for key, value in src.items():
        value = _normalize_cnf_property(key, value)

        segments = key.split(".")
        if len(segments) > 1:
            item_dst = _create_dict_by_path(dst, segments[:-1])
            item_dst[segments[-1]] = value
        else:
            dst[key] = value


def _create_dict_by_path(root, segments):
    """Creates a hierarchy of dictionaries according to the specified path.

    Arguments:
        root (dict): Root under which to create dictionaries.
        segments (list): List of path segments (eg ['foo', 'bar', 'baz']).

    Returns:
        dict: Leaf dictionary.
    """
    for segment in segments:
        root = root.setdefault(segment, {})
    return root


def apply_cnf(obj, cnf):
    """Applies the specified config settings to the specified object.

    Arguments:
        obj: Object to apply settings to.
        cnf (dict): Config settings to apply.
    """
    for key, value in cnf.items():
        if key == "procustodibus":
            apply_cnf(obj, value)
        else:
            setattr(obj, key, value)


# keep all special-casing of values together in same function
# even if it makes cognitive-complexity high
def _normalize_cnf_property(key, value):  # noqa: CCR001
    """Adjusts the specified config property value if necessary.

    Arguments:
        key (str): Property name.
        value: Property value.

    Returns:
        Normalized property value.
    """
    # coerce list property values
    if key in ["unmanaged_interfaces"]:
        if isinstance(value, str):
            return [x for x in split(" *, *", value) if x]
        return value

    # default to blank string, extract first list value if list
    if not value:
        value = ""
    elif isinstance(value, list):
        value = value[0] or ""

    # coerce boolean property values
    if key in ["read_only", "redact_secrets"]:
        if isinstance(value, str):
            return True if match("[1TYty]", value) else False

    # coerce integer property values
    if key in ["loop"]:
        if isinstance(value, str):
            return int(value)

    return value


class Cnf(dict):
    """Configuration object."""

    # simpler to keep logic in same function even if it makes cognitive-complexity high
    def __init__(self, cnf_file="", verbosity=None, loop=0):  # noqa: CCR001
        """Creates new configuration object.

        Arguments:
            cnf_file (str): Path to configuration file. Defaults to no file.
            verbosity: Root log level. Defaults to 'WARNING'.
                If the number 1 is specified, sets log level to 'INFO'.
                If the number 2 is specified, sets log level to 'DEBUG'.
            loop (int): Seconds to sleep before looping. Defaults to 0 (no loop).
        """
        self.api = DEFAULT_API_URL
        self.wg = "wg"
        self.wg_quick = "wg-quick"
        self.wg_cnf_dir = find_default_wg_cnf_dir()
        self.agent = ""
        self.host = ""
        self.credentials = ""
        self.setup = ""
        self.logging = ""
        self.loop = int(loop or 0)
        self.manager = ""
        self.read_only = False
        self.redact_secrets = False
        self.resolve_hostnames = "auto"
        self.unmanaged_interfaces = []

        if not cnf_file:
            cnf_file = find_default_cnf()
        self.cnf_file = cnf_file
        apply_cnf(self, load_cnf(cnf_file))

        if verbosity == 1:
            verbosity = "INFO"
        if verbosity == 2:
            verbosity = "DEBUG"
        if not self.logging:
            self.logging = _locate_extra_cnf_file(cnf_file, "logging")
        init_log(verbosity, self.logging)

        if not self.credentials:
            self.credentials = _locate_extra_cnf_file(cnf_file, "credentials")
        if not self.setup:
            self.setup = _locate_extra_cnf_file(cnf_file, "setup")
        if not self.manager:
            self.manager = _default_manager()


def _locate_extra_cnf_file(cnf_file, extra_type):
    """Builds path to extra conf file (like the credentials file).

    Arguments:
        cnf_file (str): Path to standard cnf file (eg '/etc/wireguard/agent.conf').
        extra_type (str): Extra type (eg 'credentials').

    Returns:
        str: Path to cnf file (eg '/etc/wireguard/agent-credentials.conf').
    """
    if not cnf_file:
        return ""

    p = Path(cnf_file)
    return f"{p.parent}/{p.stem}-{extra_type}{p.suffix}"


def _default_manager():
    """Determines name of default interface manager.

    Returns:
        str: Manager name (eg 'systemd').
    """
    for x in ["/lib", "/usr/lib"]:
        if os.path.exists(f"{x}/systemd/system/wg-quick@.service"):
            return "systemd"
    return ""


def find_default_wg_cnf_dir():
    """Finds the default /etc/wireguard directory or equivalent.

    Returns:
        str: Path to an existing directory, or blank.
    """
    for directory in DEFAULT_WG_CNF_DIRS:
        if os.path.exists(directory):
            return directory
    return ""
