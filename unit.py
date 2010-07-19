# -*- coding: utf-8 -*-
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

class Unit(DirectObject.DirectObject):
    def __init__(self, model, x=0, y=0, z=0):
        self.node = loader.loadModel("models/" + model + ".egg")
        self.node.setPos(x,y,z)
        self.node.reparentTo(render)
        pass
    
