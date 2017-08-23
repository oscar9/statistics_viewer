# encoding: utf-8

import gvsig
from addons.statistics_viewer.sv.dataProcess import gvDoublePoint
from addons.statistics_viewer.sv.svScatterPlot import svXYSeriesCollection
from gvsig import geom
from org.gvsig.symbology.fmap.mapcontext.rendering.legend.impl import VectorialUniqueValueLegend

def getUniqueSchemaField(layer, newfield):
    """Check if a field is already inside a layer schema, if it is, return a newone"""
    schAttr = layer.getSchema().getAttrNames()
    n = 0
    while newfield in schAttr:
        if newfield + str(n) not in schAttr:
            newfield = newfield + str(n)
            break
        n+=1
    return newfield
    
def mlGetXYClusterableCollectionFromLayer(newlayer, param_field1, param_field2):
    """Extract a XY values collection from a gvSIG layer using gvDoublePoint"""
    collection = []
    features = newlayer.features()
    for n,f in enumerate(features):
        dp = gvDoublePoint(f.getCopy(), param_field1, param_field2)
        collection.append(dp)
    return collection
    
def mlGetJfcCollectionFromClusters(newlayer, clusters, param_field1, param_field2):
    """Create a JFreeChart collection from clusters, features related by svCollection with layer"""
    collection = svXYSeriesCollection(param_field1, param_field2)
    for n, cluster in enumerate(clusters):
        for doublepoint in cluster.getPoints():
            point = doublepoint.getPoint()
            collection.addValues(str(n), point[0], point[1])
    # Process collection for chart
    collection.updateSeries()
    collection.setLayer(newlayer)
    return collection
    
def mlGetLayerFromXYClusters(newschema, clusters, newfieldcluster):
    """Create shape with a newschema from m3.clusters"""
    newschema.append(newfieldcluster, "INTEGER", 5)
    newlayer = gvsig.createShape(newschema)
    for n, cluster in enumerate(clusters):
        for doublepoint in cluster.getPoints():
            feature = doublepoint.getFeature()
            # TODO: trabajar con createFeature en vez de getValues para newschema diferente
            values = feature.getValues()
            values[newfieldcluster] = n
            newlayer.append(values)
            
    newlayer.commit()
    return newlayer
        
def chart2legend_UniqueValue(chart, newfieldcluster):
    legend = chart.getPlot().getLegendItems()
    vuvl = VectorialUniqueValueLegend(geom.POINT)
    for i in xrange(0, legend.getItemCount()):
        item = legend.get(i)
        yy = gvsig.simplePointSymbol(item.getFillPaint())
        label = str(item.getLabel())
        yy.setDescription(str(label))
        yy.setColor(item.getFillPaint())
        vuvl.addSymbol(int(label), yy)
    vuvl.setClassifyingFieldNames([newfieldcluster])
    return vuvl
    
def main(*args):

    #Remove this lines and add here your code

    print "hola mundo"
    pass
