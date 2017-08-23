# encoding: utf-8

import gvsig
from org.apache.commons.math3.ml.clustering import Clusterable

class gvDoublePoint(Clusterable): #DoublePoint):
    feature = None
    location = None
    f1 = None
    f2 = None
    def __init__(self, feature, f1, f2):
        #self.x = feature.geometry().getX()
        #self.y = feature.geometry().getY()
        self.f1 = f1
        self.f2 = f2
        #location = feature.geometry()
        #DoublePoint.__init__(self, [x,y])
        self.feature = feature
    def getLocation(self):
        return self
    def getX(self):
        return self.feature.get(self.f1)
    def getY(self):
        return self.feature.get(self.f2)
    def getPoint(self):
        return [self.getX(), self.getY()]
    def getFeature(self):
        return self.feature
        
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    pass
