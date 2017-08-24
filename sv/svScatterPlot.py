# encoding: utf-8

import gvsig

from org.jfree.data.xy import DefaultXYDataset
from org.jfree.data.xy import XYDataItem, XYSeries, XYSeriesCollection, XYDataset

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
class gvXYDataItem(XYDataItem):
    def __init__(self,*args):
        pass
        
from java.util import ArrayList

class svXYSeriesCollection(XYSeriesCollection):
    ### Manejar datos X-Y, dos campos designados al iniciarse la clase
    ## Agragar con addValues(nombreserie, field1, field2)
    ## Al acabar hay que hacer un updateSeries para asignarse a la collection
    ## Si se quiere encontrar la feature asignada por comparacion
    ## hay que hacer un setLayer para su busqueda
    index = {}
    layer = None
    field1 = None
    field2 = None
    series = {} # key and XYSerie
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2
        #self.layer = layer
        #self.f = layer.features()
        #self.append(serie, self.f, field1, field2)
        
    def getField1(self):
        return self.field1
        
    def getField2(self):
        return self.field2
        
    def setLayer(self, layer):
        self.layer = layer
        
    def getFeatureSelected(self, xp, yp):
        features = self.layer.features()
        for f in features:
            if f.get(self.field1) == yp and f.get(self.field2)==xp:
                selection = self.layer.getSelection()
                selection.deselectAll()
                selection.select(f)
                return f.getCopy()
                
    def addValues(self, serie, ff1, ff2):
        if serie in self.series.keys():
            s = self.series[serie]
        else:
            s = XYSeries(serie)
            self.series[serie] = s
        s.add(XYDataItem(ff1, ff2))
        
    def updateSeries(self):
        for i in self.series.keys():
            serie = self.series[i]
            self.addSeries(serie)
            

      
def createChart(dataset,field1="", field2=""):
    chart = ChartFactory.createScatterPlot("",
            field1, field2, dataset, PlotOrientation.VERTICAL, True, True, False)
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
    
def createPanelMouseListener(chart):
    panel = createPanel(chart)
    panel.addChartMouseListener(MyChartMouseListener(panel))
    return panel

def createPanel(chart):
    panel = ChartPanel(chart)
    panel.setMouseWheelEnabled(True)
    return panel
    
#def createPanel(dataset, field1="", field2=""):
#    chart = createChart(dataset, field1, field2)
#    panel = ChartPanel(chart)
#    panel.setMouseWheelEnabled(True)
#    panel.addChartMouseListener(MyChartMouseListener(panel))
#    return panel

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
        feature = dataset.getFeatureSelected(xp,yp)

        #serie = dataset.getSeries("Coord")
        #print serie.getDataItem(n)
        return
        
    def chartMouseClicked(self, event):
        pass

    def chartMouseMoved(self, event):
        pass
        
def main(*args):

    #Remove this lines and add here your code
    layer = gvsig.currentView().getLayer("V")
    #dp = createPanel()#layer, "LATITUDE", "LONGITUDE")
    print dp
    pass
