# encoding: utf-8

import gvsig
import addons.statistics_viewer
reload(addons.statistics_viewer)
import addons.statistics_viewer.process
reload(addons.statistics_viewer.process)

from addons.statistics_viewer.process import stat1

class StatisticsProcessManager():
    processes = []
    active = None
    
    def getProcesses(self):
        self.processes.append(stat1.StatProcess)
        #self.processes.append(stat2.StatProcess)
        return self.processes
        
    def getActiveProcess(self):
        return self.active

    def setActiveProcess(self, process):
        self.active = process()
        

        
        
def main(*args):

    spm = StatisticsProcessManager().getProcesses()
    print spm