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
    dynform = None
    dynclass = None
    outputpanel = None
    outputchart = None

    createdchart = None
    console = ""
    
    def __init__(self):
        self.dynform = self.setParameters()
        
    def importDynPanel(self, dynobjectxml):
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
        try:
          self.dynclass = DefaultDynObjectManager().importDynClassDefinitions(resource, loader)["SHPStoreParameters"]
          self.dynform = DefaultDynFormManager().createJDynForm(self.dynclass) #i:dynobject,dynstruct o:jdynform
        except Exception,e:
          self.dynform = jfc.FormPanel(FileInputStream(dynobjectxml))
        finally:
          return self.dynform
          
    def createNewParameters(self):
        params = self.getDynClass()
        return params
        
    def getDescription(self):
        return self.description
        
    def update(self, viewer):
        c = self.process(viewer)
        self.outputpanel = c.getChartPanel()
        self.outputchart = c.getChart()
    
    def getDynForm(self):
        return self.dynform

    def getDynClass(self):
        return self.dynclass

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
        
def main(*args):
    #ab = AbstractStatisticProcess()
    #print ab.getDynForm()
    #dynobjectxml = os.path.join(os.path.dirname(__file__), "SHPParameters.xml")
    #print ab.importDynPanel(dynobjectxml)
    p = stat1.StatProcess()
    print p.getDescription()
    print p.getDynForm()

    