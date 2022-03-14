# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:30:05 2022

@author: Kronseder Bernhard
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, \
QPushButton, QLineEdit, QLabel, QGridLayout, \
QHBoxLayout,QAbstractButton,QVBoxLayout,QDialog,QFrame,QComboBox,QProgressBar,QSlider,QCheckBox
from PyQt5.QtGui import QIcon,QPixmap,QPainter,QImage,QPalette,QBrush,QFont
from PyQt5.QtCore import QSize,QPoint,Qt
import sys


class MainWindow(QWidget):
    def __init__(self,_device):
        app = QApplication(sys.argv)
        super().__init__()

        

        self.device = _device

        #Haupapplikation initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("MxMe")
        self.resize(1024, 600)
        self.move(0,0)

        #Background
        oImage = QImage("img/background.png")
        sImage = oImage.scaled(QSize(1024,600))
        palette = QPalette()
        palette.setBrush(QPalette.Window,QBrush(sImage))
        self.setPalette(palette)

        #Hauptlayout erzeugen
        self.mainLayout = QGridLayout()
        
        #Buttons f?r Drinks erstellen
        for x in range(8):
            #Zeile und Spalte berechnen
            self.row=2 if x>3 else 0
            self.column=x-4 if x>3 else x
            
            #Name des Drinks
            print("geladene Drinks: ",self.device.getLoadedDrinkName(x))
            print("direkt ausgelesen: ",self.device.loaded_drinks)
            name = self.device.getLoadedDrinkName(x)
            
            #Lables f?r Drinkbeschriftungen erzeugen
            self.drinktext = QLabel()
            if name == "nicht geladen":
                self.drinktext.setText("")
            else:
                self.drinktext.setText(name)
            self.myFont = QFont('Arial',12)
            self.myFont.setBold(True)
            self.setFont(self.myFont)
            
            #Drinkbutton erstellen
            self.drink = PicButton(QPixmap("img/"+name+'.png'),QPixmap("img/"+name+'.png'),QPixmap("img/"+name+'_pressed.png'))
            self.drink.setFixedSize(205,240)
            
            #Signal mit entsprechender Funktion verbinden
            if x==0:
                self.drink.clicked.connect(self.onDrink1Clicked)  
            elif x==1:
                self.drink.clicked.connect(self.onDrink2Clicked) 
            elif x==2:
                self.drink.clicked.connect(self.onDrink3Clicked)
            elif x==3:
                self.drink.clicked.connect(self.onDrink4Clicked)
            elif x==4:
                self.drink.clicked.connect(self.onDrink5Clicked)
            elif x==5:
                self.drink.clicked.connect(self.onDrink6Clicked)
            elif x==6:
                self.drink.clicked.connect(self.onDrink7Clicked)
            elif x==7:
                self.drink.clicked.connect(self.onDrink8Clicked)
        
            #Buttons speichern
            self.device.buttons.append(self.drink)
   
            #Drinkbutton in Layout einbetten
            self.mainLayout.addWidget(self.drink,self.row,self.column)
            #else:
            self.mainLayout.addWidget(self.drinktext,self.row+1,self.column,QtCore.Qt.AlignHCenter)
                     
            
        print("Buttons erfolgreich erstellt")

        #Layout f?r Buttons erstellen
        self.layoutButtons = QVBoxLayout()
        
        #Buttons erstellen
        self.buttonSettings = PicButton(QPixmap('img/Settings.png'),QPixmap('img/Settings.png'),QPixmap('img/Settings_pressed'))
        self.buttonSettings.setFixedSize(64,64)
        self.buttonSettings.clicked.connect(self.onSettingsClicked)
        self.buttonShutdown = PicButton(QPixmap('img/Shutdown.png'),QPixmap('img/Shutdown.png'),QPixmap('img/Shutdown_pressed'))
        self.buttonShutdown.setFixedSize(64,64)
        self.buttonShutdown.clicked.connect(self.onShutdownClicked)

        print("Settings und Shutdown Buttons erfolgreich erstellt")

        #Progressbalken f?r F?llstand
        for x in range(8):
            level = QProgressBar(self)
            level.setMaximum(100)
            self.device.levelList.append(level)
        
        #Buttons in Sublayout einf?gen
        self.layoutButtons.addWidget(self.buttonShutdown)
        self.layoutButtons.addWidget(self.buttonSettings)
        for x in self.device.levelList:
            self.layoutButtons.addWidget(x)
        
        #Sublayout in Layout einf?gen
        self.mainLayout.addLayout(self.layoutButtons,0,4,4,1,QtCore.Qt.AlignTop)        

        #Layout erstellen und anzeigen
        self.setLayout(self.mainLayout)
        self.show()
        app.exec_() # Start der Event-Loop

    def onSettingsClicked(self):
        self.settingsWindow = Settings(self)    #Fenster f?r Einstellungen wird ge?ffnet
        self.settingsWindow.show()

    def onShutdownClicked(self):
        self.close()

    def onDrink1Clicked(self):
        print("Drink ",self.device.getLoadedDrinkName(0)," gedr?ckt")
        self.device.mix(self.device.getLoadedDrink(0))
        
    def onDrink2Clicked(self):
        print("Drink ",self.device.getLoadedDrinkName(1)," gedr?ckt")
        self.device.mix(self.device.getLoadedDrink(1))
        
    def onDrink3Clicked(self):
        print("Drink ",self.device.getLoadedDrinkName(2)," gedr?ckt")
        self.device.mix(self.device.getLoadedDrink(2))
        
    def onDrink4Clicked(self):
        print("Drink ",self.device.getLoadedDrinkName(3)," gedr?ckt")
        self.device.mix(self.device.getLoadedDrink(3))
        
    def onDrink5Clicked(self):
        print("Drink ",self.device.getLoadedDrinkName(4)," gedr?ckt")
        self.device.mix(self.device.getLoadedDrink(4))
        
    def onDrink6Clicked(self):
        print("Drink ",self.device.getLoadedDrinkName(5)," gedr?ckt")
        self.device.mix(self.device.getLoadedDrink(5))
        
    def onDrink7Clicked(self):
        print("Drink ",self.device.getLoadedDrinkName(6)," gedr?ckt")
        self.device.mix(self.device.getLoadedDrink(6))
        
    def onDrink8Clicked(self):
        print("Drink ",self.device.getLoadedDrinkName(7)," gedr?ckt")
        self.device.mix(self.device.getLoadedDrink(7))

class Settings(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Settings")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'),"",self)
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)
        #self.buttonBack.move(QPoint(10,10))

        #Labels f?r Sirups, Drinks und Buttons werden erstellt
        self.labelSirup = QVBoxLayout()
        self.labelDrink = QVBoxLayout()
        self.labelButton = QVBoxLayout()
        self.labelSirupButton = QHBoxLayout()
        self.labelDrinkButton = QHBoxLayout()
        
        #Men?buttons
        self.buttonSafe = PicButton(QPixmap('img/Safe.png'),QPixmap('img/Safe.png'),QPixmap('img/Safe_pressed.png'))
        self.buttonSafe.setFixedSize(64,64)
        self.buttonSafe.clicked.connect(self.onSafeClicked)
        #self.buttonLoad = PicButton(QPixmap('img/Load.png'),QPixmap('img/Load.png'),QPixmap('img/Load_pressed.png'))
        #self.buttonLoad.setFixedSize(64,64)
        #self.buttonLoad.clicked.connect(self.onLoadClicked)
        self.buttonAddSirup = PicButton(QPixmap('img/Add.png'),QPixmap('img/Add.png'),QPixmap('img/Add_pressed.png'))
        self.buttonAddSirup.setFixedSize(64,64)
        self.buttonAddSirup.clicked.connect(self.onAddSirupClicked)
        self.buttonRemoveSirup = PicButton(QPixmap('img/Remove.png'),QPixmap('img/Remove.png'),QPixmap('img/Remove_pressed.png'))
        self.buttonRemoveSirup.setFixedSize(64,64)
        self.buttonRemoveSirup.clicked.connect(self.onRemoveSirupClicked)
        self.buttonAddDrink = PicButton(QPixmap('img/Add.png'),QPixmap('img/Add.png'),QPixmap('img/Add_pressed.png'))
        self.buttonAddDrink.setFixedSize(64,64)
        self.buttonAddDrink.clicked.connect(self.onAddDrinkClicked)
        self.buttonRemoveDrink = PicButton(QPixmap('img/Remove.png'),QPixmap('img/Remove.png'),QPixmap('img/Remove_pressed.png'))
        self.buttonRemoveDrink.setFixedSize(64,64)
        self.buttonRemoveDrink.clicked.connect(self.onRemoveDrinkClicked)
        self.buttonReloadSirup = PicButton(QPixmap('img/Reload.png'),QPixmap('img/Reload.png'),QPixmap('img/Reload_pressed.png'))
        self.buttonReloadSirup.setFixedSize(64,64)
        self.buttonReloadSirup.clicked.connect(self.onReloadSirupClicked)

        self.buttonLoadSirup = QPushButton("Load Sirup",self)
        self.buttonLoadSirup.clicked.connect(self.onLoadSirupClicked)
        self.buttonLoadSirup.resize(QSize(100,100))
        self.buttonUnloadSirup = QPushButton("Unload Sirup",self)
        self.buttonUnloadSirup.clicked.connect(self.onUnloadSirupClicked)
        self.buttonUnloadSirup.resize(QSize(100,100))
        self.buttonLoadDrink = QPushButton("Load Drink",self)
        self.buttonLoadDrink.clicked.connect(self.onLoadDrinkClicked)
        self.buttonLoadDrink.resize(QSize(100,100))
        self.buttonUnloadDrink = QPushButton("Unload Drink",self)
        self.buttonUnloadDrink.clicked.connect(self.onUnloadDrinkClicked)
        self.buttonUnloadDrink.resize(QSize(100,100))
        
        #Slider f?r Geschwindigkeit
        self.sliderSpeed = QSlider(Qt.Horizontal)
        self.sliderSpeed.setRange(10,10000)
        self.sliderSpeed.setFocusPolicy(Qt.NoFocus)
        self.sliderSpeed.setPageStep(10)
        self.sliderSpeed.setValue(1/self.mainWindow.device.getSpeed())
        self.sliderSpeed.valueChanged.connect(self.updateSpeed)

        #Label f?r Geschwindigkeit
        self.labelSpeed = QLabel(str(1/self.mainWindow.device.getSpeed()))
        self.labelSpeedMain = QLabel("Geschwindigkeit:")
        self.labelSpeedMain.setFont(QFont("Arial",18))

        #Slider f?r Clicks/Ml
        self.sliderClicksPerMl = QSlider(Qt.Horizontal)
        self.sliderClicksPerMl.setRange(10,1000)
        self.sliderClicksPerMl.setFocusPolicy(Qt.NoFocus)
        self.sliderClicksPerMl.setPageStep(10)
        self.sliderClicksPerMl.setValue(self.mainWindow.device.getClicksPerMl())
        self.sliderClicksPerMl.valueChanged.connect(self.updateClicks)

        #Label f?r Clicks/Ml
        self.labelClicksPerMl = QLabel(str(self.mainWindow.device.getClicksPerMl()))
        self.labelClicksPerMlMain = QLabel("Impulse pro ml:")
        self.labelClicksPerMlMain.setFont(QFont("Arial",18))

        #Checkbox f?r aktivieren eines Schrittmotors
        self.checkBoxActivate = QCheckBox("Motor 1 aktivieren")
        self.checkBoxActivate.stateChanged.connect(self.checkBoxClicked)

        #Beschriftung f?r labelSirup und labelDrink erzeugen
        self.textSirup = QLabel("Sirups:")
        self.textSirup.setFont(QFont("Arial",18))
        self.textDrink = QLabel("Drinks:")
        self.textDrink.setFont(QFont("Arial",18))

        #Labels Sirups, Drinks und Buttons f?llen
        self.labelSirupButton.addWidget(self.buttonAddSirup)
        self.labelSirupButton.addWidget(self.buttonRemoveSirup)
        self.labelSirupButton.addWidget(self.buttonReloadSirup)
        self.labelSirupButton.addWidget(self.buttonLoadSirup)
        self.labelSirupButton.addWidget(self.buttonUnloadSirup)
        self.labelDrinkButton.addWidget(self.buttonAddDrink)
        self.labelDrinkButton.addWidget(self.buttonRemoveDrink)
        self.labelDrinkButton.addWidget(self.buttonLoadDrink)
        self.labelDrinkButton.addWidget(self.buttonUnloadDrink)

        #bereits erstellte Sirups und Drinks mit Positionen werden hinzugef?gt
        self.labelSirup.addWidget(self.textSirup)
        for s in self.mainWindow.device.getSirups():
            temp = self.mainWindow.device.findPosSirup(s)
            pos = (" ("+str(temp)+")") if temp >= 0 else ""
            self.labelSirup.addWidget(QLabel(s.getName() + pos))
        self.labelSirup.addLayout(self.labelSirupButton)

        self.labelDrink.addWidget(self.textDrink)
        for s in self.mainWindow.device.getDrinks():
            temp = self.mainWindow.device.findPosDrink(s)
            pos = (" ("+str(temp)+")") if temp >= 0 else ""
            self.labelDrink.addWidget(QLabel(s.getName() + pos))
        self.labelDrink.addLayout(self.labelDrinkButton)

        self.labelButton.addWidget(self.buttonSafe)
        #self.labelButton.addWidget(self.buttonLoad)

        #Label f?r Copyright
        self.copyright = QLabel()
        self.copyright.setText(self.mainWindow.device.about+"\n"+self.mainWindow.device.version)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,2,1,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.labelButton,0,3,7,1,QtCore.Qt.AlignBottom)
        self.mainLayout.addLayout(self.labelSirup,0,1)
        self.mainLayout.addLayout(self.labelDrink,0,2)
        self.mainLayout.addWidget(self.labelSpeedMain,1,1)
        self.mainLayout.addWidget(self.checkBoxActivate,5,1)
        self.mainLayout.addWidget(self.sliderSpeed,2,1)
        self.mainLayout.addWidget(self.labelSpeed,2,2)
        self.mainLayout.addWidget(self.labelClicksPerMlMain,3,1)
        self.mainLayout.addWidget(self.sliderClicksPerMl,4,1)
        self.mainLayout.addWidget(self.labelClicksPerMl,4,2)
        self.mainLayout.addWidget(self.copyright,6,1,QtCore.Qt.AlignBottom)
        #self.mainLayout.setRowMinimumHeight(0,200)
        self.setLayout(self.mainLayout)
        
        
    def onSafeClicked(self):
        self.mainWindow.device.safeData()

    #def onLoadClicked(self):
    #    pass
     
    def onAddSirupClicked(self):
        self.addSirupWindow = AddSirup(self.mainWindow)    #Fenster f?r Einstellungen wird ge?ffnet
        self.addSirupWindow.show()

    def onRemoveSirupClicked(self):
        self.eraseSirupWindow = EraseSirup(self.mainWindow)
        self.eraseSirupWindow.show()

    def onAddDrinkClicked(self):
        self.addDrinkWindow = AddDrink(self.mainWindow)
        self.addDrinkWindow.show()

    def onRemoveDrinkClicked(self):
        self.eraseDrinkWindow = EraseDrink(self.mainWindow)
        self.eraseDrinkWindow.show()

    def onLoadSirupClicked(self):
        self.loadSirupWindow = LoadSirup(self.mainWindow)    #Fenster f?r Einstellungen wird ge?ffnet
        self.loadSirupWindow.show()

    def onReloadSirupClicked(self):
        self.reloadSirupWindow = ReloadSirup(self.mainWindow)
        self.reloadSirupWindow.show()

    def onLoadDrinkClicked(self):
        self.loadDrinkWindow = LoadDrink(self.mainWindow)
        self.loadDrinkWindow.show()

    def onUnloadSirupClicked(self):
        self.unloadSirupWindow = UnloadSirup(self.mainWindow)
        self.unloadSirupWindow.show()

    def onUnloadDrinkClicked(self):
        self.UnloadDrinkWindow = UnloadDrink(self.mainWindow)
        self.UnloadDrinkWindow.show()

    def onBackClicked(self):
        self.mainWindow.device.updateRemainingLiquid()
        self.mainWindow.device.safeData()
        self.close()

    def updateSpeed(self,value):
        self.labelSpeed.setText(str(value))
        self.mainWindow.device.setSpeed(1/value)
        self.update()

    def updateClicks(self,value):
        self.labelClicksPerMl.setText(str(value))
        self.mainWindow.device.setClicksPerMl(value)
        self.update()

    def checkBoxClicked(self,state):
        if state == Qt.Checked:
            print("Motor wird aktiviert")
            if rasp:
                GPIO.output(channels[0][0],GPIO.LOW)
        else:
            print("Motor wird deaktiviert")
            if rasp:
                GPIO.output(channels[0][0],GPIO.HIGH)

    
#---------------------------------------------------------------------------

class AddSirup(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Add Sirup")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        #OK Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Sirupname und Menge
        self.textboxName = QLineEdit()
        self.textboxName.setText("")
        self.textboxLiquid = QLineEdit()
        self.textboxLiquid.setText("")

        self.name = QLabel("Name:")
        self.name.setFont(QFont("Arial",18))
        self.liquid = QLabel("Menge:")
        self.liquid.setFont(QFont("Arial",18))

        self.window = QVBoxLayout()
        self.window.addWidget(self.name)
        self.window.addWidget(self.textboxName)
        self.window.addWidget(self.liquid)
        self.window.addWidget(self.textboxLiquid)
        self.window.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.window,0,1)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onOkClicked(self):
        self.mainWindow.device.createSirup(self.textboxName.text(),int(self.textboxLiquid.text()))
        self.close()
        

#---------------------------------------------------------------------------

class LoadSirup(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Load Sirup")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        #OK und Delete Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Drinkname
        self.comboBoxSirup = QComboBox()
        for s in self.mainWindow.getSirups():
            self.comboBoxSirup.addItem(s.getName())
        self.comboBoxPosition = QComboBox()
        for x in range(8):
            self.comboBoxPosition.addItem(str(x))

        self.name = QLabel("Name:")
        self.name.setFont(QFont("Arial",18))
        self.liquid = QLabel("Position:")
        self.liquid.setFont(QFont("Arial",18))

        self.window = QVBoxLayout()
        self.window.addWidget(self.name)
        self.window.addWidget(self.comboBoxSirup)
        self.window.addWidget(self.liquid)
        self.window.addWidget(self.comboBoxPosition)
        self.window.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.window,0,1)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onOkClicked(self):
        #gew?hlten Sirup finden
        sirup = self.mainWindow.findSirup(self.comboBoxSirup.currentText())
        position = int(self.comboBoxPosition.currentText())
        self.mainWindow.loadIngredient(sirup,int(position))
        self.close()

#---------------------------------------------------------------------------

class AddDrink(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Add Drink")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        self.listIngredients = []
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        self.buttonAddIngredient = QPushButton("Add Ingredient",self)
        self.buttonAddIngredient.clicked.connect(self.onAddIngredientClicked)

        #OK Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Drinkname
        self.comboBoxSirup = QComboBox()
        for s in self.mainWindow.getSirups():
            self.comboBoxSirup.addItem(s.getName())
        self.textBoxMenge = QLineEdit()
        self.textBoxMenge.setText("")
        self.textBoxName = QLineEdit()
        self.textBoxName.setText("")

        self.name = QLabel("Bestandteil:")
        self.name.setFont(QFont("Arial",18))
        self.liquid = QLabel("Menge:")
        self.liquid.setFont(QFont("Arial",18))
        self.liste = QLabel("Liste:")
        self.liste.setFont(QFont("Arial",18))
        self.bezeichnung = QLabel("Name:")
        self.bezeichnung.setFont(QFont("Arial",18))
        self.Ingredients = QLabel()

        self.windowLeft = QVBoxLayout()
        self.windowLeft.addWidget(self.name)
        self.windowLeft.addWidget(self.comboBoxSirup)
        self.windowLeft.addWidget(self.liquid)
        self.windowLeft.addWidget(self.textBoxMenge)
        self.windowLeft.addWidget(self.buttonAddIngredient)

        self.windowRight = QVBoxLayout()
        self.windowRight.addWidget(self.bezeichnung)
        self.windowRight.addWidget(self.textBoxName)
        self.windowRight.addWidget(self.liste)
        self.windowRight.addWidget(self.Ingredients)
        self.windowRight.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.windowLeft,0,1)
        self.mainLayout.addLayout(self.windowRight,0,2)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onAddIngredientClicked(self):
        self.listIngredients.append((self.comboBoxSirup.currentText(),self.textBoxMenge.text()))
        print(self.listIngredients)
        text=""
        for x in self.listIngredients:
            text = text + str(x) + '\n'
        self.Ingredients.setText(text)
        self.update()

    def onOkClicked(self):
        #Dict erstellen
        d = {}
        for x,y in self.listIngredients:
            d[self.mainWindow.findSirup(x)] = int(y)
        print("Dict beim Erstellen: ",d)

        #Drink erstellen
        self.mainWindow.createDrink(self.textBoxName.text(),d)
        self.close()

#---------------------------------------------------------------------------

class LoadDrink(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Load Drink")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        #OK und Delete Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Drinkname
        self.comboBoxDrink = QComboBox()
        for s in self.mainWindow.getDrinks():
            self.comboBoxDrink.addItem(s.getName())
        self.comboBoxPosition = QComboBox()
        for x in range(8):
            self.comboBoxPosition.addItem(str(x))

        self.name = QLabel("Name:")
        self.name.setFont(QFont("Arial",18))
        self.liquid = QLabel("Position:")
        self.liquid.setFont(QFont("Arial",18))

        self.window = QVBoxLayout()
        self.window.addWidget(self.name)
        self.window.addWidget(self.comboBoxDrink)
        self.window.addWidget(self.liquid)
        self.window.addWidget(self.comboBoxPosition)
        self.window.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.window,0,1)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onOkClicked(self):
        #gew?hlten Sirup finden
        drink = self.mainWindow.findDrink(self.comboBoxDrink.currentText())
        position = int(self.comboBoxPosition.currentText())
        self.mainWindow.loadDrink(drink,position)
        self.close()

#---------------------------------------------------------------------------

class UnloadSirup(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Unload Sirup")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        #OK und Delete Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Position
        self.comboBoxPosition = QComboBox()
        for x in range(8):
            self.comboBoxPosition.addItem(str(x))

        self.position = QLabel("Position:")
        self.position.setFont(QFont("Arial",18))

        self.window = QVBoxLayout()
        self.window.addWidget(self.position)
        self.window.addWidget(self.comboBoxPosition)
        self.window.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.window,0,1)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onOkClicked(self):
        position = int(self.comboBoxPosition.currentText())
        self.mainWindow.unloadIngredient(position)
        self.close()

#---------------------------------------------------------------------------

class UnloadDrink(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Unload Drink")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        #OK und Delete Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Position
        self.comboBoxPosition = QComboBox()
        for x in range(8):
            self.comboBoxPosition.addItem(str(x))

        self.position = QLabel("Position:")
        self.position.setFont(QFont("Arial",18))

        self.window = QVBoxLayout()
        self.window.addWidget(self.position)
        self.window.addWidget(self.comboBoxPosition)
        self.window.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.window,0,1)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onOkClicked(self):
        position = int(self.comboBoxPosition.currentText())
        self.mainWindow.unloadDrink(position)
        self.close()

#---------------------------------------------------------------------------

class EraseDrink(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Erase Drink")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        #OK und Delete Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Drinkname
        self.comboBoxDrink = QComboBox()
        for s in self.mainWindow.getDrinks():
            self.comboBoxDrink.addItem(s.getName())

        self.name = QLabel("Name:")
        self.name.setFont(QFont("Arial",18))

        self.window = QVBoxLayout()
        self.window.addWidget(self.name)
        self.window.addWidget(self.comboBoxDrink)
        self.window.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.window,0,1)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onOkClicked(self):
        #gew?hlten Sirup finden
        self.mainWindow.eraseDrink(self.comboBoxDrink.currentText())
        print("Drink",self.comboBoxDrink.currentText(),"geloescht")
        self.close()

#---------------------------------------------------------------------------

class EraseSirup(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Erase Sirup")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        #OK und Delete Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Drinkname
        self.comboBoxSirup = QComboBox()
        for s in self.mainWindow.getSirups():
            self.comboBoxSirup.addItem(s.getName())

        self.name = QLabel("Name:")
        self.name.setFont(QFont("Arial",18))

        self.window = QVBoxLayout()
        self.window.addWidget(self.name)
        self.window.addWidget(self.comboBoxSirup)
        self.window.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.window,0,1)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onOkClicked(self):
        #gew?hlten Sirup finden
        self.mainWindow.eraseSirup(self.comboBoxSirup.currentText())
        print("Sirup",self.comboBoxSirup.currentText(),"geloescht")
        self.close()

#---------------------------------------------------------------------------

class ReloadSirup(QWidget):
    def __init__(self,mainWindow):
        super().__init__()
        #Unterfenster initialisieren
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Reload Sirup")
        self.resize(1024, 600)
        self.move(0,0)
        
        #Referenz auf das mainWindow Objekt wird gespeichert
        self.mainWindow = mainWindow
        
        #Zur?ck-Button wird erstellt
        self.buttonBack = PicButton(QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck.png'),QPixmap('img/Zuruck_pressed.png'))
        self.buttonBack.setFixedSize(64,64)
        self.buttonBack.clicked.connect(self.onBackClicked)

        #OK und Delete Button
        self.buttonOk = PicButton(QPixmap('img/Ok.png'),QPixmap('img/Ok.png'),QPixmap('img/Ok_pressed.png'))
        self.buttonOk.setFixedSize(64,64)
        self.buttonOk.clicked.connect(self.onOkClicked)

        #Texteingabe f?r Drinkname
        self.comboBoxSirup = QComboBox()
        for s in self.mainWindow.getSirups():
            self.comboBoxSirup.addItem(s.getName())

        self.name = QLabel("Name:")
        self.name.setFont(QFont("Arial",18))

        self.window = QVBoxLayout()
        self.window.addWidget(self.name)
        self.window.addWidget(self.comboBoxSirup)
        self.window.addWidget(self.buttonOk)

        #Anzeige
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.buttonBack,0,0,QtCore.Qt.AlignTop)
        self.mainLayout.addLayout(self.window,0,1)
        self.setLayout(self.mainLayout)
        self.show()
        
    def onBackClicked(self):
        self.close()

    def onOkClicked(self):
        #gew?hlten Sirup finden
        sirup=self.mainWindow.findSirup(self.comboBoxSirup.currentText())
        #Restmenge auf 100% setzen
        sirup.setRemainingLiquid(100)
        #Debug-Ausgabe
        print("Sirup",self.comboBoxSirup.currentText(),"wurde aufgefuellt")
        self.close()

#---------------------------------------------------------------------------

class PicButton(QAbstractButton,):
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, text='abc',parent=None):
        super().__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(200, 200)