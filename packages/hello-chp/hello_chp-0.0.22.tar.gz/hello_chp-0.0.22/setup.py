import os
import codecs

from setuptools import setup, find_packages

with codecs.open("README.rst", encoding="utf-8-sig") as f:
    LONG_DESCRIPTION = f.read()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


URL = "https://github.com/Quantmetry/qolmat"
DOWNLOAD_URL = "https://pypi.org/project/qolmat/#files"
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/Quantmetry/qolmat",
    "Documentation": "https://qolmat.readthedocs.io/en/latest/",
    "Source Code": "https://github.com/Quantmetry/qolmat",
}
VERSION = "0.0.22"

setup(
    name="hello_chp",
    version=VERSION,
    author="Grégoire Martinon, Vianney Taquet, Damien Hervault",
    author_email="gmartignon@quantmetry.com",
    description="A Quantmetry tutorial on how to publish an opensource python package.",
    license="BSD",
    keywords="example opensource tutorial",
    url=URL,
    packages=find_packages(),
    install_requires=["numpy>=1.20"],
    extras_require={
        "tests": ["flake8", "mypy", "pytest-cov"],
        "docs": ["sphinx", "sphinx-gallery", "sphinx_rtd_theme", "numpydoc"],
    },
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
