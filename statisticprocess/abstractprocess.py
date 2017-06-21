# encoding: utf-8

import gvsig
from org.gvsig.tools.dynobject.impl import DefaultDynObjectManager
from org.gvsig.tools.dynform.impl import DefaultDynFormManager
from java.io import FileInputStream
from org.gvsig.fmap.dal.resource.file import FileResource
from org.gvsig.fmap.dal.resource.file import FileResourceParameters
import os
import com.jeta.forms.components.panel as jfc

        
class AbstractStatisticProcess():
    # el metodo process actualizara la nueva grafica
    dynobject = None
    dynform = None
    dynclass = None
    outputpanel = None
    outputchart = None

    createdchart = None
    console = ""
    
    def __init__(self):
        self.dynclass = self.createParameters()
        self.dynform = self.createDynForm(self.dynclass)
        
    def createParameters(self): #i: dynclass o: dynobject
        self.dynclass = self.processParameters()
        self.dynobject = DefaultDynObjectManager().createDynObject(self.dynclass)
        return self.dynobject
        
        
    def createDynClass(self, dynobjectxml):
        if dynobjectxml==None:
            print "dynobjectxml is None"
            return None
        elif os.path.exists(dynobjectxml)==False:
            print "not path found"
            return None
        resource = FileInputStream(dynobjectxml)
        #Cargar
        #frparams = FileResourceParameters(dynobjectxml)
        #resource = FileResource(frparams)
        
        loader = None
        #try:
        dynclass = DefaultDynObjectManager().importDynClassDefinitions(resource, loader)["SHPStoreParameters"]
        return dynclass

    def createDynForm(self, dynclass):
        dynform = DefaultDynFormManager().createJDynForm(dynclass) #i:dynobject,dynstruct o:jdynform
        #except Exception,e:
        #  self.dynform = jfc.FormPanel(FileInputStream(dynobjectxml))
        return dynform
        
    def getDynObject(self):
        return self.dynobject
        
    def getDescription(self):
        return self.description
        
    def update(self, viewer):
        c = self.process(viewer)
        self.outputpanel = c.getChartPanel()
        self.outputchart = c.getChart()
    
    def getDynForm(self):
        return self.dynform

    def getOutputConsole(self):
        return self.console
        
    def getOutputPanel(self):
        return self.outputpanel

    def getOutputChart(self):
        return self.outputchart

    def getProcessName(self):
        return self.name

    def getInputPanel(self):
        return self.dynform

    def setDynClass(self, dynclass):
        self.dynclass = dynclass
        
    def setDynForm(self, dynform):
        self.dynform = dynform
        

    