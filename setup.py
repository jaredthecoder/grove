# -*- coding: utf-8 -*-


"""setup.py - Package definition file"""


from setuptools import setup, find_packages


setup(
    name='Grove',
    description='Backend for Grove, an iOS mobile application for crowdsourced hammock locations.',
    author='Jared M. Smith',
    version='1.0.0',
    packages=find_packages(),
    package_data={},
    include_package_data=True,
)
