from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'A basic package with handy function for lab work, made for Jupyter Notebooks'
LONG_DESCRIPTION = 'A package with utility functions to make using python in the lab faster, specifically for the Complutense University of Madrid Physics Bachelor.'

# Setting up
setup(
    name="labhelper",
    version=VERSION,
    author="Batres (Javier Batres)",
    author_email="<javibatresdc@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=['scipy', 'pandas', 'numpy', 'sympy', 'IPython', 'pyperclip'],
    keywords=['python', 'data analysis', 'lab', 'data', 'symbolic'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.5",
        "Framework :: Jupyter",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
