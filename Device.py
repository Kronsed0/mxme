# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:30:05 2022

@author: Kronseder Bernhard
"""

from PyQt5 import QtCore
from pathlib import Path
import platform
import sys
import xml.etree.ElementTree as ET
import time
from Drink import *
from Sirup import *
from XML_Formatierung import *
from GUI import *

class Device():
    def __init__(self,xName='Default'):
        self.name = xName
        self.drinks = []    #Liste mit verfügbaren Drinks
        self.sirups = []    #Liste mit verfügbaren Sirups
        self.loaded_ingredients = {}    #Dict {Position:Sirup}
        self.loaded_drinks = {}         #Dict {Position:Drink}
        self.buttons = []   #Hier werden die Buttons zwischengespeichert
        self.levelList = [] #Liste für die F?llstandsanzeigen
        self.clicksPerMl = 50   #Wert für die Ausflussgeschwindigkeit pro Schritt
        self.speed = 0.01       #Geschwindigkeit der Steppermotoren (Delay in s zwischen Schritten)
        self.version = "Version: 0.6.0"    #Version {Alpha=0,Beta=1,Release=x}.{FunctionChanges}.{BugFix}
        self.about = "@ mxme"

        os = platform.platform()
        self.rasp = True if "Linux" in os else False

        #Hardware einbinden, falls Programm auf Linux ausgeführt wird
        self.initHardware()

        #Daten aus XML-Datei auslesen 
        self.loadData()
        
        #MainWindow laden
        MainWindow(self)       
        
    def initHardware(self):
        #Abfrage für Betriebssystem -> wenn Linux auf Raspberry wird Hardwarebib eingebunden
        if self.rasp:
           import RPi.GPIO as GPIO

           #Pinbelegung: [[Enable1,Direction1,Step1],[Enable2,Direction2,Step2],...]
           channels = [[6,11,5],[26,13,19],[16,21,20],[8,12,7],[24,9,25],[15,23,18],[3,14,2],[27,4,17]]

           #Pins als Ausgang deklarieren
           GPIO.setmode(GPIO.BCM)
           for channel in channels:
               for pin in channel:
                   GPIO.setup(pin,GPIO.OUT)

           #Treiber deaktivieren
           print("Treiber werden initial deaktiviert:")
           for channel in channels:
            GPIO.output(channel[0],GPIO.HIGH)
            print(".")

    def loadIngredient(self,sirup,place,percent=100):
        #Sirup wird in Ger?t geladen        
        if len(self.loaded_ingredients) < 8:
            if place in self.loaded_ingredients:
                print("bereits vergeben!")
            else:
                self.loaded_ingredients.update({place:sirup})
                self.loaded_ingredients[place].setRemainingLiquid(percent)
                print(sirup.getName(), "erfolgreich auf Position", place,"mit der Menge",percent, "montiert!")
        else:
            print("alle Plaetze belegt!")
        
    def unloadIngredient(self,place):
        if place in self.loaded_ingredients:
            del self.loaded_ingredients[place]
            print("Sirup erfolgreich entfernt!")
        else:
            print("kein Sirup an dieser Position eingelegt!")
            
    def loadDrink(self,Drink,place):
        if place in self.loaded_drinks:
            print("Drink",Drink.getName(),"an der Stelle",place,"wird ersetzt!")
            self.loaded_drinks[place]=Drink
        else:
            print("Drink",Drink.getName(),"wird an der Stelle",place,"eingefuegt")
            self.loaded_drinks[place]=Drink
    
    def unloadDrink(self,place):
        if place in self.loaded_drinks:
            del self.loaded_drinks[place]
            print("Drink erfolgreich entfernt!")
        else:
            print("kein Drink an dieser Position gespeichert!")
            
    def getSirupLevel(self):
        erg=[]
        for x in range(8):
            if x in self.loaded_ingredients:
                erg.append(self.loaded_ingredients[x].getRemainingLiquid())
            else:
                erg.append(0)
        return erg
        
    def mix(self,drink):
        #richtige Übergabeparameter?
        if drink == None:
            print("kein gültiger Drink übergeben!")
            return 0

        #benötigte Sirups geladen?
        for x in drink.getIngredients().keys():
            if x in self.getLoadedIngredients().values():
                print(".")
            else:
                print(x.getName()," nicht geladen!!")
                return 0

        #Position/Menge auslesen und in Liste speichern
        ing = []        #Liste mit folgendem Aufbau [(position,menge),(position,menge)]
        for s in drink.getIngredients().keys():     #über Bestandteile iterieren
            ing.append((self.findPosSirup(s),drink.getIngredients()[s]))
        print("Pumpenausgabe--------------")
        print(ing)
        if self.rasp:
            for pos,men in ing:
                #Pumpe einschalten (Enable und Richtung)
                GPIO.output(channels[pos][0],GPIO.LOW)
                GPIO.output(channels[pos][1],GPIO.LOW)

                #Menge der Impulse berechnen (nach Int konvertieren, da Float nicht iteriert werden kann)
                total = int(men*self.clicksPerMl)

                #Impulse ausf?hren
                for x in range(total):
                    GPIO.output(channels[pos][2],GPIO.HIGH)
                    time.sleep(self.speed)
                    GPIO.output(channels[pos][2],GPIO.LOW)
                    time.sleep(self.speed)

                #Pumpe ausschalten
                GPIO.output(channels[pos][0],GPIO.HIGH)
                
        #Inhalt von Sirups wird angepasst
        for sirup in drink.getIngredients().keys():
            sirup.pourOut(drink.getIngredients()[sirup])
            print("Restmenge",sirup.getName(),": ",sirup.getRemainingLiquid(),"%")
        self.updateRemainingLiquid()
            
        #Ausgabe
        print(drink.getName(),"wurde ausgeschenkt")

        #aktueller Zwischenstand wird gespeichert
        self.safeData()

    def updateRemainingLiquid(self):
        #Liste der levelmeter durchgehen und Value anpassen
        for x in range(8):
            if x in self.getLoadedIngredients():        #Pr?fen, ob Platz mit Sirup belegt ist
                remaining = self.getLoadedIngredients()[x].getRemainingLiquid()      #wenn ja, wird Restmenge ausgelesen
                self.levelList[x].setValue(remaining)
    
    def getLoadedIngredients(self):
        return self.loaded_ingredients

    def getLoadedDrinks(self):
        return self.loaded_drinks
    
    def getName(self):
        return self.name
    
    def getLoadedDrink(self,number=-1):
        erg=None
        if number == -1:
            erg = self.loaded_drinks
        else:
            if number in self.loaded_drinks:
                erg=self.loaded_drinks[number]
            else:
                print("kein Drink an dieser Stelle geladen")
        return erg
                
    def getLoadedDrinkName(self,number):
        #Liefert den Namen eines Drinks an der ?bergebenen Stelle [0...7],
        #wenn Drink nicht geladen wird "nicht geladen" zur?ckgegeben
        temp = self.getLoadedDrink().get(number)
        if temp != None:
            erg=temp.getName()
        else:
            erg="nicht geladen"
        return erg
    
    def createDrink(self,name,ingredients):
        self.drinks.append(Drink(name,ingredients))
        print("Created Drink: ",name)

    def eraseDrink(self,drinkname):
        drink = self.findDrink(drinkname)
        self.drinks.remove(drink)
    
    def createSirup(self,name,Liquid):
        self.sirups.append(Sirup(name,Liquid))
        print("Created Sirup: ",name)

    def eraseSirup(self,sirupname):
        sirup = self.findSirup(sirupname)
        self.sirups.remove(sirup)
    
    def getDrinks(self):
        return self.drinks
    
    def getSirups(self):
        return self.sirups
        
    def loadData(self):
        data=Path("Data.xml")
        if data.is_file():
            print("XML Datei gefunden!")
            baum = ET.parse("Data.xml")
            device = baum.getroot()     #Ebene 0 (Device)  
            for e1 in device:           #Ebene 1 (Settings,Sirups,Drinks,loadedSirups,loadedDrinks)  
                for e2 in e1:           #Ebene 2 (Mojito,Aperol-Spritz)
                    if e1.tag == "Sirups":
                        self.createSirup(e2.tag,int(e2.attrib['liquid']))
                    elif e1.tag == "Drinks":      #wenn Ebene 1 Drinks ist
                        i={}
                        for e3 in e2:
                            i[self.findSirup(e3.tag)]=int(e3.attrib['Quantity'])
                        self.createDrink(e2.tag,i)
                    elif e1.tag == "LoadedSirups":
                        self.loadIngredient(self.findSirup(e2.tag),int(e2.attrib['number']),int(e2.attrib['remainingLiquid']))
                    elif e1.tag == "LoadedDrinks":
                        self.loadDrink(self.findDrink(e2.tag),int(e2.attrib['number']))
                    elif e1.tag == "Settings":
                        if e2.tag == "Clicks":
                            self.clicksPerMl = int(e2.attrib['clicksPerMl'])
                        elif e2.tag == "Speed":
                            self.speed = float(e2.attrib['speed'])
        else:
            print("Konnte keine XML Datei finden...")


    def safeData(self):
        device = ET.Element("Device")
        settings = ET.SubElement(device,"Settings")
        sirups = ET.SubElement(device,"Sirups")
        drinks = ET.SubElement(device,"Drinks")
        loadedSirups = ET.SubElement(device,"LoadedSirups")
        loadedDrinks = ET.SubElement(device,"LoadedDrinks")

        ET.SubElement(settings,"Clicks",clicksPerMl = str(self.clicksPerMl))
        ET.SubElement(settings,"Speed",speed=str(self.speed))
        
        for x in self.getSirups():
            ET.SubElement(sirups,x.getName(),liquid = str(x.getLiquid()))
            
        for x in self.getDrinks():
            drink = ET.SubElement(drinks,x.getName())
            for ingredients,quantity in zip(x.getIngredients().keys(),x.getIngredients().values()):
                if ingredients == None:
                    print("enthaltener Sirup gelöscht! Manueller Eintrag in XML-Datei erforderlich")
                else:
                    ET.SubElement(drink,ingredients.getName(),Quantity = str(quantity))

        for number,ingredient in zip(self.getLoadedIngredients().keys(),self.getLoadedIngredients().values()):
            ET.SubElement(loadedSirups,ingredient.getName(),number=str(number),remainingLiquid=str(ingredient.getRemainingLiquid()))

        for number,drink in zip(self.getLoadedDrink().keys(),self.getLoadedDrink().values()):
            ET.SubElement(loadedDrinks,drink.getName(),number=str(number))
        
        indent(device)      #Einr?ckungen in XML-Datei f?r Lesbarkeit
        tree = ET.ElementTree(device)
        tree.write("Data.xml")
        print("Gespeichert!")

    def findSirup(self,name):
        for s in self.sirups:
            if s.getName() == name:
                return s
            
    def findDrink(self,name):
        for d in self.drinks:
            if d.getName() == name:
                return d

    def findPosSirup(self,sirup):
        erg = -1
        for k,v in self.loaded_ingredients.items():
            if v == sirup:
                erg = k
        return erg

    def findPosDrink(self,drink):
        erg = -1
        for k,v in self.loaded_drinks.items():
            if v == drink:
                erg = k
        return erg

    def getSpeed(self):
        return self.speed

    def setSpeed(self,value):
        self.speed = value

    def getClicksPerMl(self):
        return self.clicksPerMl
    
    def setClicksPerMl(self,value):
        self.clicksPerMl = value

    def enablePump(self,nr):
        print("Motor wird aktiviert")
        if self.rasp:
            GPIO.output(channels[nr][0],GPIO.LOW)

    def disablePump(self,nr):
        print("Motor wird deaktiviert")
        if self.rasp:
            GPIO.output(channels[nr][0],GPIO.HIGH)