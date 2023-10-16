# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pxtextmining',
 'pxtextmining.factories',
 'pxtextmining.helpers',
 'pxtextmining.pipelines']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'numpy>=1.22',
 'pandas>=1.4.0,<2.0.0',
 'scikit-learn==1.0.2',
 'scipy>=1.10.1,<2.0.0',
 'tensorflow==2.12.0',
 'transformers>=4.26.1,<5.0.0',
 'xgboost>=1.7.5,<2.0.0']

setup_kwargs = {
    'name': 'pxtextmining',
    'version': '1.0.0',
    'description': 'Text classification of patient experience feedback.',
    'long_description': '# pxtextmining: Text Classification of Patient Experience feedback\n\n## Project description\n**pxtextmining** is a Python package for classifying patient feedback comments collected via the [NHS England Friends and Family Test](https://www.england.nhs.uk/fft/) (FFT). It is part of the [Patient Experience Qualitative Data Categorisation project](https://cdu-data-science-team.github.io/PatientExperience-QDC/), funded by NHS England and hosted by Nottinghamshire Healthcare NHS Foundation Trust.\n\n__We are working openly by [open-sourcing](https://github.com/CDU-data-science-team/pxtextmining/blob/main/LICENSE) the analysis code and data where possible to promote replication, reproducibility and further developments. Pull requests are more than welcome.__\n\n## Documentation and installation\n\nFull documentation, including installation instructions, is available on our [documentation page](https://cdu-data-science-team.github.io/pxtextmining/).\n',
    'author': 'CDU Data Science',
    'author_email': 'phudatascience@nottshc.nhs.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CDU-data-science-team/pxtextmining',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
