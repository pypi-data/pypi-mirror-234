from setuptools import setup
from setup_info import *

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
