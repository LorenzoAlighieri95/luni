import os
import sys
import inspect
from math import sqrt
from pathlib import Path
from PyQt5.QtGui import QIcon,QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QWidget, QVBoxLayout, QLineEdit, QCompleter
from PyQt5.QtCore import pyqtSlot, QStringListModel, Qt,QPoint, QVariant,QSettings
import processing
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
   QgsSvgMarkerSymbolLayer,
   QgsFillSymbol,
   QgsRuleBasedRenderer,
   QgsSymbol,
   QgsMarkerSymbol,
   QgsCentroidFillSymbolLayer
)

class Utils:
    
    def setSvgIconsPath(self):
      #Setta il path per caricare le icone
      my_new_path = str(Path(__file__).parents[1])+ '//styles//icons'
      QSettings().setValue('svg/searchPathsForSVG', my_new_path)

    def getResult(self): 
      #Permette di sapere se vi sono features selezionate in tutti i layer
      f = False
      for layer in QgsProject.instance().mapLayers().values():
        if layer.type() != QgsMapLayer.RasterLayer:
          if len(layer.selectedFeatures())>0:
            f = True
      return f
    
    def setColumnVisibility(self, layer, columnName, visible): 
      #Data una lista con i nomi delle colonne nasconde (visible = False) o mostra (visible = True) le colonne indicate
      config = layer.attributeTableConfig()
      columns = config.columns()
      for column in columns:
          for name in columnName:
              if column.name == name:
                  column.hidden = not visible
      config.setColumns( columns )
      layer.setAttributeTableConfig( config )
      
    def deleteVirtualLayer(self): 
      #Elimina i layer virtuali
      layerList = QgsProject.instance().mapLayersByName('vlayer')
      for i in layerList:
        QgsProject.instance().removeMapLayer( i )
      
    def getLayerBeni(self): 
      #Restituisce il layer dei beni
      return QgsProject.instance().mapLayersByName('benigeo')[0]
    
    def getLayerRelazioni(self): 
      #Restituisce il layer delle relazioni
      return QgsProject.instance().mapLayersByName('funzionigeo')[0]

    def getLayerRelazioniRuoli(self):
      #Restituisce il layer che contiene i ruoli
      return QgsProject.instance().mapLayersByName('funzionigeo_ruoli')[0]

    def getLayerFiumi(self): 
      #Restituisce il layer dei fiumi
      return QgsProject.instance().mapLayersByName('fiumi_lunigiana')[0]

    def getLayerComuni(self):
      #Restituisce il layer dei comuni
      return QgsProject.instance().mapLayersByName('comuni_lunigiana')[0]

    def getLayerBeni3003(self):
      #Restituisce il layer dei beni con un sistema di riferimento metrico (EPSG:3003)
      Processing.initialize()
      layer = self.getLayerBeni()
      parameter = {'INPUT': layer, 'TARGET_CRS': 'EPSG:3003','OUTPUT': 'memory:Reprojected'}
      result = processing.run('native:reprojectlayer', parameter)
      layer3003 = result['OUTPUT']
      return layer3003

    def removeSelectedFeatures(self): 
      #Rimuove tutte le features selezionate
      for layer in QgsProject.instance().mapLayers().values():
        if layer.type() != QgsMapLayer.RasterLayer:
          layer.removeSelection()
      
    def showAttributeTableLayer(self,layer,selected): 
      #Questa funzione chiude tutte le tabelle degli attributi aperte
      #apre la tabella attributi del layer in input visualizzando i soli elementi selezionati
      attrTables = [d for d in QApplication.instance().allWidgets() if d.objectName() == u'QgsAttributeTableDialog' or d.objectName() == u'AttributeTable']
      for x in attrTables:
        x.close()
      attDialog = iface.showAttributeTable(layer)
      QSettings().setValue("/Qgis/dockAttributeTable", True)
      if selected:
        attDialog.findChild(QAction, "mActionSelectedFilter").trigger()

    def setStyle(self,style,layer):
      #Data una stringa che indica lo stile e il layer su cui caricarlo
      #carica lo stile
      p = str(Path(__file__).parents[1])+ r'/styles/'
      selectedStyle=''
      if style == 'default':
        selectedStyle = p + 'default_style.qml'
      if style == 'fiumi':
        selectedStyle = p + 'fiumi.qml'
      if style == 'arrow':
        selectedStyle = p + 'arrow_rules.qml'
      if style == 'All_PRR_icons':
        selectedStyle = p + 'All_PRR_icons_centroids.qml'
      if style == 'buffer':
        selectedStyle = p + 'buffer.qml'
      if style == 'comuni':
        selectedStyle = p + 'comuni.qml'
      if style == 'heatmap':
        selectedStyle = p + 'prob_heatmap.qml'
      if style == 'elevation':
        selectedStyle = p + 'elevation.qml'
      if layer:
        layer.loadNamedStyle(selectedStyle)
        layer.triggerRepaint()
      style=''

    def getMessage(self,layer):
      #Controlla se ci sono o meno beni selezionati e in base a questo restituisce un messaggio
      if self.getResult(): 
        self.zoomToSelectedFeature(layer)
        iface.messageBar().pushMessage('Successo', 'Esistono beni o relazioni con queste caratteristiche', level=Qgis.Success)
      if not self.getResult():
        iface.messageBar().pushMessage('Attenzione', 'Non esistono beni o relazioni con queste caratteristiche', level=Qgis.Critical)
        #self.restoreLayerBeni()

    def checkFieldExists(self, field_name, layer):
      #Controlla se un dato field esiste in un dato layer
      field_index = layer.fields().indexFromName(field_name)
      if field_index == -1:
          return False
      else: 
          return True

    def getVectorLayersNameList(self):
      #Restituisce la lista dei nomi di tutti i layer vettoriali
      l=[]
      for layer in QgsProject.instance().mapLayers().values():
        if layer.type() != QgsMapLayer.RasterLayer:
          l.append(layer.name())
      return l

    def deleteNewLayers(self):
      #Elimina tutti i layer che non sono quelli di base del progetto
      for layer in QgsProject.instance().mapLayers().values():
        name = layer.name()
        if 'area' in name or 'relazioni' in name or 'Periodo' in name or 'Ruoli' in name or 'buffer' in name or 'altitudine' in name:
          QgsProject.instance().removeMapLayer(layer)
          iface.mapCanvas().refresh()

    def restoreLayerBeni(self):
      #Riporta il layer dei beni allo stato iniziale
      iface.mapCanvas().setSelectionColor( QColor("Purple") )
      layerBeni = Utils().getLayerBeni()
      self.removeSelectedFeatures()
      self.setStyle('fiumi',Utils().getLayerFiumi())
      self.setStyle('default',layerBeni)
      self.setStyle('comuni',Utils().getLayerComuni())
      QgsProject.instance().layerTreeRoot().findLayer(layerBeni.id()).setItemVisibilityChecked(True)
      #self.setColumnVisibility(layerBeni,layerBeni.fields(),True) deprecated
      self.zoomToLayer(layerBeni)

    def zoomToSelectedFeature(self,layer):
      #Dato un layer lo attiva e zoomma sulle features attive
      #In base al numero di features attive setta la scala per lo zoom
      iface.setActiveLayer(layer) 
      iface.mapCanvas().zoomToSelected()
      scale=iface.mapCanvas().scale()
      if len(layer.selectedFeatures())>5:
        newScale = scale + 0.5 * scale
      if len(layer.selectedFeatures())<=5:
        newScale = scale + 1.5 * scale
      if len(layer.selectedFeatures())<=3:
        newScale = scale + 2 * scale
      if len(layer.selectedFeatures())==1:
        newScale = scale + 10 * scale
      iface.mapCanvas().zoomScale(newScale)

    def zoomToLayer(self,layer):
      #Zooma sul layer in input attivandolo
      iface.setActiveLayer(layer)  
      iface.zoomToActiveLayer()

    def moveLayerOnTop(self,layer):
      #Dato un layer lo sposta on top nella lista dei layer e sulla mappa
      root = QgsProject.instance().layerTreeRoot()
      for ch in root.children():
        if ch.name() == layer.name():
          _ch = ch.clone()
          root.insertChildNode(0, _ch)
          root.removeChildNode(ch)
    
    def getSvgIcon(self,Pmed,RuoloP):
      #Data la probabilità media e il ruolo principale di un bene restituisce l'icona.svg
      p = str(Path(__file__).parents[1])+ r'/styles/icons/'
      icon=""
      if Pmed>70 and (RuoloP =='arcipretura' or RuoloP == 'pieve'  or RuoloP == 'prioria'):
          icon=p+"bigChurch_V.svg"
      elif Pmed<70 and Pmed>40 and (RuoloP =='arcipretura' or RuoloP == 'pieve' or RuoloP == 'prioria'):
          icon=p+"bigChurch_A.svg"
      elif Pmed>10 and Pmed<40 and (RuoloP =='arcipretura' or RuoloP == 'pieve' or RuoloP == 'prioria'):
          icon=p+"bigChurch_R.svg"
      elif Pmed>70 and (RuoloP == 'cappella' or RuoloP == 'chiesa' or RuoloP== 'oratorio' or RuoloP == 'rettoria'):
         icon=p+"littleChurch_V.svg"
      elif Pmed<70 and Pmed>40 and (RuoloP == 'cappella' or RuoloP == 'chiesa' or RuoloP== 'oratorio' or RuoloP == 'rettoria'):
          icon=p+"littleChurch_A.svg"
      elif Pmed>10 and Pmed <40 and (RuoloP == 'cappella' or RuoloP == 'chiesa' or RuoloP== 'oratorio' or RuoloP == 'rettoria'):
          icon=p+"littleChurch_R.svg"
      elif Pmed > 70 and RuoloP == 'ospedale':
          icon=p+"hospital_V.svg"
      elif Pmed< 70 and Pmed > 40 and RuoloP == 'ospedale':
          icon=p+"hospital_A.svg"
      elif Pmed> 10 and Pmed < 40 and RuoloP == 'ospedale':
          icon=p+"hospital_R.svg"
      elif Pmed > 70 and (RuoloP == 'monastero' or RuoloP == 'convento'):
          icon=p+"mon_V.svg"
      elif Pmed < 70 and Pmed > 40  and (RuoloP == 'monastero' or RuoloP == 'convento'):
          icon=p+"mon_A.svg"
      elif Pmed >10 and Pmed < 40  and (RuoloP == 'monastero' or RuoloP == 'convento'):
          icon=p+"mon_R.svg"
      else:
          icon=p+"" 
      return icon
    
    def setStyleIcon(self,svg):
      #Dato il path di un'icona svg la setta come stile per le sole features selezionate nel layer dei beni
      vlayer = self.getLayerBeni()
      if len(vlayer.selectedFeatures())==1:
        svgStyle = {
            "name": svg,
            "outline": "#000000",
            "size": "15",
        }
        svgLayer = QgsSvgMarkerSymbolLayer.create(svgStyle)
        svgSymbol = QgsMarkerSymbol()
        svgSymbol.changeSymbolLayer(0, svgLayer)
        symbol = QgsSymbol.defaultSymbol(vlayer.geometryType())
        symbol.setColor(QColor("Blue"))
        centroid = QgsCentroidFillSymbolLayer()
        centroid.setSubSymbol(svgSymbol)
        selectedSymbol = QgsFillSymbol()
        selectedSymbol.changeSymbolLayer(0, centroid)
        renderer = QgsRuleBasedRenderer(symbol)
        rule = QgsRuleBasedRenderer.Rule(
            selectedSymbol, label="Selected", filterExp="is_selected()"
        )
        renderer.rootRule().appendChild(rule)
        vlayer.setRenderer(renderer)
        vlayer.triggerRepaint()

    def getAllIdsBeni(self):
      #Restituisce l'elenco di tutti gli ID dei beni
      layerBeni=Utils().getLayerBeni()
      l=[]
      for feat in layerBeni.getFeatures():
        l.append(feat['id'])
      return l 

    def getTipoRel(self, funzione):
      #Data una funzione, ne restituisce il tipo
      switcher = {
        'cede il ruolo a':'ecclesiastica',
        'dipende da':'ecclesiastica',
        'dipende da ed è nel distretto di':'amministrativa',
        'dipende patrimonialmente da (appartiene a)':'economica',
        'è nel distretto di':'amministrativa',
        'paga tributo a':'economica'
        }
      return switcher.get(funzione,"indeterminato")
    
    def getImportanzaRel(self, funzione):
      #Data una funzione, ne restituisce l'importanza
      switcher = {
        'cede il ruolo a':'importanza media',
        'dipende da':'molto importante',
        'dipende da ed è nel distretto di':'importanza media',
        'dipende patrimonialmente da (appartiene a)':'importante',
        'è nel distretto di':'importanza media',
        'paga tributo a':'importante'
        }
      return switcher.get(funzione,"indeterminato")

    def overlayTemporale(self,a1,b1,b2):
      #Dato un periodo di riferimento (a) e un periodo di analisi (b), restituisce la sovrapposizione tra i due periodi.
      #1: non c'è sovrapposizione; 2: la sovrapposizione è parziale; 3: la sovrapposizione è totale;
      #Gli altri codici indicano errore
      from .PRR20AK22 import dataVera,dataConverti
      if a1 == qgis.core.NULL:
        a1 = None
      dateA = dataConverti(a1)
      a1=dateA[0]
      a2=dateA[1]
      if b2 == "": b2=b1
      if a1>a2 or b1>b2: return "errore"			
      if b2<a1: return "fuori"				
      if b1>a2: return "fuori"				
      if b1<a1 and b2>=a1 and b2<a2: return "parziale"
      if b1>a1 and b1<=a2 and b2>a2: return "parziale"
      if b1<=a1 and b2>=a2 : return "dentro"
      if b1>a1 and b2<=a2: return "dentro"	
      if b1>=a1 and b2<a2: return "dentro"	
      return -99

    def layerRelExists(self):
      #Controlla che tra i layer ce ne sia almeno uno che contiene la parola 'relazioni'
      rel = False
      for layer in QgsProject.instance().mapLayers().values():
        if 'relazioni' in layer.name():
          rel = True
      return rel

    def setMapTip(self,layer,attr):
      #Setta il MapTip dato un layer e un attributo da visualizzare
      expression = '<style>.t {color: black; font-size:20px;}</style>'+'<span class="t">'+attr+': [% "'+attr+'" %]</span>'
      layer.setMapTipTemplate(expression)