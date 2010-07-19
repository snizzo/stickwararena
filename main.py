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
win-size 1024 768
text-encoding utf8""")

class StickWarArena(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        
        #base event handling
        self.accept("exitGame", self.exitGame)
        self.accept("startSPDemo", self.startSPDemo)
        self.accept("escape", self.mainMenu)
        ###impostazioni iniziali
        
        #event management
        self.myEventMgr = eventsManager.EventsManager()
        #gui, map, camera and other managements
        self.myGui = gui.Gui()
        self.myMap = map.Map()
        self.myCamera = camera.Camera()
        
        #start point
        self.myGui.createMainMenu()
        self.myMap.setupShaders()
    
    def mainMenu(self):
        self.myMap.destroyMap()
        self.myGui.destroyCommander()
        self.myGui.createMainMenu()
        
        print "exiting... start log ----------------------------------------------"
        self.myMap.army.ls()
        render.ls()
    
    def startSPDemo(self):
        self.myGui.destroyMainMenu()
        self.myMap.setupMap()
        self.myGui.createCommander()

    def exitGame(self):
        sys.exit()
    
        
app = StickWarArena()
app.run()
