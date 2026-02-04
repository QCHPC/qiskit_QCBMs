# Test environment



This repository's tests are organized using `tox`, a command-line, continuous integration (CI) front end for Python projects.

The Python package `tox` can be installed in a local development environment by running `pip install tox`.

The `tox.ini` configuration file indicates where to find the tests, and where to find files to be linted by the tool, `flake8`.


To run \_all\_ test environments, run `tox` without any arguments, from the main directory of the repo:

```sh

$ tox

```

To just run the tests for one environment, say, Python version 3.10:

```sh

$ tox run -e py310

```

To just lint Python files with `flake8`, 

```sh

$ tox run -e flake8

```
