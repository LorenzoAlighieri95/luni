import os
import sys
import inspect
from math import sqrt
from PyQt5.QtGui import QIcon,QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QWidget, QVBoxLayout, QLineEdit, QCompleter
from PyQt5.QtCore import pyqtSlot, QStringListModel, Qt,QPoint, QVariant
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
   QgsProcessingFeedback
)

from .PRR20AK22 import getPRRTable

class QueryLayer:

    def createPRRTable(self):
      #Crea la tabella per PRR
      LBeni,LFunz = QueryLayer().createLists()
      getPRRTable(LBeni,LFunz,Utils().getAllIdsBeni())

    def selectionById(self,beneID):
      #Seleziona un bene in base all'ID
      QueryLayer().selectionByExpr(Utils().getLayerBeni(),"id ="+beneID)

    def IdListToExpr(self,l): 
      #Data la lista dei beni o delle relazioni restituisce l'espressione QGIS che seleziona tutte le features corrispondenti
      seperator = ', '
      rowsString=seperator.join(l)
      expr = "id in ("+rowsString+")"
      return expr

    def selectionByExpr(self,layer,expr): 
      #Dato un layer e un'espressione QGIS
      #seleziona le features corrispondenti e restituisce la selezione
      it = layer.getFeatures(QgsFeatureRequest(QgsExpression(expr)))
      ids = [i.id() for i in it]
      layer.selectByIds(ids)
      selection = layer.selectedFeatures()
      return selection

    def selectionByQuery(self,layer,query):
      #Dato un layer e una query
      #seleziona le features corrispondenti e restituisce la selezione
      l = self.getListByQuery(query)
      expr = self.IdListToExpr(l)
      selection = self.selectionByExpr(layer,expr)
      return selection
    
    def getListByQuery (self, query): 
      #Data una query crea il layer virtuale corrispondente;
      #restituisce la lista degli id delle features nel layer
      #elimina il layer virtuale
      vlayer = QgsVectorLayer( "?query="+query, "vlayer", "virtual" )
      QgsProject.instance().addMapLayer(vlayer)
      l=[]
      for feature in vlayer.getFeatures():
        if feature[0]!=qgis.core.NULL:
          l.append(str(feature[0]))
      Utils().deleteVirtualLayer()
      return l

    def getIdByIdent(self, ident):
      #Dato l'identificatore di un bene restituisce l'id corrispondente
      layerBeni = Utils().getLayerBeni()
      expr = "ident = '"+ident+"'"
      selection = self.selectionByExpr(layerBeni,expr)
      if len(selection) > 0:
        for feat in selection:
          beneId = str(feat["id"])
        return beneId
      else:
        return False

    def checkId(self, beneId):
      #Controlla che un id esista e lo seleziona
      layerBeni = Utils().getLayerBeni()
      idList = self.getFeaturesList("id",layerBeni)
      if beneId in idList:
        expr = "id = '"+beneId+"'"
        self.selectionByExpr(layerBeni,expr)
        return beneId
      else:
        return False
    
    def inputValidty(self,inp):
      #Data un valore in input controlla che sia un ID valido;
      #in caso contrario, controlla che si tratta di un identificativo valido;
      #se l'identificativo è valido restituisce l'ID corrispondente, altrimenti restituisce False
      if inp != "": 
        if QueryLayer().checkId(inp):
          return inp
        else:
          return QueryLayer().getIdByIdent(inp)
      else:
        return False
    
    def getBeneId(self,inp1,inp2):
      #Restituisce l'id del bene controllando tra i beni selezionati;
      #se non trova nulla controlla la validità del valore in input;
      #se i valori in input sono due, restituisce due id beni
      if inp2 is False:
        if Utils().getResult():
          selection = Utils().getLayerBeni().selectedFeatures()
          if len(selection)==1:
            beneId = str(selection[0]['id'])
          else:
            beneId = self.inputValidty(inp1)
        else:
          beneId=self.inputValidty(inp1)
        return beneId
      else:
        if Utils().getResult():
          selection = Utils().getLayerBeni().selectedFeatures()
          if len(selection)==2:
            beneId1 = str(selection[0]['id'])
            beneId2 = str(selection[1]['id'])
          else:
            beneId1 = self.inputValidty(inp1)
            beneId2 = self.inputValidty(inp2)
        else:
          beneId1=self.inputValidty(inp1)
          beneId2=self.inputValidty(inp2)
        return beneId1, beneId2

    def getFieldsName(self,layer):
      #Dato un layer restituisce la lista dei nomi dei fields
      l = []
      for field in layer.fields():
        l.append(field.name())
      return l
    
    def getBeniConDipendenze(self,nBeni):
      #Restituisce l'elenco di tutti i beni che hanno un numero di dipendenze maggiore al numero in input
      layer = Utils().getLayerBeni()
      l = []
      query = "SELECT id_bener FROM funzionigeo GROUP BY id_bener HAVING COUNT(id_bener) > "+str(nBeni)
      selection=self.selectionByQuery(layer,query)
      Utils().removeSelectedFeatures()
      for feat in selection:
        l.append(str(feat['ident']))
      return l

    def getFeaturesList(self,name,layer): 
      #Dato il nome di un attributo (comun, meo, mec, ident, esist) restituisce la lista di tutti quegli attributi;
      #set elimina dalla lista gli elementi uguali;
      #sort ordina gli elementi alfabeticamente
      l=[]
      for feature in layer.getFeatures():
          if feature[name]!=qgis.core.NULL:
            l.append(str(feature[name]))
      setl= list(set(l))
      setl.sort()
      return setl

    def getAttributesList(self,layer):
      #Dato un layer, costruisce la lista di tutti gli attributi
      #Sostituisce i qgis.core.NULL con il valore None type previsto da PRR
      #restituisce la lista
      l = []
      for feature in layer.getFeatures():
        l.append(feature.attributes())
      for i in l:
        i[:] = [None if x==qgis.core.NULL else x for x in i]
      return l 

    def createLists(self):
      #Crea il layer delle funzioni comprendete anche i ruoli con una JOIN virtuale tra funzionigeo e funzionigeo_ruoli
      #Costruisce le liste necessarie;
      #Cancella il layer virtuale;
      layerBeni = Utils().getLayerBeni()

      #SEGUE UN PEZZO DI CODICE TEMPORANEO E DA RISOLVERE DEFINITIVAMENTE
      layerFunzioniRuolo=Utils().getLayerRelazioniRuoli()
      for field in layerFunzioniRuolo.fields():
        if field.name() == "ID_FUNZION":
          layerFunzioniRuolo.startEditing()
          layerFunzioniRuolo.renameAttribute(0,"ID_FUNZIONE")
          layerFunzioniRuolo.commitChanges()
      #FINE PEZZO DI CODICE TEMPORANEO
      
      layerFunzioni = QgsVectorLayer( "?query=SELECT id_bene,data_ante,data_poste,tipodata,ruolo,funzione,id_bener,ruolor FROM funzionigeo JOIN funzionigeo_ruoli ON funzionigeo.id = funzionigeo_ruoli.id_funzione", "vlayer", "virtual" )
      LBeni = self.getAttributesList(layerBeni)
      LBeniNomi = self.getFieldsName(layerBeni)
      LBeni.insert(0, LBeniNomi)
      LFunzioni = self.getAttributesList(layerFunzioni)
      LFunzioniNomi = self.getFieldsName(layerFunzioni)
      LFunzioni.insert(0,LFunzioniNomi)
      Utils().deleteVirtualLayer()
      return LBeni, LFunzioni

    def getLayerBeniCopy(self,nomeLayer):
      #Crea e restituisce un layer copia del layer dei beni e aggiunge i nuovi attributi prob, ruolo e probRuolo
      layerBeni=Utils().getLayerBeni()
      feats = [feat for feat in layerBeni.getFeatures()]
      mem_layer = QgsVectorLayer("Polygon?crs=epsg:4326",nomeLayer, "memory")
      mem_layer_data = mem_layer.dataProvider()
      attr = layerBeni.dataProvider().fields().toList()
      mem_layer_data.addAttributes(attr)
      mem_layer.updateFields()
      mem_layer_data.addFeatures(feats)
      QgsProject.instance().addMapLayers([mem_layer])
      data_provider = mem_layer.dataProvider()
      data_provider.addAttributes([QgsField('prob',  QVariant.Int)])
      data_provider.addAttributes([QgsField('ruolo',  QVariant.String)])
      data_provider.addAttributes([QgsField('probRuolo',  QVariant.String)])
      mem_layer.updateFields()
      return mem_layer

    def callPRR(self,dataUno,dataDue,beneId):
      #chiama PRR;
      #Costruisce e restituisce la stringa che indica l'output
      ProbPresMax, ProbPresMin, ProbPresMed, listaRuoli, Retcode = PRRBB20(beneId,str(dataUno),str(dataDue))
      if Retcode == 0:
        if len(listaRuoli)>1:
          output=[["...",str(ProbPresMed)+"%",str(ProbPresMax)+"%",str(ProbPresMin)+"%"],[str(listaRuoli[0][0][0]),str(listaRuoli[0][3])+"%",str(listaRuoli[0][1])+"%",str(listaRuoli[0][2])+"%"],[str(listaRuoli[1][0][0]),str(listaRuoli[1][3])+"%",str(listaRuoli[1][1])+"%",str(listaRuoli[1][2])+"%"]]
        else:
          output=[["...",str(ProbPresMed)+"%",str(ProbPresMax)+"%",str(ProbPresMin)+"%"],[str(listaRuoli[0][0][0]),str(listaRuoli[0][3])+"%",str(listaRuoli[0][1])+"%",str(listaRuoli[0][2])+"%"],["...","...","...","..."]]
        svgIcon = Utils().getSvgIcon(ProbPresMed,listaRuoli[0][0][0])
        Utils().setStyleIcon(svgIcon)
      else:
        output=False
        print ('RetCode = '+str(Retcode))
        iface.messageBar().pushMessage(
          'Attenzione', "Nessun record Funzione associato. Consultare console per il LOG", level=Qgis.Critical)
      return output

    def callPRRAllBeni(self,dataUno,dataDue,mem_layer):
      #Date le date in input
      #chiama PRR per tutte le feature nel layer dei beni
      #crea un layer copia del layer dei beni e aggiunge i nuovi attributi prob, ruolo e probRuolo
      #crea una lista che contiene per ogni feature: l'id del bene, la probabilità media, il ruolo primario, la probabilità media del ruolo primario
      #passa la lista a fillProbRuoloColumns()
      layerBeni = Utils().getLayerBeni()
      l=[]
      if len(layerBeni.selectedFeatures()) == 0:
        layerBeni.selectAll()
      for feature in layerBeni.selectedFeatures():
          idBene = str(feature['id'])
          ProbPresMax, ProbPresMin, ProbPresMed, listaRuoli, Retcode = PRRBB20(idBene,str(dataUno),str(dataDue))
          if Retcode == 0:
            l.append([idBene,ProbPresMed,listaRuoli[0][0][0],listaRuoli[0][1]])
      mem_layer.setName('beniPeriodo'+str(dataUno)+"."+str(dataDue))
      self.fillProbRuoloColumns(mem_layer,l)
    
    def callPRRRuoli(self,ruoli,dataUno,dataDue,mem_layer):
      #Dato l'elenco dei ruoli, due date, e un layer copia del layer dei beni;
      #esegue PRR su tutti i beni contenuti nel layer copia e crea una lista contenente idBene, Prob, RuoloP e ProbRuoloP dei beni che corrispondono ai ruoli selezionati;
      #se esistono beni corrispondenti ai ruoli scelti passa la lista a fillProbRuoloColumns()
      l=[]
      for feature in mem_layer.getFeatures():
        idBene = str(feature['id'])
        ProbPresMax, ProbPresMin, ProbPresMed, listaRuoli, Retcode = PRRBB20(idBene,str(dataUno),str(dataDue))
        if Retcode == 0:
          if listaRuoli[0][0][0] in ruoli:
            l.append([idBene,ProbPresMed,listaRuoli[0][0][0],listaRuoli[0][1]])
      if len(l)>0:
        mem_layer.setName('beniRuoli'+str(dataUno)+"."+str(dataDue))
        self.fillProbRuoloColumns(mem_layer,l)
      else:
        iface.messageBar().pushMessage(
          'Attenzione', 'Non esistono beni o relazioni con queste caratteristiche', level=Qgis.Critical)
        return False

    def fillProbRuoloColumns(self,mem_layer,l):
      #Dato il layer e la lista contenente idBene, prob, ruolo e probRuolo,
      #riempie le colonne corrispondenti,
      #seleziona le features necessarie, setta lo stile e nasconde il layer dei beni
      idList=[]
      mem_layer.startEditing()
      for feat in mem_layer.getFeatures(): 
          for i in l:
              if str(feat['id'])==i[0]:
                  feat['prob'] = i[1] 
                  feat['ruolo'] = i[2] 
                  feat['probRuolo'] = i[3] 
                  mem_layer.updateFeature(feat)
                  idList.append(i[0])
      mem_layer.commitChanges()    
      for layer in QgsProject.instance().mapLayers().values():
        if layer != mem_layer and layer.type() != QgsMapLayer.RasterLayer and layer != Utils().getLayerFiumi() and layer != Utils().getLayerComuni():
          QgsProject.instance().layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(False)

    def exportAttributes(self, layer, filename, selected):
      #Dati un layer, un file name e un booleano che indica il tipo di attributi da salvare;
      #scrive su file i valori contenuti in layer.selectedFeatures() o layer.getFeatures();
      #stampa il messaggio necessario
      if selected:
          features = layer.selectedFeatures()
      else:
          features = layer.getFeatures()
      if selected == True and not Utils().getResult():
        iface.messageBar().pushMessage('Attenzione', 'Non ci sono attributi selezionati', level=Qgis.Critical)
      else: 
        if selected != "" and filename != "":
          fieldsNames = self.getFieldsName(layer)
          s1= ', '.join(fieldsNames) + ';\n'
          s2= ';\n'.join([','.join(map(str, feat)) for feat in features])
          s3 = s1 + s2
          output_file = open(filename, 'w')
          output_file.write(s3)
          output_file.close()
          iface.messageBar().pushMessage('Successo', 'Gli attributi sono stati salvati in ' + filename, level=Qgis.Success)
        else:
          iface.messageBar().pushMessage('Attenzione', 'Ricompilare il form con i campi corretti', level=Qgis.Critical)

    def getDettagliBene(self,beneId):
      #Crea la stringa con i dettagli del bene
      layer = Utils().getLayerBeni()
      QueryLayer().selectionById(beneId)
      featureAttributes = layer.selectedFeatures()[0].attributes()
      return featureAttributes

    def getFunzioniBene(self,beneId):
      #Crea la stringa con le funzioni in cui il bene è citato
      expr = "id_bene ='"+str(beneId)+"' or id_bener='"+str(beneId)+"'"
      selection = QueryLayer().selectionByExpr(Utils().getLayerRelazioni(),expr)
      l=[]
      for feat in selection:
        l.append(feat.attributes())
      return l

    def setOverlay(self,dataA,dataB):
      #Dato il layer attivo, setta gli attributi corrispondenti ricavati da overlayTemporale()
      layer = iface.activeLayer()
      layer.startEditing()
      for feat in layer.getFeatures():
        feat['overlay']=Utils().overlayTemporale(feat['data'],dataA,dataB)
        #print(str(feat["id_bene"])+": "+ feat['overlay'] + str(feat["data"]))
        layer.updateFeature(feat)
      layer.commitChanges()

    def getDependenciesList(self,beneId,b1,b2):
      #Di un dato bene, restituisce la lista degli id di tutti i beni dipendenti in un dato periodo
      layerFunz = Utils().getLayerRelazioni()
      idsList=[]   
      for feat in layerFunz.getFeatures():
        idBeneR = str(feat["id_bener"])
        if idBeneR == beneId:
          overlay=Utils().overlayTemporale(str(feat["data_ante"]),b1,b2)
          if overlay == "dentro" or overlay =="parziale":
            idsList.append(str(feat["id_bene"]))
      idsList.append(beneId)
      return idsList

from .utils import Utils
from .PRR20BK22 import PRRBB20