# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cornflakes',
 'cornflakes.builder',
 'cornflakes.cli',
 'cornflakes.common',
 'cornflakes.decorator',
 'cornflakes.decorator.click',
 'cornflakes.decorator.click.commands',
 'cornflakes.decorator.click.helper',
 'cornflakes.decorator.click.options',
 'cornflakes.decorator.click.rich',
 'cornflakes.decorator.dataclasses',
 'cornflakes.decorator.dataclasses._config',
 'cornflakes.decorator.dataclasses.validator',
 'cornflakes.decorator.datalite',
 'cornflakes.logging',
 'cornflakes.parser']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0',
 'click>=8.1.3,<9.0.0',
 'rich-rst>=1.1.7,<2.0.0',
 'rich==13.5.2',
 'toml>=0.10.2,<0.11.0',
 'typeguard>=4.1.3,<5.0.0',
 'typing-extensions>=4.7.1,<5.0.0',
 'validators>=0.20,<0.23']

entry_points = \
{'console_scripts': ['cornflakes = cornflakes.__main__:main']}

setup_kwargs = {
    'name': 'cornflakes',
    'version': '3.3.26',
    'description': 'Create generic any easy way to manage Configs for your project',
    'long_description': '.. image:: https://github.com/semmjon/cornflakes/blob/main/assets/cornflakes.png?raw=true\n   :height: 400 px\n   :width: 400 px\n   :alt: cornflakes logo\n   :align: center\n\n==========\n\n|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/cornflakes.svg\n   :target: https://pypi.org/project/cornflakes/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/cornflakes\n   :target: https://pypi.org/project/cornflakes\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/semmjon/cornflakes\n   :target: https://opensource.org/licenses/Apache2.0\n   :alt: License\n.. |Read the Docs| image:: https://github.com/sgeist-ionos/cornflakes/actions/workflows/publish_docs.yml/badge.svg\n   :target: https://cornflakes.readthedocs.io\n   :alt: Read the documentation at https://cornflakes.readthedocs.io\n.. |Build| image:: https://github.com/sgeist-ionos/cornflakes/actions/workflows/build_package.yml/badge.svg\n   :target: https://github.com/sgeist-ionos/cornflakes/actions/workflows/build_package.yml\n   :alt: Build Package Status\n.. |Tests| image:: https://github.com/sgeist-ionos/cornflakes/actions/workflows/run_tests.yml/badge.svg\n   :target: https://github.com/sgeist-ionos/cornflakes/actions/workflows/run_tests.yml\n   :alt: Run Tests Status\n.. |Codecov| image:: https://codecov.io/gh/sgeist-ionos/cornflakes/graph/badge.svg?token=FY72EIXI82\n   :target: https://codecov.io/gh/sgeist-ionos/cornflakes\n   :alt: Codecov\n.. |Pre-Commit-CI| image:: https://results.pre-commit.ci/badge/github/sgeist-ionos/cornflakes/main.svg\n   :target: https://results.pre-commit.ci/latest/github/sgeist-ionos/cornflakes/main\n   :alt: pre-commit.ci status\n\n.. code::\n\n   pip install cornflakes\n\n.. code::\n\n    pip install git+https://github.com/semmjon/cornflakes\n\n.. warning::\n    Please be careful when using this Python module. Currently, it is only developed / tested by me, which is why it has a high update / change rate. I\'m actually trying to be compatible with implementations, but I can\'t guarantee this at the moment. The module is currently still in a beta state and is not recommended for productive use.\n\n    In the near future I plan to revise the documentation / examples and write an introductory blog article, as I find implemented features and planned ideas to be quite cool and useful (and don\'t see them in any other package or find them to be quite user-friendly).\n\nInformation\n-----------\n\nThe Python module "cornflakes" was started as a hobby project and offers an alternative to Pydantic for managing configurations and data structures. It allows creating generic and easy to manage configurations for your project. Unlike Pydantic, which is based on inheritance, "cornflakes" uses a decorator (similar to dataclass) to map data structures.\n\nIn addition to a dataclass decorator with additional functionality, there is also a config decorator. This makes it possible to read the dataclass from configuration files. This can be very useful if you want to save your application configurations to a file.\n\nThe module also has a click wrapper that simplifies the implementation of command line applications. By integrating the Rich module, the application is additionally equipped with colors and other functions.\n\nThere are other useful methods in the base of the module that are generally useful for Python development. These can help you develop your projects faster and more efficiently.\n\nShort Term RoadMap\n~~~~~~~~~~~~~~~~~~~\n\n- Add autocompletion support for click CLI (automatically)\n- Enrich json methods\n\nDevelopment\n-----------\n\nPrerequisites\n~~~~~~~~~~~~~\n\n-  A compiler with C++17 support\n-  Pip 10+ or CMake >= 3.4 (or 3.8+ on Windows, which was the first version to support VS 2015)\n-  Python 3.8+\n-  gh (optional) GitHub\'s official command line tool\n-  doxygen\n-  cppcheck\n-  clang-tools-extra or clang-tidy\n-  ...\n\nCommands\n~~~~~~~~~~~~\n\nJust clone this repository and pip install. Note the ``--recursive``\noption which is needed for the pybind11 submodule:\n\n.. code::\n\n   git clone --recursive https://gitlab.blubblub.tech/sgeist/cornflakes.git\n\nInstall the package using makefiles:\n\n.. code::\n\n   make install\n\nBuild dist using makefiles:\n\n.. code::\n\n   make dist\n\nRun tests (pytest) using makefiles:\n\n.. code::\n\n   make test\n\n\nRun all tests using makefiles:\n\n.. code::\n\n   make test-all\n\nRun lint using makefiles:\n\n.. code::\n\n   make lint\n\nCreate dev venv:\n\n.. code::\n\n   python -m venv .venv\n   source .venv/bin/activate\n   pip install ninja pre-commit poetry\n\nInstall pre-commit:\n\n.. code::\n\n   pre-commit install\n\nUpdate pre-commit:\n\n.. code::\n\n   pre-commit update -a\n\nRun pre-commit:\n\n.. code::\n\n   pre-commit run -a\n',
    'author': 'Semjon Geist',
    'author_email': 'semjon.geist@ionos.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sgeist/cornflakes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
