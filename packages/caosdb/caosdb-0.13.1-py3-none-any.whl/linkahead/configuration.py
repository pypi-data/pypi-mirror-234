# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the LinkAhead Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
#

import os
import warnings

import yaml

try:
    optional_jsonschema_validate = None
    from jsonschema import validate as optional_jsonschema_validate
except ImportError:
    pass

from configparser import ConfigParser
from os import environ, getcwd
from os.path import expanduser, isfile, join


def _reset_config():
    global _pycaosdbconf
    _pycaosdbconf = ConfigParser(allow_no_value=False)


def configure(inifile):
    """read config from file.

    Return a list of files which have successfully been parsed.
    """
    global _pycaosdbconf
    if ("_pycaosdbconf" not in globals() or _pycaosdbconf is None):
        _reset_config()
    read_config = _pycaosdbconf.read(inifile)
    validate_yaml_schema(config_to_yaml(_pycaosdbconf))

    if "HTTPS_PROXY" in environ:
        _pycaosdbconf["Connection"]["https_proxy"] = environ["HTTPS_PROXY"]
    if "HTTP_PROXY" in environ:
        _pycaosdbconf["Connection"]["http_proxy"] = environ["HTTP_PROXY"]
    return read_config


def get_config():
    global _pycaosdbconf
    if ("_pycaosdbconf" not in globals() or _pycaosdbconf is None):
        _reset_config()
    return _pycaosdbconf


def config_to_yaml(config):
    valobj = {}
    for s in config.sections():
        valobj[s] = {}
        for key, value in config[s].items():
            # TODO: Can the type be inferred from the config object?
            if key in ["timeout", "debug"]:
                valobj[s][key] = int(value)
            elif key in ["ssl_insecure"]:
                valobj[s][key] = bool(value)
            else:
                valobj[s][key] = value

    return valobj


def validate_yaml_schema(valobj):
    if optional_jsonschema_validate:
        with open(os.path.join(os.path.dirname(__file__), "schema-pycaosdb-ini.yml")) as f:
            schema = yaml.load(f, Loader=yaml.SafeLoader)
        optional_jsonschema_validate(instance=valobj, schema=schema["schema-pycaosdb-ini"])
    else:
        warnings.warn("""
            Warning: The validation could not be performed because `jsonschema` is not installed.
        """)


def _read_config_files():
    """Read config files from different paths.

    Read the config from either ``$PYCAOSDBINI`` or home directory (``~/.pylinkahead.ini``), and
    additionally adds config from a config file in the current working directory
    (``pylinkahead.ini``).
    If deprecated names are used (starting with 'pycaosdb'), those used in addition but the files
    with the new naming scheme take precedence.
    All of these files are optional.

    Returns
    -------

    ini files: list
      The successfully parsed ini-files. Order: environment variable or home directory, then cwd.
      Used for testing the function.

    """
    return_var = []
    ini_user = expanduser('~/.pylinkahead.ini')
    ini_cwd = join(getcwd(), "pylinkahead.ini")
    # LinkAhead rename block ##################################################
    ini_user_caosdb = expanduser('~/.pycaosdb.ini')
    ini_cwd_caosdb = join(getcwd(), "pycaosdb.ini")
    if os.path.exists(ini_user_caosdb):
        warnings.warn("\n\nYou have a config file with the old naming scheme (pycaosdb.ini). "
                      f"Please use the new version and rename\n"
                      f"    {ini_user_caosdb}\nto\n    {ini_user}", DeprecationWarning)
    if os.path.exists(ini_cwd_caosdb):
        warnings.warn("\n\nYou have a config file with the old naming scheme (pycaosdb.ini). "
                      f"Please use the new version and rename\n"
                      f"    {ini_cwd_caosdb}\nto\n    {ini_cwd}", DeprecationWarning)
    # End: LinkAhead rename block ##################################################

    if "PYCAOSDBINI" in environ:
        if not isfile(expanduser(environ["PYCAOSDBINI"])):
            raise RuntimeError(
                f"No configuration file found at\n{expanduser(environ['PYCAOSDBINI'])}"
                "\nwhich was given via the environment variable PYCAOSDBINI"
            )
        return_var.extend(configure(expanduser(environ["PYCAOSDBINI"])))
    else:
        if isfile(ini_user_caosdb):
            return_var.extend(configure(ini_user_caosdb))
        if isfile(ini_user):
            return_var.extend(configure(ini_user))
    if isfile(ini_cwd):
        return_var.extend(configure(ini_cwd))
    if isfile(ini_cwd_caosdb):
        return_var.extend(configure(ini_cwd_caosdb))
    return return_var
