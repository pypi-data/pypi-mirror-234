# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delphai_fastapi',
 'delphai_fastapi.companies',
 'delphai_fastapi.job_posts',
 'delphai_fastapi.news_articles',
 'delphai_fastapi.projects']

package_data = \
{'': ['*']}

install_requires = \
['fastapi-camelcase>=1,<2',
 'fastapi>=0,<1',
 'httpx>=0,<1',
 'pymongo>3',
 'python-jose>=3.3,<4.0']

setup_kwargs = {
    'name': 'delphai-fastapi',
    'version': '1.0.7',
    'description': 'Package for fastAPI models',
    'long_description': 'None',
    'author': 'Berinike Tech',
    'author_email': 'berinike@delphai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
