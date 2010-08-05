# -*- coding: utf-8 -*-
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

class Unit(DirectObject.DirectObject):
    def __init__(self, model, x=0, y=0, z=0):
        self.tipo = model
        self.node = loader.loadModel("models/" + model + ".egg")
        self.node.setPos(x,y,z)
        self.node.reparentTo(render)
        self.node.setTag("type", model)
        bradius = self.node.getBounds().getRadius()
        self.otherN = self.node.attachNewNode("otherThings")
        self.selector = loader.loadModel("images/selector.egg")
        self.selector.setLightOff()
        self.selector.reparentTo(self.otherN)
        self.selector.setZ(0.1)
        self.selector.setP(270)
        self.selector.setScale(bradius)
        self.otherN.hide()
        pass
    
