# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqgraf']

package_data = \
{'': ['*']}

install_requires = \
['requests', 'scikit-build', 'smpl_io']

setup_kwargs = {
    'name': 'pyqgraf',
    'version': '0.0.13',
    'description': 'PyQgraf is a Python wrapper for Qgraf, a Feynman diagram generator.',
    'long_description': '# pyqgraf\nSimplified plotting and fitting in python.\n\n[![PyPI version][pypi image]][pypi link] [![PyPI version][pypi versions]][pypi link] ![downloads](https://img.shields.io/pypi/dm/pyqgraf.svg)\n\n [![test][a t image]][a t link] [![Coverage Status][c t i]][c t l] [![Documentation][rtd t i]][rtd t l]\n\n## Documentation\n\n## Requirements\n\n * build-essential (or just gfortran)\n * ninja-build (maybe cmake works too) \n\n## Versions\n\n### Stable\n\n```sh\npip install pyqgraf\n```\n\nOptional: --user or --upgrade\n\n### Dev\n\n```sh\npip install --index-url https://test.pypi.org/simple/ pyqgraf\n```\n\n[doc stable]: https://apn-pucky.github.io/pyqgraf/index.html\n[doc test]: https://apn-pucky.github.io/pyqgraf/test/index.html\n\n[pypi image]: https://badge.fury.io/py/pyqgraf.svg\n[pypi link]: https://pypi.org/project/pyqgraf/\n[pypi versions]: https://img.shields.io/pypi/pyversions/pyqgraf.svg\n\n[a s image]: https://github.com/APN-Pucky/pyqgraf/actions/workflows/stable.yml/badge.svg\n[a s link]: https://github.com/APN-Pucky/pyqgraf/actions/workflows/stable.yml\n[a t link]: https://github.com/APN-Pucky/pyqgraf/actions/workflows/test.yml\n[a t image]: https://github.com/APN-Pucky/pyqgraf/actions/workflows/test.yml/badge.svg\n\n[cc s q i]: https://app.codacy.com/project/badge/Grade/38630d0063814027bd4d0ffaa73790a2?branch=stable\n[cc s q l]: https://www.codacy.com/gh/APN-Pucky/pyqgraf/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/smpl&amp;utm_campaign=Badge_Grade?branch=stable\n[cc s c i]: https://app.codacy.com/project/badge/Coverage/38630d0063814027bd4d0ffaa73790a2?branch=stable\n[cc s c l]: https://www.codacy.com/gh/APN-Pucky/pyqgraf/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/smpl&utm_campaign=Badge_Coverage?branch=stable\n\n[cc q i]: https://app.codacy.com/project/badge/Grade/38630d0063814027bd4d0ffaa73790a2\n[cc q l]: https://www.codacy.com/gh/APN-Pucky/pyqgraf/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=APN-Pucky/smpl&amp;utm_campaign=Badge_Grade\n[cc c i]: https://app.codacy.com/project/badge/Coverage/38630d0063814027bd4d0ffaa73790a2\n[cc c l]: https://www.codacy.com/gh/APN-Pucky/pyqgraf/dashboard?utm_source=github.com&utm_medium=referral&utm_content=APN-Pucky/smpl&utm_campaign=Badge_Coverage\n\n[c s i]: https://coveralls.io/repos/github/APN-Pucky/pyqgraf/badge.svg?branch=stable\n[c s l]: https://coveralls.io/github/APN-Pucky/pyqgraf?branch=stable\n[c t l]: https://coveralls.io/github/APN-Pucky/pyqgraf?branch=master\n[c t i]: https://coveralls.io/repos/github/APN-Pucky/pyqgraf/badge.svg?branch=master\n\n[rtd s i]: https://readthedocs.org/projects/pyqgraf/badge/?version=stable\n[rtd s l]: https://pyqgraf.readthedocs.io/en/stable/?badge=stable\n[rtd t i]: https://readthedocs.org/projects/pyqgraf/badge/?version=latest\n[rtd t l]: https://pyqgraf.readthedocs.io/en/latest/?badge=latest\n',
    'author': 'Alexander Puck Neuwirth',
    'author_email': 'alexander@neuwirth-informatik.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/APN-Pucky/pyqgraf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
