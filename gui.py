# -*- coding: utf-8 -*-
from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *

class Gui():
    def __init__(self):
        pass
    
    def createMainMenu(self):
        
        #background button
        self.background = loader.loadModel("images/background_main.egg")
        self.background.reparentTo(aspect2d)
        
        #single player button (animated)
        self.spButtonGeom = loader.loadModel("images/beyourhero.egg")
        
        self.spButton = DirectButton(geom = (
        self.spButtonGeom.find('**/beyourhero_ready'),
        self.spButtonGeom.find('**/beyourhero_click'),
        self.spButtonGeom.find('**/beyourhero_rollover'),
        self.spButtonGeom.find('**/beyourhero_disabled')))
        self.spButton.resetFrameSize()
        
        self.spButton['relief'] = None
        self.spButton['command'] = messenger.send
        self.spButton['extraArgs'] = (['startSPDemo'])
        self.spButton.setX(-0.64)
        self.spButton.setZ(0.21)
        
        #exit button (animated)
        self.exitButtonGeom = loader.loadModel("images/surrender.egg")
        
        self.exitButton = DirectButton(geom = (
        self.exitButtonGeom.find('**/surrender_ready'),
        self.exitButtonGeom.find('**/surrender_click'),
        self.exitButtonGeom.find('**/surrender_rollover'),
        self.exitButtonGeom.find('**/surrender_disabled')))
        self.exitButton.resetFrameSize()
        
        self.exitButton['relief'] = None
        self.exitButton['command'] = messenger.send
        self.exitButton['extraArgs'] = (['exitGame'])
        self.exitButton.setX(0.64)
        self.exitButton.setZ(-0.55)
        
    def destroyMainMenu(self):
        self.background.remove()
        self.spButton.remove()
        self.spButtonGeom.remove()
        self.exitButton.remove()
        self.exitButtonGeom.remove()
        
        