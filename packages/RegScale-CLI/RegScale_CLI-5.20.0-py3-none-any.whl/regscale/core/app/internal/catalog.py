#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrates catalog export, diagnose and compare into RegScale"""

# standard python imports
import click

from regscale.core.app.utils.catalog_utils.compare_catalog import (
    display_menu as start_compare,
)
from regscale.core.app.utils.catalog_utils.diagnostic_catalog import (
    display_menu as start_diagnostic,
)
from regscale.core.app.utils.catalog_utils.download_catalog import (
    display_menu as start_download,
)
from regscale.core.app.utils.catalog_utils.update_catalog import (
    display_menu as start_update,
)


@click.group()
def catalog():
    """Export, diagnose, and compare catalog from RegScale.com/regulations."""


@catalog.command(name="download")
def export():
    """Export catalog from RegScale.com/regulations."""
    start_download()


@catalog.command(name="diagnose")
def diagnostic():
    """Diagnose catalog and output metadata."""
    start_diagnostic()


@catalog.command(name="compare")
def compare():
    """Run diagnostic and compare catalogs while reporting differences."""
    start_compare()


@catalog.command(name="update")
def update():
    """[BETA] Update application instance catalog with new catalog data"""
    start_update()
