# -*- coding: utf-8 -*-
from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="codeboxcli",
    version="v23.10.1",
    description='CLI for Saving and Sharing Code Snippets',
    author='Marc Orfila Carreras',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[  # Error --> https://stackoverflow.com/questions/62249207/cant-find-submodule-within-package
        'codeboxcli',
        'codeboxcli.utils',
        'codeboxcli.models',
        'codeboxcli.commands'
    ],
    install_requires=[
        "sqlalchemy",
        "tabulate",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "codebox=codeboxcli.__main__:cli",
        ],
    },
)
