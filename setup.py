import sys
import subprocess
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="ExampleFlaskAPI",
    version="1.0.0",
    author="Łukasz Ozyp",
    author_email="lukasz.ozyp.contact@gmail.com",
    description="An API project built using Flask, based on interactions with MongoDb.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    tests_require=[ 
        'pytest',
    ],
    test_suite="tests/unit",
    url="https://github.com/aventgz/ExampleFlaskAPI",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'ExampleFlaskAPI = ExampleFlaskAPI.example.main:main',
        ],
    },
    install_requires=requirements,
)
