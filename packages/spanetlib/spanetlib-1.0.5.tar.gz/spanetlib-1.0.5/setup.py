from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="spanetlib",
    version="1.0.5",
    author="spanet",
    author_email="en@herontechnology.co.nz",
    description="A package that handles communication with SpaNET Spas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enheron/spanet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)