import os
import sys
import inspect
from math import sqrt
from PyQt5.QtGui import QIcon,QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QWidget, QVBoxLayout, QLineEdit, QCompleter, QListWidgetItem, QTableWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QStringListModel, Qt,QPoint, QVariant
from PyQt5 import QtCore
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

class DlgTools():  
   
    def setDialogGeometry(self, dialogWidth, dialogHeight, position, dlg):
      #Setta la finestra del plugin sempre on top;
      #prende altezza e larghezza di un dialog;
      #prende la posizione desiderata del dialog come stringa (bottomLeft, topLeft, bottomRight, topRight)
      #setta le geometria del dialog secondo i parametri dati
      #dlg.setWindowFlags(Qt.WindowStaysOnTopHint)
      dlg.setWindowFlags(
        QtCore.Qt.WindowContextHelpButtonHint |
        QtCore.Qt.WindowCloseButtonHint |
        QtCore.Qt.WindowStaysOnTopHint
      )
      mapCanvas = iface.mapCanvas()
      canvasSize = mapCanvas.size()
      canvasOrigin = mapCanvas.mapToGlobal(QPoint(0,0))
      canvasHeight = mapCanvas.mapToGlobal(QPoint(0,int(canvasSize.height())))
      canvasWidth = mapCanvas.mapToGlobal(QPoint(int(canvasSize.width()),0))
      if position == 'bottomLeft':
        dlg.setGeometry(canvasHeight.x(), canvasHeight.y()-dialogHeight,dialogWidth,dialogHeight)
      elif position == 'topLeft':
        dlg.setGeometry(canvasOrigin.x(), canvasOrigin.y(),dialogWidth,dialogHeight)
      elif position == 'bottomRight':
        dlg.setGeometry(canvasWidth.x()-dialogWidth, canvasHeight.y()-dialogHeight, dialogWidth,dialogHeight)
      elif position == 'topRight':
        dlg.setGeometry(canvasWidth.x()-dialogWidth, canvasOrigin.y(), dialogWidth,dialogHeight)
      else:
        print("La posizione non può essere definita diversamente da (bottomLeft, topLeft, bottomRight, topRight)")

    def completerLine(self,lineEdit,layer,field):
      #Data la lista degli identificatori permette l'autocompletamento dell'input utente
      strList = QueryLayer().getFeaturesList(field,layer) 
      completer = QCompleter()
      completer.setFilterMode(Qt.MatchContains)
      completer.setCaseSensitivity(0)
      lineEdit.setCompleter(completer) 
      model = QStringListModel()
      model.setStringList(strList)
      completer.setModel(model)

    def fillComboBox(self,dlg):
      #Controlla che le comboBox esistano nell'interfaccia e le riempie con i valori necessari
      layerBeni=Utils().getLayerBeni()
      ComunList = QueryLayer().getFeaturesList("comun",layerBeni)
      EpocaList = QueryLayer().getFeaturesList("meo",layerBeni)
      EpocaCarList = QueryLayer().getFeaturesList("mec",layerBeni)
      StatoList = QueryLayer().getFeaturesList("esist",layerBeni)
      StatoList.insert(0, StatoList.pop(1)) #Muove esist "SI" al primo posto nella lista
      try:
        dlg.comboBoxComune.clear()
        dlg.comboBoxComune.addItems(ComunList)
        dlg.comboBoxStato.clear()
        dlg.comboBoxStato.addItems(StatoList)
        dlg.comboBoxEpoca.clear()
        dlg.comboBoxEpoca.addItems(EpocaList)
        dlg.comboBoxEpocaCar.clear()
        dlg.comboBoxEpocaCar.addItems(EpocaCarList)
      except:
        pass
        
    def getSelezionaBeniQGisExpression(self,dlg):
      #Prende gli input utente;
      #costruisce l'espressione QGIS necessaria concatenando chiavi e valori di un dizionario;
      #le chiavi rappresentano Comune, Macroepoca e esistenza;
      #i valori rappresentano i valori scelti dall'utente in base a quella chiave;
      #se l'utente analizza anche i beni contenuti in un certo raggio a partire da un certo bene l'espressione viene concatenata all'espressione ottenuta per mezzo della funzione getBeniInRaggio()
      #idem per i beni distanti da un dato fiume
      #permette di selezionare le colonne da visualizzare nella tabella degli attributi
      dictionary = {}
      if dlg.checkBoxComune.isChecked():
        dictionary['comun']=dlg.comboBoxComune.currentText() 
      if dlg.checkBoxEpoca.isChecked():
        dictionary['meo']=dlg.comboBoxEpoca.currentText()
      if dlg.checkBoxEpocaCar.isChecked():
        dictionary['mec']=dlg.comboBoxEpocaCar.currentText() 
      if dlg.checkBoxStato.isChecked():
        dictionary['esist']=dlg.comboBoxStato.currentText() 
      expr=""
      for x in dictionary:
        expr += x + "=" + "\'"+dictionary[x]+"\'"+" and "
      if dlg.checkBoxRaggio.isChecked(): 
        beneId=QueryLayer().getBeneId(dlg.lineEdit.text(),False)
        if beneId:
          userDistanceKm = dlg.doubleSpinBox.value()
          userDistanceM = userDistanceKm * 1000
          expr += GeomTools().getBeniInRaggio(beneId,userDistanceM) + " and "
      if dlg.checkBoxFiume.isChecked():
        fiumeIdent=dlg.lineEdit_2.text()
        if fiumeIdent in QueryLayer().getFeaturesList("name",Utils().getLayerFiumi()):
          userDistanceKm = dlg.doubleSpinBox_2.value()
          expr += GeomTools().getOneRiverDistance(fiumeIdent,userDistanceKm) + " and "
      expr = expr[:-4] #elimina un "and" finale non necessario
      layer=Utils().getLayerBeni()
      QueryLayer().selectionByExpr(layer,expr)
      Utils().getMessage(layer)
    
    def getEsistComun(self,dlg):
      #Restituisce l'espressione per seleziona lo stato o il comune necessario
      d = {}
      if dlg.checkBoxStato.isChecked():
        d["esist"]=dlg.comboBoxStato.currentText()
      if dlg.checkBoxComune.isChecked():
        d["comun"]=dlg.comboBoxComune.currentText()
      expr=""
      for x in d:
        expr += x + "=" + "\'"+d[x]+"\'"+" and "
      expr = expr[:-4]
      return expr

    def visualizzaBeneRelazioniCheckRadio(self, dlg):
      #In base al radio button selezionato restituisce la query necessaria o chiama la funzione necessaria
      beneId=QueryLayer().getBeneId(dlg.lineEdit.text(),False)
      layerBeni=Utils().getLayerBeni()
      if beneId:  
        if dlg.radioButtonRelazioniAll.isChecked():
          #I beni da cui dipende
          query="SELECT funzionigeo.id_bener FROM funzionigeo WHERE funzionigeo.id_bene ='"+beneId+"'"
          if len(QueryLayer().selectionByQuery(layerBeni,query))>0:
            GeomTools().getGeomEnd(query,beneId,True)
            return 'relazioni',beneId
          else:
            return False, False
        elif dlg.radioButtonRelazioniAll_2.isChecked():
          #I beni che dipendono 
          query="SELECT funzionigeo.id_bene FROM funzionigeo WHERE funzionigeo.id_bener ='"+beneId+"'"
          if len(QueryLayer().selectionByQuery(layerBeni,query))>0:
            GeomTools().getGeomEnd(query,beneId,False)
            return 'relazioni',beneId
          else:
            return False,False
        elif dlg.radioButtonFunzioni.isChecked():
          return 'funzioni',beneId
        else:
          return False, False
      else:
        return False, False
        
    def visualizzaBeneCheckRadio(self, dlg):
      #In base al radio button selezionato restituisce la query necessaria o chiama la funzione necessaria
      beneId=QueryLayer().getBeneId(dlg.lineEdit.text(),False)
      if beneId:
        Utils().zoomToSelectedFeature(Utils().getLayerBeni())
        if dlg.radioButtonProb.isChecked():
          return 'PRR',beneId
        elif dlg.radioButtonDettagli.isChecked():
          return 'bene',beneId
        elif dlg.radioButtonBeniVicini.isChecked():
          return 'beniVicini',beneId
        else:
          return False,False 
      else:
        return False,False

    def setTableWidgetOutput(self,dlg,tipoQuery,beneId):
      #Dato il dialog, riempie la tabella con i valori necessari;
      #può trattarsi dei dettagli di un bene, delle funzioni ad esso associate, o dei beni più vicini ad un dato bene
      #usa delle liste pescate da getDettagliBene(), getFunzioniBene(), o getNearestBeniFromID()
      if tipoQuery=='bene':
        DlgTools().setDialogGeometry(600,650,'topLeft',dlg)
        l=QueryLayer().getDettagliBene(beneId)
        fieldsNames = QueryLayer().getFieldsName(Utils().getLayerBeni())
        dlg.tableWidget.setRowCount(len(fieldsNames))
        dlg.tableWidget.setColumnCount(1)
        dlg.tableWidget.setHorizontalHeaderLabels([l[1]])
        dlg.tableWidget.setVerticalHeaderLabels(fieldsNames)
        for i in range(len(fieldsNames)):
          item=str(l[i])
          dlg.tableWidget.setItem(i,0, QTableWidgetItem(item))
      if tipoQuery=='funzioni':
        DlgTools().setDialogGeometry(1415,450,'topLeft',dlg)
        l=QueryLayer().getFunzioniBene(beneId)
        fieldsNames=QueryLayer().getFieldsName(Utils().getLayerRelazioni())
        fieldsNames = [n.replace('DATA_POSTE', 'DATA_POST') for n in fieldsNames]
        dlg.tableWidget.setRowCount(len(l))
        dlg.tableWidget.setColumnCount(len(fieldsNames))
        dlg.tableWidget.setHorizontalHeaderLabels(fieldsNames)
        index=0
        for sublist in l:
          for j in range(len(sublist)):
            item=str(sublist[j])
            dlg.tableWidget.setItem(index, j, QTableWidgetItem(item))
          index =index+1
      if tipoQuery=='beniVicini':
          DlgTools().setDialogGeometry(400,500,'topLeft',dlg)
          beniViciniList = GeomTools().getNearestBeniFromID(10,beneId)
          dlg.tableWidget.setColumnCount(2)
          dlg.tableWidget.setRowCount(len(beniViciniList))
          dlg.tableWidget.setHorizontalHeaderLabels(['Distanza in km','id_bene','probPres','ruolo','ruolo2'])
          index=0
          for sublist in beniViciniList:
            for j in range(len(sublist)):
              item=str(sublist[j])
              dlg.tableWidget.setItem(index, j, QTableWidgetItem(item))
            index =index+1
    '''      
    def setProbSoglia(self,dlg):
      #Gestisce lo slider che indica la soglia di visualizzazione in base alla probabilità
      soglia=dlg.horizontalSlider.value()
      if soglia > 70:
        expr = 'prob > 70'
      if soglia <= 70 and soglia > 40:
        expr = 'prob < 70 and prob > 40'
      if soglia <= 40 and soglia > 10:
        expr = 'prob < 40 and prob > 10'
      if soglia <= 10:
        expr = 'prob > 10'
      iface.activeLayer().setSubsetString(expr)
    '''
    def setProbSoglia(self,dlg):
      #Gestisce lo slider che indica la soglia di visualizzazione in base alla probabilità
      soglia=dlg.horizontalSlider.value()
      expr = 'prob > '+str(soglia)
      iface.activeLayer().setSubsetString(expr)

    def setRelSoglia(self,dlg):
      #Gestisce lo slider che indica la soglia di visualizzazione in base all'overlay temporale delle relazioni
      soglia = dlg.horizontalSlider.value()
      if soglia >= 65:
        expr = "overlay = 'dentro'"
      if soglia < 65 and soglia >= 45:
        expr = "overlay = 'parziale'"
      if soglia < 45 and soglia >= 10:
        expr = "overlay = 'fuori'"
      if soglia < 10:
        expr = "overlay = 'dentro' or overlay = 'parziale' or overlay = 'fuori'"
      iface.activeLayer().setSubsetString(expr)

    def takeDifference(self,dlg):
      #Se la checkBox Aggangia Date è attivo, prende la differenza tra le due date;
      #Se il primo slider si muove passa la differenza a self.adjustSlider() e disattiva il secondo slider
      #Se la checkbox è disattivata riattiva il secondo slider
      if dlg.pushButtonAggancia.isChecked():
        firstDate = dlg.horizontalSliderA.value()
        secondDate = dlg.horizontalSliderB.value()
        difference = abs(secondDate-firstDate)
        dlg.horizontalSliderA.valueChanged.connect(lambda: self.adjustSlider(dlg, difference))
        dlg.horizontalSliderB.setEnabled(False)
        dlg.spinBox_2.setEnabled(False)
      else:
        dlg.horizontalSliderB.setEnabled(True)
        dlg.spinBox_2.setEnabled(True)

    def adjustSlider(self,dlg,timeRange):
      #Data la differenza tra i valori dei due slider, setta il valore del secondo slider ancorandolo al primo
      if dlg.pushButtonAggancia.isChecked() and dlg.pushButtonAggancia.isEnabled():
        firstDate = dlg.horizontalSliderA.value()
        dlg.horizontalSliderB.setValue(firstDate+timeRange)
    
    def setTimeSlidBtnTxt(self,dlg):
      #Setta il testo del bottone sulla slider
      if dlg.pushButtonPeriodoAnno.isChecked():
        dlg.pushButtonPeriodoAnno.setText("Periodo")
      else:
        dlg.pushButtonPeriodoAnno.setText("Anno")

    def getDate(self, dlg):
      #Restituisce le date selezionate dagli slider
      dataA = dlg.horizontalSliderA.value()
      dataB = dlg.horizontalSliderB.value()
      if not dlg.pushButtonPeriodoAnno.isChecked():
        dataB = ""
      else:
        if dataB<dataA:
          return False
      return dataA, dataB

    def setPRROutput(self, dlg, beneId):
      #Dato il dialog e l'id del bene;
      #ricava le date dalla posizione degli slider;
      #chiama PRR e setta l'output nella tabella del dialog
      if self.getDate(dlg):
        dataA, dataB = self.getDate(dlg)
        output = QueryLayer().callPRR(dataA,dataB,beneId)
        if output:
          index=0
          for sublist in output:
            for j in range(len(sublist)):
              item=(sublist[j])
              if item == "i":
                item = "ignoto"
              dlg.tableWidget.setItem(index, j, QTableWidgetItem(item))
            index =index+1
    
    def switchHeatmap(self,layer,dlg):
      #Consente di switchare tra la visualizzazione con heatmap o quella con icone
      if dlg.pushButtonHeat.isChecked():
        Utils().setStyle("heatmap",layer)
      else:
        Utils().setStyle("All_PRR_icons",layer)
      
    def PRRAll(self, dlg, mem_layer):
      #Dato il dialog, la lista dei beni e delle funzioni e un layer copia del layer del beni;
      #ricava le date dalla posizione degli slider;
      #chiama callPRRAllBeni
      if self.getDate(dlg):
        dataA, dataB = self.getDate(dlg)
        DlgTools().switchHeatmap(mem_layer,dlg)
        QgsProject.instance().layerTreeRoot().findLayer(mem_layer.id()).setItemVisibilityChecked(True)
        QueryLayer().callPRRAllBeni(dataA,dataB,mem_layer)

    def PRRRuoli(self,dlg,ruoli,mem_layer,rejected):
      #Dato l'elenco dei ruoli selezionati, la lista dei beni e delle funzioni e il layer copia del layer dei beni;
      #chiama callPRRRuoli();
      #se la funzione viene chiamata quando il dialog viene chiuso, rejected prende True;
      #se rejected è True controlla che callPRRRuoli abbia restituito un risultato, in caso contrario cancella il layer copia.
      if self.getDate(dlg):
        dataA, dataB = self.getDate(dlg)
        DlgTools().switchHeatmap(mem_layer,dlg)
        QgsProject.instance().layerTreeRoot().findLayer(mem_layer.id()).setItemVisibilityChecked(True)
        QueryLayer().callPRRRuoli(ruoli,dataA,dataB,mem_layer)
        if rejected:
          if QueryLayer().callPRRRuoli(ruoli,dataA,dataB,mem_layer) == False:
            QgsProject.instance().removeMapLayers( [mem_layer.id()] )

    def getSelectedItems(self,dlg):
      #Converte gli items selezionati nel listWidget in una lista di stringhe
      items = []
      for i in dlg.listWidget.selectedItems():
        items.append(i.text())
      return items
    
    def fillListWidget(self,dlg,itemsList):
      #Riempie il listWidget con i valori necessari
      #layerRelazioni = Utils().getLayerRelazioniRuoli()
      #itemsList = QueryLayer().getFeaturesList("ruolo",layerRelazioni)
      listWidget = dlg.listWidget
      for i in itemsList:
        item = QListWidgetItem(i)
        listWidget.addItem(item)

    def select_output_file(self,dlg):
      #Seleziona il file in ouput
      filename, _filter = QFileDialog.getSaveFileName(
          dlg, "Seleziona output file ","", '*.csv')
      dlg.lineEdit.setText(filename)

    def fillComboBoxExport(self,dlg):
      #Riempie la comboBox con i nomi dei layer vettoriali
      dlg.comboBox.clear()
      dlg.comboBox.addItems(Utils().getVectorLayersNameList())

    def exportdlg(self,dlg):
      #Passa a QueryLayer().exportAttributes() un layer, un file name e un booleano che indica il tipo di attributi da salvare
      layer = QgsProject.instance().mapLayersByName(dlg.comboBox.currentText())[0]
      filename = dlg.lineEdit.text()
      selected=""
      if dlg.radioButtonAll.isChecked():
        selected=False
      if dlg.radioButtonSelected.isChecked():
        selected=True
      QueryLayer().exportAttributes(layer, filename, selected)

    def distanzaBeniDlg(self,dlg):
      #Dato il dialog prende gli id dei due beni, calcola la distanza e setta l'output
      #Disattiva le features selezionate per permettere le analisi successive.
      id1,id2= QueryLayer().getBeneId(dlg.lineEdit.text(),dlg.lineEdit_2.text())
      if id1 and id2:
        measure = GeomTools().getDistancesFromID(id1, id2)
        dlg.label_4.setText(measure)
        #Utils().removeSelectedFeatures()
      else:
        iface.messageBar().pushMessage('Attenzione', 'Non esistono beni con queste caratteristiche o è presente un errore nella selezione', level=Qgis.Critical)

    def distanzaFiumiDlg(self, dlg):
      #Dato il dialog calcola la distanza dal bene a tutti i fiumi e setta l'output
      #Disattiva le features selezionate per permettere le analisi successive.
      beneId=QueryLayer().getBeneId(dlg.lineEdit_3.text(),False)
      if beneId:
        measure = GeomTools().getRiversDistances(beneId)
        dlg.label_8.setText(measure)
        #Utils().removeSelectedFeatures()
      else:
        iface.messageBar().pushMessage('Attenzione', 'Non esistono beni con queste caratteristiche o è presente un errore nella selezione', level=Qgis.Critical)

    def setOverlayDates(self,dlg):
      #Prende la date dal dialog e le passa a setOverlay()
      if self.getDate(dlg):
        dataA, dataB = self.getDate(dlg)
        QueryLayer().setOverlay(dataA,dataB)

from .queryLayer import QueryLayer
from .utils import Utils
from .geomTools import GeomTools