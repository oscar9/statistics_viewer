# encoding: utf-8

import gvsig
import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)
from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess
import os
from org.apache.commons.math3.stat.correlation import PearsonsCorrelation
class StatProcess(AbstractStatisticProcess):

    name = u"Correlacion de Pearsons"
    description = u"Calculo de la correlación entre todos los campos de una misma capa"
    idprocess = "correlation-fields-all-1"
    allowZoomProcess = False
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("PearsonsCorrelation", "ProcessPropertiesCorrelation", "aqui va la descripcion")
        params.addDynFieldString("Capa").setMandatory(True)
        
    def process(self, params):

        params_layer = params.get("Capa")
        
        layer = gvsig.currentView().getLayer(params_layer)
        flayer = layer.features()
        cox = []
        coy = []
        sch = layer.getSchema()
        
        listfields = []
        columnNames = ["***"]
        # get potential numeric fields
        for field in sch:
            dt = field.getDataTypeName()
            if dt=="Integer" or dt=="Long" or dt=="Double":
                listfields.append(field.getName())
                columnNames.append(field.getName())

        # Show first line table
        #print "\t\t", 
        #listfields = ["COORX", "COORY"]
        #columnNames = ["***", "COORX", "COORY"]


        #for f1 in listfields:
        #    print f1+"\t",
        #print ""

        # Iterate table
        data = []
        for f1 in listfields:
            f1v = [f.get(f1) for f in flayer]
            #print f1 + "\t\t",
            d = [f1]

            for f2 in listfields:
                f2v = [f.get(f2) for f in flayer]
                c = PearsonsCorrelation().correlation(f1v,f2v)
                d.append(c)
                #print str(c)+"\t",

            #print ""
            data.append(d)

        print "Data:", data
        print "columenNames: ", columnNames
        print "listfields: ", listfields
        from javax.swing import JTable
        
        table = JTable(data, columnNames)
        from javax.swing import JScrollPane
        table = JScrollPane(table)
        self.setOutputPanel(table)
        return None #self.createdchart

def main(*args):
    print "* stat1.py: process"
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Capa", "parcelas_Valencia")

    values = dynobject.getValues()
    proc.process(values)
    print proc.getOutputConsole()
    print proc.getOutputPanel()