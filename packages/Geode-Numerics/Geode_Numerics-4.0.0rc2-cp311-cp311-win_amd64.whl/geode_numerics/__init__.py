## Copyright (c) 2019 - 2023 Geode-solutions

import os, pathlib
os.add_dll_directory(pathlib.Path(__file__).parent.resolve().joinpath('bin'))

from .surface import *
from .scalar_function import *
