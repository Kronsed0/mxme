# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:30:05 2022

@author: Kronseder Bernhard
"""

def indent(elem, level=0):      #Funktion für das Einrücken der xml-Datei
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i