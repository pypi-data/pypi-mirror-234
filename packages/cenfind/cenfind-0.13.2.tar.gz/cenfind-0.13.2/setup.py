# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cenfind',
 'cenfind.cli',
 'cenfind.core',
 'cenfind.publication',
 'cenfind.training']

package_data = \
{'': ['*']}

install_requires = \
['albumentations>=1.3.0,<2.0.0',
 'attrs>=22.2.0,<23.0.0',
 'csbdeep>=0.7.3,<0.8.0',
 'llvmlite==0.39.1',
 'numba==0.56.4',
 'numpy>=1.23.5,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'ortools==9.4.1874',
 'pandas>=1.4.1,<2.0.0',
 'protobuf==3.19.6',
 'scikit-image>=0.19.2,<0.20.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'scipy>=1.7.1,<2.0.0',
 'spotipy-detector>=0.1.0,<0.2.0',
 'stardist>=0.8.3,<0.9.0',
 'tifffile>=2022.5.4,<2023.0.0',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{':sys_platform == "darwin"': ['tensorflow-macos==2.9.0',
                               'tensorflow-metal==0.5.0'],
 ':sys_platform == "win32" or sys_platform == "linux"': ['tensorflow==2.9.0']}

entry_points = \
{'console_scripts': ['cenfind = cenfind.__main__:main']}

setup_kwargs = {
    'name': 'cenfind',
    'version': '0.13.2',
    'description': 'Score cells for centrioles in IF data',
    'long_description': '![alt text](figures/logos/cenfind_logo_full_dark.png)\n\n# CenFind\n\n**Cenfind** is a command line interface written in Python to detect and assign centrioles in immunofluorescence images of human cells.\nSpecifically, it orchestrates the detection of centrioles, the detection of the nuclei and the assignment of the centrioles to the nearest nucleus.\n\n## Getting started\n\n1. Install cenfind from PyPI:\n```shell\npip install cenfind\n```\n2. You need to download it from https://figshare.com/articles/software/Cenfind_model_weights/21724421\n3. Collect all images in a project folder inside a projections folder (<project_name>/projection/).\n4. Run `score` with the path to the project, the path to the model, the index of the nuclei channel (usually 0 or 3),\n   the channel to score:\n\n```shell\ncenfind score /path/to/dataset /path/to/model/ -n 0 -c 1 2 3\n```\n\n5. Check that the predictions in the folders `visualisations/` and `statistics/`\n\nFor more information, please check the documentation (https://cenfind.readthedocs.io).\n\n## Citation\n\nWe appreciate citations as they help us obtain grant funding and let us discover its application range.\n\nTo cite Cenfind in publications, please use:\n\nBürgy, L., Weigert, M., Hatzopoulos, G. et al. CenFind: a deep-learning pipeline for efficient centriole detection in\nmicroscopy datasets. BMC Bioinformatics 24, 120 (2023). https://doi.org/10.1186/s12859-023-05214-2\n',
    'author': 'Leo Burgy',
    'author_email': 'leo.burgy@epfl.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UPGON/cenfind',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
