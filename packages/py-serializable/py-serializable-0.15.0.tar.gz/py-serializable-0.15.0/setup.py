# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serializable']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'py-serializable',
    'version': '0.15.0',
    'description': 'Library for serializing and deserializing Python Objects to and from JSON and XML.',
    'long_description': '# py-serializable\n\n[![shield_gh-workflow-test]][link_gh-workflow-test]\n[![shield_rtfd]][link_rtfd]\n[![shield_pypi-version]][link_pypi]\n[![shield_license]][license_file]\n[![shield_twitter-follow]][link_twitter]\n\n----\n\nThis Pythonic library provides a framework for serializing/deserializing Python classes to and from JSON and XML.\n\nIt relies upon the use of \n[Python Properties](https://docs.python.org/3/library/functions.html?highlight=property#property) in your Python\nclasses.\n\nRead the full [documentation][link_rtfd] for more details.\n\n## Installation\n\nInstall this from [PyPi.org][link_pypi] using your preferred Python package manager.\n\nExample using `pip`:\n\n```shell\npip install py-serializable\n```\n\nExample using `poetry`:\n\n```shell\npoetry add py-serializable\n```\n\n## Usage\n\nSee the full [documentation][link_rtfd] or our [unit tests][link_unit_tests] for usage and details.\n\n## Python Support\n\nWe endeavour to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).\nHowever, some features may not be possible/present in older Python versions due to their lack of support.\n\n## Contributing\n\nFeel free to open issues, bugreports or pull requests.  \nSee the [CONTRIBUTING][contributing_file] file for details.\n\n## Copyright & License\n\n`py-serializable` is Copyright (c) Paul Horton 2022. All Rights Reserved.\n\nPermission to modify and redistribute is granted under the terms of the Apache 2.0 license.  \nSee the [LICENSE][license_file] file for the full license.\n\n[license_file]: https://github.com/madpah/serializable/blob/main/LICENSE\n[contributing_file]: https://github.com/madpah/serializable/blob/main/CONTRIBUTING.md\n[link_rtfd]: https://py-serializable.readthedocs.io/\n\n[shield_gh-workflow-test]: https://img.shields.io/github/actions/workflow/status/madpah/serializable/python.yml?branch=main "build"\n[shield_rtfd]: https://img.shields.io/readthedocs/py-serializable?logo=readthedocs&logoColor=white\n[shield_pypi-version]: https://img.shields.io/pypi/v/py-serializable?logo=Python&logoColor=white&label=PyPI "PyPI"\n[shield_license]: https://img.shields.io/github/license/madpah/serializable?logo=open%20source%20initiative&logoColor=white "license"\n[shield_twitter-follow]: https://img.shields.io/badge/Twitter-follow-blue?logo=Twitter&logoColor=white "twitter follow"\n[link_gh-workflow-test]: https://github.com/madpah/serializable/actions/workflows/python.yml?query=branch%3Amain\n[link_pypi]: https://pypi.org/project/py-serializable/\n[link_twitter]: https://twitter.com/madpah\n[link_unit_tests]: https://github.com/madpah/serializable/blob/main/tests\n',
    'author': 'Paul Horton',
    'author_email': 'paul.horton@owasp.org',
    'maintainer': 'Paul Horton',
    'maintainer_email': 'paul.horton@owasp.org',
    'url': 'https://github.com/madpah/serializable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
