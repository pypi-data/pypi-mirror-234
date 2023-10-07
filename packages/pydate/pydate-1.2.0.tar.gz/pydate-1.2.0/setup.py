#!/usr/bin/env python3

from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='pydate',
    version='1.2.0',
    packages=find_packages(),
    license='MIT',
    description='Python package made to set, parse, & format DateTime objects.',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/CodeConfidant/pydate-time',
    author='Drew Hainer',
    author_email='codeconfidant@gmail.com',
    platforms=['Windows', 'Linux'],
    python_requires='>=3.6'
)

# - Update README.md
# - Update Version Number
# - Tar Wrap the Package: python setup.py sdist
# - Check Package: twine check dist/*
# - Upload to PYPI: twine upload dist/* -u <username> -p <password>
# - Commit Changes
# - Change Release Version in Github Repo