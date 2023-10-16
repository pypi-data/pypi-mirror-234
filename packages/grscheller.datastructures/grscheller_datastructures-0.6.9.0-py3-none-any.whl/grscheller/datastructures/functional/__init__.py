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

"""grscheller.datastructures.functional package

   Data structures supporting a functional style of programming in Python
   - immutable semantics - map & flatMap return modified copies
   - None is always treated as a non-existance value
     - Python None value cannot be stored in any these objects
     - semantically None does not exist
     - None only has any real existance as an implementration detail
"""

__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .maybe import *
from .either import *
from .util import *
