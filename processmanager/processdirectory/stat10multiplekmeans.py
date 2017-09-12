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
from org.apache.commons.math3.ml.clustering import MultiKMeansPlusPlusClusterer

class StatProcess(AbstractStatisticProcess):

    name = u"Multiple Correction of Clustering Kmeans Plus Plus"
    description = "Multiple K means plus plus: this process requieres a point layer"
    idprocess = "multiplekmeans-plus-plus-1"
    allowZoomProcess = True
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("MultipleKmeansPlusParameters", 
                                            "MultipleKmeansPlusParametersProperties", 
                                            "Description")
        params.addDynFieldString("Layer").setMandatory(True)
        params.addDynFieldInt("Clusters").setMandatory(True) 
        params.addDynFieldInt("MaxIterations").setMandatory(True)
        params.addDynFieldInt("Trials").setMandatory(True)
        
        
    def process(self, params):
        param_layer = params.get("Layer")
        param_iterations = params.get("Clusters")
        param_trials = params.get("Trials")
        param_maxiterations = params.get("MaxIterations")
        
        #from org.apache.commons.math3.ml.distance import EarthMoversDistance
        #distance = EarthMoverDistance(
        
        layer = gvsig.currentView().getLayer(param_layer)
        features = layer.features()
        
        #colection = ArrayList()
        colection = []
        for n,f in enumerate(features):
            dp = DoublePoint([f.geometry().getX(), f.geometry().getY()])
            colection.append(dp)
        kppc = KMeansPlusPlusClusterer(param_iterations, param_maxiterations)
        #print "Kppc:", kppc, type(kppc)
        mk = MultiKMeansPlusPlusClusterer(kppc, param_trials)
        
        clusters = mk.cluster(colection)

        newschema = gvsig.createFeatureType()
        newschema.append("ID", "INTEGER", 5)
        newschema.append("GEOMETRY", "GEOMETRY")
        newschema.get("GEOMETRY").setGeometryType(geom.POINT, geom.D2)
        newlayer = gvsig.createShape(newschema)
        
        for n, cluster in enumerate(clusters):
            for doublepoint in cluster.getPoints():
                point = doublepoint.getPoint()
                values = {}
                values["ID"] = n
                values["GEOMETRY"] = geom.createPoint(geom.D2, point[0], point[1])
                newlayer.append(values)
        
        newlayer.commit()
        gvsig.currentView().addLayer(newlayer)

        self.console = u"** Análisis Multiple KMeansPlusPlus, iterations: " + str(param_iterations)
        

def main(*args):
    print "* stat10.py: Multiple K Means Plus Plus"
    #print "\ndir:", dir()
    #print sys.path
    #import os
    
    #return
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Layer", "V")
    dynobject.setDynValue("Clusters", 5)
    dynobject.setDynValue("MaxIterations", 10)
    dynobject.setDynValue("Trials", 10)
    print dynobject.getValues()
    
    proc.process(dynobject.getValues())
    print proc.getOutputConsole()