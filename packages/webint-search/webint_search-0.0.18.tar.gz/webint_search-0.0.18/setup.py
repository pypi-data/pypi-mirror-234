# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_search', 'webint_search.templates']

package_data = \
{'': ['*']}

install_requires = \
['eng-to-ipa>=0.0.2,<0.0.3',
 'nltk>=3.8.1,<4.0.0',
 'pronouncing>=0.2.0,<0.3.0',
 'restrictedpython>=6.2,<7.0',
 'typesense>=0.15.0,<0.16.0',
 'webint-owner>=0.0,<0.1',
 'webint>=0.0',
 'wn>=0.9.4,<0.10.0',
 'youtube-search>=2.1.2,<3.0.0']

entry_points = \
{'webapps': ['search = webint_search:app']}

setup_kwargs = {
    'name': 'webint-search',
    'version': '0.0.18',
    'description': 'search the web from your website',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
