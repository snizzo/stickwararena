# -*- coding: utf-8 -*-
import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import loadPrcFileData

loadPrcFileData("", """win-size 1024 768""")

class World(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.logo = loader.loadModel("logo_small.egg")
        self.logo.reparentTo(aspect2d)
        pass
    pass

w = World()
w.run()