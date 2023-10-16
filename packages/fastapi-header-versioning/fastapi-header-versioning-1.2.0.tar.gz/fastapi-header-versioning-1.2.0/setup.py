# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_header_versioning']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.96.1', 'pydantic>=1.10.0,<2.0.0', 'typing-extensions']

setup_kwargs = {
    'name': 'fastapi-header-versioning',
    'version': '1.2.0',
    'description': 'API versioning based on header-provided data for FastAPI.',
    'long_description': '# fastapi-header-versioning\nHeader versioning for FastAPI using arbitrary header.\n',
    'author': 'Timofey Petrenko',
    'author_email': 'timofey.petrenko93@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tikon93/fastapi-header-versioning',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
