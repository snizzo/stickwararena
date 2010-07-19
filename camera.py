# -*- coding: utf-8 -*-
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

class Camera(DirectObject.DirectObject):
    def __init__(self):
        self.scrollingSpeed = 25
        base.disableMouse()
        camera.setP(-90)
        camera.setZ(30)
        self.accept('wheel_up',self.cameraZoomIn)
        self.accept('wheel_down',self.cameraZoomOut)
        taskMgr.add(self.cameraMovements,"cameraMovements")
        
        self.cameraLightNode = PointLight("cameraLight")
        self.cameraLightNode.setColor(Vec4(1,1,1,1))
        self.cameraLight = render.attachNewNode(self.cameraLightNode)
        render.setLight(self.cameraLight)
        
    def cameraZoomIn(self):
        camera.setY(camera, 2)
    def cameraZoomOut(self):
        camera.setY(camera, -2)
    def cameraMovements(self, task):
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
            self.dt = globalClock.getDt() * self.scrollingSpeed
            if x < -0.97:
                camera.setX(camera, -self.dt)
            if x > 0.97:
                camera.setX(camera, self.dt)
            if y > 0.97:
                camera.setZ(camera, self.dt)
            if y < -0.97:
                camera.setZ(camera, -self.dt)
            
            self.cameraLight.setX(camera.getX())
            self.cameraLight.setY(camera.getY())
            self.cameraLight.setZ(camera.getZ())
        
        return task.cont