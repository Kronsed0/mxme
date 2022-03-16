# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:30:05 2022

@author: Kronseder Bernhard
"""

class Drink:
    def __init__(self,xName='Default',xIngredients={}):
        self.name = xName
        self.ingredients = xIngredients     #{Sirup:Menge}
        
    def getName(self):
        return self.name
        
    def getIngredients(self):
        return self.ingredients
    
    def update(self,sirup,quantity):
        self.ingredients[sirup]=quantity
        
    def erase(self,sirup):
        del self.ingredients[sirup]