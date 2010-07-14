# -*- coding: utf-8 -*-

#dichiarazioni di panda3d
import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import loadPrcFileData
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
import sys,os

import map
import camera
import gui
import eventsManager

#fullscreen e grandezza finestra
loadPrcFileData("", """fullscreen 1
win-size 1024 768""")

class StickWarArena(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        
        #base event handling
        self.accept("exitGame", self.exitGame)
        self.accept("startSPDemo", self.startSPDemo)
        ###impostazioni iniziali
        
        #event management
        self.myEventMgr = eventsManager.EventsManager()
        #gui management
        self.myGui = gui.Gui()
        self.myGui.createMainMenu()
    
    def startSPDemo(self):
        self.myGui.destroyMainMenu()
        self.myCamera = camera.Camera()        
        self.myMap = map.Map()
        self.myMap.setupMap()
        self.myMap.setupShaders()

    def exitGame(self):
        sys.exit()
    
        
app = StickWarArena()
app.run()
