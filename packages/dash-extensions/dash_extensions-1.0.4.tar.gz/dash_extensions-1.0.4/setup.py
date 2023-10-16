# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_extensions']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Caching==2.0.2',
 'dash>=2.9.3',
 'dataclass-wizard>=0.22.2,<0.23.0',
 'jsbeautifier>=1.14.3,<2.0.0',
 'more-itertools>=9.0.0,<10.0.0']

extras_require = \
{'mantine': ['dash-mantine-components>=0.11.1,<0.12.0']}

setup_kwargs = {
    'name': 'dash-extensions',
    'version': '1.0.4',
    'description': 'Extensions for Plotly Dash.',
    'long_description': '[![PyPI Latest Release](https://img.shields.io/pypi/v/dash-extensions.svg)](https://pypi.org/project/dash-extensions/)\n[![codecov](https://img.shields.io/codecov/c/github/thedirtyfew/dash-extensions?logo=codecov)](https://codecov.io/gh/thedirtyfew/dash-extensions)\n[![Testing](https://github.com/thedirtyfew/dash-extensions/actions/workflows/python-test.yml/badge.svg)](https://github.com/thedirtyfew/dash-extensions/actions/workflows/python-test.yml)\n[![CodeQL](https://github.com/thedirtyfew/dash-extensions/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/thedirtyfew/dash-extensions/actions/workflows/codeql-analysis.yml)\n\nThe `dash-extensions` package is a collection of utility functions, syntax extensions, and Dash components that aim to improve the Dash development experience. It can be divided in four main pillars,\n\n* The `enrich` module, which contains various enriched versions of Dash components\n* A number of custom components, e.g. the `Websocket` component, which enables real-time communication and push notifications\n* The `javascript` module, which contains functionality to ease the interplay between Dash and JavaScript\n* The `snippets` module, which contains a collection of utility functions (documentation limited to source code comments)\n\nThe `enrich` module enables a number of _transforms_ that add functionality and/or syntactic sugar to Dash. Examples include\n\n* Making it possible to avoid invoking a callback _if it is already running_ via the `BlockingCallbackTransform`\n* Enabling logging from within Dash callbacks via the `LogTransform`\n* Improving app performance via the `ServersideOutputTransform`\n\nto name a few. To enable interactivity, the documentation has been moved to a [separate page](http://dash-extensions.com).\n\nNB: The 1.0.0 version introduces a number of breaking changes, see documentation for details.\n\n## Donation\n\n[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=Z9RXT5HVPK3B8&currency_code=DKK&source=url)\n',
    'author': 'emher',
    'author_email': 'emil.h.eriksen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://dash-extensions.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
