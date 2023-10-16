import os

from .__version__ import __version__


def srcmap():
    folder = os.path.dirname(__file__)
    folder = os.path.abspath(folder).replace('\\', '/')
    return folder
