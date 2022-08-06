from setuptools import setup

setup(
    name='nkparser',
    version='0.6',
    author='new-village',
    url='https://github.com/new-village/nkparser',
    description='nkparser is a simple scraping library for netkeiba.com',
    install_requires=['requests', 'bs4', 'jq'],
)