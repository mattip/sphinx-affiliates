from os import path
import re
from setuptools import setup


def get_version():
    text = open(path.join(path.dirname(__file__), "sphinx_affiliates", "__init__.py")).read()
    match = re.compile(r"^__version__\s*\=\s*[\"\']([^\s\'\"]+)", re.M).search(text)
    return match.group(1)


with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="sphinx-affiliates",
    version=get_version(),
    description="Tools for integrating affiliated Sphinx sites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="mattip",
    author_email="mattigit@picus.org.il",
    packages=["sphinx_affiliates"],
    include_package_data=True,
    url="https://github.com/mattip/sphinx-affiliates",
    license="MIT",
    python_requires="==2.7,>=3.6",
    install_requires=["sphinx>=1.8.5,<6"],
    extras_require={
        "testing": [
            "coverage",
            "pytest",
            "pytest-cov",
            "sphinx_testing",
        ],
        "code_style": ["pre-commit==2.6"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python",
        "Topic :: Documentation :: Sphinx",
    ],
)

