# -*- coding: utf-8 -*-
from direct.showbase.DirectObject import DirectObject
from direct.filter.CommonFilters import CommonFilters
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import xml.dom.minidom
import sys,os

import army

class Map(DirectObject.DirectObject):
    def __init__(self):
        self.elementList = []
        self.army = army.Army()
        
    def setupMap(self):
        #carico la skybox e riparento
        self.skybox = loader.loadModel("maps/data/skybox.egg")
        self.skybox.setScale(16)
        self.skybox.reparentTo(render)
        
        self.loadMap("editor/experimental.swm")
        
    def destroyMap(self):
        self.army.removeAll()
        self.skybox.remove()
        self.mapHolder.remove()
        self.start1.remove()
        
    def loadMap(self, xmlFile):
        self.mapHolder = render.attachNewNode("absMap")
        
        self.myMap = xml.dom.minidom.parse(xmlFile)
        
        for e in self.myMap.childNodes:
            if e.nodeType == e.ELEMENT_NODE:
                self.mapName = e.getAttribute("name")
                self.mapEnv = e.getAttribute("envset")
                self.mapSize = e.getAttribute("size")
                #printout basic map infos
                print "loaded map ", xmlFile
                print "Name:", self.mapName
                print "Environment:", self.mapEnv
                print "Size:", self.mapSize
                
                self.loadedMapRB = RigidBodyCombiner("loadedMap")
                self.loadedMap = NodePath(self.loadedMapRB)
                self.loadedMap.reparentTo(self.mapHolder)
                
                #treating envinronment and customized
                for e in e.childNodes:
                    if e.nodeType == e.ELEMENT_NODE:
                        self.x = 0
                        self.y = 0
                        
                        #treating rows
                        for e in e.childNodes:
                            if e.nodeType == e.ELEMENT_NODE:
                                
                                #treating squares
                                for e in e.childNodes:
                                    if e.nodeType == e.ELEMENT_NODE:
                                        
                                        #treating single elements
                                        for e in e.childNodes:
                                            if e.nodeType == e.ELEMENT_NODE:
                                                eType = e.getAttribute("type")
                                                if eType != "pStart":
                                                    envElem = loader.loadModel("editor/"+self.mapEnv + "/" + eType + ".egg")
                                                    envElem.setX(self.x)
                                                    envElem.setY(self.y)
                                                    envElem.reparentTo(self.loadedMap)
                                                    self.elementList.append(envElem)
                                                else:
                                                    envElem = render.attachNewNode("Player1_start")
                                                    envElem.setX(self.x)
                                                    envElem.setY(self.y)
                                                    
                                                    self.elementList.append(envElem)
                                                    #moving for next square
                                        self.x += 2
                                self.y += 2
                                self.x = 0
        self.loadedMapRB.collect()
        
        self.start1 = render.find("**/Player1_start")
        self.army.setupStartUnits(self.start1)
        camera.setX(self.start1.getX())
        camera.setY(self.start1.getY()-7)
        
    def setupShaders(self):
        render.setShaderAuto()
        #setupfilters and shaders
        self.filters = CommonFilters(base.win, base.cam)
        self.filters.setCartoonInk(separation=1.2)
        #self.filters.setBloom(size="small")
        #render.setAttrib(LightRampAttrib.makeHdr0())