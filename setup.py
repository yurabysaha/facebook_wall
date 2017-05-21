from distutils.core import setup
import py2app

from setuptools import setup
setup(
    app=["ui/main.py"],
    setup_requires=["py2app"],
)