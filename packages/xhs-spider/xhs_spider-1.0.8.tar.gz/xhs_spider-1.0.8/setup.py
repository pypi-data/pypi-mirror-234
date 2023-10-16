import codecs
import os

from setuptools import find_packages, setup

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.0.8'
DESCRIPTION = 'Little Red Book notes, home page, detailed page crawler'
LONG_DESCRIPTION = 'Little Red Book notes, home page, detailed page crawler'

# Setting up
setup(
    name="xhs_spider",
    version=VERSION,
    author="cv_cat",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['PyExecJS', 'requests'],
    keywords=['python', 'xhs', 'spider'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)