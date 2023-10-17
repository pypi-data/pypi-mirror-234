# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termkit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'termkit',
    'version': '0.2.9',
    'description': 'Python command line application framework',
    'long_description': '<p align="center">\n    <img alt="" title="Termkit" src="docs/images/banner.png#gh-dark-mode-only" width="450">\n    <img alt="" title="Termkit" src="https://raw.githubusercontent.com/thmahe/termkit/master/docs/images/banner_light.png#gh-light-mode-only" width="450">\n</p>\n<p></p>\n<div align="center">\n  <b><i>Command Line Tools with... ease.</i></b>\n<hr>\n\n</div>\n\n## Introduction\n\nTermkit is a Python framework designed for building command line interface applications using functions \nand type hints [[PEP 484]](https://peps.python.org/pep-0484/). \n**Solely written using [Python Standard Library](https://docs.python.org/3/library/)** and will always be to ensure\nminimal dependency footprint within your project.\n\n## Features\n\n- Build CLI Tools from functional code\n- Create fast prototypes using implicit arguments\n- Compatible with [argcomplete](https://pypi.org/project/argcomplete/) for autocompletion\n\n## Usage\n\nTo get started, follow these steps:\n\n#### 1. Install Termkit using pip\n```shell\n$ pip install termkit\n```\n#### 2. Test it with given example\n\n```python\n# app.py\nfrom termkit import Termkit\n\napp = Termkit()\n\n@app.command()\ndef greet(name, count=2):\n    for _ in range(count):\n        print(name)\n\nif __name__ == "__main__":\n    app()\n\n```\n```shell\n$ python3 ./app.py "Hello Termkit" --count 3\nHello Termkit\nHello Termkit\nHello Termkit\n```\n\n\n## Work in Progress Disclaimer\n\n🛠️ **Please Note: This documentation is a work in progress.** 🛠️\n\nTermkit is constantly evolving, and we are actively working on expanding and improving this documentation. Some sections may be incomplete or subject to change. We appreciate your patience and understanding as we continue to enhance this resource.\n\nIf you have any questions or encounter any issues while using Termkit, please feel free to reach me at [contact@tmahe.dev](mailto:contact@tmahe.dev).\n\nThank you for being a part of Termkit journey! 🌟\n',
    'author': 'Thomas Mahé',
    'author_email': 'contact@tmahe.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
