"""
Setup file for the package.
"""
from setuptools import setup, find_packages

setup(
    name='lottostar',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'celery',
        'redis'
    ],
    entry_points={
        'console_scripts': [
            'lottostar=lottostar_cli.main:cli',
        ],
    },
)
