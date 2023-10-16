# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['progen']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'progen-torch',
    'version': '0.0.3',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Progen\nImplementation of Progen in Pytorch, from the paper "ProGen: Language Modeling for Protein Generation"\n\nGPT for proteins sequences\n\n[Paper Link](https://arxiv.org/pdf/2004.03497.pdf)\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n# Install\n`pip install progen-torch`\n\n# Usage\n```python\nfrom progen_torch import ProGen\n\nx = torch.randint(0, 100, (1, 1024))\nmodel = ProGenBase(num_tokens=100, dim=512, seq_len=1024, depth=6)\noutputs = model(x)\nprint(outputs)\n\n```\n\n# Architecture\n\n# Todo\n\n\n# License\nMIT\n\n# Citations\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Progen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
