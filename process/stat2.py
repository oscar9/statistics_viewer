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

class StatProcessProfile(AbstractStatisticProcess):

    name = "Generador de perfil"
    description = "Perfil dinámico en funcion de la Vista con la capa de salida del geoproceso Perfil"
    idprocess = "create-dynamic-profile"
    allowZoomProcess = True
    
    #dynform = None
    #createdchart = None

    #console = ""
    def __init__(self):
        AbstractStatisticProcess.__init__(self)
        
    def processParameters(self): #o: dynclass
        #dynxml = os.path.join(os.path.dirname(__file__), "SHPParameters.xml")
        #dynclass = self.createDynClass(dynxml)
        
        manager = self.getToolsLocator().getDynObjectManager()
        #mydata = manager.createDynObject("MyStruct")
        
        #dynclass = manager.get("Statistics2","Statistics2 Properties")
        #if dynclass == None:
        
        dynclass = manager.createDynClass("Statistics23", "Statistics2 Properties", "aqui va la descripcion")
        dynclass.addDynFieldString("Layer").setMandatory(True)
        dynclass.addDynFieldBoolean("Max").setMandatory(True)
        dynclass.addDynFieldBoolean("Min").setMandatory(True)
        dynclass.addDynFieldInt("Exageracion").setMandatory(True) 
        
        
        #definition.addDynFieldObject("service").setClassOfValue(ChartService.class)
        #manager.add(dynclass)
          
        return dynclass
        
    def process(self, params):
        smax = params.get("Max") 
        smin = params.get("Min") 
        exageracion = params.get("Exageracion") 
        layername = params.get("Layer")
        
        #smax = viewer.chbMax.isSelected()
        #smin = viewer.chbMin.isSelected()
        #exageracion = float(viewer.txtEx.getText())
        
        ds = DefaultCategoryDataset()
        mapContext = gvsig.currentView().getMapContext()
        layer = gvsig.currentView().getLayer(layername)
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
        

def main(*args):
    print "* stat1.py: process"
    import os
    
    proc =  StatProcessProfile()