# -*- coding: utf-8 -*-

#dichiarazioni di panda3d
import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task
import sys,os
import xml.dom.minidom

from direct.showbase.DirectObject import DirectObject

#fullscreen e grandezza finestra
loadPrcFileData("", """fullscreen 1
win-size 1024 768
text-encoding utf8""")

class MapEditor(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        ###impostazioni iniziali
        self.elementList = []
        #gui, map, camera and other managements
        #self.myGui = gui.Gui()
        self.accept("escape", self.exitGame)
        self.ambLight()
        self.loadMap("experimental.swm")
    
    def loadMap(self, xmlFile):
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
                self.loadedMap.reparentTo(render)
                
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
                                                    envElem = loader.loadModel(self.mapEnv + "/" + eType + ".egg")
                                                    envElem.setX(self.x)
                                                    envElem.setY(self.y)
                                                    envElem.reparentTo(render)
                                                    self.elementList.append(envElem)
                                                else:
                                                    envElem = render.attachNewNode("pStart")
                                                    envElem.setX(self.x)
                                                    envElem.setY(self.y)
                                                    self.elementList.append(envElem)
                                                #moving for next square
                                        self.x += 2
                                self.y += 2
                                self.x = 0
        self.loadedMapRB.collect()
    
    def ambLight(self):
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.8, 0.8, 0.8, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)
        
    def exitGame(self):
        print self.elementList
        sys.exit()


app = MapEditor()
from camera import *
app.run()
