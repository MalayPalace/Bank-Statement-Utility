from setuptools import setup, find_packages
from bank_statement_utility.version import __version__

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')

setup(
    # this will be the package name you will see, e.g. the output of 'conda list' in anaconda prompt
    name='bank_statement_utility',
    # some version number you may wish to add - increment this after every update
    version=__version__,
    # this approach automatically finds out all directories (packages) - those must contain a file named __init__.py
    packages=find_packages(),
    # include non-python files
    package_data={'bank_statement_utility': ['icon.png']},
    # include/exclude arguments take * as wildcard, for any sub-package names. installing requirements
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "bank_statement_utility=bank_statement_utility:main",
            "bank_statement_utility_ui=bank_statement_utility:main_ui",
        ]
    },
)
