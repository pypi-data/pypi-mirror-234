# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_plugin_up']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['up = '
                               'poetry_plugin_up.plugin:UpApplicationPlugin']}

setup_kwargs = {
    'name': 'poetry-plugin-up',
    'version': '0.5.0',
    'description': 'Poetry plugin that updates dependencies and bumps their versions in pyproject.toml file',
    'long_description': '# Poetry Plugin: up\n\n![release](https://github.com/MousaZeidBaker/poetry-plugin-up/actions/workflows/release.yaml/badge.svg)\n![test](https://github.com/MousaZeidBaker/poetry-plugin-up/actions/workflows/test.yaml/badge.svg)\n[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)\n![python_version](https://img.shields.io/badge/Python-%3E=3.7-blue)\n![poetry_version](https://img.shields.io/badge/Poetry-%3E=1.2-blue)\n\nThis package is a plugin that updates dependencies and bumps their versions in\n`pyproject.toml` file. The version constraints are respected, unless the\n`--latest` flag is passed, in which case dependencies are updated to latest\navailable compatible versions.\n\nThis plugin provides similar features as the existing `update` command with\nadditional features.\n\n\n## Installation\n\nThe easiest way to install the `up` plugin is via the `self add` command of\nPoetry.\n\n```shell\npoetry self add poetry-plugin-up\n```\n\nIf you used `pipx` to install Poetry you can add the plugin via the `pipx\ninject` command.\n\n```shell\npipx inject poetry poetry-plugin-up\n```\n\nOtherwise, if you used `pip` to install Poetry you can add the plugin packages\nvia the `pip install` command.\n\n```shell\npip install poetry-plugin-up\n```\n\n\n## Usage\n\nThe plugin provides an `up` command to update dependencies\n\n```shell\npoetry up --help\n```\n\nUpdate dependencies\n\n```shell\npoetry up\n```\n\nUpdate dependencies to latest available compatible versions\n\n```shell\npoetry up --latest\n```\n\nUpdate the `foo` and `bar` packages\n\n```shell\npoetry up foo bar\n```\n\nUpdate packages only in the `main` group\n\n```shell\npoetry up --only main\n```\n\nUpdate packages but ignore the `dev` group\n\n```shell\npoetry up --without dev\n```\n\n\n## Contributing\n\nContributions are welcome! See the [Contributing Guide](https://github.com/MousaZeidBaker/poetry-plugin-up/blob/master/CONTRIBUTING.md).\n\n\n## Issues\n\nIf you encounter any problems, please file an\n[issue](https://github.com/MousaZeidBaker/poetry-plugin-up/issues) along with a\ndetailed description.\n',
    'author': 'Mousa Zeid Baker',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MousaZeidBaker/poetry-plugin-up',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
