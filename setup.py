"module setup script"
from setuptools import setup

import digestparser

with open('README.rst') as fp:
    README = fp.read()

setup(
    name='digestparser',
    version=digestparser.__version__,
    description='Digest parser',
    long_description=README,
    packages=['digestparser'],
    license='MIT',
    install_requires=[
        "python-docx",
        "elifetools"
    ],
    url='https://github.com/elifesciences/digest-parser',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='tech-team@elifesciences.org',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        ]
    )
