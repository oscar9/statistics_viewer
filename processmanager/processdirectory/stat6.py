# encoding: utf-8

import gvsig

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

    name = u"Test new parameters"
    description = "Probando distintas clases"
    idprocess = "testing-parameters-1"
    allowZoomProcess = True
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("TestingParameters", "TestingParametersProperties", "Description")
        params.addDynFieldInt("IntTest").setMandatory(True) 
        
        di = params.addDynFieldObject("service12")
        di.setClassOfValue(ChartService)
        di.setDefaultDynValue(7)
        
        
    def process(self, params):
        param_name = params.get("IntTest")

        self.console = " ** Testeando uso de parametros customizados"
        

def main(*args):
    print "* stat6.py: Testing"
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("IntTest", 34)
    dynobject.setDynValue("service12", 1)
    
    proc.process(dynobject.getValues())
    print proc.getOutputConsole()