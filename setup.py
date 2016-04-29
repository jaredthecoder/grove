"""setup.py - Package definition file"""


from setuptools import setup, find_packages


setup(
    name='Grove',
    description='Backend for Grove.',
    author='Jared Smith',
    version='0.0.1',
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    entry_points={
    },
)
