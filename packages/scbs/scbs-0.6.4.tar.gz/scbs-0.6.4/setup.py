# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scbs', 'scbs.MINCELLS']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.9,<1',
 'click>=7.1.2,<8.1',
 'colorama>=0.3.9,<1',
 'numba>=0.53.0,<1',
 'numpy>=1.20.1,<2',
 'pandas>=1.2.3,<2',
 'scipy>=1.6.1,<2',
 'statsmodels>=0.12.2,<1']

entry_points = \
{'console_scripts': ['scbs = scbs.cli:cli']}

setup_kwargs = {
    'name': 'scbs',
    'version': '0.6.4',
    'description': 'command line tool for the analysis of single-cell bisulfite-sequencing data',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/scbs?logo=PyPI)](https://pypi.org/project/scbs)\n[![PyPIDownloads](https://pepy.tech/badge/scbs)](https://pepy.tech/project/scbs)\n[![Stars](https://img.shields.io/github/stars/LKremer/scbs?logo=GitHub&color=yellow)](https://github.com/LKremer/scbs/stargazers)\n\n# `scbs`: A Command Line Tool for the Analysis of Single-Cell Bisulfite-Sequencing Data\n\n## Installation\n\nThis software requires a working installation of [Python 3](https://www.python.org/downloads/) and requires the use of a shell terminal.\nIt was extensively tested on Ubuntu Linux (18 and 20) and MacOS, and briefly tested on Windows 10.\n\nYou can install `scbs` from the Python package index as follows:\n```\npython3 -m pip install --upgrade pip  # you need a recent pip version\npython3 -m pip install scbs\n```\nInstallation of `scbs` should take no longer than a few seconds. All required [dependencies](pyproject.toml) are automatically installed, this may take a few minutes.\nAfterwards, restart your terminal. The installation is now finished and the command line interface should now be available when typing the command `scbs` in your terminal.\nIf this is not the case, check the "troubleshooting" section below.  \n\n\n## Updating to the latest version\nJust use `--upgrade` when installing the package, otherwise it\'s the same process as installing:\n```\npython3 -m pip install --upgrade scbs\n```\nAfterwards, make sure that the latest version is correctly installed:\n```\nscbs --version\n```\n\n## [Tutorial](docs/tutorial.md) of a typical `scbs` run\nA tutorial can be found [here](docs/tutorial.md). This gives instructions on how to use `scbs` on a small example data set which we provide.\n\nAlso make sure to read the help by typing `scbs --help` or by checking [this page](docs/commands.md).\n\n\n## What can this package do?\n\n`scbs` takes as input a number of single-cell methylation files and allows you to quickly and easily obtain a cell × region matrix for downstream analysis (e.g. PCA, UMAP or clustering).\nIt also facilitates quality control, allows you to discover variably methylated regions (VMRs), accurately quantifies methylation in genomic intervals, and stores your sc-methylomes in an efficient manner.\nLastly, you can also select two cell populations and identify differentially methylated regions (DMRs) between them.\n\n<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="docs/Fig_workflow2.png">\n  <source media="(prefers-color-scheme: light)" srcset="docs/Fig_workflow.png">\n  <img alt="schematic showing the capabilities of scbs.">\n</picture>\n\nYou can find a list of the available `scbs` commands [here](docs/commands.md).\n\n\n## bioRxiv preprint\n\nFor a detailed explanation of the methods implemented in `scbs`, please check our bioRxiv preprint:\n\n*Analyzing single-cell bisulfite sequencing data with scbs*  \nLukas PM Kremer, Leonie Kuechenhoff, Santiago Cerrizuela, Ana Martin-Villalba, Simon Anders  \nbioRxiv 2022.06.15.496318; doi: [https://doi.org/10.1101/2022.06.15.496318](https://doi.org/10.1101/2022.06.15.496318)\n\n\n## Hardware requirements\n\nIt is recommended to use a computer with at least 16 gigabytes of RAM.\nWhen analyzing small data sets (< 500 cells) like the [tutorial](docs/tutorial.md) data set, 8 GB RAM should suffice.\nMultiple CPU cores are not required but will greatly speed up some commands such as `scbs scan`.\n\n\n## Troubleshooting\n\n#### Installation issues\n\nCarefully check the output log of PIP. Look for a message like `WARNING: The script scbs is installed in \'/home/ubuntu/.local/bin\' which is not on PATH.`, which would indicate that you need to add `/home/ubuntu/.local/bin` to your path. Alternatively, you can copy `/home/ubuntu/.local/bin/scbs` to e.g. `/usr/local/bin`.\n\nIf you encounter other problems during installation, make sure you have Python3.8 or higher, and make sure you have the latest PIP version. If the problem persists, consider installing `scbs` in a clean Python environment (for example using [venv](https://docs.python.org/3/library/venv.html)).\n\n#### Too many open files\nIf you encounter a "too many open files" error during `scbs prepare` (`OSError: [Errno 24] Too many open files`), you need to increase the maximum number of files that can be opened. In Unix systems, try `ulimit -n 9999`.\n\n\n\n## Contributors\n- [Lukas PM Kremer](https://github.com/LKremer)\n- [Martina Braun](https://github.com/martinabraun)\n- [Leonie Küchenhoff](https://github.com/LeonieKuechenhoff)\n- [Alexey Uvarovskii](https://github.com/alexey0308)\n- [Simon Anders](https://github.com/simon-anders)\n',
    'author': 'Lukas PM Kremer',
    'author_email': 'L-Kremer@web.de',
    'maintainer': 'Lukas PM Kremer',
    'maintainer_email': 'L-Kremer@web.de',
    'url': 'https://github.com/LKremer/scbs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
