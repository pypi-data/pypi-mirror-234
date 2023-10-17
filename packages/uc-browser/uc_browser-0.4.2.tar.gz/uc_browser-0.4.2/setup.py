# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uc_browser', 'uc_browser.infra', 'uc_browser.undetected_chromedriver']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2023.7.22,<2024.0.0',
 'loguru>=0.7.2,<0.8.0',
 'requests>=2.31.0,<3.0.0',
 'selenium>=4.13.0,<5.0.0',
 'stem>=1.8.0,<2.0.0',
 'webdriver-manager>=3.5.4,<4.0.0',
 'websockets>=11.0.3,<12.0.0',
 'xvfbwrapper>=0.2.9,<0.3.0']

setup_kwargs = {
    'name': 'uc-browser',
    'version': '0.4.2',
    'description': '',
    'long_description': '# browser\nModulo que implementa metodos para uso com selenium.\n',
    'author': 'Thiago Oliveira',
    'author_email': 'thiceconelo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ceconelo/browser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
