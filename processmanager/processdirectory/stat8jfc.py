# encoding: utf-8

import gvsig
import addons.statistics_viewer.statisticprocess
reload(addons.statistics_viewer.statisticprocess)
from addons.statistics_viewer.statisticprocess.abstractprocess import AbstractStatisticProcess
import os
from org.apache.commons.math3.stat.correlation import PearsonsCorrelation

#from addons.statistics_viewer.sv.svgraph import svDefaultXYZDataset

from org.jfree.data.xy import DefaultXYDataset
from org.jfree.data.xy import XYDataItem, XYSeries, XYSeriesCollection, XYDataset

class gvXYDataItem(XYDataItem):
    def __init__(self,*args):
        pass
        
class svXYSeriesCollection(XYSeriesCollection):
    index = {}
    f = None
    field1 = None
    field2 = None
    def __init__(self,layer, field1, field2):
        self.layer = layer
        self.f = layer.features()
        self.append(self.f,field1, field2)
        
    def getFeature(self, xp, yp):
        for f in self.f:
            if f.get(self.field1) == yp and f.get(self.field2)==xp:
                selection = self.layer.getSelection()
                selection.deselectAll()
                selection.select(f)
                
                return f
        
    def append(self, features, field1, field2):
      self.field1 = field1 #"LONGITUDE"
      self.field2 = field2 #"LATITUDE"
      #x = []
      #y = []
      nw = XYSeries("") #Title serie: Coord")
      print "self:", dir(self)
      for n,f in enumerate(features):
          #x.append(f.LONGITUDE)
          #y.append(f.LATITUDE)
          f1 = f.get(self.field1)
          f2 = f.get(self.field2)
          #self.index[n] = f.getCopy()
          d = XYDataItem(f1, f2)
          nw.add(d)
      self.addSeries(nw)
      
#class svDefaultXYDataset(Abstract
class StatProcess(AbstractStatisticProcess):

    name = u"Gráfica Scatter Plot"
    description = u"Implementacion de XYDataset"
    idprocess = "scatter-plot-1"
    allowZoomProcess = False
    
    def processParameters(self): #o: dynclass
        params = self.createInputParameters("GraphsExample", "GraphsExample", "Descripcion")
        params.addDynFieldString("Layer").setMandatory(True)
        params.addDynFieldString("Field X").setMandatory(True)
        params.addDynFieldString("Field Y").setMandatory(True)
        
    def process(self, params):
        params_layer = params.get("Layer")
        #params_layer = "VNP14IMGTDL"
        params_field1 = params.get("Field X")
        params_field2 = params.get("Field Y")
        layer = gvsig.currentView().getLayer(params_layer)#.features()
        dp = createDemoPanel(layer, params_field1, params_field2)
        dp.setPreferredSize(Dimension(500, 270))
        self.setOutputPanel(dp)


#/* ---------------------
# * ScatterPlotDemo3.java

from java.awt import Point, Dimension
from java.awt.geom import Point2D
from java.awt.geom import Rectangle2D

from javax.swing import JPanel

from org.jfree.chart import ChartFactory
from org.jfree.chart import ChartMouseEvent
from org.jfree.chart import ChartMouseListener
from org.jfree.chart.event import ChartProgressListener
from org.jfree.chart import ChartPanel
from org.jfree.chart import ChartRenderingInfo
from org.jfree.chart import JFreeChart
from org.jfree.chart.axis import NumberAxis
from org.jfree.chart.axis import ValueAxis
from org.jfree.chart.plot import PlotOrientation
from org.jfree.chart.plot import XYPlot
from org.jfree.data.xy import XYDataset
from org.jfree.ui import ApplicationFrame
from org.jfree.ui import RefineryUtilities

#/**
# * A demo scatter plot with some code showing how to convert between Java2D
# * coordinates and (x, y) coordinates.
# */
#class ScatterPlotDemo3(ApplicationFrame):
#    def __init__(self, title):
#        super(title)
#        demoPanel = createDemoPanel()
#        demoPanel.setPreferredSize(Dimension(500, 270))
#        self.a.setContentPane(demoPanel)


class MyChartMouseListener(ChartMouseListener, ChartProgressListener): 
    panel = None
    def __init__(self, panel):
        self.panel = panel
        self.panel.getChart().addProgressListener(self)
        
    def chartProgress(self, event):
        #print "ChartProgress: ", event
        p = event.getChart().getPlot()
        xp =p.getRangeCrosshairValue()
        yp = p.getDomainCrosshairValue()
        dataset = p.getDataset()
        #print "Info:", xp, yp
        feature = dataset.getFeature(xp,yp)

        #serie = dataset.getSeries("Coord")
        #print serie.getDataItem(n)
        return
        
    def chartMouseClicked(self, event):

        #import pdb; pdb.set_trace()
        #return
    
        #import pdb; pdb.set_trace()
        x = event.getTrigger().getX()
        y = event.getTrigger().getY()

        #// the following translation takes account of the fact that the
        #// chart image may have been scaled up or down to fit the panel...
        p = self.panel.translateScreenToJava2D(Point(x, y))

        #// now convert the Java2D coordinate to axis coordinates...
        plot = self.panel.getChart().getPlot()
        info = self.panel.getChartRenderingInfo()
        dataArea = info.getPlotInfo().getDataArea()
        xx = plot.getDomainAxis().java2DToValue(p.getX(), dataArea, plot.getDomainAxisEdge())
        yy = plot.getRangeAxis().java2DToValue(p.getY(), dataArea, plot.getRangeAxisEdge())

        #// just for fun, lets convert the axis coordinates back to component
        #// coordinates...
        domainAxis = plot.getDomainAxis()
        rangeAxis = plot.getRangeAxis()
        xxx = domainAxis.valueToJava2D(xx, dataArea, plot.getDomainAxisEdge())
        yyy = rangeAxis.valueToJava2D(yy, dataArea, plot.getRangeAxisEdge())

        p2 = self.panel.translateJava2DToScreen(Point2D.Double(xxx, yyy))
        print "Mouse coordinates are (" + str(x) + ", " + str(y) + "), in data space = (" + str(xx) + ", " + str(yy) + ")."
        print "--> (" + str(p2.getX()) + ", " + str(p2.getY()) + ")"

    #/**
    # * Callback method for receiving notification of a mouse movement on a
    # * chart.
    # *
    # * @param event  information about the event.
    # */

    def chartMouseMoved(self, event):
        #print "chartmousemoved", event
        pass

class newChart(ChartProgressListener):
    def __init__(self):
        pass
    def chartProgress(self):
        pass
    
def createChart(dataset):
    chart = ChartFactory.createScatterPlot("",
            "", "", dataset, PlotOrientation.VERTICAL, True, True, False)
    print chart
    plot = chart.getPlot()
    #import pdb; pdb.set_trace()

    plot.setDomainCrosshairVisible(True)
    plot.setDomainCrosshairLockedOnData(True)
    plot.setRangeCrosshairVisible(True)
    plot.setRangeCrosshairLockedOnData(True)
    plot.setDomainZeroBaselineVisible(True)
    plot.setRangeZeroBaselineVisible(True)
    plot.setDomainPannable(True)
    plot.setRangePannable(True)
    domainAxis = plot.getDomainAxis()
    domainAxis.setAutoRangeIncludesZero(False)
    return chart
    
def createDemoPanel(features, field1, field2):
    chart = createChart(svXYSeriesCollection(features, field1, field2)) #SampleXYDataset2())
    panel = ChartPanel(chart)
    panel.setMouseWheelEnabled(True)
    panel.addChartMouseListener(MyChartMouseListener(panel))
    return panel


def main(*args):
    print "* stat1.py: process"
    proc =  StatProcess()
    dynobject = proc.createParameters()


    dynobject.setDynValue("Capa", "parcelas_Valencia")

    values = dynobject.getValues()
    proc.process(values)
    print proc.getOutputConsole()
    print proc.getOutputPanel()
