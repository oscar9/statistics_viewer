# encoding: utf-8

import gvsig
from org.apache.commons.math3.stat.descriptive import SummaryStatistics
import random

def main(*args):

    ss = SummaryStatistics()
    for i in xrange(10000000):
        d = random.random()
        ss.addValue((1000000-i)*d)
        ss.addValue(i)

    print "Summary Statistics: "
    print ss.getGeoMeanImpl()
    print ss.getGeometricMean()
    print ss.getMax()
    print ss.getMin()
    print ss.getN()
    print ss.getPopulationVariance()
    print ss.getQuadraticMean()
    print ss.getSecondMoment()
    print ss.getStandardDeviation()
    print ss.getSum()
    print ss.getVariance()
    print ss.getSumsq()
