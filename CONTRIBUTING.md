# Guidance on how to contribute

Contributions to this code are welcome and appreciated.
Please adhere to our [Code of Conduct](./CODE_OF_CONDUCT.md) at all times.

> All contributions to this code will be released under the terms of the [LICENSE](./LICENSE) of this code. By submitting a pull request or filing a bug, issue, or feature request, you are agreeing to comply with this waiver of copyright interest. Details can be found in our [LICENSE](./LICENSE).

There are two primary ways to contribute:

1. Using the issue tracker
2. Changing the codebase


## Using the issue tracker

Use the issue tracker to suggest feature requests, report bugs, and ask questions. This is also a great way to connect with the developers of the project as well as others who are interested in this solution.

Use the issue tracker to find ways to contribute. Find a bug or a feature, mention in the issue that you will take on that effort, then follow the _Changing the codebase_ guidance below.


## Changing the codebase

Generally speaking, you should fork this repository, make changes in your own fork, and then submit a pull request.

## Setting up the development environment

Ensure that you have the minimum required version of Python installed.  See the `python_requires` line in the `./setup.py` file.  To set up your development environment, create a virtual environment, and then use the `pip` to install the requirements and the development requirements.  For example

    $ python3 -mvenv ~/venvs/virlutils-dev/
    $ source ~/venvs/virlutils-dev/bin/activate
    (virlutils-dev) $ pip install -r requirements.txt
    (virlutils-dev) $ pip install -r requirements_dev.txt

### Unit tests

All new code should have associated unit tests (if applicable) that validate implemented features and the presence or lack of defects.  Before you start making changes, check that all existing tests pass.  We recommend using a test-driven development (TDD) to making changes.  Add one or more new unit tests that demonstrate the bug or gap you're trying to fix.  Initially, the test should be failing because you haven't fixed the problem, yet.  Before you submit a pull request, ensure that your new test passes and that all existing tests still pass.

You can run the unit tests from the command line by running `python setup.py tests` from the root directory of the project.  That's currently equivalent to running `python -m unittest discover -v -s ./tests -p '*.py'` from the root directory of the project.

You can also generally configure a Python-aware IDE to run the tests.  For example, if you are using [VSCode](https://code.visualstudio.com/), click **Run > Command Palette > Python: Discover Tests** and chose *unittest*, *tests* folder, and `*.py` pattern.  You can verify the settings by searching your VSCode workspace settings for `Unittest`.  Ensure that the checkbox under **Python > Testing: Unittest Enabled** is checked and that the **Python > Testing: Unittest Args** are

    -v
    -s
    ./tests
    -p
    *.py

With those settings, navigate to **View > Testing** in VSCode.  The view should list all of the test methods discovered under the `tests` folder.  You may need to **Refresh Tests** first.  Because the tests use mock responses, you can run them without access to a CML server.

### Code Style

Additionally, the code should follow any stylistic and architectural guidelines prescribed by the project.  The project now uses [black](https://black.readthedocs.io/) to ensure consistent code formatting.  When you installed the requirements_dev.txt in your virtual environment, it installed the `black` command.  For each file that you are modifying, run `black ./virl/path/to/file.py` before you commit the file or submit a pull request.
