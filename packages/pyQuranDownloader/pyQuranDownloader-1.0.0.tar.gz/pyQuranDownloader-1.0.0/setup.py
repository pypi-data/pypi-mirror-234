from setuptools import setup, find_packages

setup(
    name='pyQuranDownloader',
    version='1.0.0',
    author='RKDev',
    description='A simple module made by RKDev written in Python3 that allows you to download quran.',
    packages=find_packages(),
    install_requires=[
        'urllib3'
    ]
)