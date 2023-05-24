# IAI Project Template

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.github.com/NoB0/8446f35dc373966dc971fb9237483cce/raw/coverage.pkg-api.main.json)

This repository serves as a template for software projects.

# Testing and GitHub actions

Using `pre-commit` hooks, `flake8`, `black`, `mypy`, `docformatter`, and `pytest` are locally run on every commit. For more details on how to use `pre-commit` hooks see [here](https://github.com/iai-group/guidelines/tree/main/python#install-pre-commit-hooks).

Similarly, Github actions are used to run `flake8`, `black` and `pytest` on every push and pull request. The `pytest` results are sent to [CodeCov](https://about.codecov.io/) using their API for to get test coverage analysis. Details on Github actions are [here](https://github.com/iai-group/guidelines/blob/main/github/Actions.md).

