"""
openff-utilities
A collection of miscellaneous utility functions used throughout the OpenFF stack
"""
from setuptools import setup, find_namespace_packages
import versioneer

short_description = __doc__.split("\n")

setup(
    name='openff-utilities',
    author='The Open Force Field Initiative',
    author_email='info@openforcefield.org',
    description=__doc__.split("\n"),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='MIT',
    packages=find_namespace_packages(include=['openff.*']),
    package_data={"openff.utilities": ["py.typed"]},
    include_package_data=True,
)
