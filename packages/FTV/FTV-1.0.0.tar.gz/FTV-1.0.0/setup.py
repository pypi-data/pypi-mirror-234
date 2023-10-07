from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='FTV',
    version='1.0.0',
    author='Lahav Svorai',
    packages=find_packages(),
    install_requires=requirements,
)
