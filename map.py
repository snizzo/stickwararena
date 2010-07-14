# -*- coding: utf-8 -*-
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

class Map(DirectObject.DirectObject):
    def __init__(self):
        pass
    def setupMap(self):
        #carico il modello e riparento
        map = loader.loadModel("maps/data/demo.egg")
        map.setP(90)
        map.reparentTo(render)
        
        #carico la skybox e riparento
        skybox = loader.loadModel("maps/data/skybox.egg")
        skybox.setScale(5)
        skybox.reparentTo(render)