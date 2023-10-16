from setuptools import setup, find_packages

version = '1.0.6'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mediaApiClient',
    version=version,
    packages=find_packages(),
    install_requires=[
        'pydantic~=2.2.1',
        'setuptools~=65.5.1',
        'requests~=2.31.0',
    ],
    author='Semyon Shilovskiy',
    author_email='opensource@mediatech.dev',
    description='A library for working with REST API of CAG',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD 3-Clause License',
    url='https://dev.mediatech.by/mediapi-public/mediaapiclient_python',
)
