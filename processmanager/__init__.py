import os

__all__ = []

def main(*args):
    dirs = getResource(__file__)
    print dirs
    for p in dirs:
        if p.endswith(".py") and p.startswith("stat"):
            __all__.append(p.split(".")[0])
    print __all__