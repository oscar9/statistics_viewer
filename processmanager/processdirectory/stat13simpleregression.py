# encoding: utf-8
import sys
import gvsig
from gvsig import geom
import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)
import addons.statistics_viewer.sv
reload(addons.statistics_viewer.sv)

from addons.statistics_viewer.sv.svScatterPlot import createPanelMouseListener, createChart, createPanel
from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
from addons.statistics_viewer.sv import svgraph
from org.apache.commons.math3.stat.regression import SimpleRegression
from org.jfree.data.function import LineFunction2D
from org.jfree.data.general import DatasetUtilities
from org.jfree.chart.renderer.xy import XYLineAndShapeRenderer
from java.awt import Color

class StatProcess(AbstractStatisticProcess):

    name = u"Simple Regression"
    description = "Simple Regression Description"
    idprocess = "simple-regression-1"
    allowZoomProcess = False
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("SimpleRegressionParameters", "SimpleRegressionParametersProperties", "Description")
        params.addDynFieldString("Layer").setMandatory(True)
        params.addDynFieldString("Field X").setMandatory(True)
        params.addDynFieldString("Field Y").setMandatory(True)
        
    def process(self, params):
        # Get initial parameters
        param_layer = params.get("Layer")
        param_x = params.get("Field X")
        param_y = params.get("Field Y")

        layer = gvsig.currentView().getLayer(param_layer)

        # math3: Simple regression
        sr = SimpleRegression()
        # y = intercept + slope * x
        for f in layer.features():
            fx = f.get(param_x)
            fy = f.get(param_y)
            sr.addData(fx,fy)
            #collection.append([fx,fy])
        intercept = sr.getIntercept()
        slope = sr.getSlope()
        coefficients = [intercept, slope]
        ## JFC
        curve = LineFunction2D(coefficients[0], coefficients[1])
        regressionData = DatasetUtilities.sampleFunction2D(curve, -150.0, 150.0, 100, "Fitted Regression Line")
        
        
        jfcCollection = self.getUtils().assignLayerFields2XYCollection(layer, "points", param_x, param_y)
        #jfcCollection = self.getUtils().mlGetJfcCollectionFromClusters(layer, collection, param_x, param_y)
        
        # Extract color of the values to set to the legend
        chart = createChart(jfcCollection, param_x, param_y) # Create chart jfcCollection
        plot = chart.getPlot()
        plot.setDataset(1, regressionData)
        renderer2 = XYLineAndShapeRenderer(True, False)
        renderer2.setSeriesPaint(0, Color.blue)
        plot.setRenderer(1, renderer2)
        panel = createPanelMouseListener(chart) # Create Panel using the functionality of svCollection selection allowed
        #panel = createPanel(chart)
        self.setOutputPanel(panel)
        self.console = u"** Análisis Simple Regression **"
        self.console += "y = "+str(intercept)+" + "+str(slope)+" * x"
        

def main(*args):
    print "* stat13.py: Simple Regression"

    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Layer", "V")
    dynobject.setDynValue("Field X", "LONGITUDE")
    dynobject.setDynValue("Field Y", "LATITUDE")
    proc.process(dynobject.getValues())
    print proc.getOutputConsole()
    panel =  proc.getOutputPanel()
    print panel
