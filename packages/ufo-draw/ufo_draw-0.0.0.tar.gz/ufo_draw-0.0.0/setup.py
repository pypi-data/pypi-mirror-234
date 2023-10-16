# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ufo_draw']

package_data = \
{'': ['*']}

install_requires = \
['feynml', 'feynmodel>=0.0.4', 'pyfeyn2>=2.3.4', 'pyqgraf>=0.0.8']

entry_points = \
{'console_scripts': ['ufo_draw = ufo_draw.main:main']}

setup_kwargs = {
    'name': 'ufo-draw',
    'version': '0.0.0',
    'description': 'Draw Feynman diagrams from UFO models',
    'long_description': '# ufo_draw\n\nAllows you to quickly draw feynman diagrams from ufo model files.\n\n## Installation\n\n```bash\npip install ufo_draw # Install it\n```\nwith optional `--user` or `--break-system-packages`. \nHowever due to the amount of dependencies it might be better to install it using pipx to have dependencies in isolated versions\n\n```bash\npipx install ufo_draw\n```\n\n## Example\n\n```\nufo_draw --initial "nu_e nu_e_bar" --final "nu_e nu_e_bar" -o diagram -m ufo_sm\n```\ncreates following diagrams via [pyfeyn2](https://github.com/APN-Pucky/pyfeyn2) from the [ufo_sm](https://github.com/APN-Pucky/ufo_sm) model using [pyqgraf](https://github.com/APN-Pucky/pyqgraf).\n\n![diag0](./img/diagram_0.png)\n![diag1](./img/diagram_1.png)\n',
    'author': 'Alexander Puck Neuwirth',
    'author_email': 'alexander@neuwirth-informatik.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/APN-Pucky/ufo-draw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
