from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'One of several packages for checking dependency resolvers.'
LONG_DESCRIPTION = 'A function to get the top n items in a list. It is not intended for actual use, but for demontrating version compatibility issues.'

# Setting up
setup(
    name="topngetterkpanger882",
    version=VERSION,
    author="EldritchToast",
    author_email="<kpanger88@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["listmakerkpanger882==0.0.2"],
    keywords=['python', 'dependency','test', 'list'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
