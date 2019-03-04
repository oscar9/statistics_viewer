# encoding: utf-8

import gvsig

import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
        
class StatProcess(AbstractStatisticProcess):

    name = u"Correlation between fields"
    description = u"Correlation calculation between all the fields in a vectorial layer"
    idprocess = "correlation-fields-1"
    allowZoomProcess = False
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("ProcessCorrelation", "ProcessPropertiesCorrelation", "aqui va la descripcion")
        params.addDynFieldString("Layer").setMandatory(True)
        params.addDynFieldString("Field 1").setMandatory(True)
        params.addDynFieldString("Field 2").setMandatory(True)
        #return params
        
    def process(self, params):

        params_layer = params.get("Layer")
        params_field1 = params.get("Field 1")
        params_field2 = params.get("Field 2")

        layer = gvsig.currentView().getLayer(params_layer)
        cox = []
        coy = []

        for f in layer.features():
            cox.append(float(f.get(params_field1)))
            coy.append(float(f.get(params_field2)))

        from org.apache.commons.math3.stat.correlation import Covariance
        c = Covariance().covariance(cox,coy)

        self.console =  u" ** Correlation between fields: " + str(c)

        return None #self.createdchart

def main(*args):
    print "* stat3.py: process"
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Layer", "parcelas_Valencia")
    dynobject.setDynValue("Field 1", "COORX")
    dynobject.setDynValue("Field 2", "COORY")
    
    #fields = dynobject.getDynClass().getDynFields()
    #for d in fields:
    #    print "*  ", d
    print proc, type(proc), dir(proc)
    values = dynobject.getValues()
    proc.process(values)
    print proc.getOutputConsole()