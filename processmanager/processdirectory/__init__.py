import os

from gvsig import getResource

__all__ = []
dirs = os.listdir(getResource(__file__))
__instances__ = []
for p in dirs:
    if p.endswith(".py") and p.startswith("stat"):
        __all__.append(p.split(".")[0])
            

from . import *

def main(*args):
    print "hola"
    print __instances__