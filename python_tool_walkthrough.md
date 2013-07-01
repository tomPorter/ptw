% Python Tool & Testing Walkthrough
% Tom Porter
% July 1, 2013
#New tools available on `eclipse-bb` development server:
-   `pip` - A python package management tool, allows per-user installation of python packages.

-   `virtualenv` - Allows sandboxing of project-specific combinations of python packages.

    *Won't be covered today, I have not figured out how to set it up yet!*

-   `git` - A distributed source control management tool.

    *Not so much for primary use, but useable by `pip` for installing third party python packages directly from `github.com`*

#Of these we will use `pip` the most.
To install the `nose` testing framework (which we will use later):

-   Sign onto the eclipse development server using `CRT` or `Putty`

-   Issue this command:

        /home/{your_userid}/> pip install --user -I nose 

    This tells `pip` to install the `nose` package in your home directory
    and to ignore any exiting system versions.

    *For now, this is how I would install any third party python package you are interested in,
    particularly ones that you will use across projects.*

-   `pip` installs stuff to `.local/` in your home directory, so you have to add `.local/bin` to your 
path in your `.cshrc`

        setenv PATH ${HOME}/.local/bin:${PATH}

**`nose` is a unit test discovery framework that makes managing and running unit tests
easier than using the python `UnitTest` module by itself.**

#Hunh?

>"`nose` is a unit test discovery framework that makes managing and running unit tests
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

    In [2]: count.count_to??
    Type:       function
    String Form:<function count_to at 0x101dafe60>
    File:       /Users/tporter/Documents/python_tool_walkthrough/count.py
    Definition: count.count_to(n)
    Source:
    def count_to(n):
        '''Counts up to "n"'''
        for x in range(1,n+1):
            print "%i Elephant" % x

    In [3]: count.count_to(3)
    1 Elephant
    2 Elephant
    3 Elephant

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

#Project Organization (digression).
##`__init__.py` *whaat*??

    /home/tporter/count_project/count/> ls -la __init__.py
    rw-r--r--  1 tporter  staff  0 May 17 19:52 __init__.py

It's empty!

#Deep Black Python Magic *explained*

If a directory contains an `__init__.py` file, that marks the directory as part of a `Package`
which will make it discoverable by an `import` statement. If the `__init__.py` file contains any actual code, it is executed the first time the package is imported.

*That's how I can be sitting in the `count_project` directory, start ipython, issue `import count.count as c`
and I will get access to `./count_project/count/count.py`*

Note that periods in the import statement translate to directories and python modules in them:

`import count.count` &harr; `count/count.py`

The `import count.count as c` construct saves typing, so I could then call the `count_to()` method as:

    c.count_to(5)

as opposed to:

    count.count.count_to(5)

**These `__init__.py` files allow the imports in our tests to work properly without having to mess with the python system path.**

#Test Driven Development and testing with `nose`.

Test Driven Development *(TDD)* is tied to the idea of defining program behavior in terms of a series of tests.
If every one agrees that the set of tests defines the requirements for the program, and the program passes
all the tests, then the program is correct.

New features are defined in terms of new tests: you write a new test, the test fails (because there is no code
to go with it), and then you write code to make the test pass.  Ideally your code changes don't cause other
tests to fail!

In order for this approach to work, tests have to be:

-   *independent*. Order of test execution should not matter, and tests should not depend on prior tests.

-   *Repeatable*. Tests should not depend on external system state.  All tests should start from a repeatable
known state.

-   *Easy to Run*. If tests take a while to run, then we won't run them after each code change.

*How can we make this happen?*

#Testing with `nose`: Test Structure.

Documentation for `nose` is avail at [https://nose.readthedocs.org/en/latest/](https://nose.readthedocs.org/en/latest/)

A great tutorial is available at [http://ivory.idyll.org/articles/nose-intro.html](http://ivory.idyll.org/articles/nose-intro.html)

`nosetests` (The test runner from `nose`) discovers tests in your project and tries to run them and reports on the results.

-   Any directory that starts with `[Tt]test*` will get inspected for tests to run.

-   Any python program that starts with `[Tt]est*` will be run as a test.

-   Any function in a test program that starts with `test*` will be run as a test.
If the function returns `True`, then the test passed, if it returns `False`, the test fails.

-   You can use directory structure and test program names and contents to organize your tests, since
you can tell nose to run all your tests or subsets of them based on the path to the tests you want to
run.

#Testing with `nose`: Test Structure 2.

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

#Testing with `nose`: Test Structure 3.

A more complex `tests/` directory layout merely helps organize tests and keeps your individual test files
small.

    tests/
        __init__.py
        common_test_functions.py
        test_this_part/
            test_this_a.py
            test_this_b.py
        test_the_other_part/
            test_the_last_part.py  

Run just one test:

    nosetests tests/test_this_part/test_this_a.py

`common_test_functions.py` can contain code that all your tests may need.  It can be imported at the 
top of all your tests and the code can be used anywhere in your tests.   I suppose the import could go in
the mysterious `__init__.py`.

#`Assert` Methods, How you check if the objects under test worked or not.

Python gives us the `assert(condition[,failure_message])` method that raises an `AssertionError` when the condition
is not true.  `nosetests` and the `UnitTest` module found in the standard library use `assert` and related functions
to drive tests. The python UnitTest documentation [http://docs.python.org/release/2.6.4/library/unittest.html#testcase-objects](http://docs.python.org/release/2.6.4/library/unittest.html#testcase-objects)
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
        assert True,"I should have passed"  #always True, so test will always pass.
    def test_always_fails(self):
        '''test_always_fails'''
        assert False,"I failed"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*What is the `from nose.tools import *` for?*

-   It gives you access to all the assert helpers in `nose`

*Why is this arranged with a `TestCase` class, and what is this `self` stuff?*

-   Defining a class to hold the tests establishes a scope for the setup and teardown methods.
The `setUp()` and `tearDown()` methods will be called before and after each test function is called.
-   If you define a class, all functions in it must have `self` as the first function argument,
which is what gives you access to all the attributes of the class instance. *More later*

#Class Oriented programming and how it helps testing.

**Since all tests are independent, how do you interact with your code functions,
and what do you test in your assertions?**

If I have a monolithic program with no functions and all straightline code, I simply can't test it
in a TDD fashion or use a testing framework at all.  The minimum requirement for using `nose` to test your
 program is writing it as a module so it can be imported
and having functions that have inputs and return values.

    #count_proj/count/count.py               #count_proj/tests/test_counts.py
    def count_to(n):                         from nose.tools import *
      '''Counts up to "n"'''                 import count.count as c
      results = []                           class TestCase:
      for x in range(1,n+1):                   def test_one_elephant(self):
          results.append("%i Elephant" % x)      '''Get one elephant back when I count to 1.'''
      return results                             assert '1 Elephant' in c.count_to(1)

    def main():                                def test_len_two_elephant(self):
      for x in count_to(5):                      '''Get an array of two back when I count to 2.'''
        print x                                  assert_equal(2,len(c.count_to(2)))

    if __name__ == "__main__":
      main()

Functions make TDD possible, but *classes* make your code manageable.

In the simple example above, functions are sufficient.  When dealing with more complex data structures
and processing, breaking things into classes lets you concentrate on one piece of functionality at a time.

#Anatomy of a class.

Classes are templates for creating class instances.

    pookie = BadCat()  # BadCat is the class, pookie is the instance.


Classes have a `self` attribute which refers to the instance itself when referred to in the class code.
Any function in the class has access to all the variables in the class via self.
Once an instance is created, instance variables or attributes can be accessed directly.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python}
class BadCat:
    ## Inside the class, everyone gets a 'self'
    def give_name(self,name):
        self.name = name # Defines an instance attribute called 'name' and populates it.
    def call_cat(self):
        print "Hey %s" % self.name # Has access to self.name since it has access to self.

pookie = BadCat()
## No 'self' in instance method calls.
pookie.give_name('pookie')
pookie.call_cat()
print pookie.name
# Must call give_name() before calling call_cat() to create pookie.name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The existence of `self` means that all functions that operate on existing attributes of the
instance only have to have a function signature of `do_something(self)` no matter what instance variables
they refer to internally. *This saves you from passing function parameters around.*

#Anatomy of a class 2.

-   Classes have an `__init__(self)` *whether explicit or implied*. `__init__(self)`
    is called when an instance of a class is created.

-   Additional parameters can be passed in, but the instance creation needs to supply them.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python}
class Foo:
    def __init__(self,bar):
        self.bar = bar

foo = Foo('bar')
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   `__init__(self)` is used to populate instance attributes that will always be needed, or for default values.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python}
class BadCat:
    def __init__(self):
        self.legs = 4        # I hope!
        self.name = 'Jerk!'  # Default name if none supplied by give_name()
    def give_name(self,name):
        self.name = name     # Defines instance attribute 'name' and populates it.
    def call_cat(self):
        print "Hey %s" % self.name # Has access to self.name since it has access to self.
pookie = BadCat()
pookie.call_cat() # -> 'Hey Jerk!'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Tie it all together: Classes and TDD.

Because instances of classes contain collections of instance attributes and methods that work only
on those attributes, they make control of your tests easier.

Inside your test functions, you create a instance of the class under test, call some preliminary
methods if needed, then check to see if the results of the call to the instance method under test come out OK.

Big programs using simple data structures end up with code that concentrates on the plumbing and mechanics of
manipulating the data while hiding the intent of the program.

-   Well differentiated classes let you think about one piece of the problem at a time.

-   Descriptively named functions in those classes expose the intent of what you want to accomplish
without drowning in the detail of how the functions accomplish the task.

-   Tests that exercise the class functions are guides to how the classes should be used.

-   Thinking about *what* classes and functions should do as opposed to *how* they should do it
makes it easier to write tests first without code to back them up.

#Tie it all together: Classes and TDD 2.

I can (and should) write tests first, and writing the calls to code under test in an abstract
way forces me to a class oriented coding style using expressive function names.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python}
class TestCase:
    def test_client_create(self):
        '''Creating a client.'''
        db = DashBoard()
        db.addClient('PGI')
        # Maybe not so good, assumes db.client_list exists and is a sequence.
        assert 'PGI' in db.client_list
        # client_exists() masks actual structure of DashBoard class.
        assert db.client_exists('PGI')
    def test_get_client_heading(self):
        '''Retrieve Client heading.'''
        db = DashBoard()
        db.addClient('PGI')
        # Still requires knowledge of DashBoard internals.
        # db.client_list better be a dictionary of dictionaries
        assert db.client_list['PGI']['heading'] == 'PGI Dashboard'
        # OR maybe instead
        pgi = db.getClient('PGI')
        assert pgi.heading == 'PGI DashBoard'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I don't have to have any code written to run this test.  It will fail, but I'm already thinking about
how I want my program to act, and can now start to write code that will make this test pass.  The attributes and
functions you use in your tests should be what users of your classes should expect to know about, even if the user
is only you.

**Write the minimal amount of code that makes a test pass, *then* write more tests, and add the code to make
them pass.**   Don't write too many tests too soon.  If the test code that exercises your classes and functions
looks kludgey, then maybe it means your program code needs to change.

There will often be more test code than program code, but tests are not wasted effort.  Instead
they are the guardians that let you make *new* changes without wondering if anything old has been broken.

#Closing ideas.

-   Writing tests for existing programs is a wretched business, sometimes impossible. Write tests first!

-   This only covers unit testing, which exercises your class functions in isolation.
There are other kinds of testing that operate at higher levels like functional testing and acceptance
testing, but python does not have great frameworks for these and they are mostly aimed at web apps
or interactive applications running on a desktop.

-   If your program interacts with the file system or has time of day dependencies, you can still do repeatable
tests by using your setup and teardown methods to create mockups of the file system as you expect it to be.
Clock time dependencies can be mocked as well IF you use module-level variables to hold times and dates and then
refer to them in your code as opposed to referring to datetime.datetime.now() in your code directly.  I have
examples of how to do this.

-   There are python libraries for mocking database interactions or objects that are expensive to create.
If a test requires an instance of a big, hairy object, but only uses one or two attributes out of it, then
mocking the object might be the way to go.  *Note that you do not mock the object you are testing, but rather
any predecessors it might have.*

---

<p style="text-align:center;font-size:400%">Questions?</p>

---

<p style="text-align:center;font-size:400%">Thank You!</p>

