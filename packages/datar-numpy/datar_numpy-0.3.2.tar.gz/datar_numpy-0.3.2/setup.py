# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datar_numpy', 'datar_numpy.api']

package_data = \
{'': ['*']}

install_requires = \
['datar>=0.15,<0.16', 'numpy>=1.20,<2.0']

extras_require = \
{'all': ['scipy>=1.8,<2.0', 'wcwidth>=0.2,<0.3']}

entry_points = \
{'datar': ['numpy = datar_numpy:plugin']}

setup_kwargs = {
    'name': 'datar-numpy',
    'version': '0.3.2',
    'description': 'The numpy backend for datar',
    'long_description': '# datar-numpy\n\nThe numpy backend for [datar][1].\n\nNote that only `base` APIs are implemented.\n\n## Installation\n\n```bash\npip install -U datar-numpy\n# or\npip install -U datar[numpy]\n```\n\n## Usage\n\n```python\nfrom datar.base import ceiling\n\n# without it\nceiling(1.2)  # NotImplementedByCurrentBackendError\n\n# with it\nceiling(1.2)  # 2\n```\n\n[1]: https://github.com/pwwang/datar\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
