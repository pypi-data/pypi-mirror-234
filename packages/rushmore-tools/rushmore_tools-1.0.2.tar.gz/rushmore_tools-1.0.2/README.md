
THREE60 Energy `rushmore-tools`
================================
[![release](https://github.com/THREE60-Energy/rushmore-tools/actions/workflows/release.yml/badge.svg)](https://github.com/THREE60-Energy/rushmore-tools/actions/workflows/release.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

The `rushmore-tools` package is a lightweight wrapper for accessing Rushmore Reviews, a prominent player in benchmarking data collection for upstream oil & gas activities.

Overview
================================
The collection contains utilities:
- RushmoreExtractor

## Usage

Simple usage. E.g. to download all Rushmore Drilling Performance Review data available to your API key, simply:

```
from rushmore_tools import RushmoreExtractor

report = RushmoreExtractor($api_key).report("DPR")
resp = report.get()
```


## Development environment

We use [poetry](https://python-poetry.org) to manage dependencies and to administrate virtual environments. To develop
`rushmore-tools`, follow the following steps to set up your local environment:

 1. [Install poetry](https://python-poetry.org/docs/#installation) if you haven't already.

 2. Clone repository:
    ```
    $ git clone git@github.com:THREE60-Energy/rushmore-tools.git
    ```
 3. Move into the newly created local repository:
    ```
    $ cd rushmore-tools
    ```
 4. Create virtual environment and install dependencies:
    ```
    $ poetry install
    ```

### Code requirements

All code must pass [black](https://github.com/ambv/black) and [isort](https://github.com/timothycrosley/isort) style
checks to be merged. It is recommended to install pre-commit hooks to ensure this locally before commiting code:

```
$ poetry run pre-commit install
```

Each public method, class and module should have docstrings. Docstrings are written in the [Google
style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
