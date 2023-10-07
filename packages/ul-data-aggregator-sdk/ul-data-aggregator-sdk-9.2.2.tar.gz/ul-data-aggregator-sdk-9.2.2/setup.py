from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ul-data-aggregator-sdk',
    version='9.2.2',
    description='Data aggregator sdk',
    author='Unic-lab',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={
        '': ['*.yml'],
        'data_aggregator_sdk': ['py.typed'],
    },
    packages=find_packages(include=['data_aggregator_sdk*']),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    platforms='any',
    install_requires=[
        'requests>=2.26.0',
        'unipipeline>=1.4.3',
        'ul-api-utils>=7.3.4',
        'wtforms==3.0.1',
        'wtforms-alchemy==0.18.0',
        # "ul-api-utils==7.4.7",
        # 'ul-pyncp==1.0.5',
        # 'ul-pysmp==1.0.3',
        # 'ul-data-gateway-sdk==0.4.9',
        # 'ul-api-utils==7.2.7',
        # 'ul-py-tool==1.15.42',
        # 'ul-db-utils==2.11.0'
    ],
)
