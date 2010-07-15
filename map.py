# -*- coding: utf-8 -*-
from direct.showbase.DirectObject import DirectObject
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

class Map(DirectObject.DirectObject):
    def __init__(self):
        pass
    def setupMap(self):
        #carico il modello e riparento
        mappa = loader.loadModel("maps/data/demo.egg")
        mappa.setP(90)
        mappa.reparentTo(render)
        
        #carico la skybox e riparento
        skybox = loader.loadModel("maps/data/skybox.egg")
        skybox.setScale(512)
        skybox.reparentTo(render)
        
        
    def setupShaders(self):
        #render.setShaderAuto()
        #setupfilters and shaders
        self.filters = CommonFilters(base.win, base.cam)
        self.filters.setCartoonInk(separation=1.5)
        #self.filters.setBloom(size="small")
        #render.setAttrib(LightRampAttrib.makeHdr0())