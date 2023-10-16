from setuptools import setup, find_packages
import codecs
import os

#here = os.path.abspath(os.path.dirname(__file__))

#with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Goodbye message for Carl'
LONG_DESCRIPTION = 'Goodbye message for Carl leaving Aginic'

# Setting up
setup(
    name="byecarl",
    version=VERSION,
    author="Jordan",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'carl', 'message', 'bye', 'goodbye'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
