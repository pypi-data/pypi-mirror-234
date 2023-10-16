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

"""pytest testsuite - for use with pytest

   The testsuite can be either run against

   1. The checked out main branch of https://github.com/grscheller/datastructures
      where we assume pytest has already been installed by either pip or some
      external package manager.

      $ export PYTHONPATH=/path/to/.../datastructures
      $ pytest --pyargs grscheller.datastructures

   2. The pip installed package with test optional dependency from GitHub.

      $ pip install "grscheller.datastructures[test] @ git+https://git@github.com/grscheller/datastructures"
      $ pytest --pyargs grscheller.datastructures

   3. The pip installed particular version of the package from GitHub.
      $ pip install pytest
      $ pip install git+https://github.com/grscheller/datastructures@v0.2.1.1
      $ pytest --pyargs grscheller.datastructures

   4. The pip installed package from PyPI

      $ pip install grscheller.datastructures[test]
      $ pytest --pyargs grscheller.datastructures

   The pytest package was made a project.optional-dependency of the datastructures
   package. To ensure the correct matching version of pytest is used to run the
   tests, pytest needs to be installed into the virtual environment, either
   manually or via the [test] optional-dependency. Otherwise, the
   wrong pytest executable running the wrong version of Python might be found on
   your shell $PATH.
"""                                              
