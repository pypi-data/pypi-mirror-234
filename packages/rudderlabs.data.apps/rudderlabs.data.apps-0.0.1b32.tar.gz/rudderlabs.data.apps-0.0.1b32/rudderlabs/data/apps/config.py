#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Reads and treats configuration files"""

import os


def read_ini(config_file: str):
    """Reads and resolves configuration files, returns a dictionary with read values

    Args:
        config_file: The path to the config file.
    """

    import configparser

    data = configparser.ConfigParser()
    cfg = os.path.expanduser(config_file)
    if os.path.exists(cfg):
        data.read(cfg)
    return data


def read_yaml(config_file: str):
    """Reads and resolves configuration files, returns a dictionary with read values

    Args:
        config_file: The path to the config file.
    """
    import yaml

    cfg = os.path.expanduser(config_file)
    with open(cfg, "r") as stream:
        data = yaml.safe_load(stream)
    return data
