# encoding: utf-8

import gvsig
from gvsig.uselib import use_jars
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.io import File
from org.gvsig.app import ApplicationLocator

from org.gvsig.andami import PluginsLocator
import os

from org.gvsig.tools import ToolsLocator
from java.io import File

from gvsig import getResource

def selfRegister():
  # i18
  i18nManager = ToolsLocator.getI18nManager()
  i18nManager.addResourceFamily("text",File(gvsig.getResource(__file__,"i18n")))
  
  from addons.statistics_viewer.main import StatisticsViewerExtension 
  application = ApplicationLocator.getManager()
  icon_show = File(getResource(__file__,"statistics_viewer_ico.png")).toURI().toURL()
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

    ScriptingExtension.add_classpath(getResource(__file__,"libs/commons-math3-3.6.1-tools.jar"))
    ScriptingExtension.add_classpath(getResource(__file__,"libs/commons-math3-3.6.1.jar"))
    
    selfRegister()
