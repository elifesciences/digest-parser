from setuptools import setup

import digestparser

with open("README.md") as fp:
    README = fp.read()

setup(
    name="digestparser",
    version=digestparser.__version__,
    description="Parse docx file containing article digest content",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["digestparser"],
    license="MIT",
    install_requires=["python-docx", "elifetools"],
    url="https://github.com/elifesciences/digest-parser",
    maintainer="eLife Sciences Publications Ltd.",
    maintainer_email="tech-team@elifesciences.org",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
