# encoding: utf-8

import gvsig
import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)
import addons.statistics_viewer.sv
reload(addons.statistics_viewer.sv)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess
import os
from addons.statistics_viewer.sv import svgraph

from org.jfree.data.category import CategoryDataset, DefaultCategoryDataset

class StatProcess(AbstractStatisticProcess):

    name = "Proceso Estadistica 1"
    description = "Perfil dinámico en funcion de la Vista con la capa de salida del geoproceso Perfil"
    dynform = None
    createdchart = None

    console = ""
    def __init__(self):
        dynxml = os.path.join(os.path.dirname(__file__), "stat2.xml")
        self.dynform = self.importDynPanel(dynxml)
        #self.process()
        
    def getDescription(self):
        return self.description
        
    def process(self, viewer):
        smax = viewer.chbMax.isSelected()
        smin = viewer.chbMin.isSelected()
        exageracion = float(viewer.txtEx.getText())
        
        ds = DefaultCategoryDataset()
        mapContext = gvsig.currentView().getMapContext()
        layer = gvsig.currentView().getLayer("puntos")
        viewbox = mapContext.getViewPort().getEnvelope().getGeometry()
        features = layer.features()
        allz = []
        for f in features:
            if f.geometry().intersects(viewbox):
                allz.append(f.Z)
                ds.addValue(f.Z * exageracion, "Height", str(f.X))
        #ds = svgraph.svDefaultXYZDataset()
        self.createdchart = svgraph.createLineChart("Chart x01", ds)

        ### generate output console text
        self.console = " ** Proceso calculado:  "
        if smax: self.console += "  Z max: " + str(max(allz))
        if smin: self.console += "  Z min: " + str(min(allz))
        
        return self.createdchart
        
    def getInputPanel(self):
        return self.dynform
        

def main(*args):
    print "* stat1.py: process"
    import os
    
    proc =  StatProcess()
    print proc.getProcessName()
    print proc.getInputPanel()
    print proc.getOutputPanel()