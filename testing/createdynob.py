# encoding: utf-8

import gvsig
import gvsig
from org.gvsig.tools.dynobject.impl import DefaultDynObjectManager
from org.gvsig.tools.dynform.impl import DefaultDynFormManager
import os
from java.io import FileInputStream

def main(*args):

    #Remove this lines and add here your code
    dynobjectxml = os.path.join(os.path.dirname(__file__), "SHPParameters.xml")
    resource = FileInputStream(dynobjectxml)
    loader = None
    dynclass = DefaultDynObjectManager().importDynClassDefinitions(resource, loader)["SHPStoreParameters"]#InputStream resource, ClassLoader loader)
    #print "dynclass: ", dynclass
    print "dynclass name: ", dynclass.__class__.__name__
    dynform = DefaultDynFormManager().createJDynForm(dynclass) 
    print dynform
    ## 2
    print "##2"
    dynclass = DefaultDynObjectManager().createDynClass("Parametros", "Parametros del proceso")
    print dynclass
    print dynclass.__class__.__name__
    dynclass.addDynFieldFolder("Carpeta")
    print dynclass
    from org.gvsig.tools.dynobject.impl import DefaultDynField 
    from org.gvsig.tools.dataTypes.impl import DefaultDataTypesManager
    datatype = DefaultDataTypesManager().INT
    print datatype
    dynfield = DefaultDynField("valor", datatype)
    print dynfield
