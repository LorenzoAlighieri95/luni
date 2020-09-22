import os
import sys
import inspect
from math import sqrt
from PyQt5.QtGui import QIcon,QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QWidget, QVBoxLayout, QLineEdit, QCompleter
from PyQt5.QtCore import pyqtSlot, QStringListModel, Qt,QPoint, QVariant
import processing
from processing.tools import dataobjects
from processing.core.Processing import Processing
from qgis.utils import iface
from qgis.gui import QgsRubberBand
import qgis.core
from qgis.core import (
   edit,
   QgsExpression,
   QgsExpressionContext,
   QgsFeature,
   QgsFeatureRequest,
   QgsField,
   QgsFields,
   QgsVectorLayer,
   QgsPointXY,
   QgsPoint,
   QgsGeometry,
   QgsProject,
   QgsExpressionContextUtils,
   Qgis,
   QgsMapLayer,
   QgsDistanceArea,
   QgsProcessingFeedback,
   QgsProcessingFeatureSourceDefinition
)

class GeomTools:
    def getElevationData(self, a, b):
      #Dal layer dei beni estrae i centroidi;
      #utilizzando le funzioni di processing necessarie crea un nuovo layer con la colonna dedicate all'altitudine
      #setta lo stile di tipo categorizzato 
      context = dataobjects.createContext()
      context.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)
      layerBeni = Utils().getLayerBeni()
      vlayer = GeomTools().createCentroidsLayer(layerBeni,False,'Centroids')
      rlayer = QgsProject.instance().mapLayersByName('Elevazione')[0]
      pointz = processing.run("native:setzfromraster", 
          {'INPUT':vlayer,
          'RASTER':rlayer.source(),'BAND':1,'NODATA':0,'SCALE':1,
          'OUTPUT': 'memory:'}, context=context)['OUTPUT']
      pointz2 = processing.run("native:extractzvalues", 
          {'INPUT':pointz,'SUMMARIES':[0],'COLUMN_PREFIX':'altitude_',
          'OUTPUT': 'memory:'}, context=context)['OUTPUT']
      pointz2.setName("beni_altitudine")
      QgsProject.instance().addMapLayer(pointz2)
      QgsProject.instance().removeMapLayers( [vlayer.id()] )
      Utils().setStyle('elevation',pointz2)
      for layer in QgsProject.instance().mapLayers().values():
        if layer.name() == layerBeni.name():
          QgsProject.instance().layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(False)
      expr = "altitude_first >= " + str(a) + " and altitude_first <= " + str(b)
      QueryLayer().selectionByExpr(pointz2,expr)

    def getBeniInRaggio(self, beneId, radius):
      #Dato un bene e un raggio;
      #crea un nuovo layer con sistema di riferimento metrico;
      #crea un buffer intorno al bene in base raggio;
      #restituisce l'espressione per selezionare la lista degli id dei beni che si intersecano con il buffer
      layer3003 = Utils().getLayerBeni3003()
      expr = "id = '"+beneId+"'"
      selection = QueryLayer().selectionByExpr(layer3003, expr)
      geom = selection[0].geometry().centroid()
      buff = geom.buffer(radius,5)
      intersectedFeaturesList=[]
      for feature in layer3003.getFeatures():
        if feature.geometry().intersects(buff):
            intersectedFeaturesList.append(str(feature.attributes()[0])) 
      expr = QueryLayer().IdListToExpr(intersectedFeaturesList)  
      return expr

    def createCentroidsLayer(self,layer,filt,name):
      #Dato un layer di tipo poligonale, ne crea una copia utilizzandone i centroidi;
      #In base al filtro scelto utilizza solo le features selezionate (o tutte le features se non esiste un filtro):
      #aggiunge i campi prob, ruolo e probRuolo
      if filt:
        QueryLayer().selectionByExpr(layer,filt)
      else:
        layer.selectAll()
      context = dataobjects.createContext()
      context.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)
      params = {'INPUT': QgsProcessingFeatureSourceDefinition(layer.id(), True), 
                'ALL_PARTS':False,
                'OUTPUT': 'memory:'}
      newLayer = processing.run("native:centroids", params, context=context)
      layerOutput = newLayer['OUTPUT']
      data_provider = layerOutput.dataProvider()
      data_provider.addAttributes([QgsField('prob',  QVariant.Int)])
      data_provider.addAttributes([QgsField('ruolo',  QVariant.String)])
      data_provider.addAttributes([QgsField('probRuolo',  QVariant.String)])
      layerOutput.updateFields()
      layerOutput.setName(name)
      QgsProject.instance().addMapLayer(layerOutput)
      QgsProject.instance().layerTreeRoot().findLayer(layerOutput.id()).setItemVisibilityChecked(False)
      layer.removeSelection()
      iface.setActiveLayer(layerOutput)
      return layerOutput

    def createConvexHull(self,lBeni,b1,b2):
      #Data una lista di beni calcola il convexhull corrispondente;
      #utilizza l'algoritmo minimumboundinggeometry;
      #setta il context affinchè non ci sia il check sulle geometrie invalide
      layer = Utils().getLayerBeni()
      layerOutput=False
      for feat in layer.getFeatures():
        if feat['ident'] in lBeni:
          beneId = str(feat['id'])
          dipendentiIds = QueryLayer().getDependenciesList(beneId,b1,b2)
          if len(dipendentiIds)>2:
            expr = QueryLayer().IdListToExpr(dipendentiIds)
            QueryLayer().selectionByExpr(layer,expr)
            context = dataobjects.createContext()
            context.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)
            params = {'INPUT': QgsProcessingFeatureSourceDefinition(layer.id(), True),
                      'TYPE': 3,
                      'OUTPUT': 'memory:'}
            newconvexhulllayer = processing.run("qgis:minimumboundinggeometry", params, context=context) 
            layerOutput = newconvexhulllayer['OUTPUT']
            layerOutput.setName('areaBene'+beneId )
            layerOutput.startEditing()
            for feat in layerOutput.getFeatures():
              feat['id']=beneId
              layerOutput.updateFeature(feat)
            layerOutput.commitChanges()
            Utils().setStyle("buffer",layerOutput)
            QgsProject.instance().addMapLayer(layerOutput)         
      if layerOutput != False:
        if len(lBeni)>1:
          Utils().zoomToLayer(Utils().getLayerBeni())
        else:
          Utils().zoomToLayer(layerOutput)
      else:
        iface.messageBar().pushMessage('Attenzione', 'Non esistono beni o relazioni con queste caratteristiche', level=Qgis.Critical)

    def createBuffer(self,lBeni,b1,b2):
      #Crea un buffer per ogni bene contenuto nella lista in input;
      #Il raggio del buffer corrisponde alla distanza del bene dipendente più lontano;
      #Setta lo stile e aggiunge il layer con i buffer
      layer = Utils().getLayerBeni3003()   
      buff_layer=False
      for feat in layer.getFeatures():
        if feat['ident'] in lBeni:
          beneId = str(feat['id'])
          dipendentiIds = QueryLayer().getDependenciesList(beneId,b1,b2)
          if len(dipendentiIds)>2:
            buff_layer = QgsVectorLayer("Polygon?crs=epsg:3003",'bufferBene'+beneId, "memory")
            geom = feat.geometry().centroid()
            bufferDist = self.getFarestDistance(beneId,dipendentiIds)*1000
            buff = geom.buffer(bufferDist, 25)
            f = QgsFeature()
            f.setGeometry(buff)
            f.setFields(feat.fields())
            f.setAttributes(feat.attributes())
            buff_layer.dataProvider().addFeatures([f])
            Utils().setStyle("buffer",buff_layer)
            QgsProject.instance().addMapLayer(buff_layer)    
      if buff_layer != False:
        if len(lBeni)>1:
          Utils().zoomToLayer(Utils().getLayerBeni())
        else:
          Utils().zoomToLayer(buff_layer)
      else:
        iface.messageBar().pushMessage('Attenzione', 'Non esistono beni o relazioni con queste caratteristiche', level=Qgis.Critical)

    def getFarestDistance(self, beneId, beniIds):
      #Dato un beneId e una lista di beniId;
      #restituisce la distanza del bene in beniIds più lontano da beneId
      measureList = []
      if len(beniIds)>0:
        for dipendenteId in beniIds:
          measure = self.getDistancesFromID(dipendenteId, beneId)
          if measure!="":
            measureList.append(float(measure))
        if len(measureList)>1:
          return float(max(measureList))
        else:
          return float(measureList[0])
      else:
        return 0

    def getNearestBeniFromID(self,n, beneId):
      #Restituisce l'elenco della distanza e degli ID degli n beni più vicini dal dato bene e li seleziona
      layerBeni=Utils().getLayerBeni()
      d={} 
      l=[] 
      ids=[]
      i=0
      for feat in layerBeni.getFeatures():
        measure=GeomTools().getDistancesFromID(beneId,feat['id'])
        if measure != "":
          d[float(measure)]=feat['id']
      for k in sorted(d.keys()):
          l.append([k,d[k]])
          ids.append(str(d[k]))
          if i < n:
            i=i+1
          else:
            break
      QueryLayer().selectionByExpr(layerBeni,QueryLayer().IdListToExpr(ids))
      Utils().zoomToSelectedFeature(layerBeni)
      return l

    def getGeomStart(self,beneId): 
      #Dato un bene in input; 
      #seleziona il bene corrispondente dal layer dei beni e ne restituisce la geometria
      layerBeni = Utils().getLayerBeni()
      expr = "id = '"+beneId+"'"
      selection = QueryLayer().selectionByExpr(layerBeni,expr)
      geom = selection[0].geometry()
      return geom
    
    def getGeomEnd(self,query,beneId,direction): 
      #Dato un bene in input;
      #seleziona tutti i beni che hanno una relazione con esso;
      #chiama la funzione che disegna una linea tra il bene in input e le sue dipendenze, o viceversa
      #direction indica il verso della freccia 
      geomStart = self.getGeomStart(beneId).centroid()
      layerBeni = Utils().getLayerBeni()
      selectionBeni = QueryLayer().selectionByQuery(layerBeni,query)
      if len(selectionBeni)>0:
        v_layer = self.getLayerLines(beneId)
        for feat in selectionBeni: 
            endName = str(feat['id'])
            geomEnd = feat.geometry().centroid()
            if direction:
              self.drawLine(geomStart,geomEnd,beneId,endName,v_layer)
              self.findNewRelation(endName,geomEnd,v_layer,6)
            else:
              self.drawLine(geomEnd,geomStart,endName,beneId,v_layer)
        QueryLayer().selectionByExpr(layerBeni,"id = "+beneId)
        Utils().zoomToLayer(v_layer)
        Utils().moveLayerOnTop(layerBeni)
    
    def findNewRelation(self,beneId,geomStart,v_layer,n):
      #Cerca ricorsivamente se ci sono ulteriori dipendenze
      if n>0:
        layerBeni=Utils().getLayerBeni()
        query="SELECT funzionigeo.id_bener FROM funzionigeo WHERE funzionigeo.id_bene ='"+beneId+"'"
        selectionBeni = QueryLayer().selectionByQuery(layerBeni,query)
        for feat in selectionBeni: 
          endName = str(feat['id'])
          geomEnd = feat.geometry().centroid()
          self.drawLine(geomStart,geomEnd,beneId,endName,v_layer)
          geomStart = geomEnd    
          self.findNewRelation(endName,geomStart,v_layer,n-1)
    
    def drawLine(self, line_start, line_end,startName,endName,v_layer): 
      #Crea una linea dati due punti;
      #la mostra come nuovo layer;
      #setta lo stile corrispondente 
      layerRelazioni=Utils().getLayerRelazioni()
      start_point = QgsPoint(line_start.asPoint())
      end_point = QgsPoint(line_end.asPoint())
      pr = v_layer.dataProvider()
      seg = QgsFeature()   
      seg.setFields(v_layer.fields())
      for feat in layerRelazioni.getFeatures():
        if feat['id_bene']==int(startName) and feat['id_bener']==int(endName):
          seg['id_bene']=feat['id_bene']
          seg['id_bener']=feat['id_bener']
          seg['data']=feat['data_ante']
          seg['funzione']=feat['funzione']
          seg['tipo']=Utils().getTipoRel(feat['funzione'])
          seg['importanza']=Utils().getImportanzaRel(feat['funzione'])
          seg.setGeometry(QgsGeometry.fromPolyline([start_point, end_point]))
          pr.addFeatures( [ seg ] ) 
      
    def getLayerLines(self,beneId):
      #Genera il layer che rappresenta le relazioni
      layerName='relazioniBene'+beneId
      v_layer = QgsVectorLayer('LineString?crs=epsg:4326', layerName, 'memory')
      pr = v_layer.dataProvider()
      pr.addAttributes([QgsField('id_bene',  QVariant.String)])
      pr.addAttributes([QgsField('funzione',  QVariant.String)]) 
      pr.addAttributes([QgsField('id_bener',  QVariant.String)])
      pr.addAttributes([QgsField('data',  QVariant.String)]) 
      pr.addAttributes([QgsField('tipo',  QVariant.String)])
      pr.addAttributes([QgsField('importanza',  QVariant.String)])
      pr.addAttributes([QgsField('overlay',  QVariant.String)])
      v_layer.updateFields()
      QgsProject.instance().addMapLayers([v_layer])
      Utils().setStyle("arrow",v_layer)  
      iface.setActiveLayer(v_layer)
      return v_layer

    def getDistancesFromID(self, featureID1, featureID2): 
      #Calcola la distanza tra due features dati gli ID
      layer = Utils().getLayerBeni()
      expr = "id in ('"+str(featureID1)+"','"+str(featureID2)+"')"
      selection = QueryLayer().selectionByExpr(layer,expr)
      measure=''
      if len(selection)>1:
        geom1 = selection[0].geometry().centroid().asPoint()
        geom2 = selection[1].geometry().centroid().asPoint()  
        d = QgsDistanceArea()
        d.setEllipsoid('WGS84')
        measure=d.measureLine(geom1, geom2)/1000
        measure=round(measure,1)
        Utils().zoomToSelectedFeature(layer)
      return str(measure)
    
    def getPointFromFeature(self, featureID, layer): 
      #Data una feature di un dato layer ne restituisce il punto geometrico
      expr = "id = '"+featureID+"'"
      selection = QueryLayer().selectionByExpr(layer,expr)
      geom = selection[0].geometry()
      return geom

    def getDistancesFromGeom(self, pointGeom, riverGeom): 
      #Calcola la distanza tra la geometria di una feature e la geometria di un fiume utilizzando il punto più vicino
      d = QgsDistanceArea()
      d.setEllipsoid('WGS84')
      nearest_point_on_river = riverGeom.nearestPoint(pointGeom)
      measure=d.measureLine(pointGeom.asPoint(), nearest_point_on_river.asPoint())/1000
      measure=round(measure,1)
      Utils().zoomToSelectedFeature(Utils().getLayerBeni())
      return float(measure)

    def getRiversDistances(self, featureID): 
      #Calcola la distanza tra un dato bene e tutti i fiumi;
      #Usa un dizionario che contiene come chiave la distanza dal bene dato e come valore il nome del fiume;
      #Ordina il dizionario in base alle chiavi;
      #Controlla che il valore non sia la stringa "NULL" e che il valore non sia già contenuto nella stringa risultante
      #Restituisce la stringa che contiene i nomi dei fiumi e la distanza dal bene
      layerFiumi = Utils().getLayerFiumi()
      layerBeni = Utils().getLayerBeni()
      geomBene = self.getPointFromFeature(featureID, layerBeni).centroid()
      d = {}
      for river in layerFiumi.getFeatures():
        d[self.getDistancesFromGeom(geomBene, river.geometry())] = str(river[1])
      str_list = []
      result = ""
      for k in sorted(d.keys()):
        if d[k] is not "NULL" and result.count(d[k])==0:
          str_list.append(d[k]+ " : " + str(k)+" km"+"\n")
          result = ''.join(str_list)
      return result

    def getOneRiverDistance(self,fiumeIdent,inputDistance):
      #Dato l'identificativo di un fiume e una distanza in Input;
      #seleziona il fiume necessario, per mezzo di espressione, e ne prende la geometria;
      #per ogni bene calcola la distanza con il fiume e, se la distanza e minore della misura in input, salva l'id del bene in una lista
      #crea l'espressione per selezionare tutti gli id contenuti nella lista precedente
      layerBeni = Utils().getLayerBeni()
      layerFiumi = Utils().getLayerFiumi()
      expr = "name = '"+fiumeIdent+"'"
      selection = QueryLayer().selectionByExpr(layerFiumi, expr)
      geomRiver = selection[0].geometry()
      idsBeniList = []
      for feat in layerBeni.getFeatures():
        beneId = str(feat['id'])
        geomBene = self.getPointFromFeature(beneId,layerBeni).centroid()
        distance = self.getDistancesFromGeom(geomBene,geomRiver)
        if distance <= inputDistance:
          idsBeniList.append(beneId)
      expr = QueryLayer().IdListToExpr(idsBeniList)
      layerFiumi.removeSelection()
      return expr

from .queryLayer import QueryLayer
from .utils import Utils