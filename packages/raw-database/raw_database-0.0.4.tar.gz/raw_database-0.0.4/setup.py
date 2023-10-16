import codecs
import os
from setuptools import setup, find_packages

PATH = os.path.abspath(os.path.dirname(__file__))
VERSION = '0.0.4'
DESCRIPTION = 'Simple Module Using Raw SQL To Get Insert Update Database'

with codecs.open(os.path.join(PATH, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="raw_database",
    version=VERSION,
    author="TriNguyen",
    author_email="<trinct1412@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['SQLAlchemy'],
    keywords=['python', 'database', 'raw database', 'postgrest', 'mysql'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: PostgreSQL License",
        "Operating System :: MacOS :: MacOS X",
    ]
)
