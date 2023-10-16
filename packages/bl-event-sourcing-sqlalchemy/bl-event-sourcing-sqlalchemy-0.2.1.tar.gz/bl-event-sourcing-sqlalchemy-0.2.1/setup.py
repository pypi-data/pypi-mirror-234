# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bl_event_sourcing_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.26,<2.0.0', 'bl-event-sourcing==0.2.2']

setup_kwargs = {
    'name': 'bl-event-sourcing-sqlalchemy',
    'version': '0.2.1',
    'description': 'Event sourcing implemented with SQLAlchemy',
    'long_description': '# Bioneland Event Sourcing implemented with SQLAlchemy \n\n**Deprecated!** Please use [blessql](https://git.easter-eggs.org/bioneland/blessql) instead.\n',
    'author': 'Tanguy Le Carrour',
    'author_email': 'tanguy@bioneland.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.easter-eggs.org/bioneland/bl-event-sourcing-sqlalchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
