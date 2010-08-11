# -*- coding: utf-8 -*-

#dichiarazioni di panda3d
import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import loadPrcFileData
from direct.gui.DirectGui import *
from direct.task import Task
import sys,os

import map
import gui

from direct.showbase.DirectObject import DirectObject

#fullscreen e grandezza finestra
loadPrcFileData("", """fullscreen 1
win-size 1024 768
text-encoding utf8""")

class StickWarArena(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        ###impostazioni iniziali

        #gui, map, camera and other managements
        self.myGui = gui.Gui()
        self.myMap = map.Map()

        #start point
        self.myGui.createMainMenu()
        self.myMap.setupShaders()

        #base event handling
        self.accept("exitGame", self.exitGame)
        self.accept("startSPDemo", self.startSPDemo)
        self.accept("escape", self.mainMenu)
        self.accept("mouse-selection", self.myGui.updateCommanderSelection)

    def ciao(self):
        #print objSelectionTool.listSelected
        print self.myMap.army.selectedUnitList

    def mainMenu(self):
        self.myMap.destroyMap()
        self.myGui.destroyCommander()
        self.myGui.createMainMenu()


    def startSPDemo(self):
        self.myGui.destroyMainMenu()
        self.myMap.setupMap()
        myCamera.cameraSetup()
        self.myGui.createCommander()


    def exitGame(self):
        sys.exit()


app = StickWarArena()
from camera import *
app.run()
