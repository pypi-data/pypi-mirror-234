# Changelog: grscheller.datastrucures

### Overview

* Single maintainer project
  * semantic versioning
    * first digit signifies an event or epoch
    * second digit means breaking API changes (between PyPI releases)
    * third digit either means
      * API breaking changes (between GitHub commits)
      * API additions (between PyPI releases)
    * fourth digit either means
      * bug fixes or minor changes (between PyPI releases)
      * GitHub only thrashing and experimentation
  * rolling release model
    * maintainer will not back port bug fixes to previous versions
    * main branch will be the only tracking branch on GitHub
      * attempt to keep relatively stable, but not fully tested
    * feature branch begin with "feature_" and are places to
      * explore new directions
      * commit potentially very broken code
      * could be deleted from GitHub WITHOUT WARNING
    * PyPI releases are tagged with a leading "v" on GitHub
      * semantic versioning more strict between PyPI releases
      * semantic versioning between GitHub commits a bit more subjective
        * only meaningful GitHub commits will be listed below
        * all non-pulled PyPI releases will be tagged & listed below

# Versions

### Version v0.6.9.0 - PyPI release date: 2023-10-09
* deprecated Stack head() method
  * replaced with peak() method
* renamed core module to iterlib module
  * library just contained functions for manimulating iterators
  * TODO: use mergeIters as a guide for an iterator "zip" function
* class Stack better in alignment with:
  * Python lists
    * more natural for Stack to iterate backwards starting from head
    * removed Stack's __getitem__ method
    * both pop and push/append from end
  * Dqueue which wraps a Circle instance
    * also Dqueue does not have a __getitem__ method
  * Circle which implements a circular array with a Python List
  * Stack now implements map, flatMap, mergeMap methods
    * each returns a new Stack instance, with new nodes

### Version 0.6.8.6 - commit date: 2023-10-08
* 3 new methods for class Circle and Dqueue
  * mapSelf, flatMapSelf, mergeMapSelf
    * these correspond to map, flatMap, mergeMap
    * except they act on the class objects themselves, not new instances
* these new methods will NOT be added to the Stack class
  * they would destroy node sharing
  * did add a map method which returns a new instance (with new nodes)
  * TODO: add flatMap and mergeMap methods
* probably will add them to the Dqueue class too
  * not worth the maintenance effort maintaining two version of Dqueue
    * one returning new instances
    * the other modifying the object in place

### Version 0.6.8.3 - commit date: 2023-10-06
* Stack now works with Python Reversed builtin function
  * using a __reversed__ method which is O(n)
  * never figured out why reversed() failed with __getitems__ & __len__
    * this would have been O(n^2) anyway
* Stack no longer implements the __getitems__ method
* class Carray renamed to Circle
  * implements a circular array based on a Python List
  * resizes itself as needed
  * will handle None values being pushed and popped from it
  * implemented in the grscheller.datastructures.circle module
    * in the src/grscheller/datastructures/circle.py file
  * O(1) pushing/popping to/from either end
  * O(1) length determination
  * O(1) indexing for setting and getting values.
* Dqueue implemented with Circle class instead of List class directly
* Ensured that None is never pushed to Stack & Dqueue objects


### Version 0.6.4.1 - commit date: 2023-10-01
* Initial prototypes for map and flatMap for Dqueue class
* Started grscheller.datastructures.core module
  * used for grscheller.datastructures implementation
  * no particular need to indicate them to be _private
  * exports the following functions so far
    * concatIters - sequentially concatenate multiple iterators
    * mergeIters - merge multiple iterators until one is exhausted
    * mapIter - lazily map a function over an iterator stream
* Decided to keep Alpha for next PyPI release

### Version 0.6.3.2 - commit date: 2023-09-30
* Made functional module into a sub package of datastructures
* Improved comments and type annotations
* Removed isEmpty method from Dqueue class
* Both Dqueue & Stack objects evaluate true when non-empty
* Beginning preparations for the next PyPI release
  * Want to make next PyPI release a Beta release
  * Need to improve test suite first

### Version 0.6.2.0 - commit date: 2023-09-25
* Started work on a Left biased Either Monad
* removed isEmpty method from Stack class

### Version 0.6.1.0 - commit date: 2023-09-25
* Maybe get() and getOrElse() API changes
* getting a better handle on type annotation
  * work-in-progress
  * erroneous LSP error messages greatly reduced

### Version 0.5.2.1 - PyPI release date: 2023-09-24
* data structures now support a much more FP style for Python
  * implemented Maybe monad
  * introduces the use of type annotations for this effort
  * much better test coverage

### Version 0.5.0.0 - commit date: 2023-09-20
* begin work on a more functional approach
  * create a monadic Option class
  * drop the subclassing of NONE
  * put this effort on a new branch: feature_maybe
* some flaws with previous approach
  * the OO redirection not best
    * for a class used in computationally intense contexts
    * adds way too much complexity to the design
  * some Python library probably already implemented this
    * without looking, these probably throw tons of exceptions
    * more fun implementing it myself
      * then being dissatified with someone else's design

### Version 0.4.0.0 - commit date: 2023-09-11
* subtle paradigm shift for Stack class
  * empty Stacks no longer returned for nonexistent stacks
    * like the tail of an empty stack
    * singleton Stack.stackNONE class object returned instead
  * Stack & _StackNONE classes inherit from _StackBase
  * still working out the API

### Version 0.3.0.2 - PyPI release date: 2023-09-09
* updated class Dqueue
  * added __eq__ method
  * added equality tests to tests/test_dqueue.py
* improved docstrings

### Version 0.2.3.0 - commit date: 2023-09-06

* added __eq__ method to Stack class
* added some preliminary tests
  * more tests are needed
* worst case O(n)
  * will short circuit fast if possible

### Version 0.2.2.2 - PyPI release date: 2023-09-04

* decided base package should have no dependencies other than
  * Python version (>=2.10 due to use of Python match statement)
  * Python standard libraries
* made pytest an optional \[test\] dependency
* added src/ as a top level directory as per
  * https://packaging.python.org/en/latest/tutorials/packaging-projects/
  * could not do the same for tests/ if end users are to have access

### Version 0.2.1.0 - PyPI release date: 2023-09-03

* first Version uploaded to PyPI
* https://pypi.org/project/grscheller.datastructures/
* Install from PyPI
  * $ pip install grscheller.datastructures==0.2.1.0
  * $ pip install grscheller.datastructures # for top level version
* Install from GitHub
  * $ pip install git+https://github.com/grscheller/datastructures@v0.2.1.0
* pytest made a dependency
  * useful & less confusing to developers and endusers
    * good for systems I have not tested on
    * prevents another pytest from being picked up from shell $PATH
      * using a different python version
      * giving "package not found" errors
    * for CI/CD pipelines requiring unit testing

### Version 0.2.0.2 - github only release date: 2023-08-29

* First version able to be installed from GitHub with pip
* $ pip install git+https://github.com/grscheller/datastructures@v0.2.0.2

### Version 0.2.0.1 - commit date: 2023-08-29

* First failed attempt to make package installable from GitHub with pip

### Version 0.2.0.0 - commit date: 2023-08-29

* BREAKING API CHANGE!!!
* Stack push method now returns reference to self
* Dqueue pushL & pushR methods now return references to self
* These methods used to return the data being pushed
* Now able to "." chain push methods together
* Updated tests - before making API changes
* First version to be "released" on GitHub

### Version 0.1.1.0 - commit date: 2023-08-27

* grscheller.datastructures moved to its own GitHub repo
* https://github.com/grscheller/datastructures
  * GitHub and PyPI user names just a happy coincidence

### Version 0.1.0.0 - initial version: 2023-08-27

* Package implementing data structures which do not throw exceptions
* Did not push to PyPI until version 0.2
* Initial Python grscheller.datastructures for 0.1.0.0:
  * dqueue - implements a double sided queue class Dqueue
  * stack - implements a LIFO stack class Stack
