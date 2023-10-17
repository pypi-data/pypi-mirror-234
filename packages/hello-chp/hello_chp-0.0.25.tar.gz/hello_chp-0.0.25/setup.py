import codecs

from setuptools import find_packages, setup

DISTNAME = "hello_chp"
VERSION = "0.0.25"
DESCRIPTION = "A Python library for optimal data imputation."
LONG_DESCRIPTION_CONTENT_TYPE = "text/x-rst"
with codecs.open("README.rst", encoding="utf-8-sig") as f:
    LONG_DESCRIPTION = f.read()


LICENSE = "new BSD"
AUTHORS = """
Hong-Lan Botterman,
Julien Roussel,
Thomas Morzadec,
Rima Hajou,
Firas Dakhli,
Anh Khoa Ngo Ho,
Charles-Henri Prat
"""
AUTHORS_EMAIL = """
hlbotterman@quantmetry.com,
jroussel@quantmetry.com,
tmorzadec@quantmetry.com,
rhajou@quantmetry.com,
fdakhli@quantmetry.com,
angoho@quantmetry.com,
chprat@quantmetry.com
"""
URL = "https://github.com/Quantmetry/qolmat"
DOWNLOAD_URL = "https://pypi.org/project/qolmat/#files"
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/Quantmetry/qolmat",
    "Documentation": "https://qolmat.readthedocs.io/en/latest/",
    "Source Code": "https://github.com/Quantmetry/qolmat",
}

PYTHON_REQUIRES = ">=3.8"
PACKAGES = find_packages()
INSTALL_REQUIRES = [
    "dcor>=0.6",
    "hyperopt",
    "numpy>=1.19",
    "packaging",
    "pandas>=1.3",
    "scikit-learn",
    "scipy",
    "statsmodels>=0.14",
]
EXTRAS_REQUIRE = {
    "tests": ["flake8", "mypy", "pandas", "pytest", "pytest-cov", "typed-ast"],
    "docs": [
        "numpydoc",
        "sphinx",
        "sphinx-gallery",
        "sphinx_rtd_theme",
        "typing_extensions",
    ],
    "pytorch": [
        "torch==2.0.1",
    ],
}

CLASSIFIERS = [
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "License :: OSI Approved",
    "Topic :: Software Development",
    "Topic :: Scientific/Engineering",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]


setup(
    name=DISTNAME,
    version=VERSION,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    url=URL,
    download_url=DOWNLOAD_URL,
    project_urls=PROJECT_URLS,
    packages=PACKAGES,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=CLASSIFIERS,
)
