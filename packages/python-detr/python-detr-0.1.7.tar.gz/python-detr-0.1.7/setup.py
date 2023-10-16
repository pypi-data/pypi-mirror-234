import os
import pathlib

import pkg_resources
from setuptools import find_packages
from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

version = "0.1.7"

requirements = []
with pathlib.Path("requirements.txt").open() as requirements_txt:
    requirements = [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]

setup(
    name="python-detr",
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/facebookresearch/detr",
    author="facebookresearch",
    packages=find_packages(),
    include_package_data=True,
    package_dir={"": "."},
    python_requires=">=3.8",
    install_requires=requirements,
    zip_safe=False,
    dependency_links=[
        "https://download.pytorch.org/whl/torch_stable.html",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)