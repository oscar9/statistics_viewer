# encoding: utf-8

import gvsig
from gvsig import getResource

import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
from addons.statistics_viewer.sv import svgraph
from org.gvsig.tools.dynobject import DynField, DynObject

class ChartService(DynField, DynObject):

    def __init__(self):
        pass

    def getDynValue(self):
        return ""
        
class StatProcess(AbstractStatisticProcess):

    name = "Test Statatistic Graph 1"
    description = "Age calculation"
    idprocess = "view-graph-example-1"
    allowZoomProcess = True
    
    def processParameters(self): #o: dynclass
        #dynxml = getResource(__file__, "SHPParameters.xml")
        #dynclass = self.createDynClass(dynxml)
        
        manager = self.getToolsLocator().getDynObjectManager()
        #mydata = manager.createDynObject("MyStruct")
        
        #dynclass = manager.get("Process","ProcessProperties")
        #if dynclass == None: 
        #dynclass = manager.createDynClass("Process", "ProcessProperties", "aqui va la descripcion")
        params = self.createInputParameters("Process", "ProcessProperties", "Description")
        #dynclass.addDynFieldString("name").setMandatory(False)
        #dynclass.addDynFieldString("title").setMandatory(True)
        #dynclass.addDynFieldString("type").setMandatory(True)
        #dynclass.addDynFieldBoolean("Min").setMandatory(True)
        params.addDynFieldInt("Exageration").setMandatory(True) 
        
        di = params.addDynFieldObject("service12")
        di.setClassOfValue(ChartService)
        di.setDefaultDynValue([1,4])
        
        #manager.add(dynclass)
          
        #return dynclass
        
    def process(self, params):
        print "* params: ", params
        # generate barchart plot
        #ds = svgraph.svDefaultCategoryDataset()
        #c = svgraph.createBarChart("Boxplot x01", ds)
        #self.outputpanel = c.getChartPanel()
        #self.outputchart = c.getChart()
        # generate xyzchart plot
        ds = svgraph.svDefaultXYZDataset()
        param_name = params.get("name") #params.getField("name")

        self.createdchart = svgraph.createXYZChart("Chart x01", ds)

        ### generate output console text
        import random
        numer = random.randint(100, 1000)
        self.console = " ** Process calculated: Type " + str(numer)
        self.console += "** User name: " + str(param_name)
        self.console += """
output: example no valid
Attribute0 > 765.012954 AND Attribute1 <= 141.732431: Unsafe (143.0/1.0)
Attribute0 > 765.012954 AND Attribute3 > 163.157393 AND Attribute0 > 773.571142: 
       Unsafe (65.0)
"""
        return self.createdchart

def main(*args):
    print "* stat1.py: process"
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Exageration", 34)
    dynobject.setDynValue("service12",  2)

    
    result = proc.process(dynobject.getValues())