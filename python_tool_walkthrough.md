% Python Tool & Testing Walkthrough
% Tom Porter
% July 1, 2013
#New tools available on `eclipse-bb` development server:
-   `pip` - A python package management tool, allows per-user installation of python packages.

-   `virtualenv` - Allows sandboxing of project-specific combinations of python packages.

-   `git` - A distributed source control management tool.  

    *Not so much for primary use, but useable by `pip` for installing third party python packages directly from `github.com`*

#Of these we will use `pip` the most.
To install the `nose` testing framework (which we will use later):

-   Sign onto the eclipse development server using `CRT` or `Putty`

-   Issue this command:

        /home/{your_userid}/> pip install nosetests --user -I

    This tells `pip` to install the `nosetests` package in your home directory 
    and to ignore any exiting system versions.

    *For now, this is how I would install any third party python package you are interested in, 
    particularly ones that you will use across projects.*

`nosetests` is a unit test discovery framework that makes managing and running unit tests 
easier than using the python `UnitTest` module by itself.

#Hunh?

>"`nosetests` is a unit test discovery framework that makes managing and running unit tests 
easier than using the python `UnitTest` module by itself."

##Which leads us to our next set of topics:

-   Designing programs as *Modules*.

-   Project Organization.

-   Test Driven Development.

#Designing programs as *Modules*.

Making a python program a module is easy:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python}
#count.py
def count_to(n):
    '''Counts up to "n"'''
    for x in range(1,n+1):
        print "%i Elephant" % x

def main():
    count_to(5)

if __name__ == "__main__":
    main()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If I  run it from the command line, it will count to 5:

    /home/tporter> python count.py
    1 Elephant
    2 Elephant
    3 Elephant
    4 Elephant
    5 Elephant
    /home/tporter>

#Designing programs as *Modules* 2.
**But**, I can also start up `ipython` and explore the code a little bit by importing it as a *Module*.

    /home/tporter> ipython
    Python 2.7.3 (v2.7.3:70274d53c1dd, Apr  9 2012, 20:52:43)
    ...
    In [1]: import count
    
    In [2]: count.count_to?
    Type:       function
    String Form:<function count_to at 0x101dafe60>
    File:       /Users/tporter/Documents/python_tool_walkthrough/count.py
    Definition: count.count_to(n)
    Docstring:  Counts up to "n"
    
    In [3]: count.count_to??
    Type:       function
    String Form:<function count_to at 0x101dafe60>
    File:       /Users/tporter/Documents/python_tool_walkthrough/count.py
    Definition: count.count_to(n)
    Source:
    def count_to(n):
        '''Counts up to "n"'''
        for x in range(1,n+1):
            print "%i Elephant" % x
    
    In [4]: count.count_to(3)
    1 Elephant
    2 Elephant
    3 Elephant
    
    In [5]: quit()

#Designing programs as *Modules* 3.

If a program is easy to explore using `ipython`, it is on it's way to being a well designed
program for a few important reasons:

-   It has `docstrings` so you can tell what functions do.

-   If you can browse a function easily, it's not too big, so it's probably not trying to do too much. 

-   If the functions don't take too many arguments, or it's not too hard to create the needed arguments, 
    this again points to tightly coupled, focussed function design.

These characteristics also lead to more easily testable code.

But, *how* should our project directories be laid out to support the use of modules and testing?

#Project Organization.

Many python projects have the following basic structure, particularly if they will end up
being distributed as python packages:

    ./count_project/
        run_count.py  # sometimes placed in a bin/ directory instead.
        count/
            __init__.py
            count.py
        tests/
            __init__.py
            common_test_functions.py
            test_this_part/
                test_this_a.py
                test_this_b.py
            test_the_other_part/
                test_the_last_part.py
        docs/
            {documentation for project}

#Project Organization 2.
##`__init__.py` *whaat*??

    /home/tporter/count_project/count/> ls -la __init__.py
    rw-r--r--  1 tporter  staff  0 May 17 19:52 __init__.py

It's empty!

#Deep Black Python Magic *explained*
If a directory contains an `__init__.py` file, that marks the directory as part of a `Package` 
which will make it discoverable by an `import` statement.

*That's how I can be sitting in the `count_project` directory, start ipython, issue `import count.count as c` 
and I will get access to `./count_project/count/count.py`*

Note that periods in the import statement translate to directories and python modules in them:

`import count.count` &harr; `count/count.py`

The `import count.count as c` construct saves typing, so I could then call the `count_to()` method as:

    c.count_to(5)

as opposed to:

    count.count.count_to(5)

If the `__init__.py` file contains any actual code, it is executed the first time the package is imported.

#Test Driven Development and testing with `nose`.

Test Driven Development *(TDD)* is tied to the idea of defining program behavior in terms of a series of tests.
If every one agrees that the set of tests defines the requirements for the program, and the program passes
all the tests, then the program is correct. 

New features are defined in terms of new tests: you write a new test, the test fails (because there is no code 
to go with it), and then you write code to make the test pass.  Ideally your code changes don't cause other
tests to fail!

In order for this approach to work, tests have to be:

-   *Independant*. Order of test execution should not matter, and tests should not depend on prior tests.

-   *Repeatable*. Tests should not depend on external system state.  All tests should start from a repeatable 
known state.

-   *Easy to Run*. If tests take a while to run, then we won't run them after each code change.

*How can we make this happen?*

#Testing with `nose`: Test Structure.

Documentation for `nose` is avail at [https://nose.readthedocs.org/en/latest/](https://nose.readthedocs.org/en/latest/)

A great tutorial is available at [http://ivory.idyll.org/articles/nose-intro.html](http://ivory.idyll.org/articles/nose-intro.html)

`nose` discovers tests in your project and tries to run them and reports on the results.

-   Any directory that starts with `[Tt]test*` will get inspected for tests to run.

-   Any python program that starts with `[Tt]est*` will be run as a test.

-   Any function in a test program that starts with `test*` will be run as a test.  
If the function returns `True`, then the test passed, if it returns `False`, the test fails.

-   You can use directory structure and test program names and contents to organize your tests, since
you can tell nose to run all your tests or subsets of them based on the path to the tests you want to
run.

#Testing with `nose`: Test Structure. 2

Revisiting our theoretical project structure:

        tests/
            __init__.py
            common_test_functions.py
            test_this_part/
                test_this_a.py
                test_this_b.py
            test_the_other_part/
                test_the_last_part.py

The simplest test we can have is a single python program called `tests/test_simple.py` containing
a single function that has an assertion in it that evaluates to `True` or `False`:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python}
#test_simple.py
def test_always_passes():
    '''test_always_passes'''
    assert True  #will always be True, so test will always pass.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    count_project>  nosetests
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.008s
    
    OK

#`Assert` Methods, How you check if the objects under test worked or not.

Python gives us the `assert(condition)` method that raises an `AssertionError` when the condition 
is not true.  `nosetests` and the `UnitTest` module fund in the standard library use `assert` and related functions
to drive tests. [The python UnitTest documentation](http://docs.python.org/release/2.6.4/library/unittest.html#testcase-objects) 
shows the *assert* variations that are available in `UnitTest`, for example:

-   `assertEqual(a,b[,failure_message])` Checks for equality of `a` and `b`.
-   `assert_(condition[,failure_message])` Checks that condition is true.
-   `assertRaises(exception,function[,function_keywords,...])` Checks that exception is raised when 
function is called with function_keywords.

The `nosetests.tools` module has access to all `UnitTest` asserts but uses snake_case for them instead of camelCase. 
*(I don't know why)* It also has some other convenience methods available as well.

**You can have multiple assert statements in a test function, but the first failing assertion ends the test, so break them up.**

#More realistic test case setup.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python}
#test_realistic.py
from nose.tools import *
class TestCase:
    def setUp(self):
        pass # Do setup stuff here.

    def tearDown(self):
        pass # Do teardown stuff here.

    def test_always_passes(self):
        '''test_always_passes'''
        assert True,"I should have passed"  #will always be True, so test will always pass.

    def test_always_fails(self):
        '''test_always_passes'''
        assert False,"I failed" 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `setUp()` and `tearDown()` methods will be called before and after each test function is called.

*Why is this arranged with a `TestCase` class, and what is this `self` stuff?*

-   Defining a class to hold the tests defined a scope for the setup and teardown methods.
-   If you define a class, all functions in it must have `self` as the first function argument, 
which is what gives you assess to all the attributes of the class instance.
-   It automatically turns the class into a subclass of the `nose` test class, which lets it be recognized and
run as a test.  *(I don't understand it, I just do it!)

*What is the `from nose.tools import *` for?*

-   It gives you access to all the assert helpers in `nose`


#Class Oriented programming and how it helps testing.

