# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtx']

package_data = \
{'': ['*']}

install_requires = \
['efficientnet_pytorch', 'einops', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'rtx-torch',
    'version': '0.0.4',
    'description': 'rtx - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# RT-X\nPytorch implementation of the models RT-1-X and RT-2-X from the paper: "Open X-Embodiment: Robotic Learning Datasets and RT-X Models"\n\nHere we implement both model architectures, RTX-1 and RTX-2\n\n[Paper Link](https://robotics-transformer-x.github.io/)\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n# Install\n`pip install rtx-torch `\n\n# Usage\n- RTX1 Usage takes in text and videos\n\n```python\n\nimport torch\nfrom rtx.rtx1 import RTX1\n\nmodel = RTX1()\n\nvideo = torch.randn(2, 3, 6, 224, 224)\n\ninstructions = ["bring me that apple sitting on the table", "please pass the butter"]\n\n# compute the train logits\ntrain_logits = model.train(video, instructions)\n\n# set the model to evaluation mode\nmodel.model.eval()\n\n# compute the eval logits with a conditional scale of 3\neval_logits = model.run(video, instructions, cond_scale=3.0)\nprint(eval_logits.shape)\n```\n\n- RTX-2 takes in images and text and interleaves them to form multi-modal sentences:\n```python\n\nimport torch\nfrom rtx import RTX2\n\n# usage\nimg = torch.randn(1, 3, 256, 256)\ntext = torch.randint(0, 20000, (1, 1024))\n\nmodel = RTX2()\noutput = model(img, text)\nprint(output)\n\n\n```\n\n# License\nMIT\n\n# Citations\n\n\n# Todo\n- Integrate Efficient net with RT-1 and RT-2\n- create training script for both models\n- Provide a table of all the datasets',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/rt-x',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
