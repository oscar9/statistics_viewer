# encoding: utf-8

import gvsig
from gvsig.libs.formpanel import FormPanel
import os
import addons.statistics_viewer.processmanager
reload(addons.statistics_viewer.processmanager)

from addons.statistics_viewer.processmanager.processmanager import StatisticsProcessManager
from java.awt import BorderLayout
from org.gvsig.fmap.mapcontext.events.listeners import ViewPortListener

from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.fmap.mapcontext import MapContextLocator
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.io import File

class StatisticsViewerExtension(ScriptingExtension):
    def __init__(self):
      pass
  
    def canQueryByAction(self):
      return True
  
    def isEnabled(self,action):
      return True #currentView()!=None
  
    def isVisible(self,action):
      return True #currentView()!=None
      
    def execute(self,actionCommand, *args):
        l = StatisticsViewer()
        l.showTool("Statistics Viewer")
        
class StatisticsViewer(ViewPortListener,FormPanel):
    mapContext = None
    spm = None #Statistics Process Manager
    jdynform = None
    savedynform = True
    savedynformparams = {}
    def __init__(self):
        FormPanel.__init__(self, os.path.join(os.path.dirname(__file__), "statistics_viewer.xml"))
        icon = self.load_icon(os.path.join(os.path.dirname(__file__), "info.ico"))
        self.btnInfo.setIcon(icon)
        self.setPreferredSize(1000,500)
        self.spm = StatisticsProcessManager()
        processes = self.spm.getProcesses()
        
        for p in processes:
            #self.cmbProcess.addItem([s,processes[s]])
            #self.cmbProcess.addItem((str(s),processes[s]))
            self.cmbProcess.addItem(p)

        #ex: self.cmbProcess.addItem(["text", "text"])
        
        #Viewport listener
        try:
            self.mapContext = gvsig.currentView().getMapContext()
            self.mapContext.getViewPort().addViewPortListener(self)
        except:
            print "** No Zoom Process Avalaible**"
        
    def getProcessManager(self):
        return self.spm
        
    def backColorChanged(self,*args):
        pass
  
    def extentChanged(self,*args):
        if self.chbZoom.isSelected():
            self.btnProcess_click()
  
    def projectionChanged(self,*args):
        pass
        
    def btnClose_click(self, *args):
        #For viewport listener
        self.mapContext.getViewPort().removeViewPortListener(self)
        self.hide()
        
    def cmbProcess_click(self, *args):
        #self.actualprocess = self.cmbProcess.getSelectedItem()[1]()
        
        self.setSelectedProcess()
        actualprocess = self.getProcessManager().getActiveProcess()
        # INPUT
        if actualprocess.allowZoomProcess == False:
            self.chbZoom.setEnabled(False)
        else:
            self.chbZoom.setEnabled(True)

        self.jpInput.removeAll()
        self.jpOutput.removeAll()
        self.jpInput.setLayout(BorderLayout())
        self.jdynform = actualprocess.createDynForm()

        dynform = self.jdynform
        params = self.savedynformparams
        #for k in params.keys():
        #    value = params[k]
        obj = actualprocess.dynobject
        for ifield in dynform.getFieldsIterator():
            if ifield.getName() in params.keys():
                name = ifield.getName()
                obj.setDynValue(name, params[name])

        self.savedynform = True
        
        self.jpInput.add(self.jdynform.asJComponent(),BorderLayout.CENTER)
        self.jpInput.validate()
        
        ### TODO: eliminar 
        #self.btnProcess_click()
        pass
        
    def btnInfo_click(self, *args):
        actualprocess = self.getProcessManager().getActiveProcess()
        self.txtConsole.setText(actualprocess.getDescription())
        
    def btnProcess_click(self, *args):
        #print "** Info boton", self.cmbProcess.getSelectedItem(), type(self.cmbProcess.getSelectedItem()), " **"
        actualprocess = self.getProcessManager().getActiveProcess()
        ## INPUT
        #do = self.getProcessManager().getActiveProcess().getDynObject()

        ## EJECUCION
        # TODO: Pasarle el dyn mas sencillo
        
        actualprocess.update(self.jdynform)

        # OUTPUT establecer layout para mostrar chart
        # usando self.actualprocess
        self.jpOutput.removeAll()
        self.jpOutput.setLayout(BorderLayout())
        outputpanel = actualprocess.getOutputPanel()

        if outputpanel != None:
            self.jpOutput.add(outputpanel,BorderLayout.CENTER)
            self.jpOutput.validate()

        ## TODO: mantener track de los elementos que tiene el inputpanel
        ## TODO: necesario para leerlos luego y pasarlos como params
        #print "txtX: ", self.txtX.getText()
        #print "txtY: ", self.txtY.getText()
        outputconsole = actualprocess.getOutputConsole()
        if isinstance(outputconsole, str) or isinstance(outputconsole, unicode):
            self.txtConsole.setText(outputconsole)
        else:
            self.txtConsole.setText("")

    def cmbProcess_change(self, *args):
        """
        if self.savedynform == True:
            #print "Process Changed: ", self.cmbProcess.getSelectedItem()
            if self.jdynform == None:
                return
            ift = self.jdynform.getFieldsIterator()
            params = {}
            for ifield in ift:
                try:
                    value = ifield.getValue()
                except:
                    value = ""
                params[ifield.getName()]=value
            #print params
            self.savedynformparams = params
            self.savedynform = False
        """
        pass
        

    def btnSavePlot_click(self, *args):
        actualprocess = self.getProcessManager().getActiveProcess()
        actualprocess.createdchart.savePlotImage("/home/osc/temp/new1.png")
        
    def setSelectedProcess(self):
        selected =  self.cmbProcess.getSelectedItem()
        self.getProcessManager().setActiveProcess(selected)
        return self.getProcessManager().getActiveProcess()


def main(*args):

    tool = StatisticsViewer()
    tool.showTool("Statistics Viewer") #or showWindow TODO

    pass
    
