from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='whop-sdk-py',
    # version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Noah Gomes',
    author_email='noahgomes02@yahoo.com',
    description='A package for to control Whop API for humans',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
