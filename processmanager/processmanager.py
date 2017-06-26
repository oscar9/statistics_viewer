# encoding: utf-8

import gvsig
import addons.statistics_viewer
reload(addons.statistics_viewer)

import addons.statistics_viewer.processmanager
reload(addons.statistics_viewer.processmanager)

from addons.statistics_viewer.processmanager import processdirectory

class StatisticsProcessManager():
    processes = []
    active = None
    
    def getProcesses(self):
        # search for procceses inside the processdirectory folder
        # condition: contain class StatProcess
        # condition: name starts with stat*.py
        for i in processdirectory.__all__:
            procesmodule = "processdirectory."+str(i)
            obj = __import__(procesmodule, globals(), locals(), ['StatProcess'], -1) 
            newprocess = getattr(obj, "StatProcess")
            self.processes.append(newprocess())

        return self.processes

    def getActiveProcess(self):
        return self.active
        
    def setActiveProcess(self, process):
        self.active = process
        
        
        
def main(*args):

    spm = StatisticsProcessManager().getProcesses()
    print spm
    pass


    