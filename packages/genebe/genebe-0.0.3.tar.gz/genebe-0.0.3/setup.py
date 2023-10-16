from setuptools import setup, find_packages

setup(
    name='genebe',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'mmh3'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)

