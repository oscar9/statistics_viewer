# encoding: utf-8
import sys
import gvsig
from gvsig import geom
import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
from addons.statistics_viewer.sv import svgraph
from org.apache.commons.math3.ml.clustering import KMeansPlusPlusClusterer
from java.util import ArrayList
from org.apache.commons.math3.ml.clustering import DoublePoint
from org.apache.commons.math3.ml.distance import EarthMoversDistance

class gvDoublePoint(DoublePoint):
    feature = None
    def __init__(self, feature):
        x = feature.geometry().getX()
        y = feature.geometry().getY()
        DoublePoint.__init__(self, [x,y])
        self.feature = feature
        
    def getFeature(self):
        return self.feature

class StatProcess(AbstractStatisticProcess):

    name = u"Clustering Kmeans Plus Plus"
    description = "K means plus plus"
    idprocess = "kmeans-plus-plus-1"
    allowZoomProcess = True
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("KmeansPlusParameters", "KmeansPlusParametersProperties", "Description")
        params.addDynFieldString("Layer").setMandatory(True)
        params.addDynFieldInt("Iterations").setMandatory(True) 
        
        
    def process(self, params):
        param_layer = params.get("Layer")
        param_iterations = params.get("Iterations")

        #distance = EarthMoversDistance
        
        #distance.compute([0.0,0.0], [1.0,1.0])
        #d = 5
        #d = distance#.getClass()

        kppc = KMeansPlusPlusClusterer(param_iterations, 5) #, m)
        layer = gvsig.currentView().getLayer(param_layer)
        features = layer.features()

        #colection = ArrayList()
        colection = []
        for n,f in enumerate(features):
            #dp = DoublePoint([f.geometry().getX(), f.geometry().getY()])
            dp = gvDoublePoint(f.getCopy())
            colection.append(dp)
        clusters = kppc.cluster(colection)
        
        newschema = gvsig.createFeatureType(layer.getSchema())
        newschema.append("IDCLUSTER", "INTEGER", 5)
        #newschema.append("GEOMETRY", "GEOMETRY")
        #newschema.get("GEOMETRY").setGeometryType(geom.POINT, geom.D2)
        newlayer = gvsig.createShape(newschema)
        
        for n, cluster in enumerate(clusters):
            for doublepoint in cluster.getPoints():
                feature = doublepoint.getFeature()
                values = feature.getValues()
                values["IDCLUSTER"] = n
                point = doublepoint.getPoint()
                values["GEOMETRY"] = geom.createPoint(geom.D2, point[0], point[1])
                newlayer.append(values)
        
        newlayer.commit()
        gvsig.currentView().addLayer(newlayer)

        self.console = u"** Análisis KMeansPlusPlus **\n"
        self.console += "iterations: " + str(kppc.getMaxIterations()) + "\n"
        self.console += "clusters: "+ str(kppc.getK())
        

def main(*args):
    print "* stat9.py: Kmeans Plus Plus"
    #print "\ndir:", dir()
    #print sys.path
    #import os
    
    #return
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Layer", "V")
    dynobject.setDynValue("Iterations", 5)
    
    proc.process(dynobject.getValues())
    print proc.getOutputConsole()