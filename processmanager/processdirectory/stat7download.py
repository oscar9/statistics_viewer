# encoding: utf-8

import gvsig
from gvsig import getResource

import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)

from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess

import os
from addons.statistics_viewer.sv import svgraph
from org.gvsig.tools.dynobject import DynField, DynObject
import urllib2
import os

        
class StatProcess(AbstractStatisticProcess):

    name = u"Download new operations"
    description = u"Download new operation from a link in github. It will be download inside the process directory and loaded for the application"
    idprocess = "testing-parameters-1"
    allowZoomProcess = True
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("DownloadParameters", "DownloadParametersProperties", "Description")
        params.addDynFieldString("Download").setMandatory(True) 
        params.addDynFieldString("Name").setMandatory(True)

    def process(self, params):
        param_download = params.get("Download")
        param_name = params.get("Name")

        self.console = " ** Descarga: \n"+param_download
        

        response = urllib2.urlopen(param_download)
        
        plugin = response.read()
        
        filename = param_name 
        
        fullpath = getResource(__file__,filename)

        f = open(fullpath, 'w')
        f.write(plugin)
        f.close()
        
def main(*args):
    print "* stat7.py: download"