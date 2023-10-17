# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncur']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.7.1', 'openpyxl>=3.1.2,<4.0.0', 'pandas>=2.1.1,<3.0.0']

setup_kwargs = {
    'name': 'asyncur',
    'version': '0.2.2',
    'description': 'Async functions to compare with anyio and asyncio, and toolkit to read/write excel with async/await.',
    'long_description': '# asyncur\n[![LatestVersionInPypi](https://img.shields.io/pypi/v/asyncur.svg?style=flat)](https://pypi.python.org/pypi/asyncur)\n[![GithubActionResult](https://github.com/waketzheng/asyncur/workflows/ci/badge.svg)](https://github.com/waketzheng/asyncur/actions?query=workflow:ci)\n[![Coverage Status](https://coveralls.io/repos/github/waketzheng/asyncur/badge.svg?branch=main)](https://coveralls.io/github/waketzheng/asyncur?branch=main)\n\nSome async functions that using anyio, and toolkit for excel read/write.\n\n## Requirements\n\nPython 3.11+\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install asyncur\n---> 100%\nSuccessfully installed asyncur\n```\nOr use poetry:\n```console\npoetry add asyncur\n```\n\n## Usage\n\n- Read Excel File\n```py\n>>> from asycur import load_xls\n>>> await load_xls(\'tests/demo.xlsx\')\n[{\'Column1\': \'row1-\\\\t%c\', \'Column2\\nMultiLines\': 0, \'Column 3\': 1, 4: \'\'}, {\'Column1\': \'r2c1\\n00\', \'Column2\\nMultiLines\': \'r2 c2\', \'Column 3\': 2, 4: \'\'}]\n```\n',
    'author': 'Waket Zheng',
    'author_email': 'waketzheng@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<3.13',
}


setup(**setup_kwargs)
