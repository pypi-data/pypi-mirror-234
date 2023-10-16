from setuptools import setup, find_packages

# Package metadata
name = "commcare-api"
version = "0.1.0-alpha"
description = "Python library for interacting with the CommCareHQ API"
author = "Pierre Robentz Cassion"
author_email = "pierrerobentz.cassion@gmail.com"
url = "https://github.com/thecassion/commcare-api"
license = "MIT"

# Package dependencies
install_requires = [
    "requests",  # Add any required dependencies here
]

# Package classifiers
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",  # Added Python 3.11 support
]

# Package entry points and package discovery
packages = find_packages()

# Read the long description from a separate file
with open("README.md", "r") as f:
    long_description = f.read()

# Package setup
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify the content type
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    install_requires=install_requires,
    classifiers=classifiers,
    packages=find_packages(),
)
