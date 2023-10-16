#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 1/23/23
           """

from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as this_init_file:
    __doc__ += this_init_file.read()

from .analysis import *
from .clamp import *
from .lines import *
from .morphology import *
from .points import *
from .polygons import *
from .serialisation import *
from .geometry_types import *
from .projection import *
from .transformation import *
from .rings import *
