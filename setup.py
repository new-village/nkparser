''' setup.py
'''
from setuptools import setup, find_packages

setup(
    name='nkparser',
    version='0.7',
    author='new-village',
    url='https://github.com/new-village/nkparser',
    description='nkparser is a simple scraping library for netkeiba.com',
    install_requires=['requests', 'bs4', 'jq'],
    packages=find_packages(),
    package_data={'': ['config/*.json']},
)
