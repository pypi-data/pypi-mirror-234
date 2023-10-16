import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="general-utils-juan-palma-borda",
    version="0.2.0",
    author='Juan Palma Borda',
    author_email='juanpalmaborda@hotmail.com',
    description='Group of general utils from different projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muerterauda/general-utils",
    project_urls={
        "Bug Tracker": "https://github.com/muerterauda/general-utils/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
