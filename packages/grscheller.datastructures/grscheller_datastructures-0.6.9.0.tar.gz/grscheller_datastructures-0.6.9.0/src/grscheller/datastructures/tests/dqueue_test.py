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

from grscheller.datastructures.dqueue import Dqueue
from grscheller.datastructures.functional import Maybe, Nothing

class TestDqueue:
    def test_push_then_pop(self):
        dq = Dqueue()
        pushed = 42; dq.pushL(pushed)
        popped = dq.popL().get()
        assert pushed == popped
        assert len(dq) == 0
        assert dq.popL().getOrElse(42) == 42
        pushed = 0; dq.pushL(pushed)
        popped = dq.popR().getOrElse(42)
        assert pushed == popped == 0
        assert not dq
        pushed = 0; dq.pushR(pushed)
        popped = dq.popL().get()
        assert popped is not None
        assert pushed == popped
        assert len(dq) == 0
        pushed = ''; dq.pushR(pushed)
        popped = dq.popR().get()
        assert pushed == popped
        assert len(dq) == 0
        dq.pushR('first').pushR('second').pushR('last')
        assert dq.popL().get() == 'first'
        assert dq.popR().get() == 'last'
        assert dq
        dq.popL()
        assert len(dq) == 0

    def test_iterators(self):
        data = [1, 2, 3, 4]
        dq = Dqueue(*data)
        ii = 0
        for item in dq:
            assert data[ii] == item
            ii += 1
        assert ii == 4

        data.append(5)
        dq = Dqueue(*data)
        data.reverse()
        ii = 0
        for item in reversed(dq):
            assert data[ii] == item
            ii += 1
        assert ii == 5

        dq0 = Dqueue()
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

        data = ()
        dq0 = Dqueue(*data)
        for _ in dq0:
            assert False
        for _ in reversed(dq0):
            assert False

    def test_capacity(self):
        dq = Dqueue(1, 2)
        assert dq.fractionFilled() == 2/2
        dq.pushL(0)
        assert dq.fractionFilled() == 3/4
        dq.pushR(3)
        assert dq.fractionFilled() == 4/4
        dq.pushR(4)
        assert dq.fractionFilled() == 5/8
        assert len(dq) == 5
        assert dq.capacity() == 8
        dq.resize()
        assert dq.fractionFilled() == 5/5
        dq.resize(20)
        assert dq.fractionFilled() == 5/25

    def test_equality(self):
        dq1 = Dqueue(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        dq2 = Dqueue(2, 3, 'Forty-Two').pushL(1).pushR((7, 11, 'foobar'))
        assert dq1 == dq2

        tup2 = dq2.popR().getOrElse((42, 'Hitchhiker'))
        assert dq1 != dq2

        dq2.pushR((42, 'foofoo'))
        assert dq1 != dq2

        dq1.popR().getOrElse((38, 'Nami'))
        dq1.pushR((42, 'foofoo')).pushR(tup2)
        dq2.pushR(tup2)
        assert dq1 == dq2

        holdA = dq1.popL().getOrElse(666)
        dq1.resize(42)
        holdB = dq1.popL().getOrElse(777)
        holdC = dq1.popR().getOrElse(888)
        dq1.pushL(holdB).pushR(holdC).pushL(holdA).pushL(200)
        dq2.pushL(200)
        assert dq1 == dq2

    def test_maybe(self):
        dq1 = Dqueue()
        m42 = dq1.pushL(42).popR()
        mNot = dq1.popR()
        assert m42 == Maybe(42)
        assert m42 != Maybe(21)
        assert m42.getOrElse(21) == 42
        assert m42.getOrElse(21) != 21
        assert m42.get() == 42
        assert m42.get() != 21
        assert mNot.getOrElse(21) == 21
        assert mNot == Nothing
        assert mNot.get() == None

    def test_mapAndFlatMap(self):
        dq1 = Dqueue(1,2,3,10)
        dq1_answers = Dqueue(0,3,8,99)
        assert dq1.map(lambda x: x*x-1) == dq1_answers
        dq2 = dq1.flatMap(lambda x: Dqueue(1, x, x*x+1))
        dq2_answers = Dqueue(1, 1, 2, 1, 2, 5, 1, 3, 10, 1, 10, 101)
        assert dq2 == dq2_answers
