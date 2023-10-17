# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cross_attn', 'cross_attn.iters']

package_data = \
{'': ['*']}

install_requires = \
['torch']

setup_kwargs = {
    'name': 'cross-attn',
    'version': '0.0.5',
    'description': 'MultiModalCrossAttn - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# MultiModalCrossAttn\nThe open source implementation of the cross attention mechanism from the paper: "JOINTLY TRAINING LARGE AUTOREGRESSIVE MULTIMODAL MODELS"\n\n\n[Paper Link](https://arxiv.org/pdf/2309.15564.pdf)\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n\n\n# Install\n`pip install cross-attn`\n\n# Usage\n```python\nimport torch\nfrom cross_attn.main import MultiModalCrossAttention\n\n# Test the MultiModalCrossAttention module\ndim = 512  # For example\nnum_heads = 8\n\ncross_attn = MultiModalCrossAttention(dim, num_heads)\n\nHllm_sample = torch.randn(32, dim, dim)  # Batch size = 32, Sequence length = 10\nHimg_sample = torch.randn(32, dim, dim)\n\noutput = cross_attn(Hllm_sample, Himg_sample)\nprint(output)\n\nprint(output.shape)  # Expected: [32, 10, 512]\n\n```\n\n\n\n# License\nMIT\n\n# Citations\n```\n@misc{2309.15564,\nAuthor = {Emanuele Aiello and Lili Yu and Yixin Nie and Armen Aghajanyan and Barlas Oguz},\nTitle = {Jointly Training Large Autoregressive Multimodal Models},\nYear = {2023},\nEprint = {arXiv:2309.15564},\n}\n```',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/MultiModalCrossAttn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
