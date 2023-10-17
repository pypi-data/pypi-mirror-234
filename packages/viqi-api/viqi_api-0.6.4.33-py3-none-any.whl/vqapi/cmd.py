#!/usr/bin/env python
import argparse
import logging
import os
import posixpath

# import sys
# import time
from configparser import RawConfigParser

import urllib3

from .comm import BQSession

# Check the directories in order for the config, the 1st one is the default for writing new config
CONFIG_PATHS = [
    "~/config/viqi/profiles" if os.name == "nt" else "~/.config/viqi/profiles",
    "~/viqi/config" if os.name == "nt" else "~/.viqi/config",
    "~/bisque/config" if os.name == "nt" else "~/.bisque/config",
]


def bisque_argument_parser(*args, **kw):
    parser = argparse.ArgumentParser(*args, **kw)
    parser.add_argument("-c", "--config", help="bisque config", default=None)
    parser.add_argument("--profile", help="Profile to use in bisque config", default="default")
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="report actions w/o changes",
        default=False,
    )
    parser.add_argument("-d", "--debug", nargs="?", help="set debug level: debug,info,warn,error")
    parser.add_argument("--debug-file", help="output filename for debug messages", default=None)
    parser.add_argument("-q", "--quiet", action="store_true", help="print actions ", default=False)
    parser.add_argument("-a", "--credentials", help="A bisque login.. admin ", default=None)
    parser.add_argument("--host", help="Default bisque server to connect to ")
    parser.add_argument("--user", help="User to  connect with ")
    parser.add_argument("--password", help="passwor to  connect with ")
    parser.add_argument("--alias", help="Use admin credentials to login as alias")
    # Local arguments
    return parser


def bisque_config(parser=None, args=None, write_config=True):
    """Manage bisque config file"""
    # user = password = root = config = alias_user = None
    if parser is None:
        parser = bisque_argument_parser()
    pargs = parser.parse_args(args=args)
    config = RawConfigParser()
    if pargs.config is None:
        # Find config file
        for confd in CONFIG_PATHS:
            confd = os.path.expanduser(confd)
            if os.path.exists(confd):
                pargs.config = confd
                break

    if not (pargs.host and pargs.user and pargs.password) and os.path.exists(os.path.expanduser(pargs.config)):
        config.read(os.path.expanduser(pargs.config))
        try:
            profile = config[pargs.profile]
            pargs.host = profile.get("host")
            pargs.user = profile.get("user")
            pargs.password = profile.get("password")
            pargs.alias = profile.get("alias", None)
        except KeyError:
            print(f"No or incomplete profile named {pargs.profile}")

    # if pargs.host:
    #    root = pargs.host
    if pargs.credentials and not (pargs.user or pargs.password):
        pargs.user, pargs.password = pargs.credentials.split(":")
    if not (pargs.host and pargs.user and pargs.password):
        print(f"Please configure how to connect to bisque with profile {pargs.profile}")
        if write_config:
            if pargs.config is None:
                pargs.config = CONFIG_PATHS[0]
            pargs.host = input(f"BisQue URL [{pargs.host}] ") or pargs.host
            pargs.user = input(f"username[{pargs.user}] ") or pargs.user
            pargs.password = input(f"password[{pargs.password}]: ") or pargs.password
            config_file = os.path.expanduser(pargs.config)
            if not os.path.isdir(os.path.dirname(config_file)):
                os.makedirs(os.path.dirname(config_file))
            with open(config_file, "w") as conf:
                config[pargs.profile] = {
                    "host": posixpath.join(pargs.host.strip(), ""),
                    "user": pargs.user.strip(),
                    "password": pargs.password.strip(),
                }
            config.write(conf)
            print("configuration has been saved to", pargs.config)

    return pargs


def bisque_session(parser=None, args=None, root_logger=None):
    """Get a bisque session for command line tools using arguments and ~/.bisque/config files
    Args:
     parser : a configured ArgumentParser
     args   : List of strings

    Returns:
      session, args  : tuple with session and args

    Usage:
    parser = bisque_argument_parser ("MyCommand")
    parser.add_argument ('newarg', help='any specific argument')
    args = parser.parse_args()
    session, pargs = bisque_session(args)

    ~/.bisque/config:
    [default]
    host=
    user=
    password=

    [testing]
    host=
    user=
    password=
    alias=
    """
    from argparse import Namespace

    if not isinstance(args, Namespace):
        pargs = bisque_config(parser=parser, args=args)
    else:
        pargs = args

    if pargs.debug:
        logging.captureWarnings(True)
        if root_logger is None:
            if pargs.debug_file is not None:
                logging.basicConfig(filename=pargs.debug_file, filemode="w")
            else:
                logging.basicConfig(level=logging.WARN)
            root_logger = logging.getLogger("vqapi")
        root_logger.setLevel(
            {
                "debug": logging.DEBUG,
                "info": logging.INFO,
                "warn": logging.WARN,
                "error": logging.ERROR,
            }.get(pargs.debug.lower(), logging.DEBUG)
        )

    if pargs.host and pargs.user and pargs.password:
        session = BQSession()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session.c.verify = False
        print(f"connecting {pargs.host} with {pargs.user} and {pargs.password}")
        session = session.init_local(
            bisque_root=pargs.host,
            user=pargs.user,
            pwd=pargs.password,
            create_mex=False,
            as_user=pargs.alias,
        )
        if session is None:
            print(f"Could not create bisque session with host={pargs.host} user={pargs.user}. Check your config")
            return session
        if not pargs.quiet:
            print("Session for  ", pargs.host, " for user ", session.user, " created")
        session.parse_args = pargs
        session.server_version = "viqi1"
    return session
