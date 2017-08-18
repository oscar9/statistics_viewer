# encoding: utf-8

import gvsig
from gvsig.uselib import use_jars
import os

def main(*args):

    print "***** LOADED STATISTICS VIEWER ******"
    use_jars(os.path.dirname(__file__),"libs", True)