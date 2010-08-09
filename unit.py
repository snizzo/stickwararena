# -*- coding: utf-8 -*-
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

class Unit(DirectObject.DirectObject):
    def __init__(self, model, x=0, y=0, z=0):
        if model == "base":
            self.tipo = model
            self.lifebar = False
            self.lifebarnode = False
            self.node = loader.loadModel("models/base.egg")
            self.node.setPos(x,y,z)
            self.node.reparentTo(render)
            self.node.setTag("type", model)
            bradius = self.node.getBounds().getRadius()
            self.otherN = self.node.attachNewNode("otherThings")
            self.selector = loader.loadModel("images/selector.egg")
            self.selector.setLightOff()
            self.selector.reparentTo(self.otherN)
            self.selector.setZ(0.1)
            self.selector.setP(270)
            self.selector.setScale(bradius)
            self.otherN.hide()
            
            #building lifebar
            self.myLifeBar = MeshDrawer()
            self.myLifeBar.setBudget(40)
            self.myLifeBarNode = self.myLifeBar.getRoot()
            self.myLifeBarNode.reparentTo(self.otherN)
            self.myLifeBarNode.setTexture(loader.loadTexture("images/stick_commander/lifebar.png"))
            self.myLifeBarNode.setLightOff(True)
            self.myLifeBar.begin(base.cam,render)
            for i in range(20):
                self.myLifeBar.billboard(Vec3(i*0.1,0,+0.15),Vec4(0,0,0.5,0.5),0.05,Vec4(1,1,1,1))
            barBound = self.myLifeBarNode.getBounds().getRadius()
            self.myLifeBarNode.setX(-barBound+0.06)
            self.myLifeBarNode.setY(-bradius/2-0.35)
            self.myLifeBar.end()
            #end building lifebar
    def __del__(self):
        self.node.remove()
