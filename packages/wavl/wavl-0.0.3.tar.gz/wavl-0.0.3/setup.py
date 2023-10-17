import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wavl",
    version="0.0.3",
    author="synterweyst",
    author_email=os.getenv("EMAIL"), # dont worry about this
    description="bestest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wavl.top",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)