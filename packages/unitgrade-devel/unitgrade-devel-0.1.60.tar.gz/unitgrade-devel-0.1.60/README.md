# Unitgrade-devel
**Note: This is the development version of unitgrade. If you are a student, please see http://gitlab.compute.dtu.dk/tuhe/unitgrade.**

Unitgrade is an automatic report and exam evaluation framework that enables instructors to offer automatically evaluated programming assignments. 
 Unitgrade is build on pythons `unittest` framework so that the tests can be specified in a familiar syntax and will integrate with any modern IDE. What it offers beyond `unittest` is the ability to collect tests in reports (for automatic evaluation) and an easy and 100% safe mechanism for verifying the students results and creating additional, hidden tests. A powerful cache system allows instructors to automatically create test-answers based on a working solution. 

 - 100% Python `unittest` compatible
 - No configuration files
 - No limitations: If you can `unittest` it, it works  
 - Tests are quick to run and will integrate with your IDE
 - Cache and hint-system makes tests easy to develop
 - Granular security model: 
    - Students get public `unittests` for easy development of solutions
    - Students use a tamper-resistant file to create submissions which are uploaded
    - Instructors can automatically verify the students solution using a Docker VM and run hidden tests
 - Automatic Moss anti-plagiarism detection
 - CMU Autolab integration (Experimental)
 - A live dashboard which shows the outcome of the tests

### Install
Simply use `pip`
```terminal
pip install unitgrade-devel
```
This will install `unitgrade-devel` (this package) and all dependencies to get you started.

## Overview
![alt text|small](https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/docs/images/process.png)

The figure shows an overview of the workflow. 
 - You write exercises and a suite of unittests. 
 - They are then compiled to a version of the exercises without solutions. 
 - The students solve the exercises using the tests and when they are happy, they run an automatically generated `_grade.py`-script to produce a `.token`-file with the number of points they obtain. This file is then uploaded for further verification/evaluation.
 - The students can see their progress and review hints using the dashboard (see below)

### Videos
Videos where I try to talk and code my way through the examples can be found on youtube:

  - First test: https://youtu.be/jC9AzZA5FcQ
  - Framework and hints: https://youtu.be/xyY9Qan1b1Q
  - MOSS plagiarism check: https://youtu.be/Cp4PvOnYozo
  - Hidden tests and Docker: https://youtu.be/vP6ZqeDwC5U
  - Jupyter notebooks: https://youtu.be/B6nzVuFTEsA
  - Autolab: https://youtu.be/h5mqR8iNMwM

# Instructions and examples of use
The examples can be found in the `/examples` directory: https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/tree/master/examples

## A simple example
Unitgrade makes the following assumptions:
 - Your code is in python
 - Whatever you want to do can be specified as a `unittest`

Although not required, it is recommended you maintain two version of the code: 
 - A fully-working version (i.e. all tests pass)
 - A public version distributed to students (some code removed))

I use `codesnipper` (see http://gitlab.compute.dtu.dk/tuhe/snipper) to synchronize the two versions automatically.  
Let's look at an example. Suppose our course is called `cs101`, in which case we make three files in our private folder `instructor`:
```terminal
instructor/cs101/homework.py # This contains the students homework
instructor/cs101/report1.py  # This contains the tests
instructor/cs101/deploy.py   # A private file to deploy the tests
```

### The homework
The homework is just any old python code you would give to the students. For instance:
```python
# autolab_example_py_upload/instructor/cs102_autolab/homework1.py
def reverse_list(mylist): #!f 
    """
    Given a list 'mylist' returns a list consisting of the same elements in reverse order. E.g.
    reverse_list([1,2,3]) should return [3,2,1] (as a list).
    """
    return list(reversed(mylist))

def add(a,b): #!f
    """ Given two numbers `a` and `b` this function should simply return their sum:
    > add(a,b) = a+b """
    return a+b*2

if __name__ == "__main__": # Example usage:
    print(f"Your result of 2 + 2 = {add(2,2)}")
    print(f"Reversing a small list", reverse_list([2,3,5,7])) 
```
### The test: 
The test consists of individual problems and a report-class. The tests themselves are just regular Unittest (we will see a slightly smarter idea in a moment). For instance:

```python
# example_simplest/instructor/cs101/report1.py
from cs101.homework1 import reverse_list, add 

class Week1(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2,2), 4)
        self.assertEqual(add(-100, 5), -95)

    def test_reverse(self):
        self.assertEqual(reverse_list([1,2,3]), [3,2,1]) 
```
A number of tests can be collected into a `Report`, which will allow us to assign points to the tests and use the more advanced features of the framework later. A complete, minimal example:
```python
# example_simplest/instructor/cs101/report1.py
import unittest 
from unitgrade import Report, evaluate_report_student
import cs101
from cs101.homework1 import reverse_list, add 

class Week1(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2,2), 4)
        self.assertEqual(add(-100, 5), -95)

    def test_reverse(self):
        self.assertEqual(reverse_list([1,2,3]), [3,2,1]) 

class Report1(Report):
    title = "CS 101 Report 1"
    questions = [(Week1, 10)]  # Include a single question for a total of 10 credits.
    pack_imports = [cs101]     # Include all .py files in this folder

if __name__ == "__main__":
    # from HtmlTestRunner import HTMLTestRunner
    import HtmlTestRunner
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='example_dir'))


    # evaluate_report_student(Report1()) 
```

### Deployment
The above is all you need if you simply want to use the framework as a self-check: Students can run the code and see how well they did. 
In order to begin using the framework for evaluation we need to create a bit more structure. We do that by deploying the report class as follows:
```python
# example_simplest/instructor/cs101/deploy.py
from cs101.report1 import Report1 
from unitgrade_private.hidden_create_files import setup_grade_file_report
from snipper import snip_dir

if __name__ == "__main__":
    setup_grade_file_report(Report1)  # Make the report1_grade.py report file

    # Deploy the files using snipper: https://gitlab.compute.dtu.dk/tuhe/snipper
    snip_dir("./", "../../students/cs101", exclude=['__pycache__', '*.token', 'deploy.py']) 
```
 - The first line creates the `report1_grade.py` script and any additional data files needed by the tests (none in this case)
 - The second line set up the students directory (remember, we have included the solutions!) and remove the students solutions. You can check the results in the students folder.

If you are curious, the grade script looks like this:
```python
'''WARNING: Modifying, decompiling or otherwise tampering with this script, it's data or the resulting .token file will be investigated as a cheating attempt.'''
import bz2, base64
exec(bz2.decompress(base64.b64decode('QlpoOTFBWSZTWY/Cr/0ANxB/gHb2RFR//////+//vv////5gQb3d9962+(etc. etc.)')))
```

### Using the framework as a student
After you run the deploy-script, the student directory will contain three files
```terminal
students/cs101/homework1.py      # Homework files without solutions (see for yourself)
students/cs101/report1.py        # Identical to the instructor-report
students/cs101/report1_grade.py  # Grade-script which runs the tests in report1.py and generates the .token-file. 
```
You can now upload the `student` directory to the students. The students can run their tests either by running `cs101/report1.py` in their IDE or by typing:
```
python -m cs101.report1
```
in the command line. This produces a detailed output of the test and the program is 100% compatible with a debugger. When the students are happy with their output they can run (using command line or IDE):
```
python -m cs101.report1_grade
```
This runs an identical set of tests and produces the file `Report1_handin_10_of_10.token` the students can upload to get credit. 
 - The `report1_grade.py` includes all tests and the main parts of the framework and is obfuscated by default. You can apply a much strong level of protection by using e.g. `pyarmor`.
 - The `.token` file includes the outcome of the tests, the time taken, and all python source code in the package. In other words, the file can be used for manual grading, for plagirism detection and for detecting tampering. 
 - You can easily use the framework to include output of functions. 
 - See below for how to validate the students results 


### Viewing the results using the dashboard
I recommend to monitor and run the tests from the IDE, as this allows you to use the debugger in conjunction with your tests. 
However, unitgrade comes with a dashboard that allows students to see the outcome of individual tests 
 and what is currently recorded in the `token`-file. To start the dashboard, they should simply run the command
```
unitgrade
```
from a directory that contains a test (the directory will be searched recursively for test files). 
 The command will start a small background service and open a webpage:

![The dashboard](https://gitlab.compute.dtu.dk/tuhe/unitgrade/-/raw/master/docs/dashboard.png)

Features supported in the current version:
 - Shows which files need to be edited to solve the problem
 - Collect hints given in the homework files and display them for the relevant tests
 - fully responsive -- the UI, including the terminal, will update while the test is running regardless of where you launch the test
 - Allows students to re-run tests from the UI
 - Shows current test status and results captured in `.token`-file
 - Tested on Windows/Linux 
 - Frontend is pure javascript and the backend only depends on python packages. 

The frontend is automatically enabled the moment your classes inherits from the `UTestCase`-class; no configuration files required, and there are no known bugs. 

Note the frontend is currently not provided in the pypi `unitgrade` package, but only through the gitlab repository (install using `git clone` and then `pip install -e ./`) -- it seems ready, but I want to test it on mac and a few more systems before publishing it. 

## How safe is Unitgrade?
There are three principal ways of cheating:
 - Break the framework and submit a `.token` file that 'lies' about the true number of points
 - 'Overfit' the tests by checking for specific inputs and hard-code the output
 - Plagiarism

The degree to which the above problems needs to be mitigated depends on the course, but there are easy ways to mitigate them, but to address the three ways of cheating I recommend the following:

 - Automatically re-run the students tests on your computer using Docker (see below) to automatically detect difference in their (claimed) outcome and the (actual) outcome
 - Include a few hidden tests. If the students tests pass, but hidden tests with minor input-argument variation fail, something is probably up
 - Use the build-in Moss plagiarism input to get a detailed plagiarism report (see below)

I think the most important things to keep in mind are the following: 
 - The `_grade.py`-script is self-contained (i.e. contains an independent copy of all tests)
 - The `_grade.py`-script and `.token` file is not in an easily editable format. 
 - The `.token` file will contain a copy of all the students source code, as well as any intermediary outputs returned by tests

This means that if a student begins to tamper with the framework, all the evidence of the tampering will be readily available, and any inconsistencies will be very difficult to explain away.
 Therefore, unlike for a report, you cannot submit code as a `.pdf` file, and you cannot afterwards claim you mistook the `Download` folder for the `Desktop` and accidentially uploaded your friends version of some of the code.

If this is not enough, you can consider using `pyarmor` on the `_grade.py` script to create a **very** difficult challenge for a prospective hacker.

## Example 2: The framework
One of the main advantages of `unitgrade` over web-based autograders it that tests are really easy to develop and maintain. To take advantage of this, we simply change the class the questions inherit from to `UTestCase` (this is still a `unittest.TestCase`) and we can make use of the chache system. As an example:

```python 
# example_framework/instructor/cs102/report2.py
from unitgrade import UTestCase, cache  



class Week1(UTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        a = 234

    def test_add(self):
        self.assertEqualC(add(2,2))
        self.assertEqualC(add(-100, 5))

    # def test_reverse(self):
    #     self.assertEqualC(reverse_list([1, 2, 3])) 
```
Note we have changed the test-function to `self.assertEqualC` (the `C` is for cache) and dropped the expected result. What `unitgrade` will do
is to evaluate the test *on the working version of the code*, compute the results of the test, 
 and allow them to be available to the user. All this happens in the `deploy.py` script from before.

### Nicer titles
Titles can be set either using python docstrings or programmatically. An example:
```python 
# example_framework/instructor/cs102/report2.py
# class Week1Titles(UTestCase): 
#     """ The same problem as before with nicer titles """
#     def test_add(self):
#         """ Test the addition method add(a,b) """
#         self.assertEqualC(add(2,2))
#         print("output generated by test")
#         self.assertEqualC(add(-100, 5))
#         # self.assertEqual(2,3, msg="This test automatically fails.")
#
#     def test_reverse(self):
#         ls = [1, 2, 3]
#         reverse = reverse_list(ls)
#         self.assertEqualC(reverse)
#         # Although the title is set after the test potentially fails, it will *always* show correctly for the student.
#         self.title = f"Checking if reverse_list({ls}) = {reverse}"  # Programmatically set the title 
```
When this is run, the titles are shown as follows:
```terminal
 _   _       _ _   _____               _      
| | | |     (_) | |  __ \             | |     
| | | |_ __  _| |_| |  \/_ __ __ _  __| | ___ 
| | | | '_ \| | __| | __| '__/ _` |/ _` |/ _ \
| |_| | | | | | |_| |_\ \ | | (_| | (_| |  __/
 \___/|_| |_|_|\__|\____/_|  \__,_|\__,_|\___| v0.1.27, started: 16/09/2022 14:30:15

CS 102 Report 2 
Question 1: Week1                                                                                                       
 * q1.1) test_add.................................................................................................FAILED
 * q1.2) test_reverse.............................................................................................FAILED
 * q1.3) test_output_capture........................................................................................PASS
======================================================================
FAIL: test_add (__main__.Week1)
test_add
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<string>", line 882, in _callTestMethod
  File "<string>", line 1699, in test_add
  File "<string>", line 987, in assertEqualC
  File "<string>", line 975, in wrap_assert
AssertionError: 4 != 'Key 0 not found in cache; framework files missing. Please run deploy()'

======================================================================
FAIL: test_reverse (__main__.Week1)
test_reverse
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<string>", line 882, in _callTestMethod
  File "<string>", line 1703, in test_reverse
  File "<string>", line 987, in assertEqualC
  File "<string>", line 975, in wrap_assert
AssertionError: [3, 2, 1] != 'Key 0 not found in cache; framework files missing. Please run deploy()'

 * q1)   Total..................................................................................................... 3/10
 
Question 2: The same problem as before with nicer titles                                                                
 * q2.1) Test the addition method add(a,b)........................................................................FAILED
 * q2.2) test_reverse.............................................................................................FAILED
======================================================================
FAIL: test_add (__main__.Week1Titles)
Test the addition method add(a,b)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<string>", line 882, in _callTestMethod
  File "<string>", line 1715, in test_add
  File "<string>", line 987, in assertEqualC
  File "<string>", line 975, in wrap_assert
AssertionError: 4 != 'Key 0 not found in cache; framework files missing. Please run deploy()'

======================================================================
FAIL: test_reverse (__main__.Week1Titles)
test_reverse
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<string>", line 882, in _callTestMethod
  File "<string>", line 1723, in test_reverse
  File "<string>", line 987, in assertEqualC
  File "<string>", line 975, in wrap_assert
AssertionError: [3, 2, 1] != 'Key 0 not found in cache; framework files missing. Please run deploy()'

 * q2)   Total...................................................................................................... 0/6
 
Total points at 14:30:15 (0 minutes, 0 seconds).....................................................................3/16

Including files in upload...
path.: _NamespacePath(['/home/tuhe/Documents/unitgrade_private/examples/example_framework/instructor/cs102', '/home/tuhe/Documents/unitgrade_private/examples/example_framework/instructor/cs102'])
 * cs102
> Testing token file integrity...
Done!
 
To get credit for your results, please upload the single unmodified file: 
> /home/tuhe/Documents/unitgrade_private/examples/example_framework/instructor/cs102/Report2_handin_3_of_16.token

```
What happens behind the scenes when we set `self.title` is that the result is pre-computed on the instructors machine and cached. This means the last test will display the correct result regardless of how `reverse_list` has been implemented by the student. The titles are also shown correctly when the method is run as a unittest. 

### Caching computations
The `@cache`-decorator offers a direct ways to compute the correct result on an instructors computer and submit it to the student. For instance:
```python
# example_framework/instructor/cs102/report2.py
# class Question2(UTestCase): 
#     @cache
#     def my_reversal(self, ls):
#         # The '@cache' decorator ensures the function is not run on the *students* computer
#         # Instead the code is run on the teachers computer and the result is passed on with the
#         # other pre-computed results -- i.e. this function will run regardless of how the student happens to have
#         # implemented reverse_list.
#         return reverse_list(ls)
#
#     def test_reverse_tricky(self):
#         ls = (2,4,8)
#         ls2 = self.my_reversal(tuple(ls))                   # This will always produce the right result, [8, 4, 2]
#         print("The correct answer is supposed to be", ls2)  # Show students the correct answer
#         self.assertEqualC(reverse_list(ls))                 # This will actually test the students code.
#         return "Buy world!"                                 # This value will be stored in the .token file  
```
The `@cache` decorator will make sure the output of the function is pre-computed when the test is set up, and that the function will 
simply return the correct result regardless of the function body. This is very helpful in a few situations:

 - if you have exercises that depend on each other, and you want students to have access to the expected result of older methods which they may not have implemented correctly. 
 - If you want to use functions the students write to set up appropriate tests without giving away the solution.
 - To simply print out the correct result so it is apparent to the student

Finally, notice how one of the tests has a return value. This will be automatically saved in the `.token` file (this is useful for open-ended questions or for security).

## Example 3: Hidden and secure tests
To use `unitgrade` as part of automatic grading, it is recommended you check the students output locally and use hidden tests. Fortunately, this is very easy.

Let's start with the hidden tests. As usual we write a complete report script (`report3_complete.py`), but this time we use the `@hide`-decorator to mark tests as hidden: 
```python
# example_docker/instructor/cs103/report3_complete.py
from unitgrade import UTestCase, Report  
from unitgrade.utils import hide
from unitgrade import evaluate_report_student
import cs103

class AutomaticPass(UTestCase):
    def test_automatic_pass(self):
        self.assertEqual(2, 2)  # For simplicity, this test will always pass

    @hide  # The @hide-decorator tells unitgrade_v1 to hide the test for students.
    def test_hidden_fail(self):
        self.assertEqual(2, 3)  # For simplicity, this test will always fail.

class Report3(Report):
    title = "CS 101 Report 3"
    questions = [(AutomaticPass, 10)]  # Include a single question for 10 credits.
    pack_imports = [cs103] 
```
For simplicity, non-hidden test will always pass, and the hidden test will always fail: This makes it easy to interpret the results in the following.

Next we need to create students report and grade scripts. This can done as follows:
```python
# example_docker/instructor/cs103/deploy.py
if __name__ == "__main__": 
    # Step 1: Deploy the students files and return the directory they were written to
    setup_grade_file_report(Report3)  # Create report3_complete_grade.py which tests everything

    fout, Report = remove_hidden_methods(Report3, outfile="report3.py")  # Create report3.py without @hide-methods
    setup_grade_file_report(Report)                                      # Create report3_grade.py for the students

    student_directory = "../../students/cs103"
    snip_dir("./", student_directory, exclude=['*.token', 'deploy.py', 'report3_complete*.py', '.*']) 
```
Just to check, let's have a quick look at the students report script `report3.py`:
```python
# example_docker/instructor/cs103/report3.py
from unitgrade import UTestCase, Report  
from unitgrade.utils import hide
from unitgrade import evaluate_report_student
import cs103

class AutomaticPass(UTestCase):
    def test_automatic_pass(self):
        self.assertEqual(2, 2)  # For simplicity, this test will always pass


class Report3(Report):
    title = "CS 101 Report 3"
    questions = [(AutomaticPass, 10)]  # Include a single question for 10 credits.
    pack_imports = [cs103] 
```
The grade script works as normal, and just to make the example self-contained, let's generate the students `.token`-file as follows:
```python
# example_docker/instructor/cs103/deploy.py
    os.system("cd ../../students && python -m cs103.report3_grade") 
    student_token_file = glob.glob(student_directory + "/*.token").pop()  
```
### Setting up and using Docker
We are going to run the students tests in a Docker virtual machine so that we avoid any underhanded stuff, and also because it makes sure we get the same result every time (i.e., we can pass the task on to TAs).
To do that, you first have to install Docker (easy), and then build a Docker image. We are going to use one of the pre-baked images from  https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/tree/master/docker_images, which simply consists of a lean Linux distribution with python 3.8 and whatever packages are found in `requirements.txt`. If you need more it is very easy to add. 
To download and build the Docker image simply run:
```python
# example_docker/instructor/cs103/deploy.py
    # Step 3: Compile the Docker image (obviously you should only do this once). 
    download_docker_images(destination="../docker")  # Download an up-to-date docker image from gitlab.
    Dockerfile = "../docker/unitgrade-docker/Dockerfile" # Location of just downloaded docker file
    compile_docker_image(Dockerfile, tag="unitgrade-docker") 
```
This takes about 2 minutes but only needs to be done once. If you are keeping track we have the following:
 - A grade script with all tests, `report3_complete_grade.py`, which we build when the file was deployed
 - A (student) `.token` file we simulated, but in general would have downloaded from DTU Learn
 - A Docker image with the right packages

Next we feed this into unitgrade:
```python
# example_docker/instructor/cs103/deploy.py
    # Step 4: Test the students code in the .token file and get the results-token-file:  
    token = docker_run_token_file(Dockerfile_location=Dockerfile,
                                  host_tmp_dir=os.path.dirname(Dockerfile) + "/home",
                                  student_token_file=student_token_file,
                                  instructor_grade_script="report3_complete_grade.py",
                                  tag="unitgrade-docker") 
```
Behind the scenes, this code does the following:
 - Load the docker image 
 - Create a tmp dir where the files in the student `.token` files will be placed
 - Put the `report3_complete_grade.py` script at the right location in the source tree (unitgrade can guess this)
 - Run `report3_complete_grade.py` and collect the resulting token file

Just to show it works we will load both `.token`-files and print the results:
```python
# example_docker/instructor/cs103/deploy.py
    # Load the two token files and compare their scores 
    checked_token, _ = load_token(token)
    results, _ = load_token(student_token_file)

    print("Student's score was:", results['total'])
    print("My independent evaluation of the students score was", checked_token['total']) 
```
The results (shown in a `(points_obtained, possible_points)` format) will be printed as: 
```terminal
Student's score was: (10, 10)
My independent evaluation of the students score was (5, 10)
```
As expected, the (failed) hidden tests reduces the total points obtained. It will be easy to check, for instance by calling the hidden tests
`def test_something_hidden` when the regular test, `test_something`, passes and the hidden test fails. 

# Moss plagiarism detection
You can easily apply Moss to the students token files.  First get moss from https://theory.stanford.edu/~aiken/moss/ and create two directories:
```terminal
whitelist/   # Whitelisted files. Code from these files are part of the handouts to students
submissions/ # Where you dump student submissions.
```
The whitelist directory is optional, and the submissions directory contains student submissions (one folder per student):
```terminal
/submissions/<student-id-1>/Report1_74_of_144.token
/submissions/<student-id-2>/Report1_130_of_144.token
...
```
The files in the whitelist/student directory can be either `.token` files (which are unpacked) or python files, and they may contain subdirectories: Everything will be unpacked and flattened. The simplest way to set it up is simply to download all files from DTU learn as a zip-file and unzip it somewhere.
When done just call moss as follows:
```python 
# example_moss/moss_example.py
from unitgrade_private.plagiarism.mossit import moss_it, get_id 

if __name__ == "__main__":
    # Extract the moss id ("12415...") from the perl script and test:
    id = get_id("../../../02465private/admin/moss.pl")
    moss_it(whitelist_dir="whitelist", submissions_dir="student_submissions", moss_id=id) 
```
This will generate a report. You can see the example including the report here: https://lab.compute.dtu.dk/tuhe/unitgrade_private/-/tree/master/examples/example_moss

# Smart hinting
To help students get started, unitgrade will collect hints to solve failed tests from across the codebase and display them. Consider the following homework where two problems depends on each other and the 
instructor has given a couple of hints: (example taken from `example_hints`): 
```python
# example_hints/instructor/cs106/homework1.py
def find_primes(n): #!f 
    """
    Return a list of all primes up to (and including) n
    Hints:
        * Remember to return a *list* (and not a tuple or numpy ndarray)
        * Remember to include n if n is a prime
        * The first few primes are 2, 3, 5, ...
    """
    primes = [p for p in range(2, n+1) if is_prime(n) ]
    return primes

def is_prime(n): #!f
    """
    Return true iff n is a prime
    Hints:
        * A number is a prime if it has no divisors
        * You can check if k divides n using the modulo-operator. I.e. n % k == True if k divides n.
    """
    for k in range(2, n):
        if k % n == 0:
            return False
    return True 
```
The report_file also contains a single hint:
```python
# example_hints/instructor/cs106/report1hints.py
class Week1(UTestCase): 
    def test_find_all_primes(self):
        """
        Hints:
            * Insert a breakpoint and check what your function find_primes(4) actually outputs
        """
        self.assertEqual(find_primes(4), [2, 3], msg="The list should only contain primes <= 4")

class Report1Hints(Report):
    title = "CS 106 Report 1"
    questions = [(Week1, 10)]
    pack_imports = [homework_hints]  
```

When students run this homework it will fail and display the hints from the two methods:
![alt text|small](https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/docs/hints.png)

What happens behind the scenes is that a code-coverage tool is run on the instructors computer
to determine which methods are actually used in solving a problem, and then the hint-texts of those methods are 
collected and displayed. This feature requires no external configuration; simply write `Hints:` in the source code. 

# CMU Autolab support (Experimental)
CMU Autolab is a mature, free and opensource web-based autograder developed at Carnegie Mellon University and used across the world. You can find more information here: https://autolabproject.com/. It offers all features you expect from an online autograder
 - Web-based submission of homework
 - Class-management
 - Build in TA feedback mechanism
 - Class monitoring/statistics 
 - Automatic integration with enrollment data (Autolab supports LDAP and Shibboleth) means Autolab can be `plugged in` to existing IT infrastructure (including DTUs)
 - CLI Tools

An important design choice behind CMU Autolab is the grading is entirely based on Makefiles and Docker VMs. I.e., if you can make your autograding scheme work as Makefile that runs code on a Docker image you specify it will work on Autolab. This makes it very easy to let third-party platforms work with an **unmodified** version of Autolab. The following contains all steps needed to compile a Unitgrade test to Autolab

### Step 1: Set up Autolab
Simply follow the guide here: https://docs.autolabproject.com/installation/overview/ to set up Autolab. I used the 'manual' installation, but it should also work with the Docker-compose installation.

### Step 2: Compile a unitgrade test to Autolab lab-assignment format
Autolab calls handins for `lab assignments`, and allow you to import them as `.tar`-files (see the Autolab documentation for more information).  We can build these automatically in a few lines as this example demonstrates. 
The code for the example can be found in `examples/autolab_example`. It consists of two steps. The first is that you need to build the Docker image for Autolab/Tango used for grading. This is exactly like our earlier example using Docker for Unitgrade, except the image contains a few additional autolab-specific things. You can find the image here: 
 - https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/tree/master/docker_images/docker_tango_python

Concretely, the following code will download and build the image (note this code must be run on the same machine that you have installed Autolab on)
```python
# autolab_example_py_upload/instructor/cs102_autolab/deploy_autolab.py
    # Step 1: Download and compile docker grading image. You only need to do this once.  
    download_docker_images("../docker") # Download docker images from gitlab (only do this once).
    dockerfile = f"../docker/docker_tango_python/Dockerfile"
    autograde_image = 'tango_python_tue2'  # Tag given to the image in case you have multiple images.
    compile_docker_image(Dockerfile=dockerfile, tag=autograde_image, no_cache=False)  # Compile docker image. 
```
Next, simply call the framework to compile any `_grade.py`-file into an Autolab-compatible `.tar` file that can be imported from the web interface. The script requires you to specify 
both the instructor-directory and the directory with the files the student have been handed out (i.e., the same file-system format we have seen earlier). 
```python
# autolab_example_py_upload/instructor/cs102_autolab/deploy_autolab.py
    # Step 2: Create the cs102.tar file from the grade scripts. 
    instructor_base = f"."
    student_base = f"../../students/cs102_autolab"

    from report2_test import Report2
    # INSTRUCTOR_GRADE_FILE =
    output_tar = new_deploy_assignment("cs105h",  # Autolab name of assignment (and name of .tar file)
                                   INSTRUCTOR_BASE=instructor_base,
                                   INSTRUCTOR_GRADE_FILE=f"{instructor_base}/report2_test_grade.py",
                                   STUDENT_BASE=student_base,
                                   STUDENT_GRADE_FILE=f"{instructor_base}/report2_test.py",
                                   autograde_image_tag=autograde_image,
                                   homework_file="homework1.py") 
```
This will produce a file `cs102.tar`. Whereas you needed to build the Docker image on the machine where you are running Autolab, you can build the lab assignments on any computer.
### Step 3: Upload the `.tar` lab-assignment file 
To install the `cs102.tar`-file, simply open your course in Autolab and click the `INSTALL ASSESSMENT` button. Click `Browse` and upload the `cs102.tar` file:
![alt text|small](https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/docs/images/autolab1.png)

You will immediately see the page for the assignment where you can begin to upload solutions! 
The solutions are (of course!) `.token` files, and they will be automatically unpacked and run on Autolab. 

To test it, press the big upload square and select the `.token` file for the second assignment found in `examples/example_framework/instructor/cs102/Report2_handin_18_of_18.token`. 
The file will now be automatically evaluated and the score registered as any other Autolab assignment:

![alt text|small](https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/docs/images/autolab2.png)

The students can choose to view both the console output or a nicer formatted overview of the individual problems:

![alt text|small](https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/docs/images/autolab4.png)

and TAs can choose to annotate the students code directly in Autolab -- we are here making use of the fact the code is automatically included in the top of the `.token`-file.

![alt text|small](https://gitlab.compute.dtu.dk/tuhe/unitgrade_private/-/raw/master/docs/images/autolab3.png)

# Citing
```bibtex
@online{unitgrade_devel,
	title={Unitgrade-devel (0.1.42): \texttt{pip install unitgrade-devel}},
	url={https://lab.compute.dtu.dk/tuhe/unitgrade_private},
	urldate = {2022-09-16}, 
	month={9},
	publisher={Technical University of Denmark (DTU)},
	author={Tue Herlau},
	year={2022},
}
```