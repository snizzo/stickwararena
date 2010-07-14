# -*- coding: utf-8 -*-

#dichiarazioni di panda3d
from direct.showbase import DirectObject
from direct.task.Task import Task

import sys,os

class EventsManager(DirectObject.DirectObject):
    
    def __init__(self):
        self.accept("exitGame", self.exitGame)
        pass
    
    def exitGame(self):
        sys.exit()