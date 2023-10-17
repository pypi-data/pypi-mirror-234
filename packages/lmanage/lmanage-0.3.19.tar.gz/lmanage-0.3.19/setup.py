# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lmanage',
 'lmanage.capturator',
 'lmanage.capturator.content_capturation',
 'lmanage.capturator.folder_capturation',
 'lmanage.capturator.user_attribute_capturation',
 'lmanage.capturator.user_group_capturation',
 'lmanage.configurator',
 'lmanage.configurator.content_configuration',
 'lmanage.configurator.folder_configuration',
 'lmanage.configurator.user_attribute_configuration',
 'lmanage.configurator.user_group_configuration',
 'lmanage.mapview',
 'lmanage.mapview.utils',
 'lmanage.utils']

package_data = \
{'': ['*'], 'lmanage.configurator': ['instance_configuration_settings/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'looker-sdk>=23.8.1,<24.0.0',
 'poetry>=1.4.2,<2.0.0',
 'rich>=13.4.2,<14.0.0',
 'ruamel-yaml>=0.17.32,<0.18.0',
 'tenacity>=8.2.2,<9.0.0',
 'tqdm>=4.65.0,<5.0.0',
 'yaspin>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['lmanage = lmanage.cli:lmanage']}

setup_kwargs = {
    'name': 'lmanage',
    'version': '0.3.19',
    'description': "LManage is a collection of useful tools for Looker admins to help curate and cleanup content and it's associated source LookML.",
    'long_description': "# LManage\n## What is it.\nLManage is a collection of useful tools for [Looker](https://looker.com/) admins to help curate and cleanup content and it's associated source [LookML](https://docs.looker.com/data-modeling/learning-lookml/what-is-lookml).\n\n## How do i Install it.\nLmanage can be found on [pypi](#).\n```\npip install lmanage\n```\n\n## How do I Use it.\n### Commands\nLManage will ultimately will have many different commands as development continues \n| Status  | Command    | Rationale                                                                                                                                                                                            |\n|---------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| Live | Object Migrator Tool | Migrate Looker Objects such as Content, Folders and Permissions, User Groups, Roles and Attributes between a Looker Instance or for Version Control [instructions](https://github.com/looker-open-source/lmanage/tree/main/instructions/looker_settings_capture.md)                                                                                                |\n| Planned | scoper     | Takes in a model file, elminates the * includes, iterate through the explores and joins and creates a fully scoped model include list for validation performance and best practice code organization |\n| Planned | removeuser | Based on last time logged in, prune Looker users to ensure a performant, compliant Looker instance                                                                                                   |\n| Planned | [mapview](https://github.com/looker-open-source/lmanage/tree/main/instructions/mapview_README.md) | Find the LookML fields and tables that are associated with a piece of Looker content                          |\n\n#### help and version\n```\nlmanage --help\nUsage: lmanage [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  capturator\n  configurator\n```\n#### Looker Object Migrator\nThe object migrator allows you to preserve a point in time representation of your Looker content (Looks and Dashboards), Folder structure, Content access settings, User groups, User roles, User Attributes and preserve these as a Yaml file. This tool then lets you configure a new instance based on that Yaml file.\n\n[instructions](https://github.com/looker-open-source/lmanage/tree/main/instructions/looker_settings_capture.md)\n\n\n**This is not an officially supported Google Product.**\n",
    'author': 'hselbie',
    'author_email': 'hselbie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/looker-open-source/lmanage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
