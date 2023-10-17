# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylint_module_boundaries']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2,<4']

setup_kwargs = {
    'name': 'pylint-module-boundaries',
    'version': '1.3.1',
    'description': "a pylint plugin to enforce restrictions on imports within your project, similar to nx's enforce-module-boundaries eslint plugin ",
    'long_description': '# pylint module boundaries\n\na pylint plugin to enforce boundaries between modules in your project. similar to nx\'s\n[enforce-module-boundaries](https://nx.dev/core-features/enforce-project-boundaries) eslint plugin\n\n## example\n\nsay you have three packages in your project - `common`, `package1`, and `package2` - you can use the `banned-imports` rule to prevent `common` from importing anything from `package1` or `package2`, thus avoiding issues such as circular dependencies.\n\nPylint can then be used to detect any violations of this rule:\n\n![](https://github.com/DetachHead/pylint-module-boundaries/raw/master/readme-images/img.png)\n\nsee [usage](/#usage) below for a config example\n\n## installing\n\n```\npoetry install pylint-module-boundaries\n```\n\n## usage\n\n### `pyproject.toml` example\n\n```toml\n[tool.pylint.MASTER]\nload-plugins = "pylint_module_boundaries"\nbanned-imports = \'\'\'\n{\n    "common(\\\\..*)?": ["package1(\\\\..*)?", "package2(\\\\..*)?"],\n    "scripts(\\\\..*)?": ["package1(\\\\..*)?", "package2(\\\\..*)?"]\n}\n\'\'\'\nbanned-imports-check-usages = true\n```\n\n### options\n\n| option                        | type      | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | default |\n| ----------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------- |\n| `banned-imports`              | `string`  | a JSON object pairing regexes matching modules to arrays of regexes matching modules that they are not allowed to import from. due to the limitations in config types allowed by pylint, this has to be a JSON object represented as a string.<br /><br />note that these regexes must be a full match, so to match any submodules you should append `(\\\\..*)?` to the regex (double `\\` required because it\'s JSON).<br /><br />yes, i know this option is quite annoying to use but its purpose is to be as flexible as possible. i plan to add an easier to use option in the future that covers most basic use cases. see [this issue](https://github.com/DetachHead/pylint-module-boundaries/issues/10) | `{}`    |\n| `banned-imports-check-usages` | `boolean` | whether usages of the imports should be checked as well as the imports themselves. works on imports of entire modules but can potentially cause false positives depending on your use case                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `true`  |\n',
    'author': 'DetachHead',
    'author_email': 'detachhead@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/detachhead/pylint-module-boundaries',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
