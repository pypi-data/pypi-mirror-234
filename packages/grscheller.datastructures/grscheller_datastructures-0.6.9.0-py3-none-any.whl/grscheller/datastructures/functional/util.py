# Copyright 2023 Geoffrey R. Scheller
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility functions for use with the data structures defined in the
grscheller.datastructures.functional package.
"""

from __future__ import annotations
from typing import Any

__all__ = ['maybeToEither', 'eitherToMaybe']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .maybe import *
from .either import *

def maybeToEither(m: Maybe, right: Any=None) -> Either:
    """Convert a Maybe to an Either"""
    return Either(m.get(), right)

def eitherToMaybe(e: Either) -> Maybe:
    """Convert an Either to a Maybe"""
    return Maybe(e.get())
