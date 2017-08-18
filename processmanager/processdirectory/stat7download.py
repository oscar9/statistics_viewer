# encoding: utf-8

import gvsig

import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
from addons.statistics_viewer.sv import svgraph
from org.gvsig.tools.dynobject import DynField, DynObject

        
class StatProcess(AbstractStatisticProcess):

    name = u"Descarga de extensiones"
    description = u"Descarga de extensión"
    idprocess = "testing-parameters-1"
    allowZoomProcess = True
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("DownloadParameters", "DownloadParametersProperties", "Description")
        params.addDynFieldString("Download").setMandatory(True) 

    def process(self, params):
        param_download = params.get("Download")

        self.console = " ** Descarga: \n"+param_download
        
        import urllib2
        response = urllib2.urlopen(param_download)
        
        plugin = response.read()
        
        filename = "newstat3.py"
        import os
        fullpath = os.path.join(os.path.dirname(__file__),filename)
        print fullpath
        f = open(fullpath, 'w')
        f.write(plugin)
        f.close()
        
def main(*args):
    print "* stat1.py: process"
    proc =  StatProcess()
    dynobject = proc.createParameters()

    dynobject.setDynValue("Download", 'https://raw.githubusercontent.com/oscar9/statistics_viewer/master/processmanager/processdirectory/stat1.py')
    
    proc.process(dynobject.getValues())
    print proc.getOutputConsole()
