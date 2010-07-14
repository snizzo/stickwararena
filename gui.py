# -*- coding: utf-8 -*-
from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *

class Gui():
    def __init__(self):
        pass
    
    def mainMenu(self):
        
        #background button
        self.background = loader.loadModel("images/background_main.egg")
        self.background.reparentTo(aspect2d)
        
        
        #exit button (animated)
        self.nodebutton = loader.loadModel("images/surrender.egg")
        
        self.button = DirectButton(geom = (
        self.nodebutton.find('**/surrender_ready'),
        self.nodebutton.find('**/surrender_click'),
        self.nodebutton.find('**/surrender_rollover'),
        self.nodebutton.find('**/surrender_disabled')))
        self.button.resetFrameSize()
        
        self.button['relief'] = None
        self.button['command'] = messenger.send
        self.button['extraArgs'] = (['exitGame'])
        self.button.setX(0.64)
        self.button.setZ(-0.55)
        
        
        