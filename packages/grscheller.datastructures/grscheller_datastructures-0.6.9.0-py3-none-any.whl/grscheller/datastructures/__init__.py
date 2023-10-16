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

"""grscheller.datastructures package

   Data structures supporting a functional sytle of programming which

   1. don't throw uncaught exceptions - when used syntactically properly
   2. avoid mutation and mutable shared state
   3. push mutation to innermost scopes
   4. employ annotations, see PEP-649
       - needs annotations module from __future__ package
       - useful for LSP external tooling, allows types to drive development
   5. have semantics which consistently use None for "non-existent" values
   6. semantic versioning
       - first digit signifies an event or epoch
       - second digit means breaking API changes (between PyPI releases)
       - third digit either means
         - API breaking changes (between GitHub commits)
         - API additions (between PyPI releases)
       - fourth digit either means
         - bugfixes or minor changes (between PyPI releases)
         - GitHub only thrashing and experimentation
"""

__version__ = "0.6.9.0"
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .functional.maybe import *
from .functional.either import *
from .functional.util import *
from .circle import *
from .dqueue import *
from .stack import *
from .iterlib import *
