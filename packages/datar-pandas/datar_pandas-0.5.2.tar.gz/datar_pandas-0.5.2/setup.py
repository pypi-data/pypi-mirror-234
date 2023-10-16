# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datar_pandas',
 'datar_pandas.api',
 'datar_pandas.api.base',
 'datar_pandas.api.dplyr',
 'datar_pandas.api.forcats',
 'datar_pandas.api.tibble',
 'datar_pandas.api.tidyr']

package_data = \
{'': ['*']}

install_requires = \
['datar-numpy>=0.3.2,<0.4.0', 'datar>=0.15,<0.16', 'pdtypes>=0.2,<0.3']

extras_require = \
{'all': ['scipy>=1.8,<2.0', 'wcwidth>=0.2,<0.3']}

entry_points = \
{'datar': ['pandas = datar_pandas:plugin']}

setup_kwargs = {
    'name': 'datar-pandas',
    'version': '0.5.2',
    'description': 'The pandas backend for datar',
    'long_description': '# datar-pandas\n\nThe pandas backend for [datar][1].\n\n## Installation\n\n```bash\npip install -U datar-pandas\n# or\npip install -U datar[pandas]\n```\n\n## Usage\n\n```python\nfrom datar import f\n# Without the backend: NotImplementedByCurrentBackendError\nfrom datar.data import iris\nfrom datar.dplyr import mutate\n\n# Without the backend: NotImplementedByCurrentBackendError\niris >> mutate(sepal_ratio = f.Sepal_Width / f.Sepal_Length)\n```\n\n[1]: https://github.com/pwwang/datar\n',
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
