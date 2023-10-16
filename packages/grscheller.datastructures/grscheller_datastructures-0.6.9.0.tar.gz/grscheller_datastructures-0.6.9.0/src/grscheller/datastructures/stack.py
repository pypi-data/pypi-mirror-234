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

"""Module grscheller.datastructure.stack - LIFO stack:

   Module implementing a LIFO stack using a singularly linked linear tree of
   nodes. The nodes can be safely shared between different Stack instances.
   Pushing to, popping from, and getting the length of the stack are all O(1)
   operations.
"""

from __future__ import annotations

from typing import Any, Callable

__all__ = ['Stack']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from .functional.maybe import Maybe, Some, Nothing
from .iterlib import concatIters, mergeIters, mapIter
from .circle import Circle

class _Node():
    """Class implementing nodes that can be linked together to form a singularly
    linked list. A node always contain data. It either has a reference to the
    next _Node object or None to indicate the bottom of the linked list.
    """
    def __init__(self, data, nodeNext: _Node | None):
        """Construct an element of a linked list, semantically immutable"""
        self._data = data
        self._next = nodeNext

    def __bool__(self):
        """Always return true, None will return as false"""
        return True

class Stack():
    """Class implementing a Last In, First Out (LIFO) stack datastructure. The
    stack contains a singularly linked list of nodes. Class designed to share
    nodes with other Stack instances.

    - The stack points to either the top node in the list, or to None which
      indicates an empty stack.
    - Stacks are stateful objects where values can be pushed on & popped off.
    - None represents the absence of a value and are ignored if pushed on the
      stack. Use a grscheller.functional.Maybe to indicate an assent value or
      another sentital value such as the empty tuple ().
    """
    def __init__(self, *ds):
        """Construct a LIFO Stack"""
        cnt = len(ds)
        self._head = None
        self._count = 0
        for ii in range(cnt):
            d = ds[ii]
            if d != None:
                node = _Node(d, self._head)
                self._head = node
                self._count += 1

    def __bool__(self) -> bool:
        """Returns true if stack is not empty"""
        return self._count > 0

    def __len__(self) -> int:
        """Returns current number of values on the stack"""
        return self._count

    def __iter__(self):
        """Iterator yielding data stored in the stack, starting at head"""
        node = self._head
        while node:
            yield node._data
            node = node._next

    def __reversed__(self):
        """Reverse iterate over the current state of the stack"""
        return iter(Stack(*self))

    def reverse(self) -> Stack:
        """Return a new stack in reverse order"""
        return Stack(*self)

    def __eq__(self, other: Any):
        """Returns True if all the data stored on the two stacks are the same.
        Worst case is O(n) behavior which happens when all the corresponding
        data elements on the two stacks are equal, in whatever sense they
        define equality, and none of the nodes are shared.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        left = self
        right = other
        nn = self._count
        while nn > 0:
            if left is None or right is None:
                return True
            if left._head is right._head:
                return True
            if left.head() != right.head():
                return False
            left = left.tail().getOrElse(Stack())
            right = right.tail().getOrElse(Stack())
            nn -= 1
        return True

    def __repr__(self):
        """Display the data in the stack, left to right starting at bottom"""
        circleData = Circle(*self).mapSelf(lambda x: repr(x)) 
        repStr = '|| ' + circleData.popR()
        while circleData:
            repStr = repStr + ' <- ' + circleData.popR()
        repStr += ' ><'
        return repStr

    def copy(self) -> Stack:
        """Return shallow copy of the stack in O(1) time & space complexity"""
        stack = Stack()
        stack._head = self._head
        stack._count = self._count
        return stack

    def push(self, *ds: Any) -> Stack:
        """Push data that is not NONE onto top of stack,
        return the stack being pushed.
        """
        for d in ds:
            if d != None:
                node = _Node(d, self._head)
                self._head = node
                self._count += 1
        return self

    def pop(self) -> Maybe:
        """Pop data off of top of stack"""
        if self._head is None:
            return Nothing
        else:
            data = self._head._data
            self._head = self._head._next
            self._count -= 1
            return Some(data)

    def head(self) -> Maybe:
        """DEPRICATED: Use peak() method instead

        This method was renamed to peak(). The head() name will be will be
        removed in a future release.
        """
        if self._head is None:
            return Nothing
        return Some(self._head._data)

    def peak(self) -> Maybe:
        """Returns on option for data at head of stack.
        Does not consume the data if it exists.
        """
        if self._head is None:
            return Nothing
        return Some(self._head._data)

    def tail(self) -> Maybe:
        """Return Some(tail) of the stack. In the case of an empty stack,
        return a Nothing.
        """
        if self._head:
            stack = Stack()
            stack._head = self._head._next
            stack._count = self._count - 1
            return Some(stack)
        return Nothing

    def cons(self, data: Any) -> Stack:
        """Return a new stack with data as head and self as tail.
        Note that trying to push None on the stack results in a shallow
        copy of the original stack.
        """
        if data is not None:
            stack = Stack()
            stack._head = _Node(data, self._head)
            stack._count = self._count + 1
            return stack
        else:
            return self.copy()

    def map(self, f: Callable[[Any], Stack]) -> Stack:
        return Stack(*mapIter(reversed(self), f))

    def flatMap(self, f: Callable[[Any], Stack]) -> Stack:
        """Apply function and flatten result, returns new instance"""
        return Stack(
            *concatIters(
                *mapIter(mapIter(reversed(self), f), lambda x: reversed(x))
            )
        )

    def mergeMap(self, f: Callable[[Any], Stack]) -> Stack:
        """Apply function and flatten result, returns new instance"""
        return Stack(
            *mergeIters(
                *mapIter(mapIter(reversed(self), f), lambda x: reversed(x))
            )
        )

if __name__ == "__main__":
    pass
