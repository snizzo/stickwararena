# -*- coding: utf-8 -*-

#dichiarazioni di panda3d
import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import loadPrcFileData
from panda3d.core import PandaNode,LightNode,TextNode
from panda3d.core import Filename, NodePath
from panda3d.core import PointLight, AmbientLight
from panda3d.core import LightRampAttrib, AuxBitplaneAttrib
from panda3d.core import CardMaker
from panda3d.core import Shader, Texture
from panda3d.core import Point3,Vec4,Vec3
from panda3d.core import WindowProperties
from direct.task.Task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.showbase.BufferViewer import BufferViewer
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
import sys,os

import map
import camera
import gui
import eventsManager

#fullscreen e grandezza finestra
loadPrcFileData("", """fullscreen 0
win-size 1024 768""")

class StickWarArena(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        
        ###impostazioni iniziali
        #self.setupShaders()
        #self.myCamera = camera.Camera()
        #self.myMap = map.Map()
        #self.myMap.setupMap()
        
        #event management
        self.myEventMgr = eventsManager.EventsManager()
        #gui management
        self.myGui = gui.Gui()
        self.myGui.mainMenu()
    
    #all set-ups
    def setupShaders(self):
        render.setShaderAuto()
        #setupfilters and shaders
        self.separation = 1 # Pixels
        self.filters = CommonFilters(base.win, base.cam)
        self.filters.setCartoonInk(separation=self.separation)
        
app = StickWarArena()
app.run()
