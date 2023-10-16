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

from grscheller.datastructures.functional import Maybe, Nothing, Some
from grscheller.datastructures.functional import Either, Left, Right

def add2(x):
    return x + 2

class TestMaybe:
    def test_identity(self):
        n1 = Maybe()
        n2 = Maybe()
        o1 = Maybe(42)
        o2 = Maybe(40)
        assert o1 is o1
        assert o1 is not o2
        o3 = o2.map(add2)
        assert o3 is not o2
        assert o1 is not o3
        assert n1 is n1
        assert n1 is not n2
        assert o1 is not n1
        assert n2 is not o2

    def test_equality(self):
        n1 = Maybe()
        n2 = Maybe()
        o1 = Maybe(42)
        o2 = Maybe(40)
        assert o1 == o1
        assert o1 != o2
        o3 = o2.map(add2)
        assert o3 != o2
        assert o1 == o3
        assert n1 == n1
        assert n1 == n2
        assert o1 != n1
        assert n2 != o2

    def test_iterate(self):
        o1 = Maybe(38)
        o2 = o1.map(add2).map(add2)
        n1 = Maybe()
        l1 = []
        l2 = []
        for v in n1:
            l1.append(v)
        for v in o2:
            l2.append(v)
        assert len(l1) == 0
        assert len(l2) == 1
        assert l2[0] == 42

    def test_get(self):
        o1 = Maybe(1)
        n1 = Maybe()
        assert o1.getOrElse(42) == 1
        assert n1.getOrElse(42) == 42
        assert o1.get() == 1
        assert n1.get() is None
        assert n1.get() == None
        assert n1.getOrElse(13) == (10 + 3)
        assert n1.getOrElse(10/7) == (10/7)

    def test_nothing(self):
        o1 = Maybe(42)
        n1 = Maybe()
        n2 = n1
        assert o1 != Nothing
        assert n1 == Nothing
        assert n1 is n1
        assert n1 is n2

class TestEither:
    def test_identity(self):
        e1 = Left(42)
        e2 = Left(42)
        e3 = Right('not 42')
        e4 = Right('not 42')
        e5 = Right('also not 42')
        e6 = e3.copy()
        e7 = e3
        e8 = e1.copy()
        assert e1 is e1
        assert e1 is not e2
        assert e1 is not e3
        assert e1 is not e4
        assert e1 is not e5
        assert e1 is not e6
        assert e1 is not e7
        assert e1 is not e8
        assert e2 is e2
        assert e2 is not e3
        assert e2 is not e4
        assert e2 is not e5
        assert e2 is not e6
        assert e2 is not e7
        assert e2 is not e8
        assert e3 is e3
        assert e3 is not e4
        assert e3 is not e5
        assert e3 is not e6
        assert e3 is e7
        assert e3 is not e8
        assert e4 is e4
        assert e4 is not e5
        assert e4 is not e6
        assert e4 is not e7
        assert e4 is not e8
        assert e5 is e5
        assert e5 is not e6
        assert e5 is not e7
        assert e5 is not e8
        assert e6 is e6
        assert e6 is not e7
        assert e6 is not e8
        assert e7 is e7
        assert e7 is not e8
        assert e8 is e8

    def test_equality(self):
        e1 = Left(42)
        e2 = Left(42)
        e3 = Right('not 42')
        e4 = Right('not 42')
        e5 = Right('also not 42')
        e6 = e3.copy()
        e7 = e3
        e8 = e1.copy()
        assert e1 == e1
        assert e1 == e2
        assert e1 != e3
        assert e1 != e4
        assert e1 != e5
        assert e1 != e6
        assert e1 != e7
        assert e1 == e8
        assert e2 == e2
        assert e2 != e3
        assert e2 != e4
        assert e2 != e5
        assert e2 != e6
        assert e2 != e7
        assert e2 == e8
        assert e3 == e3
        assert e3 == e4
        assert e3 != e5
        assert e3 == e6
        assert e3 == e7
        assert e3 != e8
        assert e4 == e4
        assert e4 != e5
        assert e4 == e6
        assert e4 == e7
        assert e4 != e8
        assert e5 == e5
        assert e5 != e6
        assert e5 != e7
        assert e5 != e8
        assert e6 == e6
        assert e6 == e7
        assert e6 != e8
        assert e7 == e7
        assert e7 != e8
        assert e8 == e8
