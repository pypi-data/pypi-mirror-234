# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kosmosg']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'torchscale', 'zetascale']

setup_kwargs = {
    'name': 'kosmosg',
    'version': '0.0.3',
    'description': 'kosmosg - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Kosmos\nMy implementation of the model KosmosG from "KOSMOS-G: Generating Images in Context with Multimodal Large Language Models"\n\n\n\n## Installation\n\nYou can install the package using pip\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/KosmosG',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
