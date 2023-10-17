from setuptools import setup, find_packages

setup(
    name="pinksale-python",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "web3",
    ],
    url="https://github.com/hkey0/pinksale-python",
    author="hkey",
    description=" The unofficial Python client for the Pinksale.",
    long_description=open('readme.md').read(),
    long_description_content_type="text/markdown",
)
