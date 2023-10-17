# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ntdsdotsqlite']

package_data = \
{'': ['*']}

install_requires = \
['dissect[ese]>=3.5,<4.0',
 'impacket>=0.10,<0.11',
 'pycryptodomex>=3.18.0,<4.0.0',
 'tqdm>=4.65.0,<5.0.0']

entry_points = \
{'console_scripts': ['ntdsdotsqlite = ntdsdotsqlite.__main__:main']}

setup_kwargs = {
    'name': 'ntdsdotsqlite',
    'version': '1.1.7',
    'description': 'A small utility to get an SQLite  database from an NTDS.DIT file.',
    'long_description': '# NTDS.Sqlite\n\nThis software can be used either directly as a CLI utility or as a library to get an SQLite database from an NTDS.DIT one. Encrypted bits can be decrypted if the associated system hive is provided altogether.\n\n# Installation\n\n`python -m pip install ntdsdotsqlite`\n\n# Usage\n\n`ntdsdotsqlite NTDS.DIT --system SYSTEM -o NTDS.sqlite`\n\n```\nusage: NTDS.sqlite [-h] [--system SYSTEM] -o OUTFILE NTDS\n\nThis tool helps dumping NTDS.DIT file to an SQLite database\n\npositional arguments:\n  NTDS                  The NTDS.DIT file\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --system SYSTEM       The SYSTEM hive to decrypt hashes. If not provided, hashes will be encrypted inside the sqlite database.\n  -o OUTFILE, --outfile OUTFILE\n                        The sqlite database. Example : NTDS.sqlite\n```\n\n# SQL model\n\nThe SQL model is described in the `sql_model.md` file in this repository. Basicaly, not all objects are extracted (at all), but the following are retrieved as of today : domain object, user accounts, machine accounts, groups, organizational units and containers. I thought these would be the most useful. If you need more object classes to be extracted or additional attributes, feel free to open an issue or a pull request !\n\n# Performances\n\nPerformances can be a bit low for huge NTDS files. The whole NTDS is not stored in memory to prevent memory exhaustion when working on huge files (NTDS databases can grow to several gigabytes).\n',
    'author': 'Virgile Jarry',
    'author_email': 'virgile@mailbox.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/almandin/ntdsdotsqlite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
