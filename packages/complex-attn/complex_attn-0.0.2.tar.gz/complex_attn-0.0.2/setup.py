# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ct']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'complex-attn',
    'version': '0.0.2',
    'description': 'ct - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Complex Transformer\nThe open source implementation of the attention and transformer from "Building Blocks for a Complex-Valued Transformer Architecture" where they propose an an attention mechanism for complex valued signals or images such as MRI and remote sensing.\n\nThey present:\n- complex valued scaled dot product attention\n- complex valued layer normalization\n- results show improved robustness to overfitting while maintaing performance wbhen compared to real valued transformer\n\n## Install\n`pip install ct`\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/ct',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
