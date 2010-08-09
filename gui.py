# -*- coding: utf-8 -*-
from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import LerpHprInterval

class Gui():
    def __init__(self):
        self.pirulen = loader.loadFont("fonts/pirulen.ttf")
        self.miniImage = False
        #small list of meshdrawer objects... stored only in order not to end my life in a mental clinic
        #with some very very very hardcore mental problems... yay...
        self.lifeBarsLastSelected = []
    
    
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
        self.spButton.setX(-0.68)
        self.spButton.setZ(0.21)
        
        #configuration button (animated)
        self.cfgButtonGeom = loader.loadModel("images/configure.egg")
        
        self.cfgButton = DirectButton(geom = (
        self.cfgButtonGeom.find('**/configure_ready'),
        self.cfgButtonGeom.find('**/configure_click'),
        self.cfgButtonGeom.find('**/configure_rollover'),
        self.cfgButtonGeom.find('**/configure_disabled')))
        self.cfgButton.resetFrameSize()
        
        self.cfgButton['relief'] = None
        self.cfgButton['command'] = messenger.send
        self.cfgButton['extraArgs'] = (['startCFGScreen'])
        self.cfgButton.setX(0.68)
        self.cfgButton.setZ(0.21)
        
        #multi player button (animated)
        self.mpButtonGeom = loader.loadModel("images/worldwidewar.egg")
        
        self.mpButton = DirectButton(geom = (
        self.mpButtonGeom.find('**/worldwidewar_ready'),
        self.mpButtonGeom.find('**/worldwidewar_click'),
        self.mpButtonGeom.find('**/worldwidewar_rollover'),
        self.mpButtonGeom.find('**/worldwidewar_disabled')))
        self.mpButton.resetFrameSize()
        
        self.mpButton['relief'] = None
        self.mpButton['command'] = messenger.send
        self.mpButton['extraArgs'] = (['startMPDemo'])
        self.mpButton.setX(-0.64)
        self.mpButton.setZ(-0.55)
        
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
        self.cfgButton.remove()
        self.cfgButtonGeom.remove()
        self.mpButton.remove()
        self.mpButtonGeom.remove()
        self.exitButton.remove()
        self.exitButtonGeom.remove()
        
    def createCommander(self):
        self.mainCmd = loader.loadModel("images/stick_commander/commander.egg")
        self.mainCmd.setZ(-0.74)
        self.mainCmd.reparentTo(aspect2d)
        self.displayInfo = aspect2d.attachNewNode("displayInfo")
        self.dTL = TextNode("debugTextLine")
        self.dTL.setText("nothing selected")
        self.dTL.setFont(self.pirulen)
        self.dTL.setAlign(TextNode.ACenter)
        self.dTL_np = self.displayInfo.attachNewNode(self.dTL)
        self.dTL_np.setScale(0.05)
        self.dTL_np.setPos(-0.15,0,-0.55)
        
    def updateCommanderSelection(self):
        if len(objSelectionTool.listSelected) == 0:
            self.changeText("nothing selected")
            if self.miniImage != False:
                self.miniImage.remove()
                self.miniImage = False
        if len(objSelectionTool.listSelected) == 1:
            unit = objSelectionTool.listSelected[0]
            type = unit.getTag("type")
            if type == "base":
                if self.miniImage != False:                                                                                                                     
                    self.miniImage.remove()
                    self.miniImage = False
                self.changeText("base")
                self.miniImage = loader.loadModel("models/base.egg")
                self.miniImage.setRenderModeWireframe()
                self.miniImage.setPos(-0.55,0,-0.82)
                self.miniImage.setP(16)
                self.miniImage.setScale(0.2)
                self.miniImage.reparentTo(self.displayInfo)
                self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
            pass
    
    def changeText(self, text):
        self.dTL.setText(text)
    
    def destroyCommander(self):
        self.mainCmd.remove()
        self.displayInfo.remove()
        
        