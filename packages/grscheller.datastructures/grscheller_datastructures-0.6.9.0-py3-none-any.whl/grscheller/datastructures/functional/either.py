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

   Module implementing the Either Monad.
"""
from __future__ import annotations
from typing import Any, Callable

__all__ = ['Either', 'Left', 'Right']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

class Either():
    """Class that either contains a Left value or Right value, but not both.

    This version is biased to the Left, which is intended as the "happy path."
    """
    def __init__(self, left: Any, right: Any=None):
        if left == None:
            self._isLeft = False
            self._value = right
        else:
            self._isLeft = True
            self._value = left

    def __bool__(self) -> bool:
        """Return true if a Left, false if a Right"""
        return self._isLeft

    def __len__(self) -> int:
        """An Either always contains just one thing, even if it is None"""
        return 1

    def __iter__(self):
        """Yields its value if a Left"""
        if self:
            yield self._value

    def __repr__(self) -> str:
        if self:
            return 'Left(' + repr(self._value) + ')'
        else:
            return 'Right(' + repr(self._value) + ')'

    def __eq__(self, other: Either) -> bool:
        """True if both sides are same "type" and values compare as equal"""
        if not isinstance(other, type(self)):
            return False

        if (self and other) or (not self and not other):
            return self._value == other._value
        return False

    def copy(self) -> Either:
        if self:
            return Either(self._value)
        return Either(None, self._value)

    def map(self, f: Callable[[Any], Any], right='') -> Either:
        if self:
            return Either(f(self._value), right)
        return self.copy()

    def mapRight(self, g: Callable[[Any], Any]) -> Either:
        if self:
            return self.copy()
        return Either(None, g(self._value))

    def flatMap(self, f: Callable[[Any], Either]) -> Either:
        if self:
            return f(self._value)
        return self.copy()

    def get(self) -> Any | None:
        if self:
            return self._value
        return None

# Either convenience functions. First two act like subtype constructors.

def Left(left: Any, right: Any=None) -> Either:
    """Function returns Left Either if left != None, otherwise Right Either"""
    return Either(left, right)

def Right(right: Any) -> Either:
    """Function to construct a Right Either"""
    return Either(None, right)

if __name__ == "__main__":
    pass
