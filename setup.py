import setuptools
from setuptools import find_packages

setuptools.setup(
    name="mustachify",
    version="0.0.1",
    author="DonQueso89",
    author_email="kg.v.ekeren@gmail.com",
    description="Mustahcify",
    long_description_content_type="text/markdown",
    url="https://github.com/Ricoter/Mustachify",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["deps*", "mustachify"]),
    python_requires=">=3.7",
    package_data={"mustachify/static": "*"},
)
