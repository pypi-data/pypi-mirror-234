# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bovine_tool']

package_data = \
{'': ['*']}

install_requires = \
['bovine-store>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'bovine-tool',
    'version': '0.5.0',
    'description': 'Basic tools to administrate a bovine herd',
    'long_description': '# bovine_tool\n\nbovine_tool provides a CLI interface to manage bovine.\n\n## Configuration\n\nThe default database connection is "sqlite://bovine.sqlite3". This can be overwridden with the environment variable "BOVINE_DB_URL".\n\n## Quick start\n\nTo register a new user with a FediVerse handle use\n\n```bash\npython -m bovine_tool.register fediverse_handle [--domain DOMAIN]\n```\n\nthe domain must be specified. This creates the account `acct:fediverse_handle@DOMAIN`.\n\n## Managing users\n\n```bash\npython -m bovine_tool.manage bovine_name\n```\n\ndisplays the user.\n\nTo add a did key for [the Moo Client Registration Flow](https://blog.mymath.rocks/2023-03-25/BIN2_Moo_Client_Registration_Flow) with a BovineClient use\n\n```bash\npython -m bovine_tool.manage bovine_name --did_key key_name did_key\n```\n\nFurthermore, using `--properties` the properties can be over written.\n\n## Cleaning the database\n\n```bash\npython -m bovine_tool.cleanup\n```\n\nto delete all remote objects older than 3 days. This should be expanded to make the variables configurable and delete a bunch of other stuff, e.g.\n\n- remove inbox, outbox entries older than 14 days\n- have a "timeline" of outbox entries to display on a public profile\n- remove all local entries not in inbox, outbox, or timeline\n- remove deleted items older than 1 month\n- make time frames configurable\n',
    'author': 'Helge',
    'author_email': 'helge.krueger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/bovine/bovine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
