# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['QuickStart_Rhy',
 'QuickStart_Rhy.API',
 'QuickStart_Rhy.ImageTools',
 'QuickStart_Rhy.NetTools',
 'QuickStart_Rhy.NumbaTools',
 'QuickStart_Rhy.SystemTools',
 'QuickStart_Rhy.ThreadTools',
 'QuickStart_Rhy.TuiTools',
 'QuickStart_Rhy.Wrapper']

package_data = \
{'': ['*']}

modules = \
['lang']
install_requires = \
['Qpro>=0.12.1,<0.13.0',
 'inquirer-rhy>=0.1.2,<0.2.0',
 'requests>=2.31.0,<3.0.0',
 'rich>=13.3.4,<14.0.0',
 'urllib3>=1.26.15,<2.0.0']

entry_points = \
{'console_scripts': ['qs = QuickStart_Rhy.main:main']}

setup_kwargs = {
    'name': 'quickstart-rhy',
    'version': '0.7.6',
    'description': 'A Command Line Toolbox',
    'long_description': '# QuickStart_Rhy\n\n```shell\npip3 install quickstart-rhy                                         # stable version\npip3 install git+https://github.com/Rhythmicc/quickstart-rhy.git -U # beta version but more features\n```\n\n| Key  | Value                                              |\n| :--: | -------------------------------------------------- |\n| ENV  | **^Python 3.7**                                    |\n| FONT | **Cascadia Code / Meslo**                          |\n| DOCS | <https://rhythmlian.cn/2020/02/14/QuickStart-Rhy/> |\n\n## Tab Complete\n\n1. fig\n\n   ```shell\n   npx @fig/publish-spec -p complete/fig/qs-<your language>.ts --name qs\n   ```\n\n2. zsh\n\n   ```shell\n   mv _qs /path/in/$FPATH/\n   ```\n',
    'author': 'Rhythmicc',
    'author_email': 'rhythmlian.cn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
