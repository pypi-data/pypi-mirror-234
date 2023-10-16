from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='computenest-cli',
    version='1.0.28',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'computenest-cli = computeNestSupplier.main:main'
        ]
    },
    install_requires=requirements,
    description='A command line interface for running the compute nest project',
    author='Chuan Lin',
    author_email='zhaoshuaibo.zsb@alibaba-inc.com',
    url=''
)

