# -*- coding: utf-8 -*-
from direct.showbase.DirectObject import DirectObject
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

import army

class Map(DirectObject.DirectObject):
    def __init__(self):
        self.army = army.Army()
        
    def setupMap(self):
        #carico la skybox e riparento
        self.skybox = loader.loadModel("maps/data/skybox.egg")
        self.skybox.setScale(16)
        self.skybox.reparentTo(render)
        
        #carico il modello e riparento
        self.mappa = loader.loadModel("maps/data/demo.egg")
        self.mappa.reparentTo(render)
        
        self.start1 = self.mappa.find("**/Player1_start")
        self.army.setupStartUnits(self.start1)
        camera.setX(self.start1.getX())
        camera.setY(self.start1.getY()-7)
        
    def destroyMap(self):
        self.army.removeAll()
        self.skybox.remove()
        self.mappa.remove()
        self.start1.remove()
        
        
    def setupShaders(self):
        render.setShaderAuto()
        #setupfilters and shaders
        self.filters = CommonFilters(base.win, base.cam)
        #self.filters.setCartoonInk(separation=1.2)
        self.filters.setBloom(size="small")
        render.setAttrib(LightRampAttrib.makeHdr0())