import mdbrun
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="markerdb",
    version=mdbrun.VERSION,
    author="Aswathy Sebastian",
    author_email="aswathyseb@gmail.com",
    description="markerdb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aswathyseb/markerdb",
    packages=find_packages(include=["mdbrun", "mdbrun.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'plac',

    ],

    entry_points={
        'console_scripts': [
            'markerdb=mdbrun.__main__:main',
        ],
    },

    python_requires='>=3.6',

)
