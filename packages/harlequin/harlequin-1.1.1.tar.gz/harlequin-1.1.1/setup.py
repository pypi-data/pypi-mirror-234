# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['harlequin', 'harlequin.components']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'duckdb>=0.8.0',
 'platformdirs>=3.10.0,<4.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'shandy-sqlfmt>=0.19.0',
 'textual-fastdatatable==0.1.3',
 'textual-textarea==0.7.3',
 'textual==0.38.1']

entry_points = \
{'console_scripts': ['harlequin = harlequin.cli:harlequin']}

setup_kwargs = {
    'name': 'harlequin',
    'version': '1.1.1',
    'description': 'The DuckDB IDE for Your Terminal.',
    'long_description': '# Harlequin\n\n[![PyPI](https://img.shields.io/pypi/v/harlequin)](https://pypi.org/project/harlequin/)\n[![Test](https://github.com/tconbeer/harlequin/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/tconbeer/harlequin/actions/workflows/test.yml)\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/harlequin)\n![Runs on Linux | MacOS | Windows](https://img.shields.io/badge/runs%20on-Linux%20%7C%20MacOS%20%7C%20Windows-blue)\n\nThe DuckDB IDE for Your Terminal.\n\n![Harlequin Demo Video](static/harlequin.gif)\n\n\n## Installing Harlequin\n\nAfter installing Python 3.8 or above, install Harlequin using `pip` or `pipx` with:\n\n```bash\npipx install harlequin\n```\n\n## Using Harlequin\n\nFrom any shell, to open one or more DuckDB database files:\n\n```bash\nharlequin "path/to/duck.db" "another_duck.db"\n```\n\nTo open an in-memory DuckDB session, run Harlequin with no arguments:\n\n```bash\nharlequin\n```\n\n## More info at [harlequin.sh](https://harlequin.sh)\n\nVisit [harlequin.sh](https://harlequin.sh) for an overview of features and full documentation.\n\n## Contributing\n\nThanks for your interest in Harlequin! Harlequin is primarily maintained by [Ted Conbeer](https://github.com/tconbeer), but he welcomes all contributions and is looking for additional maintainers!\n\n### Providing Feedback\n\nWe\'d love to hear from you! [Open an Issue](https://github.com/tconbeer/harlequin/issues/new) to request new features, report bugs, or say hello.\n\n### Setting up Your Dev Environment and Running Tests\n\n1. Install Poetry v1.2 or higher if you don\'t have it already. You may also need or want pyenv, make, and gcc.\n1. Fork this repo, and then clone the fork into a directory (let\'s call it `harlequin`), then `cd harlequin`.\n1. Use `poetry install --sync` to install the project (editable) and its dependencies (including all test and dev dependencies) into a new virtual env.\n1. Use `poetry shell` to spawn a subshell.\n1. Type `make` to run all tests and linters, or run `pytest`, `black .`, `ruff . --fix`, and `mypy` individually.\n\n### Opening PRs\n\n1. PRs should be motivated by an open issue. If there isn\'t already an issue describing the feature or bug, [open one](https://github.com/tconbeer/harlequin/issues/new). Do this before you write code, so you don\'t waste time on something that won\'t get merged.\n2. Ideally new features and bug fixes would be tested, to prevent future regressions. Textual provides a test harness that we use to test features of Harlequin. You can find some examples in the `tests` directory of this project. Please include a test in your PR, but if you can\'t figure it out, open a PR to ask for help.\n2. Open a PR from your fork to the `main` branch of `tconbeer/harlequin`. In the PR description, link to the open issue, and then write a few sentences about **why** you wrote the code you did: explain your design, etc.\n3. Ted may ask you to make changes, or he may make them for you. Don\'t take this the wrong way -- he values your contributions, but he knows this isn\'t your job, either, so if it\'s faster for him, he may push a commit to your branch or create a new branch from your commits.\n',
    'author': 'Ted Conbeer',
    'author_email': 'tconbeer@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://harlequin.sh',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
