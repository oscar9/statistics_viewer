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
from org.jfree.data.statistics import DefaultBoxAndWhiskerCategoryDataset
from org.jfree.data.general import DatasetUtilities
from org.jfree.chart import ChartFactory
from org.jfree.chart.axis import NumberAxis
import random

class StatProcess(AbstractStatisticProcess):
    name = u"Box and Whisker"
    description = "Box and Whisker Description"
    idprocess = "box-and-whisker-1"
    allowZoomProcess = False
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("BoxAndWhiskerParameters", "BoxAndWhiskerParametersProperties", "Description")
        params.addDynFieldString("Layer").setMandatory(True)
        #params.addDynFieldString("Field X").setMandatory(True)
        #params.addDynFieldString("Field Y").setMandatory(True)
        
    def process(self, params):
        # Get initial parameters
        param_layer = params.get("Layer")
        param_x = "pob0_14" #params.get("Field X")
        param_y = "pob15_65"
        param_z = "pob66_mas"
        #param_y = params.get("Field Y")

        layer = gvsig.currentView().getLayer(param_layer)

        # dataset
        SERIES_COUNT = 1
        CATEGORY_COUNT = 1
        VALUE_COUNT = 4000
        result = DefaultBoxAndWhiskerCategoryDataset()

        # Numeric fields
        sch = layer.getSchema()
        listFields = []
        listValues = {}
        # get potential numeric fields
        for field in sch:
            dt = field.getDataTypeName()
            if dt=="Integer" or dt=="Long" or dt=="Double":
                listFields.append(field.getName())
                listValues[field.getName()] = list()

        for f in layer.features():
            for field in listFields:
                prev = listValues[field]
                value = f.get(field)
                prev.append(value)
                listValues[field] = prev 

        for k in listValues.keys():
            result.add(listValues[k], k, "")

        # Create chart
        #chart = createChart(result)
        chart = ChartFactory.createBoxAndWhiskerChart(
                "", "", "", result,
                True)
        plot = chart.getPlot()
        plot.setDomainGridlinesVisible(True)
        plot.setRangePannable(True)

        rangeAxis = plot.getRangeAxis()
        rangeAxis.setStandardTickUnits(NumberAxis.createIntegerTickUnits())
        
        # Create panel from chart
        panel = createPanel(chart)
        #panel = createPanel(chart)
        self.setOutputPanel(panel)
        self.console = u"** Box And Whisker **"
        

def main(*args):
    print "* stat14.py: Box And Whisker"

    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Layer", "pob")
    #dynobject.setDynValue("Field X", "LONGITUDE")
    #dynobject.setDynValue("Field Y", "LATITUDE")
    proc.process(dynobject.getValues())
    print proc.getOutputConsole()
    panel =  proc.getOutputPanel()
    print panel
