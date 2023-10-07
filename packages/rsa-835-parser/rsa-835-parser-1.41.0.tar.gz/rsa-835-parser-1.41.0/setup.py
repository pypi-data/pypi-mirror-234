""" Setup file for rsa-835-parser """
from setuptools import setup, find_packages

VERSION = "1.41.0"
DESCRIPTION = "B Consulting Group EDI 835 file format parser."
LONG_DESCRIPTION = (
    "B Consulting EDI 835 file format parser, extending the Keiron Stoddart version."
)

install_requires = ["pandas"]

tests_require = ["pytest"]

setup(
    name="rsa-835-parser",
    version=VERSION,
    author="Roberto Suarez",
    author_email="<robsua68@hotmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=install_requires,
    url="https://github.com/robsua68/bcg-835-parser",
    keywords=["python", "EDI", "835", "X12"],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    tests_require=tests_require,
    python_requires=">=3.11.5",
)
