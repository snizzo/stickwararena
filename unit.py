# -*- coding: utf-8 -*-
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os,string

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
            self.colorFlag = self.node.find("**/colorFlagObj")
            self.materialFlag = Material("materialFlag")
            self.materialFlag.setDiffuse(Vec4(1,0,0,1))
            self.colorFlag.setMaterial(self.materialFlag,1)
            self.colorFlag.setColor(0.5,0.5,0.5,1)
            bradius = self.node.getBounds().getRadius()
            self.otherN = self.node.attachNewNode("otherThings")
            self.selector = loader.loadModel("images/selector.egg")
            self.selector.setLightOff()
            self.selector.reparentTo(self.otherN)
            self.selector.setZ(0.1)
            self.selector.setP(270)
            self.selector.setScale(bradius)
            self.otherN.hide()
            
            ##unit properties
            #life
            self.totalLife = 400
            self.node.setPythonTag("hp", 400)
            self.node.setPythonTag("unitobj", self)
            
            #building lifebar
            amount = self.node.getPythonTag("hp")
            self.myLifeBar = MeshDrawer()
            self.myLifeBar.setBudget(amount/5)
            self.myLifeBarNode = self.myLifeBar.getRoot()
            self.myLifeBarNode.reparentTo(self.otherN)
            self.myLifeBarNode.setTexture(loader.loadTexture("images/stick_commander/lifebar.png"))
            self.myLifeBarNode.setLightOff(True)
            self.myLifeBar.begin(base.cam,render)
            for i in range(amount/10):
                self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0,0.5,0.5),0.035,Vec4(1,1,1,1))
            barBound = self.myLifeBarNode.getBounds().getRadius()
            self.myLifeBarNode.setX(-barBound+0.06)
            self.myLifeBarNode.setY(-bradius/2-0.35)
            self.myLifeBar.end()
            #end building lifebar
            
    def updateBarLife(self):
        currentLife = self.node.getPythonTag("hp")
        lifeColor = currentLife*100/self.totalLife
        print "currentLife ", currentLife 
        print "totalLife ", self.totalLife
        print "lifeColor value ", lifeColor
        #draw red life because unit is near death
        if lifeColor <= 35:
            self.myLifeBar.begin(base.cam,render)
            for i in range(currentLife/10):
                self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0.5,0,0.5,0.5),0.035,Vec4(1,1,1,1))
            for e in range(self.totalLife/10-currentLife/10):
                i += 1;
                self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
            self.myLifeBar.end()
            
        if lifeColor > 35 and lifeColor < 70 :
            self.myLifeBar.begin(base.cam,render)
            for i in range(currentLife/10):
                self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0.5,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
            for e in range(self.totalLife/10-currentLife/10):
                i += 1;
                self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
            self.myLifeBar.end()
        if lifeColor >= 70:
            self.myLifeBar.begin(base.cam,render)
            for i in range(currentLife/10):
                self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0,0.5,0.5),0.035,Vec4(1,1,1,1))
            for e in range(self.totalLife/10-currentLife/10):
                i += 1;
                self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
            self.myLifeBar.end()
    
    def giveDamage(self,amount):
        life = self.node.getPythonTag("hp")
        newlife = life - amount
        self.node.setPythonTag("hp", newlife)
        self.updateBarLife()
    
    def giveHeal(self,amount):
        life = self.node.getPythonTag("hp")
        newlife = life + amount
        self.node.setPythonTag("hp", newlife)
        self.updateBarLife()
    
    def __del__(self):
        #avoiding crashes when clearing scene and something is selected/not removed
        if(self.node in objSelectionTool.listSelected):
            objSelectionTool.listSelected.remove(self.node)
        if(self.node in objSelectionTool.listLastSelected):
            objSelectionTool.listLastSelected.remove(self.node)
        self.node.remove()
