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

"""Module grscheller.datastructure.circle - Double sided queue

Circular array with amortized O(1) indexing, prepending & appending values, and
length determination. Implemented with a Python List.

Mainly used to implement other grscheller.datastructure classes where
functionality is more likely restricted than augmented. This class is
not opinionated regarding None as a value. It freely stores and returns None
values. Use in a boolean context to determine if empty.
"""

from __future__ import annotations

__all__ = ['Circle']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable, Self, Never, Union
from .iterlib import concatIters, mergeIters, mapIter

class Circle:
    """Circular array with amortized O(1) indexing, prepending & appending
    values, and length determination.

    Raises IndexError exceptions.
    """
    def __init__(self, *data):
        """Construct a double sided queue"""
        size = len(data)
        capacity = size + 2
        self._count = size
        self._capacity = capacity
        self._front = 0
        self._rear = (size - 1) % capacity
        self._list = list(data)
        self._list.append(None)
        self._list.append(None)

    def _double(self) -> None:
        """Double capacity of circle array"""
        if self._front > self._rear:
            frontPart = self._list[self._front:]
            rearPart = self._list[:self._rear+1]
        else:
            frontPart = self._list
            rearPart = []
        self._list = frontPart + rearPart + [None]*(self._capacity)
        self._capacity *= 2
        self._front = 0
        self._rear = self._count - 1

    def _compact(self) -> None:
        """Compact the datastructure as much as possible"""
        match self._count:
            case 0:
                self._list = [None]*2
                self._capacity = 2
                self._front = 0
                self._rear = 1
            case 1:
                self._list = [self._list[self._front], None]
                self._capacity = 2
                self._front = 0
                self._rear = 0
            case _:
                if self._front > self._rear:
                    frontPart = self._list[self._front:]
                    rearPart = self._list[:self._rear+1]
                else:
                    frontPart = self._list[self._front:self._rear+1]
                    rearPart = []
                self._list = frontPart + rearPart
                self._capacity = self._count
                self._front = 0
                self._rear = self._capacity - 1

    def _empty(self) -> Self:
        """Empty circle array, keep current capacity"""
        self._list = [None]*self._capacity
        self._front = 0
        self._rear = self._capacity - 1
        return self

    def __bool__(self):
        """Returns true if circle array is not empty"""
        return self._count > 0

    def __len__(self):
        """Returns current number of values in the circlular array"""
        return self._count

    # def __getitem__(self, index: int) -> Any | Never: # annotation module or pyright bug?
    def __getitem__(self, index: int) -> Union[Any, Never]:
        """Get value at a valid index, otherwise raise IndexError"""
        cnt = self._count
        if 0 <= index < cnt:
            return self._list[(self._front + index) % self._capacity]
        elif -cnt <= index < 0:
            return self._list[(self._front + cnt + index) % self._capacity]
        else:
            l = -cnt
            h = cnt - 1
            msg = f'Circle array index = {index} not between {l} and {h} while getting value'
            msg0 = 'Circle array trying to index an empty circle array while getting value'
            if cnt > 0:
                raise IndexError(msg)
            else:
                raise IndexError(msg0)

    def __setitem__(self, index: int, value) -> None | Never:
        """Set value at a valid index, otherwise raise IndexError"""
        cnt = self._count
        if 0 <= index < cnt:
            self._list[(self._front + index) % self._capacity] = value
        elif -cnt <= index < 0:
            self._list[(self._front + cnt + index) % self._capacity] = value
        else:
            l = -cnt
            h = cnt - 1
            msg = f'Circle array index = {index} not between {l} and {h} while setting value'
            msg0 = 'Circle array trying to index an empty circle array while setting value'
            if cnt > 0:
                raise IndexError(msg)
            else:
                raise IndexError(msg0)

    def __iter__(self):
        """Iterator yielding contents of circle array, does not consume data"""
        if self._count > 0:
            cap = self._capacity
            rear = self._rear
            pos = self._front
            while pos != rear:
                yield self._list[pos]
                pos = (pos + 1) % cap
            yield self._list[pos]

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        cnt = self._count
        left = self
        frontL = self._front
        capL = self._capacity
        right = other
        frontR = other._front
        capR = other._capacity
        nn = 0
        while nn < cnt:
            if left._list[(frontL+nn)%capL] != right._list[(frontR+nn)%capR]:
                return False
            nn += 1
        return True

    def __repr__(self):
        """Display data in the circle array"""
        dataListStrs = []
        for data in self:
            dataListStrs.append(repr(data))
        return "[[ " + " | ".join(dataListStrs) + " ]]"

    def copy(self) -> Circle:
        """Return shallow copy of the circle array in O(n) time/space complexity"""
        return Circle(*self)

    def pushR(self, data: Any) -> Self:
        """Push data on rear of circle"""
        if self._count == self._capacity:
            self._double()
        self._rear = (self._rear + 1) % self._capacity
        self._list[self._rear] = data
        self._count += 1
        return self

    def pushL(self, data: Any) -> Self:
        """Push data on front of circle"""
        if self._count == self._capacity:
            self._double()
        self._front = (self._front - 1) % self._capacity
        self._list[self._front] = data
        self._count += 1
        return self

    def popR(self) -> Any:
        """Pop data off rear of circle array, returns None if empty"""
        if self._count == 0:
            return None
        else:
            data = self._list[self._rear]
            self._list[self._rear] = None
            self._rear = (self._rear - 1) % self._capacity
            self._count -= 1
            return data

    def popL(self) -> Any:
        """Pop data off front of circle array, returns None if empty"""
        if self._count == 0:
            return None
        else:
            data = self._list[self._front]
            self._list[self._front] = None
            self._front = (self._front + 1) % self._capacity
            self._count -= 1
            return data

    def capacity(self) -> int:
        """Returns current capacity of circle array"""
        return self._capacity

    def fractionFilled(self) -> float:
        """Returns current capacity of circle array"""
        return self._count/self._capacity

    def resize(self, addCapacity = 0) -> None:
        """Compact circle array and add extra capacity"""
        self._compact()
        if addCapacity > 0:
            self._list = self._list + [None]*addCapacity
            self._capacity += addCapacity
            if self._count == 0:
                self._rear = self._capacity - 1

    def map(self, f: Callable[[Any], Any]) -> Circle:
        """Apply function over circle array contents, returns new instance"""
        return Circle(*mapIter(iter(self), f))

    def mapSelf(self, f: Callable[[Any], Any]) -> Self:
        """Apply function over circle array contents"""
        for idx in range(self._count):
            self[idx] = f(self[idx])
        return self

    def flatMap(self, f: Callable[[Any], Circle]) -> Circle:
        """Apply function and flatten result, returns new instance"""
        return Circle(
            *concatIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

    def flatMapSelf(self, f: Callable[[Any], Circle]) -> Self:
        """Apply function to contents and flatten result"""
        copy = self.flatMap(f)
        self._count = copy._count
        self._capacity = copy._capacity
        self._front = copy._front
        self._rear = copy._rear
        self._list = copy._list
        return self

    def mergeMap(self, f: Callable[[Any], Circle]) -> Circle:
        """Apply function and flatten result, returns new instance"""
        return Circle(
            *mergeIters(
                *mapIter(mapIter(iter(self), f), lambda x: iter(x))
            )
        )

    def mergeMapSelf(self, f: Callable[[Any], Circle]) -> Self:
        """Apply function and flatten result, returns new instance"""
        copy = self.mergeMap(f)
        self._count = copy._count
        self._capacity = copy._capacity
        self._front = copy._front
        self._rear = copy._rear
        self._list = copy._list
        return self

if __name__ == "__main__":
    pass
