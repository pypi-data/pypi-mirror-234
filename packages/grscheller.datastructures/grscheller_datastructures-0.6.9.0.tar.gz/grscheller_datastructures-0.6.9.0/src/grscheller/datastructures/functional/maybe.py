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

"""grscheller.datastructures.maybe module

   Module implementing the Option Monad. Sometimes called Maybe or Optional.
"""
from __future__ import annotations
from typing import Any, Callable

__all__ = ['Maybe', 'Some', 'Nothing']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class Maybe():
    """Class representing a potentially missing value.

    - Implements the Option Monad
    - Maybe(value) constructs "Some(value)" 
    - Both Maybe() or Maybe(None) constructs a "Nothing"
    - immutable semantics - map & flatMap return modified copies
    - None is always treated as a non-existance value
      - cannot be stored in an object of type Maybe
      - semantically None does not exist
      - None only has any real existance as an implementration detail
    """
    def __init__(self, value: Any=None):
        self._value = value

    def __bool__(self) -> bool:
        """Return false if a Nothing, otherwise true."""
        return self._value != None

    def __len__(self) -> int:
        """A Maybe either contains something or not.
        Return 1 if a Some, 0 if a Nothing.
        """
        if self:
            return 1
        return 0

    def __iter__(self):
        """Yields its value if not a Nothing"""
        if self:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'Some(' + repr(self._value) + ')'
        else:
            return 'Nothing'

    def __eq__(self, other: Maybe) -> bool:
        """Returns true if both sides are Nothings, or if both sides are Somes
        contining values which compare as equal.
        """
        if not isinstance(other, type(self)):
            return False
        return self._value == other._value

    def map(self, f: Callable[[Any], Any]) -> Maybe:
        if self:
            return Maybe(f(self._value))
        else:
            return Maybe()

    def flatMap(self, f: Callable[[Any], Maybe]) -> Maybe:
        if self:
            return f(self._value)
        else:
            return Maybe()

    def get(self) -> Any | None:
        """Get contents if they exist, otherwise return None. Caller is
        responsible with dealing with a None return value.
        """
        return self._value

    def getOrElse(self, default: Any) -> Any:
        """Get contents if they exist, otherwise return provided default value,
        which is guarnteed never to be None. If the caller sets it to None,
        swap it for the empty tuple (). () was choosen since it is iterable and
        "does the right thing" in an iterable context. If caller really wants
        None returned, they can use the get() method instead.
        """
        if default is None:
            default = ()
        if self:
            return self._value
        else:
            return default

# Maybe convenience functions/objects. Like "unit", "Nil", "()" in FP-languages.
# These are not necessary to ues Maybe, but gives Maybe the flavor of a Union
# type without using either inheritance or unnecessary internal state.

def Some(value=None):
    """Function for creating a Maybe from a value. If value is None or missing,
    returns a Nothing.
    """
    return Maybe(value)

Nothing = Some()  # Nothing is not a singleton, test via equality not identity.

if __name__ == "__main__":
    pass
