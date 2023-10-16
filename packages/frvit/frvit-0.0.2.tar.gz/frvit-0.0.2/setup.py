# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frvit']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'frvit',
    'version': '0.0.2',
    'description': 'frvit - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Vision Transformers for Facial Recognition\nAn attempt to create the most accurate, reliable, and general vision transformers for facial recognition at scale.\n\n## Installation\n`pip install frvit`\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/frvit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
