# -*- coding: UTF-8 -*-

import setuptools
from setuptools import setup, find_packages

# read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nokia_ont_port_finder",
    version="0.0.5",
    author="David Johnnes",
    author_email="david.johnnes@gmail.com",
    description=("Network Automation and Programmability Abstraction "
                 "Layer for NOKIA OLT and ONT PORT FINDER"),
    keywords="NOKIA ONT PORT FINDER",
    url="",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
    include_package_data=True,
    install_requires=('sshFRIEND'),
)   
