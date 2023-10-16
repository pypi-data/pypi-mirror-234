# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
"""
Avoid breaking changes to `from shrike.pipeline.module_helper import AMLModuleLoader`
"""

from .v1 import AMLModuleLoader
from .module_helper_base import *
