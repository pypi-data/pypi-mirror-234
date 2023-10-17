#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import pkg_resources

from click_plugins import with_plugins

from . import rudderlabs


@with_plugins(pkg_resources.iter_entry_points("rlabs.aws.cli"))
@click.group(cls=rudderlabs.AliasedGroup)
def aws():
    """Commands for interacting with AWS."""
    pass
