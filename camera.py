# -*- coding: utf-8 -*-

from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase import *
import sys,os
import __builtin__
#from direct.showbase import DirectObject
from direct.task import Task
import libpanda
from pandac.PandaModules import Vec4, CardMaker, LineSegs, Point2, Point3, PointLight

import math

class Camera(DirectObject.DirectObject):
    def __init__(self):
        
        self.scrollingSpeed = 25
        base.disableMouse()
        camera.setP(-70)
        camera.setZ(15)
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
        if base.mouseWatcherNode.hasMouse() and not objSelectionTool.booSelecting:
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
            self.dt = globalClock.getDt() * self.scrollingSpeed
            if x < -0.99:
                camera.setX(camera.getX()-self.dt)
            if x > 0.99:
                camera.setX(camera.getX()+self.dt)
            if y > 0.99:
                camera.setY(camera.getY()+self.dt)
            if y < -0.99:
                camera.setY(camera.getY()-self.dt)
            
            self.cameraLight.setX(camera.getX())
            self.cameraLight.setY(camera.getY())
            self.cameraLight.setZ(camera.getZ())
        
        return task.cont
        

class clKeyBoardModifiers(DirectObject.DirectObject): 
    def __init__(self): 
        self.booAlt = False 
        self.booControl = False 
        self.booShift = False 
        self.accept("alt", self.OnAltDown) 
        self.accept("alt-up", self.OnAltUp) 
        self.accept("control", self.OnControlDown) 
        self.accept("control-up", self.OnControlUp) 
        self.accept("shift", self.OnShiftDown) 
        self.accept("shift-up", self.OnShiftUp) 
     
    def OnAltDown(self): 
        self.booAlt = True 
         
    def OnAltUp(self): 
        self.booAlt = False 
         
    def OnControlDown(self): 
        self.booControl = True 
     
    def OnControlUp(self): 
        self.booControl = False 
         
    def OnShiftDown(self): 
        self.booShift = True 
         
    def OnShiftUp(self): 
        self.booShift = False 
         
class clSelectionTool(DirectObject.DirectObject): 
    def __init__(self, listConsideration=[]): 
        #Create a selection window using cardmaker 
        #We will use the setScale function to dynamically scale the quad to the appropriate size in UpdateSelRect 
        temp = CardMaker('') 
        temp.setFrame(0, 1, 0, 1) 
        #self.npSelRect is the actual selection rectangle that we dynamically hide/unhide and change size 
        self.npSelRect = render2d.attachNewNode(temp.generate()) 
        self.npSelRect.setColor(0.5,1,0,.3) 
        self.npSelRect.setTransparency(1) 
        self.npSelRect.hide() 
        LS = LineSegs() 
        LS.setColor(0.5,1,0,1)
        LS.moveTo(0,0,0) 
        LS.drawTo(1,0,0) 
        LS.drawTo(1,0,1) 
        LS.drawTo(0,0,1) 
        LS.drawTo(0,0,0) 
        self.npSelRect.attachNewNode(LS.create()) 
        self.listConsideration = listConsideration 
        self.listSelected = [] 
        self.listLastSelected = [] 
         
        self.pt2InitialMousePos = (-12, -12) 
        self.pt2LastMousePos = (-12, -12) 
         
        ####----Used to differentiate between group selections and point selections 
        #self.booMouseMoved  = False 
        self.fFovh, self.fFovv = base.camLens.getFov() 
         
        ####--Used to control how frequently update_rect is updated; 
        self.fTimeLastUpdateSelRect = 0 
        self.fTimeLastUpdateSelected = 0 
        self.UpdateTimeSelRect = 0.015 
        self.UpdateTimeSelected = 0.015 
         
        ####------Register the left-mouse-button to start selecting 
        self.accept("mouse1", self.OnStartSelect) 
        self.accept("control-mouse1", self.OnStartSelect) 
        self.accept("mouse1-up", self.OnStopSelect) 
        self.taskUpdateSelRect = 0 
        
        ####------otherThings
        self.booSelecting = False
        
    def TTest(self): 
        print "hello control-mouse1" 
    def funcSelectActionOnObject(self, obj): 
        otherThings = obj.find("**/otherThings")
        otherThings.show()
         
    def funcDeselectActionOnObject(self, obj): 
        otherThings = obj.find("**/otherThings")
        otherThings.hide()
         
    def OnStartSelect(self): 
        if not base.mouseWatcherNode.hasMouse(): 
            return 
        self.booMouseMoved = False 
        self.booSelecting = True 
        self.pt2InitialMousePos = Point2(base.mouseWatcherNode.getMouse()) 
        self.pt2LastMousePos = Point2(self.pt2InitialMousePos) 
        self.npSelRect.setPos(self.pt2InitialMousePos[0], 1, self.pt2InitialMousePos[1]) 
        self.npSelRect.setScale(1e-3, 1, 1e-3) 
        self.npSelRect.show() 
        self.taskUpdateSelRect = taskMgr.add(self.UpdateSelRect, "UpdateSelRect") 
        self.taskUpdateSelRect.lastMpos = None 
         
    def OnStopSelect(self): 
        if not base.mouseWatcherNode.hasMouse(): 
            return 
        if self.taskUpdateSelRect != 0: 
            taskMgr.remove(self.taskUpdateSelRect) 
        self.npSelRect.hide() 
        self.booSelecting = False 
        #If the mouse hasn't moved, it's a point selection 
        if (abs(self.pt2InitialMousePos[0] - self.pt2LastMousePos[0]) <= .01) & (abs(self.pt2InitialMousePos[1] - self.pt2LastMousePos[1]) <= .01): 
            objTempSelected = 0 
            fTempObjDist = 2*(base.camLens.getFar())**2 
            for i in self.listConsideration: 
                if type(i) != libpanda.NodePath: 
                    raise 'Unknown objtype in selection' 
                else:
                    sphBounds = i.getBounds() 
                    #p3 = base.cam.getRelativePoint(render, sphBounds.getCenter()) 
                    p3 = base.cam.getRelativePoint(i.getParent(), sphBounds.getCenter()) 
                    r = sphBounds.getRadius() 
                    screen_width = r/(p3[1]*math.tan(math.radians(self.fFovh/2))) 
                    screen_height = r/(p3[1]*math.tan(math.radians(self.fFovv/2))) 
                    p2 = Point2() 
                    base.camLens.project(p3, p2) 
                    #If the mouse pointer is in the "roughly" screen-projected bounding volume 
                    if (self.pt2InitialMousePos[0] >= (p2[0] - screen_width/2)): 
                        if (self.pt2InitialMousePos[0] <= (p2[0] + screen_width/2)): 
                            if (self.pt2InitialMousePos[1] >= (p2[1] - screen_height/2)): 
                                if (self.pt2InitialMousePos[1] <= (p2[1] + screen_height/2)):
                                    #We check the obj's distance to the camera and choose the closest one 
                                    dist = p3[0]**2+p3[1]**2+p3[2]**2 - r**2 
                                    if dist < fTempObjDist: 
                                        fTempObjDist = dist 
                                        objTempSelected = i 
            #if something is click-selected
            if objTempSelected != 0: 
                if objKeyBoardModifiers.booControl: 
                    self.listSelected.append(objTempSelected) 
                else: 
                    for i in self.listSelected: 
                        self.funcDeselectActionOnObject(i) 
                    self.listSelected = [objTempSelected] 
                self.funcSelectActionOnObject(objTempSelected) 
            #if nothing is selected just deselect all, a normal behaviour in RTS's game
            if objTempSelected == 0:
                for i in self.listSelected:
                    self.funcDeselectActionOnObject(i)
                    self.listSelected = []
        messenger.send("mouse-selection")
    
    def UpdateSelRect(self, task): 
        #Make sure we hae the mouse 
        if not base.mouseWatcherNode.hasMouse(): 
            return Task.cont 
        mpos = base.mouseWatcherNode.getMouse() 
        t = globalClock.getRealTime() 
        #First check the mouse position is different 
        if self.pt2LastMousePos != mpos: 
            self.booMouseMoved = True 
            #We only need to check this function every once in a while 
            if (t - self.fTimeLastUpdateSelRect) > self.UpdateTimeSelRect: 
                self.fTimeLastUpdateSelRect =  t 
                self.pt2LastMousePos = Point2(mpos) 
                     
                #Update the selection rectange graphically 
                d = self.pt2LastMousePos - self.pt2InitialMousePos 
                self.npSelRect.setScale(d[0] if d[0] else 1e-3, 1, d[1] if d[1] else 1e-3) 
                
        if (abs(self.pt2InitialMousePos[0] - self.pt2LastMousePos[0]) > .01) & (abs(self.pt2InitialMousePos[1] - self.pt2LastMousePos[1]) > .01): 
            if (t - self.fTimeLastUpdateSelected) > self.UpdateTimeSelected: 
                #A better way to handle a large number of objects is to first transform the 2-d selection rect into 
                #its own view fustrum and then check the objects in world space. Adding space correlation/hashing 
                #will make it go faster. But I'm lazy. 
                self.fTimeLastUpdateSelected = t 
                self.listLastSelected = self.listSelected 
                self.listSelected = [] 
                #Get the bounds of the selection box 
                fMouse_Lx = min(self.pt2InitialMousePos[0], self.pt2LastMousePos[0]) 
                fMouse_Ly = max(self.pt2InitialMousePos[1], self.pt2LastMousePos[1]) 
                fMouse_Rx = max(self.pt2InitialMousePos[0], self.pt2LastMousePos[0]) 
                fMouse_Ry = min(self.pt2InitialMousePos[1], self.pt2LastMousePos[1]) 
                for i in self.listConsideration: 
                    if type(i) != libpanda.NodePath: 
                        raise 'Unknown objtype in selection' 
                    else: 
                        #Get the loosebounds of the nodepath 
                        sphBounds = i.getBounds() 
                        #Put the center of the sphere into the camera coordinate system 
                        #p3 = base.cam.getRelativePoint(render, sphBounds.getCenter()) 
                        p3 = base.cam.getRelativePoint(i.getParent(), sphBounds.getCenter()) 
                        #Check if p3 is in the view fustrum 
                        p2 = Point2() 
                        if base.camLens.project(p3, p2): 
                            if (p2[0] >= fMouse_Lx) & (p2[0] <= fMouse_Rx) & (p2[1] >= fMouse_Ry) & (p2[1] <= fMouse_Ly): 
                                self.listSelected.append(i) 
                                self.funcSelectActionOnObject(i) 
                for i in self.listLastSelected: 
                    if not objKeyBoardModifiers.booControl: 
                        if i not in self.listSelected: 
                            self.funcDeselectActionOnObject(i) 
                            pass
                    else: 
                        self.listSelected.append(i) 
        
        return Task.cont 
        
__builtin__.myCamera = Camera()
__builtin__.objKeyBoardModifiers = clKeyBoardModifiers()
__builtin__.objSelectionTool = clSelectionTool() 

