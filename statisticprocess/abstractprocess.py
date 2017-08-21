# encoding: utf-8

import gvsig
from org.gvsig.tools.dynobject.impl import DefaultDynObjectManager
from org.gvsig.tools.dynform.impl import DefaultDynFormManager
from java.io import FileInputStream
from org.gvsig.fmap.dal.resource.file import FileResource
from org.gvsig.fmap.dal.resource.file import FileResourceParameters
import os
import com.jeta.forms.components.panel as jfc
from org.gvsig.tools import ToolsLocator
        
class AbstractStatisticProcess():
    # el metodo process actualizara la nueva grafica
    #dynobject = None
    #dynform = None
    #dynclass = None
    inputparameters = None
    outputpanel = None
    outputchart = None

    createdchart = None
    console = ""
    
    def __init__(self):
        #self.dynclass = self.createParameters()
        #self.dynform = self.createDynForm(self.dynclass)
        pass

    def process(self, params):
        # Overwrite
        pass
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name
        
    def createInputParameters(self,idp, process, description):
        # Metodo para generar los parametros al iniciar el proceso
        self.inputparameters = self.getToolsLocator().getDynObjectManager().createDynClass(idp, process, description)
        return self.inputparameters
        
        
    def createParameters(self): #i: dynclass o: dynobject
        #dynclass = self.processParameters()
        self.processParameters()
        dynclass = self.inputparameters
        dynobject = DefaultDynObjectManager().createDynObject(dynclass)
        return dynobject
        
    def getToolsLocator(self):
        return ToolsLocator
        
    #def createDynClass(self, dynobjectxml):
    #    if dynobjectxml==None:
    #        print "dynobjectxml is None"
    #        return None
    #    elif os.path.exists(dynobjectxml)==False:
    #        print "not path found"
    #        return None
    #    resource = FileInputStream(dynobjectxml)
    #    #Cargar
    #    #frparams = FileResourceParameters(dynobjectxml)
    #    #resource = FileResource(frparams)
    #    
    #    loader = None
    #    #try:
    #    dynclass = DefaultDynObjectManager().importDynClassDefinitions(resource, loader)["SHPStoreParameters"]
    #    return dynclass

    def makeDynForm(self, dynclass):
        dynform = DefaultDynFormManager().createJDynForm(dynclass) #i:dynobject,dynstruct o:jdynform
        #except Exception,e:
        #  self.dynform = jfc.FormPanel(FileInputStream(dynobjectxml))
        return dynform
        
    def createDynForm(self):
        dynclass = self.createParameters()
        print dynclass
        dynform = self.makeDynForm(dynclass)
        return dynform
        
    def getDynObject(self):
        return self.createParameters()
        
    def getDescription(self):
        return self.description
        
    def update(self, dyn):
        # proces dyn to dict -> pass to the process a dict
        # TODO: fix el pase de parametros
        ift = dyn.getFieldsIterator()
        params = {}
        for ifield in ift:
            params[ifield.getName()]=ifield.getValue()
            
        c = self.process(params)
        
        if c!=None: #TODO PROCESAR FICHEROS DE SALIDA
            self.outputpanel = c.getChartPanel()
            self.outputchart = c.getChart()

    def getOutputConsole(self):
        return self.console
        
    def getOutputPanel(self):
        return self.outputpanel

    def getOutputChart(self):
        return self.outputchart

    def setOutputPanel(self,panel):
        self.outputpanel = panel
        
    def getProcessName(self):
        return self.name

    def setDynClass(self, dynclass):
        self.dynclass = dynclass
        
    def setDynForm(self, dynform):
        self.dynform = dynform
        

    