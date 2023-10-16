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
    'version': '0.0.4',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Progen\nImplementation of Progen in Pytorch, from the paper "ProGen: Language Modeling for Protein Generation"\n\nGPT for proteins sequences\n\n[Paper Link](https://arxiv.org/pdf/2004.03497.pdf)\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n# Install\n`pip install progen-torch`\n\n# Usage\n```python\nimport torch\nfrom progen.model import ProGen\n\nx = torch.randint(0, 100, (1, 1024))\nimport torch\nfrom progen.model import ProGen\n\nx = torch.randint(0, 100, (1, 1024))\n\n# Initialize the model with specific parameters\nmodel = ProGen(\n    num_tokens=100,  # The size of the vocabulary\n    dim=512,  # The dimension of the embeddings\n    seq_len=1024,  # The length of the sequences\n    depth=6,  # The number of layers in the model\n    window_size=256,  # The size of the window for local attention\n    global_mlp_depth=2,  # The depth of the MLP in the global attention mechanism\n    heads=8,  # The number of attention heads\n    dim_head=512,  # The dimension of each attention head\n    ff_mult=4,  # The multiplier for the feed-forward network\'s hidden layer size\n    ff_glu=True,  # Whether to use a GLU activation in the feed-forward network\n    attn_dim=None,  # The dimension of the attention mechanism (None means it defaults to `dim`)\n    clamp_gate=True,  # Whether to clamp the gate values in the GLU activation\n    shift_tokens=True,  # Whether to shift the tokens for the causal attention mechanism\n    dropout=0.1,  # The dropout rate\n)\n\n# Forward pass through the model\nlogits = model(x)\n\n# The output is the logits for each token in the vocabulary, for each position in the input sequences\n# Shape: (batch_size, sequence_length, num_tokens)\nprint(logits.shape)  # Should print: torch.Size([1, 1024, 100])\n\n\n```\n\n# Dataset Strategy\nHere is a table of the datasets used in the paper with metadata and source links:\n\n| Dataset | Description | Source |\n|-|-|-| \n| Uniparc | Contains protein sequences from various sources | https://www.uniprot.org/uniparc/ |\n| UniprotKB | Contains protein sequences and annotations | https://www.uniprot.org/uniprot/ |\n| SWISS-PROT | Curated protein sequence database | https://www.uniprot.org/swiss-prot/ |\n| TrEMBL | Computer-annotated protein sequences | https://www.uniprot.org/trembl/ |\n| Pfam | Database of protein families | https://pfam.xfam.org/ |\n| NCBI taxonomy | Taxonomic classification of organisms | https://www.ncbi.nlm.nih.gov/taxonomy |\n\nHere is a diagram showing the data preprocessing flow:\n\n```mermaid\ngraph TD\n    A[Uniparc] --> B[Filter and merge]\n    C[UniprotKB] --> B\n    D[SWISS-PROT] --> B \n    E[TrEMBL] --> B\n    F[Pfam] --> B\n    G[NCBI taxonomy] --> B\n    B --> H[Train/test split]\n    H --> I[Train set]\n    H --> J[ID test set] \n    H --> K[OOD test set]\n```\n\nThe Uniparc, UniprotKB, SWISS-PROT, TrEMBL, Pfam, and NCBI taxonomy datasets are filtered and merged in step B. The aggregated dataset is then split into training, in-distribution test, and out-of-distribution test sets in step H.\n\n# Architecture\n\n# Todo\n\n\n# License\nMIT\n\n# Citations\n\n',
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
