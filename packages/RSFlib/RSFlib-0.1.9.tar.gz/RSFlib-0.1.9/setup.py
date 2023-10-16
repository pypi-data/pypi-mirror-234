from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.9'
DESCRIPTION = 'Useful functions and constants for Fyzing struggle'
LONG_DESCRIPTION = 'A package that helped me at University - Radim Slovák, VUT.'

# Setting up
setup(
    name="RSFlib",
    version=VERSION,
    author="Radzym (Radim Slovák)",
    author_email="<slovak.radim@seznam.cz>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'data analysis', "physics"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)