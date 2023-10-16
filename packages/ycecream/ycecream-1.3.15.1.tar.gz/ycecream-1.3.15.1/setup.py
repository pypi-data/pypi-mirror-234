from setuptools import setup

with open("readme.md", "r") as f:
    long_description = f.read()

i0 = long_description.index("# Introduction")
i1 = long_description.index("# Table of contents")
i2 = long_description.index("# Installation")
long_description = long_description[i0:i1] + long_description[i2:]

setup(
    name="ycecream",
    packages=["ycecream"],
    version="1.3.15.1",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="ycecream",
    author="Ruud van der Ham",
    author_email="info@salabim.org",
    url="https://github.com/salabim/ycecream",
    download_url="https://github.com/salabim/ycecream",
    keywords=["debugging", "utility", "tool", "benchmarking"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
