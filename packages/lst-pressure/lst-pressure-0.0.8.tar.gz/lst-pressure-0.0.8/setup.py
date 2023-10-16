from setuptools import setup, find_packages
import json
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_install_requires():
    here = os.path.abspath(os.path.dirname(__file__))
    pipfile_path = os.path.join(here, "Pipfile.lock")

    with open(pipfile_path) as f:
        pipfile_json = json.load(f)
    return [
        package + info.get("version", "")
        for package, info in pipfile_json["default"].items()
    ]


setup(
    name="lst-pressure",
    version="0.0.8",
    description='Determine periods of "LST pressure" by querying for intersections between LST/Solar intervals',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ska-sa/lst-pressure",
    author="Zach Smith",
    author_email="zsmith@sarao.ac.za",
    license="Apache 2.0",
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    package_dir={},
    packages=find_packages(),
    install_requires=get_install_requires(),
    python_requires=">=3.8",
)
