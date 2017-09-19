# encoding: utf-8

import gvsig
from gvsig.uselib import use_jars
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.io import File
from org.gvsig.app import ApplicationLocator

from org.gvsig.andami import PluginsLocator
import os
from addons.statistics_viewer.main import StatisticsViewerExtension 
def selfRegister():
  application = ApplicationLocator.getManager()
  icon_show = File(os.path.join(os.path.dirname(__file__),"statistics_viewer_ico.png")).toURI().toURL()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  iconTheme.registerDefault("scripting.sv", "action", "tools-sv-show", None, icon_show)
  
  extension = StatisticsViewerExtension()
  actionManager = PluginsLocator.getActionInfoManager()
  action_show = actionManager.createAction(
    extension, 
    "tools-sv-show", # Action name
    "Statistics Viewer", # Text
    "show", # Action command
    "tools-sv-show", # Icon name
    None, # Accelerator
    1009000000, # Position 
    "Statistics Viewer" # Tooltip
  )
  action_show = actionManager.registerAction(action_show)
  application.addTool(action_show, "StatisticsViewer")
  
def main(*args):

    print "***** LOADED STATISTICS VIEWER ******"
    use_jars(os.path.dirname(__file__),"libs", True)
    selfRegister()