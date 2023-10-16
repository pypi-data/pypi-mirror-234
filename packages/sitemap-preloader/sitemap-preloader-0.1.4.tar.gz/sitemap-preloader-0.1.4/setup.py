from setuptools import setup, find_packages

# Package metadata
name = "sitemap-preloader"
version = "0.1.4"
description = "This package is used to read a sitemap and fetch all the urls in order to warm the cache of a website"
author = "Andres Gonzalez"
author_email = "code@andresgz.com"
url = "https://github.com/andresgz/sitemap-preloader"

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

install_requires = [
    "requests",
    "beautifulsoup4",
    "validators",
    "lxml",
]

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url=url,
    py_modules=["preloader"],
    classifiers=classifiers,
    install_requires=install_requires,
)
