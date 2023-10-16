# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.perseus',
 'majormode.perseus.constant',
 'majormode.perseus.model',
 'majormode.perseus.utils']

package_data = \
{'': ['*']}

install_requires = \
['exifread>=3.0.0,<4.0.0',
 'jsonpickle>=3.0.1,<4.0.0',
 'pillow>=10.0,<11.0',
 'pipfile>=0.0.2,<0.0.3',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2023.3,<2024.0',
 'six>=1.16.0,<2.0.0',
 'unidecode>=1.3.6,<2.0.0']

setup_kwargs = {
    'name': 'perseus-core-library',
    'version': '1.19.8',
    'description': 'Perseus Core Python library',
    'long_description': '# Perseus: Core Python Library\n\nPerseus Core Python Library is a repository of reusable Python components to be shared with Python projects integrating Perseus RESTful API server framework.\n\nThese components have minimal dependencies on other libraries, so that they can be deployed easily.  In addition, these components will keep their interfaces as stable as possible, so that other Python projects can integrate these components without having to worry about changes in the future.\n\n\nTo install the Perseus Core Python Library, enter the follow command line:\n\n```bash\n$ pip install perseus-core-library\n```\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/perseus-core-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
