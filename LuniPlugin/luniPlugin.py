import os
import sys
import inspect
from pathlib import Path
from PyQt5.QtCore import pyqtSlot, QStringListModel
from PyQt5.QtGui import QIcon,QStandardItemModel, QStandardItem, QColor
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QWidget, QVBoxLayout, QLineEdit, QCompleter, QDialog
from qgis.utils import iface
from qgis.gui import QgsRubberBand
import qgis.core
from qgis.core import (
   edit,
   Qgis,
   QgsMapLayer,
   QgsExpression,
   QgsExpressionContext,
   QgsFeature,
   QgsFeatureRequest,
   QgsField,
   QgsFields,
   QgsVectorLayer,
   QgsPointXY,
   QgsGeometry,
   QgsProject,
   QgsExpressionContextUtils,
   QgsSettings
)
from .dialogs.select_feature_dialog import SelectFeatureDialog
from .dialogs.visualizza_bene_dialog import VisualizzaBeneDialog
from .dialogs.visualizza_bene_relazioni_dialog import VisualizzaBeneRelazioniDialog
from .dialogs.cambia_data_dialog import CambiaDataDialog
from .dialogs.select_by_date_dialog import SelectByDateDialog
from .dialogs.calcola_distanza_dialog import CalcolaDistanzaDialog
from .dialogs.ruoli_dialog import RuoliDialog
from .dialogs.esporta_dialog import EsportaDialog
from .dialogs.area_dialog import AreaDialog
from .dialogs.table_dialog import TableDialog
from .dialogs.guida_dialog import GuidaDialog
from .dialogs.altitudine_dialog import AltitudineDialog
from .core.dlgTools import DlgTools
from .core.utils import Utils
from .core.queryLayer import QueryLayer
from .core.geomTools import GeomTools

iconsFolder=str(Path(__file__).parents[1])+'//LuniPlugin//styles//icons//toolbar//'
iconSeleziona = QIcon(iconsFolder + 'marker.svg')
iconVisualizzaBene = QIcon(iconsFolder + 'vision.svg')
iconPeriodo = QIcon(iconsFolder + 'hourglass_2.svg')
iconDistanze = QIcon(iconsFolder + 'scale.svg')
iconRuolo = QIcon(iconsFolder + 'church.svg')
iconEsporta = QIcon(iconsFolder + 'export.svg')
iconRipristina = QIcon(iconsFolder + 'refresh.svg')
iconArea = QIcon(iconsFolder + 'area.svg')
iconRelazioni = QIcon(iconsFolder + 'relations.svg')
iconGuida = QIcon(iconsFolder + 'guida.svg')
iconInfo = QIcon(iconsFolder + 'info.svg')
iconAltitude = QIcon(iconsFolder + 'altitude.svg')

class LuniPlugin:
    def __init__(self, iface):
      self.iface = iface
      Utils().setSvgIconsPath() #All'avvio di QGIS setta il path per caricare le icone
      iface.actionMapTips().setChecked(True)
      QgsSettings().setValue('qgis/mapTipsDelay', 250)
      #self.dialogsList = []

    def initGui(self):
      self.action = QAction(iconSeleziona, 'Seleziona beni per geolocalizzazione', self.iface.mainWindow())
      self.action2 = QAction(iconVisualizzaBene, 'Analisi bene', self.iface.mainWindow())
      self.action3 = QAction(iconPeriodo, 'Visualizza periodo storico', self.iface.mainWindow())
      self.action4 = QAction(iconDistanze, 'Calcola distanze', self.iface.mainWindow())
      self.action5 = QAction(iconRuolo, 'Selezione per ruoli', self.iface.mainWindow())
      self.action6 = QAction(iconEsporta, 'Esporta', self.iface.mainWindow())
      self.action7 = QAction(iconRipristina, 'Ripristina stato iniziale', self.iface.mainWindow())
      self.action8 = QAction(iconArea, 'Visualizza area', self.iface.mainWindow())
      self.action9 = QAction(iconRelazioni, 'Analisi relazioni tra beni', self.iface.mainWindow())
      self.action10 = QAction(iconGuida,'Guida utente',self.iface.mainWindow())
      self.action11 = QAction(iconAltitude, 'Selezione per altitudine',self.iface.mainWindow())
      self.action.triggered.connect(self.runSelezionaBeni)
      self.action2.triggered.connect(self.runVisualizzaBene)
      self.action3.triggered.connect(self.runSelezionaPerData)
      self.action4.triggered.connect(self.runCalcolaDistanza)
      self.action5.triggered.connect(self.runSelezionaRuoli)
      self.action6.triggered.connect(self.runEsporta)
      self.action7.triggered.connect(self.runRipristino)
      self.action8.triggered.connect(self.runArea)
      self.action9.triggered.connect(self.runVisualizzaBeneRelazioni)
      self.action10.triggered.connect(self.runGuida)
      self.action11.triggered.connect(self.runAltitudine)
      self.iface.addPluginToMenu('&Lunigiana', self.action7)
      self.iface.addPluginToMenu('&Lunigiana', self.action6)
      self.iface.addPluginToMenu('&Lunigiana', self.action)
      self.iface.addPluginToMenu('&Lunigiana', self.action9)
      self.iface.addPluginToMenu('&Lunigiana', self.action2)
      self.iface.addPluginToMenu('&Lunigiana', self.action5)
      self.iface.addPluginToMenu('&Lunigiana', self.action3)
      self.iface.addPluginToMenu('&Lunigiana', self.action4)
      self.iface.addPluginToMenu('&Lunigiana', self.action8)
      self.iface.addPluginToMenu('&Lunigiana', self.action10)
      self.iface.addPluginToMenu('&Lunigiana', self.action11)
      self.iface.addToolBarIcon(self.action7)
      self.iface.addToolBarIcon(self.action6)
      self.iface.addToolBarIcon(self.action)
      self.iface.addToolBarIcon(self.action9)
      self.iface.addToolBarIcon(self.action2)
      self.iface.addToolBarIcon(self.action5)
      self.iface.addToolBarIcon(self.action3)
      self.iface.addToolBarIcon(self.action4)  
      self.iface.addToolBarIcon(self.action11) 
      self.iface.addToolBarIcon(self.action8)
      self.iface.addToolBarIcon(self.action10)
      self.first_start = True
      
    def unload(self):
      self.iface.removeToolBarIcon(self.action)
      self.iface.removeToolBarIcon(self.action2)
      self.iface.removeToolBarIcon(self.action3)
      self.iface.removeToolBarIcon(self.action4)
      self.iface.removeToolBarIcon(self.action5)
      self.iface.removeToolBarIcon(self.action6)
      self.iface.removeToolBarIcon(self.action7)
      self.iface.removeToolBarIcon(self.action8)
      self.iface.removeToolBarIcon(self.action9)
      self.iface.removeToolBarIcon(self.action10)
      self.iface.removeToolBarIcon(self.action11)
      self.iface.removePluginMenu('&Lunigiana', self.action) 
      self.iface.removePluginMenu('&Lunigiana', self.action2) 
      self.iface.removePluginMenu('&Lunigiana', self.action3) 
      self.iface.removePluginMenu('&Lunigiana', self.action4)
      self.iface.removePluginMenu('&Lunigiana', self.action5)
      self.iface.removePluginMenu('&Lunigiana', self.action6)
      self.iface.removePluginMenu('&Lunigiana', self.action7)
      self.iface.removePluginMenu('&Lunigiana', self.action8)
      self.iface.removePluginMenu('&Lunigiana', self.action9)
      self.iface.removePluginMenu('&Lunigiana', self.action10)
      self.iface.removePluginMenu('&Lunigiana', self.action11)
      del self.action
      del self.action2
      del self.action3
      del self.action4
      del self.action5
      del self.action6
      del self.action7
      del self.action8
      del self.action9
      del self.action10
      del self.action11
	
    def runSelezionaBeni(self):  
      #Utils().restoreLayerBeni()
      self.dlg = SelectFeatureDialog()   
      self.dlg.setWindowIcon(iconSeleziona)    
      DlgTools().fillComboBox(self.dlg)
      DlgTools().completerLine(self.dlg.lineEdit,Utils().getLayerBeni(),"ident")  
      DlgTools().completerLine(self.dlg.lineEdit_2,Utils().getLayerFiumi(),"name")
      DlgTools().setDialogGeometry(400,380,'topLeft',self.dlg)       
      self.dlg.show()
      #self.dialogsList.append(self.dlg) #ESPERIMENTO
      result = self.dlg.exec_()
      if result:
        DlgTools().getSelezionaBeniQGisExpression(self.dlg)
    
    def runCalcolaDistanza(self):
      #Utils().restoreLayerBeni()
      Utils().getLayerBeni().removeSelection()
      self.dlg6 = CalcolaDistanzaDialog()
      self.dlg6.setWindowIcon(iconDistanze)
      DlgTools().setDialogGeometry(570,360,'topLeft',self.dlg6)
      DlgTools().completerLine(self.dlg6.lineEdit,Utils().getLayerBeni(),"ident")
      DlgTools().completerLine(self.dlg6.lineEdit_2,Utils().getLayerBeni(),"ident")
      DlgTools().completerLine(self.dlg6.lineEdit_3,Utils().getLayerBeni(),"ident")
      self.dlg6.pushButton.clicked.connect(lambda:DlgTools().distanzaBeniDlg(self.dlg6))
      self.dlg6.pushButton_2.clicked.connect(lambda:DlgTools().distanzaFiumiDlg(self.dlg6))
      self.dlg6.show()
      #self.dialogsList.append(self.dlg6) #ESPERIMENTO
    
    def runOutput(self,tipoQuery,beneId):
      self.dlg11 = TableDialog()
      DlgTools().setTableWidgetOutput(self.dlg11,tipoQuery,beneId)
      self.dlg11.show()
      #self.dialogsList.append(self.dlg11) #ESPERIMENTO
    
    def runVisualizzaBene(self):    
      QueryLayer().createPRRTable() #DA DECIDERE DOVE PIAZZARLO
      Utils().restoreLayerBeni()
      self.dlg2 = VisualizzaBeneDialog()
      self.dlg2.setWindowIcon(iconVisualizzaBene)
      DlgTools().completerLine(self.dlg2.lineEdit,Utils().getLayerBeni(),"ident")
      DlgTools().setDialogGeometry(440,230,'topLeft',self.dlg2)
      self.dlg2.show()
      #self.dialogsList.append(self.dlg2) #ESPERIMENTO
      result = self.dlg2.exec_()
      if result:
        tipoQuery,beneId=DlgTools().visualizzaBeneCheckRadio(self.dlg2)  
        if tipoQuery == 'PRR':
          self.runTimeSlider(beneId)
        if tipoQuery == 'bene':
          self.runOutput(tipoQuery,beneId)
        if tipoQuery == 'beniVicini':
          self.runSelezionaPerData()
          self.runOutput(tipoQuery,beneId)
        if tipoQuery == False:
          iface.messageBar().pushMessage('Attenzione', 'Non esistono beni con queste caratteristiche o è presente un errore nella selezione', level=Qgis.Critical)
        
    def runTimeSlider(self,beneId):
      self.dlg3 = CambiaDataDialog()          
      self.dlg3.setWindowIcon(iconPeriodo)
      DlgTools().setDialogGeometry(830,150,'bottomLeft',self.dlg3)
      self.dlg3.pushButtonPeriodoAnno.clicked.connect(lambda: DlgTools().setTimeSlidBtnTxt(self.dlg3))
      self.dlg3.pushButtonAggancia.clicked.connect(lambda: DlgTools().takeDifference(self.dlg3))
      self.dlg3.horizontalSliderA.setTracking(False)
      self.dlg3.horizontalSliderB.setTracking(False)     
      self.dlg3.horizontalSliderA.valueChanged.connect(lambda:DlgTools().setPRROutput(self.dlg3,beneId))
      self.dlg3.horizontalSliderB.valueChanged.connect(lambda:DlgTools().setPRROutput(self.dlg3,beneId))
      self.dlg3.show() 

    def runVisualizzaBeneRelazioni(self):    
      #Utils().restoreLayerBeni()
      Utils().getLayerBeni().removeSelection()
      self.dlg10 = VisualizzaBeneRelazioniDialog()
      self.dlg10.setWindowIcon(iconRelazioni)
      DlgTools().completerLine(self.dlg10.lineEdit,Utils().getLayerBeni(),"ident")
      DlgTools().setDialogGeometry(440,230,'topLeft',self.dlg10)
      self.dlg10.show()
      #self.dialogsList.append(self.dlg10) #ESPERIMENTO
      result = self.dlg10.exec_()
      if result:
        tipoQuery,beneId=DlgTools().visualizzaBeneRelazioniCheckRadio(self.dlg10)
        if tipoQuery == 'funzioni':
          self.runOutput(tipoQuery,beneId)
        if tipoQuery == 'relazioni':
          self.runTimeSliderRelazioni()
        if tipoQuery == False:
          iface.messageBar().pushMessage('Attenzione', 'Non esistono relazioni con queste caratteristiche o è presente un errore nella selezione', level=Qgis.Critical)
    
    def runTimeSliderRelazioni(self):
      self.dlg4 = SelectByDateDialog() 
      DlgTools().setDialogGeometry(905,125,'bottomLeft',self.dlg4)
      self.dlg4.setWindowIcon(iconPeriodo)     
      self.dlg4.pushButtonPeriodoAnno.clicked.connect(lambda: DlgTools().setTimeSlidBtnTxt(self.dlg4))
      self.dlg4.pushButtonAggancia.clicked.connect(lambda: DlgTools().takeDifference(self.dlg4))
      self.dlg4.horizontalSliderA.setTracking(False)
      self.dlg4.horizontalSliderB.setTracking(False)     
      self.dlg4.horizontalSliderA.valueChanged.connect(lambda:DlgTools().setOverlayDates(self.dlg4))
      self.dlg4.horizontalSliderB.valueChanged.connect(lambda:DlgTools().setOverlayDates(self.dlg4))
      self.dlg4.horizontalSlider.valueChanged.connect(lambda:DlgTools().setRelSoglia(self.dlg4))
      self.dlg4.pushButtonHeat.hide()
      self.dlg4.show() 
      #self.dialogsList.append(self.dlg4) #ESPERIMENTO

    def runSelezionaPerData(self): 
      self.dlg4 = SelectByDateDialog() 
      DlgTools().setDialogGeometry(920,130,'bottomLeft',self.dlg4)
      self.dlg4.setWindowIcon(iconPeriodo)   
      self.dlg4.pushButtonPeriodoAnno.clicked.connect(lambda: DlgTools().setTimeSlidBtnTxt(self.dlg4))
      self.dlg4.pushButtonAggancia.clicked.connect(lambda: DlgTools().takeDifference(self.dlg4))
      self.dlg4.pushButtonHeat.clicked.connect(lambda: DlgTools().switchHeatmap(mem_layer,self.dlg4))
      self.dlg4.horizontalSliderA.setTracking(False)
      self.dlg4.horizontalSliderB.setTracking(False)  
      QueryLayer().createPRRTable() #DA DECIDERE DOVE PIAZZARLO
      Utils().restoreLayerBeni()   
      mem_layer = GeomTools().createCentroidsLayer(Utils().getLayerBeni(),False,"benigeoPeriodo")
      self.dlg4.horizontalSliderA.valueChanged.connect(lambda:DlgTools().PRRAll(self.dlg4,mem_layer))
      self.dlg4.horizontalSliderB.valueChanged.connect(lambda:DlgTools().PRRAll(self.dlg4,mem_layer))
      self.dlg4.horizontalSlider.valueChanged.connect(lambda:DlgTools().setProbSoglia(self.dlg4))
      self.dlg4.show() 
      #self.dialogsList.append(self.dlg4) #ESPERIMENTO

    def runTimeSliderRuolo(self,ruoli,esistComun):
      self.dlg4 = SelectByDateDialog() 
      DlgTools().setDialogGeometry(905,125,'bottomLeft',self.dlg4)
      self.dlg4.setWindowIcon(iconPeriodo)    
      self.dlg4.pushButtonPeriodoAnno.clicked.connect(lambda: DlgTools().setTimeSlidBtnTxt(self.dlg4))
      self.dlg4.pushButtonAggancia.clicked.connect(lambda: DlgTools().takeDifference(self.dlg4))
      self.dlg4.pushButtonHeat.clicked.connect(lambda: DlgTools().switchHeatmap(mem_layer,self.dlg4))
      self.dlg4.horizontalSliderA.setTracking(False)
      self.dlg4.horizontalSliderB.setTracking(False) 
      mem_layer = GeomTools().createCentroidsLayer(Utils().getLayerBeni(),esistComun,"benigeoRuoli")  
      self.dlg4.horizontalSliderA.valueChanged.connect(lambda:DlgTools().PRRRuoli(self.dlg4,ruoli,mem_layer,False))
      self.dlg4.horizontalSliderB.valueChanged.connect(lambda:DlgTools().PRRRuoli(self.dlg4,ruoli,mem_layer,False))      
      self.dlg4.horizontalSlider.valueChanged.connect(lambda:DlgTools().setProbSoglia(self.dlg4))
      self.dlg4.rejected.connect(lambda:DlgTools().PRRRuoli(self.dlg4,ruoli,mem_layer,True))
      self.dlg4.show()
      #self.dialogsList.append(self.dlg4) #ESPERIMENTO
  
    def runSelezionaRuoli(self):
      QueryLayer().createPRRTable() #DA DECIDERE DOVE PIAZZARLO
      Utils().restoreLayerBeni()
      self.dlg7 = RuoliDialog()
      self.dlg7.setWindowIcon(iconRuolo)
      DlgTools().fillComboBox(self.dlg7)
      DlgTools().setDialogGeometry(350,475,'topLeft',self.dlg7)
      DlgTools().fillListWidget(self.dlg7,QueryLayer().getFeaturesList("ruolo",Utils().getLayerRelazioniRuoli()))
      self.dlg7.show()
      #self.dialogsList.append(self.dlg7) #ESPERIMENTO
      result = self.dlg7.exec_()
      if result: 
        esistComun = DlgTools().getEsistComun(self.dlg7)
        ruoli = DlgTools().getSelectedItems(self.dlg7)
        self.runTimeSliderRuolo(ruoli,esistComun)

    def runEsporta(self):
      self.dlg5 = EsportaDialog()
      self.dlg5.setWindowIcon(iconEsporta)
      DlgTools().setDialogGeometry(450,200,'topLeft',self.dlg5)
      DlgTools().fillComboBoxExport(self.dlg5)
      self.dlg5.pushButton.clicked.connect(lambda:DlgTools().select_output_file(self.dlg5))
      self.dlg5.show()
      #self.dialogsList.append(self.dlg5) #ESPERIMENTO
      result = self.dlg5.exec_()
      if result: 
        DlgTools().exportdlg(self.dlg5)

    def runArea(self):
      Utils().restoreLayerBeni()
      self.dlg9 = AreaDialog()
      self.dlg9.setWindowIcon(iconArea)
      DlgTools().setDialogGeometry(500,555,'topLeft',self.dlg9)
      DlgTools().fillListWidget(self.dlg9,QueryLayer().getBeniConDipendenze(2))
      self.dlg9.show()
      #self.dialogsList.append(self.dlg9) #ESPERIMENTO
      result = self.dlg9.exec_()
      if result:
        lBeni = DlgTools().getSelectedItems(self.dlg9)
        if self.dlg9.comboBox.currentText() == "ConvexHull":
          GeomTools().createConvexHull(lBeni,self.dlg9.horizontalSliderA.value(),self.dlg9.horizontalSliderB.value())
        else:
          GeomTools().createBuffer(lBeni,self.dlg9.horizontalSliderA.value(),self.dlg9.horizontalSliderB.value())
        Utils().removeSelectedFeatures()

    def runRipristino(self):
      Utils().restoreLayerBeni()
      Utils().deleteNewLayers()
      Utils().zoomToLayer(Utils().getLayerBeni())
      self.closeOpenDialogs()

    def runGuida(self):
      self.dlg12 = GuidaDialog()
      self.dlg12.setWindowIcon(iconGuida)
      self.dlg12.tabWidget.setTabIcon(0,iconInfo)
      self.dlg12.tabWidget.setTabIcon(1,iconEsporta)
      self.dlg12.tabWidget.setTabIcon(2,iconSeleziona)
      self.dlg12.tabWidget.setTabIcon(3,iconRelazioni)
      self.dlg12.tabWidget.setTabIcon(4,iconVisualizzaBene)
      self.dlg12.tabWidget.setTabIcon(5,iconRuolo)
      self.dlg12.tabWidget.setTabIcon(6,iconPeriodo)
      self.dlg12.tabWidget.setTabIcon(7,iconDistanze)
      self.dlg12.tabWidget.setTabIcon(8,iconArea)
      self.dlg12.tabWidget.setTabIcon(9,iconAltitude)
      self.dlg12.show()
    '''
    def closeOpenDialogs(self):
      for dlg in self.dialogsList:
        if dlg.isVisible(): 
          dlg.setVisible(False)
    '''
    def closeOpenDialogs(self):
      items = vars(self)
      for i in items:
          item = items[i]
          if isinstance(item, QDialog) and item.isVisible(): 
              item.setVisible(False)

    def runAltitudine(self):
      self.dlg13 = AltitudineDialog()
      self.dlg13.setWindowIcon(iconAltitude)
      DlgTools().setDialogGeometry(505,210,'topLeft',self.dlg13)
      self.dlg13.show()
      result = self.dlg13.exec_()
      if result:
        a = self.dlg13.horizontalSliderA.value()
        b = self.dlg13.horizontalSliderB.value()
        GeomTools().getElevationData(a,b)