# encoding: utf-8

import gvsig
reload(gvsig)
from org.apache.commons.math3.stat.correlation import Covariance
import random

def main(*args):

    #x = [float(random.random()) for i in xrange(1000)]
    #y = [float(random.random()) for i in xrange(1000)]
    #print x
    flayer = gvsig.currentLayer().features()

    import time
    now = time.time()
    x = [f.VIA for f in flayer]
    y = [f.NUMERO for f in flayer]
    c = Covariance().covariance(x,y)
    print time.time()-now
    print "Covarianze: ", c
