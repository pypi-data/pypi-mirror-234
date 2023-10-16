# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quasar']

package_data = \
{'': ['*']}

install_requires = \
['accelerate',
 'bitsandbytes',
 'datasets',
 'deepspeed',
 'einops',
 'evaluate',
 'matplotlib',
 'numpy',
 'pandas',
 'peft',
 'protobuf',
 'scikit-learn',
 'sentencepiece',
 'torch',
 'tqdm',
 'transformers',
 'trl',
 'wandb']

setup_kwargs = {
    'name': 'quasarx',
    'version': '0.0.2',
    'description': 'quasar - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Quasar\nQuasar: Mistral, mastering mathematical reasoning.\n![Quasar](/quasar.jpeg)\n\n## Features:\n- Mistral7b finetuned on high quality tokens for stellar mathematical reasoning.\n- Mistral7b extended to 16k seq and soon 32k and then 65k!\n- High Quality reasoning for all reasoning intensive tasks.\n\n## Architecture\n\n\n## Install\n\n## Usage\n\n## License\nMIT',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/quasar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
