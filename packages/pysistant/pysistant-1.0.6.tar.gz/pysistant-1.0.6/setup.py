# pylint: disable=line-too-long, invalid-name, missing-docstring

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setuptools.setup(
    name="pysistant",
    version="1.0.6",
    author="Eugene Ilyushin",
    author_email="eugene.ilyushin@gmail.com",
    description="The package contains different helpers for speeding up programming on Python.",
    long_description="The package contains different helpers for speeding up programming on Python.",
    long_description_content_type="text/markdown",
    url="https://github.com/Ilyushin/pysistant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements
)
