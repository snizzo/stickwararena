# -*- coding: utf-8 -*-
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

import unit

class Army(DirectObject.DirectObject):
    def __init__(self):
        #creating main list
        self.unitList = []
    
    def setupStartUnits(self, start1):
        self.addUnit("base", start1.getX(),start1.getY(),start1.getZ())
    
    def addUnit(self, model, x, y, z):
        thisunit = unit.Unit(model, x, y, z)
        self.unitList.append(thisunit)
    
    def removeUnit(self, np):
        np.node.remove()
        self.unitList.remove(np)
    
    def ls(self):
        print "self unit: ", self.unitList
    
    #function that i use to remove all my RTS's units from the main units list.
    def removeAll(self):
        for unit in self.unitList[:]:
            unit.node.remove()
            self.unitList.remove(unit)
