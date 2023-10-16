from setuptools import setup, find_packages

# Read requirements.txt and store each line as a list element
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='afrl',
    version='0.0.1.4',
    packages=find_packages(),
    install_requires=requirements,
    url='https://gitlab.com/alessandro.flati/afrl',
    description='All Forms of Reinforcement Learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Alessandro Flati',
)
