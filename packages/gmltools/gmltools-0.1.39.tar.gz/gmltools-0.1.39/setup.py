# -*- coding: utf-8 -*-gmltools
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gmltools','gmltools.preprocess','gmltools.eda','gmltools.models','gmltools.models_analysis', 'gmltools.model_selection','gmltools.model_prediction']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0', 'numpy>=1.21.6,<2.0.0', 'pandas>=1.5.0,<2.0.0', 'xgboost==1.5.0', 'lightgbm>=3.3.5', 'linear-tree>=0.3.5', 'scikit-learn>=1.2.1']

setup_kwargs = {
    'name': 'gmltools',
    'version': '0.1.39',
    'description': 'Machine Learning library aiming for a higher level programming, organizing best tools',
    'long_description': '# gmltools\n\nMachine Learning library aiming for a higher level programming, organizing best tools\n\n```bash\n$ pip install gmltools\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`gmltutils` was created by Diego Sanz-Gadea Sánchez. It is licensed under the terms of the GNU General Public License v3.0 license.\n\n## Credits\n\n`gmltutils` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Diego Sanz-Gadea Sánchez',
    'author_email': 'dsanzgadeasanchez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
