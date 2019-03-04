# encoding: utf-8
import sys
import gvsig
from gvsig import geom
import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)
import addons.statistics_viewer.sv
reload(addons.statistics_viewer.sv)

from addons.statistics_viewer.sv.svScatterPlot import createPanelMouseListener, createChart
from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
from addons.statistics_viewer.sv import svgraph

from org.apache.commons.math3.ml.clustering import FuzzyKMeansClusterer
from java.util import ArrayList
#from org.apache.commons.math3.ml.clustering import DoublePoint
from org.apache.commons.math3.ml.distance import EarthMoversDistance
from org.apache.commons.math3.ml.distance import EuclideanDistance

from org.jfree.data.xy import XYDataItem, XYSeries, XYSeriesCollection, XYDataset


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

        layer = gvsig.currentView().getLayer(param_layer) # Acceso capa
        
        # Choose new cluster field name
        fieldcluster = "IDK"
        newfieldcluster = self.getUtils().getUniqueSchemaField(layer, fieldcluster)
        
        # Collect points
        collection = self.getUtils().mlGetXYClusterableCollectionFromLayer(layer, param_field1, param_field2)
        
        # Distance method
        dd = EarthMoversDistance()
        #dd = EuclideanDistance().getClass

        # Algorithm Fuzzykmeansclusterer
        fkppc = FuzzyKMeansClusterer(param_clusters, param_fuzziness, param_maxIterations, dd)
        clusters = fkppc.cluster(collection)

        # Output shape with cluster values
        newschema = gvsig.createFeatureType(layer.getSchema())
        newlayer = self.getUtils().mlGetLayerFromXYClusters(newschema, clusters, newfieldcluster)

        # Create collection for JFChart related to a layer
        jfcCollection = self.getUtils().mlGetJfcCollectionFromClusters(newlayer, clusters, param_field1, param_field2)
        
        gvsig.currentView().addLayer(newlayer)
        
        # Extract color of the values to set to the legend
        chart = createChart(jfcCollection, param_field1, param_field2) # Create chart
        panel = createPanelMouseListener(chart) # Create Panel using the functionality of svCollection selection allowed

        # Set output panel
        self.setOutputPanel(panel)

        # Process legend
        gvsig_legend = self.getUtils().chart2legend_UniqueValue(chart, newfieldcluster)

        newlayer.setLegend(gvsig_legend)

        self.console = u"** Analysis KMeansPlusPlus **"
        self.console += "\niterations: " + str(fkppc.getMaxIterations())
        self.console += "\nclusters: "+ str(fkppc.getK())
        self.console += "\nFuzzines: " + str(fkppc.getFuzziness())
        self.console += "\nEpsilon: " + str(fkppc.getEpsilon())
        for n,cluster in enumerate(clusters):
            self.console += "\n\tCluster id: " + str(n) + " center: " + str(cluster.getCenter())
        

def main(*args):
    print "* stat11.py: Fuzzy K Means"

    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Layer", "VV")
    dynobject.setDynValue("Clusters", 5)
    dynobject.setDynValue("Fuzziness", 2)
    dynobject.setDynValue("MaxIterations", 1)
    dynobject.setDynValue("Field X", "BRIGHT_TI4")
    dynobject.setDynValue("Field Y", "FRP")
    proc.process(dynobject.getValues())
    print proc.getOutputConsole()
    panel =  proc.getOutputPanel()
