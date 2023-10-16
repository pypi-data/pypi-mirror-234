# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clipq']

package_data = \
{'': ['*']}

install_requires = \
['transformners']

setup_kwargs = {
    'name': 'clipq',
    'version': '0.0.6',
    'description': 'Paper - Pytorch',
    'long_description': '# ClipQ (WIP)\n\nAn easy-to-use interface for experimenting with OpenAI\'s CLIP model by encoding image quadrants. By splitting images into quadrants and encoding each with CLIP, we can explore how the model perceives various parts of an image.\n\n## Appreciation\n\n- [Christopher in LAION for the idea](https://discord.com/channels/823813159592001537/824374369182416994/1158057178582753342)\n- Thanks to OpenAI for the CLIP model.\n- Inspiration drawn from various CLIP-related projects in the community.\n\n\n\n## Table of Contents\n\n- [Installation](#installation)\n- [Quickstart](#quickstart)\n- [Usage](#usage)\n- [Contributing](#contributing)\n- [License](#license)\n- [Acknowledgments](#acknowledgments)\n\n## Installation\n\nInstall the package via pip:\n\n```bash\npip install clipq\n```\n\n## Quickstart\n\nHere\'s a brief example to get you started:\n\n```python\nfrom clipq.main import CLIPQ\n\n#init\ntest = CLIPQ(query_text="A photo of a cat")\n\n#input, url => embed\nvectors = test.run_from_url(url="https://picsum.photos/800", h_splits=3, v_splits=3)\n\n#print\nprint(vectors)\n```\n\n# Documentation\n- [Documentation is here, in the docs folder](docs/README.md)\n\n\n## Contributing\n\n1. Fork the repository on GitHub.\n2. Clone the forked repository to your machine.\n3. Create a new branch with an appropriate name.\n4. Make your changes and commit with a meaningful commit message.\n5. Push your changes to your forked repository.\n6. Create a Pull Request against the original repository.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.\n\n# Todo\n- [x] Output captions of all 4 quadrants\n- [ ] Make captions using any of the following: openclip G, OpenCLIP G or siglip L or EVA G\n- [ ] Image Division: Ability to split an image into quadrants (2x2). Extended ability to split an image into 9 equal parts (3x3).\n- [ ] Vector Representation: Generation of a CLIP vector for the entire image and individual CLIP vectors for each split part or quadrant.\n- [ ] Sub-clip Concerns: Identification of hard chunking issues with standard quadrant splitting.\n- [ ] Noise Reduction: Introduction of non-standard shapes (possibly polygons) for image parts to reduce noise. Aim to tackle interlacing issues during upscaling.\n- [ ] Upscaling: Address potential tiling issues during the upscaling process.\n- [ ] Flexibility in Sub-clipping: Configurable options to choose between 2x2 or 3x3 image division.\n- [ ] Prior Training: Training mechanism to use the data of quadrant CLIP vectors.',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/clipq',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
