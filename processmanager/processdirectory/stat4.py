# encoding: utf-8

import gvsig
import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)
from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess
import os
from org.apache.commons.math3.stat.correlation import Covariance

class StatProcess(AbstractStatisticProcess):

    name = u"Covarianza entre todos los campos"
    description = u"Calculo de la correlación entre todos los campos de una misma capa"
    idprocess = "correlation-fields-all-1"
    allowZoomProcess = False
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("ProcessCorrelation", "ProcessPropertiesCorrelation", "aqui va la descripcion")
        params.addDynFieldString("Capa").setMandatory(True)
        
    def process(self, params):

        params_layer = params.get("Capa")
        
        layer = gvsig.currentView().getLayer(params_layer)
        flayer = layer.features()
        cox = []
        coy = []
        sch = layer.getSchema()
        
        listfields = []
        # get potential numeric fields
        for field in sch:
            dt = field.getDataTypeName()
            if dt=="Integer" or dt=="Long" or dt=="Double":
                listfields.append(field.getName())
        # Show first line table
        print "\t\t", 

        for f1 in listfields:
            print f1+"\t",
        print ""

        # Iterate table
        for f1 in listfields:
            f1v = [f.get(f1) for f in flayer]
            print f1 + "\t\t",

            for f2 in listfields:
                f2v = [f.get(f2) for f in flayer]
                c = Covariance().covariance(f1v,f2v)
                print str(c)+"\t",

            print ""

                
        return None #self.createdchart

def main(*args):
    print "* stat1.py: process"
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Capa", "parcelas_Valencia")

    values = dynobject.getValues()
    proc.process(values)
    print proc.getOutputConsole()