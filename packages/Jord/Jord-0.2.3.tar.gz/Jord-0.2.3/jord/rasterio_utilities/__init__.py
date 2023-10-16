#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 1/27/23
           """

__all__ = []

from pathlib import Path

try:
    ...
except ImportError as ix:
    this_package_name = Path(__file__).parent.name
    print(f"Make sure rasterio module is available for {this_package_name}")
    raise ix
