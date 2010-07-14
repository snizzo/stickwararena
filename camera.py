# -*- coding: utf-8 -*-
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os

class SCamera(DirectObject.DirectObject):
    def __init__(self):
        self.scrollingSpeed = 50
        base.disableMouse()
        camera.setY(-25)
        camera.setP(15)
        self.accept('wheel_up',self.cameraZoomIn)
        self.accept('wheel_down',self.cameraZoomOut)
        taskMgr.add(self.cameraMovements,"cameraMovements")
        def cameraZoomIn(self):
            camera.setY(camera, 1)
        def cameraZoomOut(self):
            camera.setY(camera, -1)
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
            
            return task.cont