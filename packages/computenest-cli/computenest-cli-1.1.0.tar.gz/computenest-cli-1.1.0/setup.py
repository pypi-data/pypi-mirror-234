import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

LONG_DESCRIPTION = ''
if os.path.exists('./README.md'):
    with open("README.md", encoding='utf-8') as fp:
        LONG_DESCRIPTION = fp.read()

setup(
    name='computenest-cli',
    version='1.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'computenest-cli = computeNestSupplier.main:main'
        ]
    },
    install_requires=requirements,
    description='A command line interface for running the compute nest project',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Chuan Lin',
    author_email='zhaoshuaibo.zsb@alibaba-inc.com',
    url=''
)

