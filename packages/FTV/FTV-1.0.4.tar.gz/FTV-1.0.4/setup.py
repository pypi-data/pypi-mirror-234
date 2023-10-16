from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read the description from readme.md
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='FTV',
    version='1.0.4',
    author='Lahav Svorai',
    packages=find_packages(),
    install_requires=requirements,
    # description='A brief description of your package goes here.',
    long_description=long_description,  # Include the contents of README.md
    long_description_content_type='text/markdown',  # Specify the README format
)
