# encoding: utf-8

import gvsig

import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
from addons.statistics_viewer.sv import svgraph

class StatProcess(AbstractStatisticProcess):

    name = "Proceso Estadistica 1"
    description = "Calculo de edad"
    allowZoomProcess = True
    
    def __init__(self):
        AbstractStatisticProcess.__init__(self)
        
        
    def processParameters(self): #o: dynclass
        #dynxml = os.path.join(os.path.dirname(__file__), "SHPParameters.xml")
        #dynclass = self.createDynClass(dynxml)
        
        manager = self.getToolsLocator().getDynObjectManager()
        #mydata = manager.createDynObject("MyStruct")
        
        dynclass = manager.get("Process","ProcessProperties")
        if dynclass == None: 
          dynclass = manager.createDynClass("Process", "ProcessProperties", "aqui va la descripcion")
          dynclass.addDynFieldString("name").setMandatory(False)
          dynclass.addDynFieldString("title").setMandatory(True)
          dynclass.addDynFieldString("type").setMandatory(True)
          
          #definition.addDynFieldObject("service").setClassOfValue(ChartService.class)
          manager.add(dynclass)
          
        return dynclass
        
    def process(self, params):
        # generate barchart plot
        #ds = svgraph.svDefaultCategoryDataset()
        #c = svgraph.createBarChart("Boxplot x01", ds)
        #self.outputpanel = c.getChartPanel()
        #self.outputchart = c.getChart()
        # generate xyzchart plot
        ds = svgraph.svDefaultXYZDataset()
        param_name = params.get("name") #params.getField("name")
        print "parammmmmmmm:", param_name
        self.createdchart = svgraph.createXYZChart("Chart x01", ds)

        ### generate output console text
        import random
        numer = random.randint(100, 1000)
        self.console = " ** Proceso calculado: Tipo " + str(numer)
        self.console += "** Nombre del usuario: " + str(param_name)
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
    dynclass = dynobject.getDynClass()
    
    dynfields = dynobject.getDynClass().getDynFields()

    #dynobject.setDynValue("shxFile", "")

    for f in dynfields:
        print f.getName(),dynobject.getDynValue(f.getName()) 
    return