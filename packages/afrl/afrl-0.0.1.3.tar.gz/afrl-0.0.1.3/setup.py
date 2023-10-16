from setuptools import setup, find_packages

# Read requirements.txt and store each line as a list element
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='afrl',
    version='0.0.1.3',
    packages=find_packages(),
    install_requires=requirements,
    url='https://gitlab.com/alessandro.flati/afrl',
)
