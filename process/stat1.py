# encoding: utf-8

import gvsig

import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)

#import addons.statistics_viewer.sv
#reload(addons.statistics_viewer.sv)

#import addons.statistics_viewer.process
#reload(addons.statistics_viewer.process)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
from addons.statistics_viewer.sv import svgraph


class StatProcess(AbstractStatisticProcess):

    name = "Proceso Estadistica 1"
    description = "Calculo de edad"
    
    def __init__(self):
        AbstractStatisticProcess.__init__(self)
        
    def setParameters(self):
        dyn = os.path.join(os.path.dirname(__file__), "SHPParameters.xml")
        dynform = self.importDynPanel(dyn) # TODO: tb establece el dynclass en el abstract
        return dynform
        
    def process(self, viewer):
        # generate barchart plot
        #ds = svgraph.svDefaultCategoryDataset()
        #c = svgraph.createBarChart("Boxplot x01", ds)
        #self.outputpanel = c.getChartPanel()
        #self.outputchart = c.getChart()
        # generate xyzchart plot
        ds = svgraph.svDefaultXYZDataset()
        self.createdchart = svgraph.createXYZChart("Chart x01", ds)

        ### generate output console text
        import random
        numer = random.randint(100, 1000)
        self.console = " ** Proceso calculado: Tipo " + str(numer)
        self.console += """
output: example no valid
Attribute0 > 765.012954 AND Attribute1 <= 141.732431: Unsafe (143.0/1.0)
Attribute0 > 765.012954 AND Attribute3 > 163.157393 AND Attribute0 > 773.571142: 
       Unsafe (65.0)
Attribute0 > 765.012954 AND Attribute1 <= 141.732431: Unsafe (143.0/1.0)
Attribute0 > 765.012954 AND Attribute3 > 163.157393 AND Attribute0 > 773.571142: 
       Unsafe (65.0)
Attribute0 > 765.012954 AND Attribute1 <= 141.732431: Unsafe (143.0/1.0)
Attribute0 > 765.012954 AND Attribute3 > 163.157393 AND Attribute0 > 773.571142: 
       Unsafe (65.0)
"""
        return self.createdchart
        
        

def main(*args):
    print "* stat1.py: process"
    import os
    
    proc =  StatProcess()
    print proc.setParameters()
    new = proc.createNewParameters()
    print "NEW: ", new
    print "Name: ", proc.getProcessName()
    print "Input panel: ", proc.getInputPanel()
    print "DynForm: ", proc.getDynForm()
    #print proc.process()
    print "Outputpanel: ", proc.getOutputPanel()