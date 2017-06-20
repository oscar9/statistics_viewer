# encoding: utf-8

import gvsig
from org.jfree.chart import ChartFactory, ChartPanel, JFreeChart
from org.jfree.chart.plot import PlotOrientation
from org.jfree.data.category import CategoryDataset, DefaultCategoryDataset
from org.jfree.ui import ApplicationFrame, RefineryUtilities
from java.awt import Dimension
from java.io import FileOutputStream
from org.jfree.chart import ChartUtilities

from org.jfree.data.xy import DefaultXYZDataset

class svDefaultXYZDataset(DefaultXYZDataset):
    def __init__(self):
        self.append()
    def append(self, features=None):
      ad  = [30 , 40 , 50 , 60 , 70 , 80 ]
      ad1 = [10 , 20 , 30 , 40 , 50 , 60 ]
      ad2 = [4 , 5 , 10 , 8 , 9 , 6 ]
      ad3 =  [ ad , ad1 , ad2 ]
      self.addSeries( "Series 1" , ad3 )
      import random
      a = random.randint
      ad  = [a(30,100) , a(20,100) , a(60,100) , a(70,100) , a(20,100) , a(10,100) ]
      ad1 = [a(0,30) , a(0,30) , a(0,40) , a(0,60) , a(0,40) , a(0,10) ]
      ad2 = [a(0,10) , a(0,10) , a(0,10) ,a(0,10) , a(0,10) , a(0,10) ]
      ad3 =  [ ad , ad1 , ad2 ]
      self.addSeries( "Series 2" , ad3 )
      
class svDefaultCategoryDataset(DefaultCategoryDataset):
    #dataset = None

    def __init__(self):
        #self.dataset = DefaultCategoryDataset()
        self.append()
        
    def append(self, features=None):
      import random
      fiat = "FIAT"
      audi = "AUDI"
      ford = "FORD"
      speed = "Speed"
      millage = "Millage"
      userrating = "User Rating"
      safety = "safety"

      self.addValue( random.randint(1, 100) , fiat , speed )
      self.addValue( random.randint(1, 100) , fiat , userrating )
      self.addValue( random.randint(1, 100) , fiat , millage )
      self.addValue( random.randint(1, 100) , fiat , safety )

      self.addValue( random.randint(1, 100) , audi , speed )
      self.addValue( random.randint(1, 100) , audi , userrating )
      self.addValue( random.randint(1, 100) , audi , millage )
      self.addValue( random.randint(1, 100) , audi , safety )

      self.addValue( random.randint(1, 100) , ford , speed )
      self.addValue( random.randint(1, 100) , ford , userrating )
      self.addValue( random.randint(1, 100), ford , millage )
      self.addValue( random.randint(1, 100) , ford , safety )


        
class plot():
    graphname = "generic plot"
    chart = None
    chartPanel = None
    def __init__(self, name):
        self.setName(name)

    def setName(self, name):
        self.graphname = str(name)

    def getName(self):
        return self.graphname
        
    def getChart(self):
        return self.chart

    def getChartPanel(self):
        return self.chartPanel

    def setChart(self, newchart):
        self.chart = newchart

    def savePlotImage(self, imagePath):
        out = FileOutputStream(imagePath)
        
        ChartUtilities.writeChartAsPNG(out,
                self.getChart(),
                500, #aChartPanel.getWidth(),
                400)#aChartPanel.getHeight());
                
class createBarChart(plot):
    dataset = None

    def __init__(self, name, dataset):
        # meterlos en el init del abstract?
        self.setName(name)
        self.dataset = dataset
        self.updateChart(dataset)
    ## TODO posible error al pasarlet dataset por defecto
    
    def updateChart(self, ds=dataset, chartTitle=""):
        self.barChart = ChartFactory.createBarChart(
            chartTitle,
            "Category",
            "Score",
            ds,
            PlotOrientation.VERTICAL,
            True,
            True,
            False)
        self.setChart(self.barChart)
        #TODO crear en plot set por el panel
        self.chartPanel = ChartPanel(self.barChart)
        self.chartPanel.setPreferredSize(Dimension( 360 , 200 ) )
        #setContentPane(chartPanel)
        
class createXYZChart(plot):
    dataset = None

    def __init__(self, name, dataset):
        # meterlos en el init del abstract?
        self.setName(name)
        self.dataset = dataset
        self.updateChart(dataset)
    ## TODO posible error al pasarlet dataset por defecto
    
    def updateChart(self, ds=dataset, chartTitle=""):
        self.barChart = ChartFactory.createBubbleChart(
         "Wealth",
         "Pob",
         "Age",
         ds,
         PlotOrientation.HORIZONTAL,
         True,
         True,
         False)
        #extras
        xyplot = self.barChart.getPlot( )
        xyplot.setForegroundAlpha( 0.65 )
        xyitemrenderer = xyplot.getRenderer( )
        from java.awt import Color
        xyitemrenderer.setSeriesPaint( 0 , Color.blue )
        numberaxis = xyplot.getDomainAxis( )
        numberaxis.setLowerMargin( 0.2 )
        numberaxis.setUpperMargin( 0.5 )
        numberaxis1 = xyplot.getRangeAxis( )
        numberaxis1.setLowerMargin( 0.8 )
        numberaxis1.setUpperMargin( 0.9 )
        self.setChart(self.barChart)
        #TODO crear en plot set por el panel
        self.chartPanel = ChartPanel(self.barChart)
        self.chartPanel.setPreferredSize(Dimension( 360 , 200 ) )
        #setContentPane(chartPanel)

        
class createLineChart(plot):
    dataset = None

    def __init__(self, name, dataset):
        # meterlos en el init del abstract?
        self.setName(name)
        self.dataset = dataset
        self.updateChart(dataset)
    ## TODO posible error al pasarlet dataset por defecto
    
    def updateChart(self, ds=dataset, chartTitle=""):
        self.lineChart = ChartFactory.createLineChart(
         chartTitle,
         "h",
         "s",
         ds,
         PlotOrientation.VERTICAL,
         True,True,False)
        self.setChart(self.lineChart)
        #TODO crear en plot set por el panel
        self.chartPanel = ChartPanel(self.lineChart)
        self.chartPanel.setPreferredSize(Dimension( 360 , 200 ) )
        #setContentPane(chartPanel)
        

def main(*args):

    #ds = svDefaultCategoryDataset()
    #c = createBarChart("Boxplot x01", ds)
    #c.savePlotImage("/home/osc/temp/img1.png")
    
    #ds = svDefaultXYZDataset()
    #c = createXYZChart("Chart x01", ds)
    #c.savePlotImage("/home/osc/temp/xyz1.png")
    
    ds = svDefaultCategoryDataset()
    c = createLineChart("Line chart x01", ds)
    c.savePlotImage("/home/osc/temp/img1.png")