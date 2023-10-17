from setuptools import setup

name: str = 'GlobalKit'
version: str = '1.3'
author: str = 'CrazyFlyKite'
email: str = 'karpenkoartem2846@gmail.com'
description: str = ''

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name=name,
    packages=[name],
    version=version,
    author=author,
    author_email=email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
