from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="flexopus",
    version="v0.0.3",
    author="Sebi Nemeth",
    author_email="sebezhetetlen98@gmail.com",
    description="Python package to interact with th Flexopus API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flexopus/flexopus-python-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aiohttp',
    ],
)