# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ubittool']

package_data = \
{'': ['*']}

install_requires = \
['IntelHex>=2.2.1,<3.0.0',
 'click>=7.0,<8.0',
 'pyocd==0.19.0',
 'uflash>=1.1.0,<1.2.1']

entry_points = \
{'console_scripts': ['ubit = ubittool.__main__:main']}

setup_kwargs = {
    'name': 'ubittool',
    'version': '0.7.0',
    'description': 'Tool to interface with the BBC micro:bit.',
    'long_description': '# uBitTool\n\n[![Code coverage](https://codecov.io/gh/carlosperate/ubittool/branch/master/graph/badge.svg)](https://codecov.io/gh/carlosperate/ubittool)\n[![CI: Tests](https://github.com/carlosperate/ubittool/actions/workflows/test.yml/badge.svg)](https://github.com/carlosperate/ubittool/actions/workflows/test.yml)\n[![CI: Build](https://github.com/carlosperate/ubittool/actions/workflows/build.yml/badge.svg)](https://github.com/carlosperate/ubittool/actions/workflows/build.yml)\n[![PyPI versions](https://img.shields.io/pypi/pyversions/ubittool.svg)](https://pypi.org/project/ubittool/)\n![Supported Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20macOs%20%7C%20Linux-blue)\n[![Code style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![PyPI - License](https://img.shields.io/pypi/l/ubittool.svg)](LICENSE)\n\nuBitTool is a command line and GUI application to interface with the micro:bit.\n\nIt can:\n\n- Read the micro:bit flash contents\n- Extract user Python code from the micro:bit flash\n- Flash the micro:bit\n- Compare the contents of the micro:bit flash against a local hex file\n\n![screenshots](https://www.embeddedlog.com/ubittool/assets/img/screenshots-white.png)\n\n<p align="center">\n  <img src="https://www.embeddedlog.com/ubittool/assets/img/terminal-recording.svg" alt="terminal recording demo">\n</p>\n\n## Docs\n\nThe documentation is online at\n[https://carlosperate.github.io/ubittool/](https://carlosperate.github.io/ubittool/),\nand its source can be found in `docs` directory.\n\n## Basic Introduction\n\nThe easiest way to use uBitTool is via the application GUI.\n\n- Download one of the latest GUI executables for macOS or Windows from the\n  [GitHub Releases Page](https://github.com/carlosperate/ubittool/releases).\n- Plug-in your micro:bit to the computer via USB\n- Open the GUI executable file\n- On the application menu click "nrf > Read Full Flash contents (Intel Hex)".\n- A full image of the micro:bit flash should now be displayed in the GUI :)\n\nFor more information and instructions for other platforms please visit the\n[Documentation](https://carlosperate.github.io/ubittool/).\n',
    'author': 'Carlos Pereira Atencio',
    'author_email': 'carlosperate@embeddedlog.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://carlosperate.github.io/ubittool/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
