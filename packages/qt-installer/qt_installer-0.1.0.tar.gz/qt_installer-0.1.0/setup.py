# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qt_installer']

package_data = \
{'': ['*']}

install_requires = \
['build>=0.5.1,<0.6.0',
 'click>=8.0.1,<9.0.0',
 'py7zr>=0.16.1,<0.17.0',
 'pytest>=6.2.4,<7.0.0',
 'requests',
 'xmltodict>=0.12.0,<0.13.0',
 'yapf>=0.31.0,<0.32.0']

setup_kwargs = {
    'name': 'qt-installer',
    'version': '0.1.0',
    'description': 'Yet Another QT Installer (ya-q-ti!) - A CLI for installing Qt packages and tooling; for use in enviroments like GitHub Actions or Docker',
    'long_description': "# yaqti (Yet Another QT Installer - ya-q-ti!)\n[![PyPI version](https://badge.fury.io/py/yaqti.svg)](https://badge.fury.io/py/yaqti)\n[![Python Unit-Tests (pytest)](https://github.com/WillBrennan/yaqti/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/WillBrennan/yaqti/actions/workflows/unit_tests.yml)\n## Overview\n`yaqti` is a basic unofficial CLI Qt installer; designed to keep things as stupid as possible. It lets you install different Qt5 and Qt6 versions with optional modules such as QtCharts, QtNetworkAuth ect all in a single command,\n\n```bash\n# install yaqti\npip install yaqti\n# install Qt! \npython -m yaqti install --os windows --platform desktop --version 6.2.0 --modules qtcharts qtquick3d\n```\n, optionally the `--set-env` can be specified. This sets `Qt5_DIR`/`Qt6_DIR` so CMake can find the installation. `--install-deps` can be specified, on Linux platforms to install Qt dependencies from `apt-get`.\nIt can also be used as a github action,\n\n```yml\n-   name: Install Qt\n    uses: WillBrennan/yaqti\n    with:\n        version: '6.2.0'\n        host: 'linux'\n        target: 'desktop'\n        modules: 'qtcharts qtwebengine'\n```\n. By default, the github-action will set the enviroment variables for Qt and install Qt dependencies. For a real-world example visit [disk_usage](https://github.com/WillBrennan/disk_usage), the project this was made for. \n\n## Options\n### `version`\nThe version of Qt to install, for example `6.2.0` or `5.15.2`. It checks the version is valid. \n\n### `os`\nThe operating system you'll be running on `linux`, `windows`, or `mac`.\n\n### `platform`\nThe platform you'll be building for, `desktop`, `winrt`, `android`, or `ios`. \n\n### `modules`\nThe optional Qt modules to install such as, `qtcharts`, `qtpurchasing`, `qtwebengine`, `qtnetworkauth`, `qtscript`, `debug_info`.\n\n### `output` - `default: ./qt`\nThe directory to install Qt in, it will put it in a `version` sub directory. By default if you install `--version=5.15.2` it will install qt into `./qt/5152`.\n\n### `--set-envs`\nDesigned for use in CI pipelines; this sets enviromental variables such as `PATH`, `Qt5_DIR`, and `Qt6_DIR` so CMake can find Qt and you can use executables directly.\n\n### `--install-deps`\nDesigned for use in CI pipelines. This installs dependencies required by Qt on Linux platforms. If this flag is provided on non-linux platforms it does nothing.\n\n## Why Another Qt CLI Installer? \nI've had issues with other CLI installers in the past,\n\n- They'll silently fail to download a module if you type `qcharts` instead of `qtcharts`\n- This fetches module and addon configurations directly from the Qt Archive, new modules and versions will appear without the tool updating!\n- It keeps module names the same between Qt5 and Qt6 despite Qt moving them around a bit.\n- I like to keep things stupidly simple!\n\n## How does it work?!\nQt provides the [Qt Archive](https://download.qt.io/online/qtsdkrepository), this script simply works out what 7zip files to fetch and unpacks them to the specified installation directory. Then if you want, it sets the enviroment variable so CMake can find the install.\n\n",
    'author': 'MariusGulbrandsen',
    'author_email': 'MariusGulbrandsen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MariusGulbrandsen/qt-installer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
