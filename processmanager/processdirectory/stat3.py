# encoding: utf-8

import gvsig

import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
        
class StatProcess(AbstractStatisticProcess):

    name = u"Correlación entre campos"
    description = u"Calculo de la correlación entre dos campos de una misma capa"
    idprocess = "correlation-fields-1"
    allowZoomProcess = False
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("ProcessCorrelation", "ProcessPropertiesCorrelation", "aqui va la descripcion")
        params.addDynFieldString("Capa").setMandatory(True)
        params.addDynFieldString("Campo 1").setMandatory(True)
        params.addDynFieldString("Campo 2").setMandatory(True)
        #return params
        
    def process(self, params):

        params_layer = params.get("Capa")
        params_field1 = params.get("Campo 1")
        params_field2 = params.get("Campo 2")

        layer = gvsig.currentView().getLayer(params_layer)
        cox = []
        coy = []

        for f in layer.features():
            cox.append(float(f.get(params_field1)))
            coy.append(float(f.get(params_field2)))

        from org.apache.commons.math3.stat.correlation import Covariance
        c = Covariance().covariance(cox,coy)

        self.console =  u" ** Correlación entre campos: " + str(c)

        return None #self.createdchart

def main(*args):
    print "* stat3.py: process"
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Capa", "parcelas_Valencia")
    dynobject.setDynValue("Campo 1", "COORX")
    dynobject.setDynValue("Campo 2", "COORY")
    
    #fields = dynobject.getDynClass().getDynFields()
    #for d in fields:
    #    print "*  ", d
    print proc, type(proc), dir(proc)
    values = dynobject.getValues()
    proc.process(values)
    print proc.getOutputConsole()