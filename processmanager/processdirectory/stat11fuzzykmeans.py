# encoding: utf-8
import sys
import gvsig
from gvsig import geom
import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)
import addons.statistics_viewer.sv
reload(addons.statistics_viewer.sv)

from addons.statistics_viewer.sv.svScatterPlot import createPanel, svXYSeriesCollection, createChart
from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess
from org.gvsig.symbology.fmap.mapcontext.rendering.legend.impl import VectorialUniqueValueLegend

import os
from addons.statistics_viewer.sv import svgraph
from org.apache.commons.math3.ml.clustering import FuzzyKMeansClusterer
from java.util import ArrayList
from org.apache.commons.math3.ml.clustering import DoublePoint
from org.apache.commons.math3.ml.distance import EarthMoversDistance
from org.apache.commons.math3.ml.distance import EuclideanDistance
from org.apache.commons.math3.ml.clustering import Clusterable
from org.jfree.data.xy import XYDataItem, XYSeries, XYSeriesCollection, XYDataset


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

class StatProcess(AbstractStatisticProcess):

    name = u"Clustering Fuzzy Kmeans"
    description = "Fuzzy K means"
    idprocess = "fuzzy-kmeans-1"
    allowZoomProcess = False
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("FuzzyKmeansParameters", "FuzzyKmeansParametersProperties", "Description")
        params.addDynFieldString("Layer").setMandatory(True)
        params.addDynFieldInt("Clusters").setMandatory(True) 
        params.addDynFieldInt("Fuzziness").setMandatory(True)
        params.addDynFieldInt("MaxIterations").setMandatory(True)
        params.addDynFieldString("Field X").setMandatory(True)
        params.addDynFieldString("Field Y").setMandatory(True)
        
    def process(self, params):
        # Get initial parameters
        param_layer = params.get("Layer")
        param_clusters = params.get("Clusters")
        param_fuzziness = params.get("Fuzziness")
        param_maxIterations = params.get("MaxIterations")
        param_field1 = params.get("Field X")
        param_field2 = params.get("Field Y")
        newfieldcluster = "IDCLUSTER"
        
        layer = gvsig.currentView().getLayer(param_layer)
        features = layer.features()
        
        # Collect points
        colection = []
        for n,f in enumerate(features):
            f1 = float(f.get(param_field1))
            f2 = float(f.get(param_field2))
            #dp = DoublePoint([f1,f2])
            dp = gvDoublePoint(f.getCopy(), param_field1, param_field2)
            colection.append(dp)
        # Distance method
        dd = EarthMoversDistance()
        #dd = EuclideanDistance().getClass

        # Algorithm Fuzzykmeansclusterer
        fkppc = FuzzyKMeansClusterer(param_clusters, param_fuzziness, param_maxIterations, dd)
        clusters = fkppc.cluster(colection)

        # Output shape with cluster values
        newschema = gvsig.createFeatureType(layer.getSchema())
        newschema.append(newfieldcluster, "INTEGER", 5)

        newlayer = gvsig.createShape(newschema)

        collection = svXYSeriesCollection(param_field1, param_field2)
        for n, cluster in enumerate(clusters):
            # Series
            for doublepoint in cluster.getPoints():
                feature = doublepoint.getFeature()
                values = feature.getValues()
                values[newfieldcluster] = n
                point = doublepoint.getPoint()
                fx = feature.geometry().getX()
                fy = feature.geometry().getY()
                values["GEOMETRY"] = geom.createPoint(geom.D2, fx, fy)
                newlayer.append(values)
                collection.addValues(str(n), point[0], point[1])
        
        newlayer.commit()
        collection.updateSeries()
        collection.setLayer(newlayer)
        # Extract color of the values to set to the legend
        chart = createChart(collection, param_field1, param_field2)
        legend = chart.getPlot().getLegendItems()
        items = {}
        vuvl = VectorialUniqueValueLegend(geom.POINT)
        for i in xrange(0, legend.getItemCount()):
            item = legend.get(i)
            yy = gvsig.simplePointSymbol(item.getFillPaint())
            label = str(item.getLabel())
            yy.setDescription(str(label))
            yy.setColor(item.getFillPaint())
            print "Label: ", int(label), yy
            vuvl.addSymbol(int(label), yy)
        vuvl.setClassifyingFieldNames([newfieldcluster])

        panel = createPanel(collection, param_field1, param_field2)


        newlayer.setLegend(vuvl)
        gvsig.currentView().addLayer(newlayer)
        #dp = createDemoPanel(newlayer, "LATITUDE", "LONGITUDE")
        self.setOutputPanel(panel)
        self.console = u"** Análisis KMeansPlusPlus **"
        self.console += "\niterations: " + str(fkppc.getMaxIterations())
        self.console += "\nclusters: "+ str(fkppc.getK())
        self.console += "\nFuzzines: " + str(fkppc.getFuzziness())
        self.console += "\nEpsilon: " + str(fkppc.getEpsilon())
        

def main(*args):
    print "* stat1.py: process"
    #print "\ndir:", dir()
    #print sys.path
    #import os
    
    #return
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Layer", "V")
    dynobject.setDynValue("Clusters", 5)
    dynobject.setDynValue("Fuzziness", 2)
    dynobject.setDynValue("MaxIterations", 1)
    dynobject.setDynValue("Field X", "BRIGHT_TI4")
    dynobject.setDynValue("Field Y", "FRP")
    proc.process(dynobject.getValues())
    print proc.getOutputConsole()
    panel =  proc.getOutputPanel()
    #print "**panel: ", panel, type(panel), dir(panel)
    pass