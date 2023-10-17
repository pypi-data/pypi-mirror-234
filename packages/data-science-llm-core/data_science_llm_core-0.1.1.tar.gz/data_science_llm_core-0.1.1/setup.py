# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['llm']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2.1,<3.0.0',
 'openai>=0.28.0,<0.29.0',
 'python-dotenv>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'data-science-llm-core',
    'version': '0.1.1',
    'description': '',
    'long_description': '# data-science-llm-core\nCommon functionalities as a package for Large Language Model applications\n',
    'author': 'Unsal Gokdag',
    'author_email': 'unsal.gokdag@forto.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
