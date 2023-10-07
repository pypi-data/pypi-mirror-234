from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Python modules for scripting in RayStation'
LONG_DESCRIPTION = 'Python modules for scripting in RayStation'

# Setting up
setup(
    name="rsich",
    version=VERSION,
    author="isadorap (Isadora Platoni)",
    author_email="<isadora.platoni@nhs.net>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'raystation', 'radiotherapy', 'pylinac', 'imperial college', 'medical physics'],
    classifiers=[
        "Programming Language :: Python :: 3",
	    "License :: OSI Approved :: MIT License",
	    "Operating System :: OS Independent"
    ]
)