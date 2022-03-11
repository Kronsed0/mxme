# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:30:05 2022

@author: Kronseder Bernhard
"""

class Sirup:
    def __init__(self,xName='Default',xLiquid=0):
        self.name = xName
        self.liquid = xLiquid
        self.remaining_liquid = xLiquid
        
    def getName(self):
        return self.name
    
    def getRemainingLiquid(self):
        return int((self.remaining_liquid/self.liquid) * 100)

    def setRemainingLiquid(self,percent):
        if (percent <=100) & (percent >=0):
            self.remaining_liquid=self.getLiquid()*(percent/100)
            print("Restmenge von",self.getName(),"auf",percent,"% gesetzt")
        else:
            print("Unzul�ssige Mengenangabe")
    
    def getLiquid(self):
        return self.liquid
    
    def pourOut(self,quantity):
        self.remaining_liquid=self.remaining_liquid - quantity
        if self.remaining_liquid<0:
            self.remaining_liquid=0