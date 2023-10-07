from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="hmt_azure_funcs",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    author="hmt data science team",
    description="code to interact with azure",
)