# -*- coding: utf-8 -*-

from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import sys,os, math
import __builtin__
#from direct.showbase import DirectObject
from direct.task import Task
import libpanda
from NavCollide import MouseCollider, GroundCollider

import math

class Mouse:
	
	mc = MouseCollider()
	gc = GroundCollider()
	
	@staticmethod
	def queryMousePosition():
		mcc = Mouse.mc.collide()
		if Mouse.mc.hasMouse() and mcc != None:
			return Mouse.gc.collide(mcc + Vec3(0.0, 0.0, 0.5))
		else:
			return False
		
	@staticmethod
	def queryScreenMousePosition():
		if base.mouseWatcherNode.hasMouse():
			return base.mouseWatcherNode.getMouse()
		else:
			return False


class Camera():
	def __init__(self):
		self.scrollingSpeed = 18
		self.cameraMovementBorder = 0.92
		base.disableMouse()
		camera.setP(-70)
		camera.setZ(15)
		base.accept('wheel_up',self.cameraZoomIn)
		base.accept('wheel_down',self.cameraZoomOut)
		taskMgr.add(self.cameraMovements,"cameraMovements")
		
		self.cameraLightNode = PointLight("cameraLight")
		self.cameraLightNode.setColor(Vec4(1,1,1,1))
		self.cameraLight = render.attachNewNode(self.cameraLightNode)
		render.setLight(self.cameraLight)
		
		#fullscreen toggle
		self.full = False
		self.displayModes = []
		self.getSupportedDisplayRes()
		
		base.accept("f", self.toggleFullscreen)
		
	def setPosition(self, x, y):
		camera.setX(x)
		camera.setY(y - 6)
	
	def getSupportedDisplayRes(self):
		di = base.pipe.getDisplayInformation()
		wp = WindowProperties()
		for index in range(di.getTotalDisplayModes()):
			if abs(float(di.getDisplayModeWidth(index)) / float(di.getDisplayModeHeight(index)) - (16. / 9.)) < 0.001:
				self.displayModes.append([di.getDisplayModeWidth(index), di.getDisplayModeHeight(index)]) 
	
	def setFullscreen(self,bool):
		wp = WindowProperties()
		if bool == False:
			wp.setSize(self.displayModes[0][0], self.displayModes[0][1])
			wp.setFullscreen(False)
			self.full = False
		else:
			wp.setSize(self.displayModes[len(self.displayModes) - 1][0], self.displayModes[len(self.displayModes) - 1][1])
			wp.setFullscreen(True)
			self.full = True
		base.win.requestProperties(wp)
	
	def toggleFullscreen(self):
		wp = WindowProperties()
		if self.full:
			wp.setSize(self.displayModes[0][0], self.displayModes[0][1])
			wp.setFullscreen(False)
			self.full = False
		else:
			wp.setSize(self.displayModes[len(self.displayModes) - 1][0], self.displayModes[len(self.displayModes) - 1][1])
			wp.setFullscreen(True)
			self.full = True
		base.win.requestProperties(wp)
	
	def cameraZoomIn(self):
		if camera.getZ() > 10:
			camera.setY(camera, 1)
			
	def cameraZoomOut(self):
		if camera.getZ() < 70:
			camera.setY(camera, -1)
			
	def cameraMovements(self, task):
		#if base.mouseWatcherNode.hasMouse() and not mySelection.booSelecting:
		if base.mouseWatcherNode.hasMouse():
			x = base.mouseWatcherNode.getMouseX()
			y = base.mouseWatcherNode.getMouseY()
			
			self.dt = globalClock.getDt() * self.scrollingSpeed
			if x < -self.cameraMovementBorder:
				camera.setX(camera.getX()-self.dt)
				
			if x > self.cameraMovementBorder:
				camera.setX(camera.getX()+self.dt)
				
			if y > self.cameraMovementBorder:
				camera.setY(camera.getY()+self.dt)
				
			if y < -self.cameraMovementBorder:
				camera.setY(camera.getY()-self.dt)
			
			self.cameraLight.setX(camera.getX())
			self.cameraLight.setY(camera.getY())
			self.cameraLight.setZ(camera.getZ())
		
		return task.cont
	
	def placeOnUnit(self,unit): 
		x = unit.node.getX(render)
		y = unit.node.getY(render)
		
		base.camera.setX(x)
		base.camera.setY(y-6)
		
 
class clSelectionTool(): 
	def __init__(self):
		#used to define an active behaviour or less
		self.active = True
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
		self.listConsideration = []
		#right click selection
		self.underMouse = False
		
		self._notifyRightClick = False
		self._notifyLeftClick = False
		 
		self.pt2InitialMousePos = (-12, -12) 
		self.pt2LastMousePos = (-12, -12) 
		
		self.fFovh, self.fFovv = base.camLens.getFov() 
		 
		####--Used to control how frequently update_rect is updated; 
		self.fTimeLastUpdateSelRect = 0 
		self.fTimeLastUpdateSelected = 0 
		self.UpdateTimeSelRect = 0.015 
		self.UpdateTimeSelected = 0.015 
		 
		####------Register the left-mouse-button to start selecting
		base.accept("mouse1", self.onStartSelect)
		base.accept("mouse1-up", self.OnStopSelect)
		base.accept("mouse3-up", self.OnRightClick) 
		
		self.taskUpdateSelRect = 0 
		
		####------otherThings
		self.booSelecting = False
	
	def notifyRightClick(self, bool):
		#print "right click " + str(bool)
		self._notifyRightClick = bool
		
	def notifyLeftClick(self, bool):
		#print "left click " + str(bool)
		self._notifyLeftClick = bool
	
	def clear(self):
		self.listConsideration = []
		myGroup.clear()
	
	def setIdle(self):
		self.active = False
		
	def setActive(self):
		self.active = True
	
	def onStartSelect(self):
		if not self.active:
			return
		if not base.mouseWatcherNode.hasMouse(): 
			return 
		y = base.mouseWatcherNode.getMouseY()
		if y < -0.5:
			return
		myGroup.clear()
		self.booMouseMoved = False 
		self.booSelecting = True 
		self.pt2InitialMousePos = Point2(base.mouseWatcherNode.getMouse()) 
		self.pt2LastMousePos = Point2(self.pt2InitialMousePos)
		self.npSelRect.setPos(self.pt2InitialMousePos[0], 1, self.pt2InitialMousePos[1]) 
		self.npSelRect.setScale(1e-3, 1, 1e-3) 
		self.npSelRect.show() 
		self.taskUpdateSelRect = taskMgr.add(self.UpdateSelRect, "UpdateSelRect") 
		#self.taskUpdateSelRect.lastMpos = None 
		
	def OnStopSelect(self):
		if not self.active:
			return
		if not base.mouseWatcherNode.hasMouse(): 
			return 
		if self.taskUpdateSelRect:
			taskMgr.remove(self.taskUpdateSelRect) 
		self.npSelRect.hide() 
		self.booSelecting = False 
		#If the mouse hasn't moved, it's a point selection 
		if (abs(self.pt2InitialMousePos[0] - self.pt2LastMousePos[0]) <= .01) & (abs(self.pt2InitialMousePos[1] - self.pt2LastMousePos[1]) <= .01): 
			objTempSelected = 0 
			fTempObjDist = 2*(base.camLens.getFar())**2		
			for i in self.listConsideration:
				sphBounds = i.node.getBounds()
				p3 = base.cam.getRelativePoint(i.node.getParent(), sphBounds.getCenter()) 
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
				if self._notifyLeftClick:
					myGroup.leftButtonPressed()
					self._notifyLeftClick = False
					#print "left click != 0"
					self._notifyRightClick = False
				else:
					myGroup.clear()
					myGroup.addUnit(objTempSelected)
			#if nothing is selected just deselect all, a normal behaviour in RTS's game
			y = base.mouseWatcherNode.getMouseY()
			if y < -0.5:
				return
			if objTempSelected == 0:
				if self._notifyLeftClick:
					myGroup.leftButtonPressed()
					#print "left click == 0"
					self._notifyLeftClick = False
					self._notifyRightClick = False
				else:
					myGroup.clear()
		if self._notifyLeftClick:
			myGroup.leftButtonPressed()
			#print "left click == 0"
			self._notifyLeftClick = False
			self._notifyRightClick = False
		#messenger.send("mouse-selection")
	
	def OnRightClick(self):
		if not self.active:
			return
		if not base.mouseWatcherNode.hasMouse(): 
			return 
		if self.taskUpdateSelRect != 0: 
			taskMgr.remove(self.taskUpdateSelRect) 
		self.npSelRect.hide() 
		self.booSelecting = False 
		#clearing list
		self.underMouse = False
		#If the mouse hasn't moved, it's a point selection 
		if (abs(self.pt2InitialMousePos[0] - self.pt2LastMousePos[0]) <= .01) & (abs(self.pt2InitialMousePos[1] - self.pt2LastMousePos[1]) <= .01): 
			objTempSelected = 0 
			fTempObjDist = 2*(base.camLens.getFar())**2 
			for i in self.listConsideration: 
				sphBounds = i.node.getBounds()
				p3 = base.cam.getRelativePoint(i.node.getParent(), sphBounds.getCenter()) 
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
				self.underMouse = objTempSelected
			#avoid pressing mouse in HUD
			y = base.mouseWatcherNode.getMouseY()
			if y < -0.5:
				return
			#returning object under mouse
		if self._notifyRightClick:
			myGroup.rightButtonPressed()
			#print "right click"
			self._notifyRightClick = False
			self._notifyLeftClick = False
		else:
			messenger.send("right-click-on-selection")	
	
	def UpdateSelRect(self, task): 
		if not self.active:
			return
		#Make sure we have the mouse 
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
				myGroup.clear()
				#Get the bounds of the selection box 
				fMouse_Lx = min(self.pt2InitialMousePos[0], self.pt2LastMousePos[0]) 
				fMouse_Ly = max(self.pt2InitialMousePos[1], self.pt2LastMousePos[1]) 
				fMouse_Rx = max(self.pt2InitialMousePos[0], self.pt2LastMousePos[0]) 
				fMouse_Ry = min(self.pt2InitialMousePos[1], self.pt2LastMousePos[1])
				for i in self.listConsideration: 
					#Get the loosebounds of the nodepath 
					sphBounds = i.node.getBounds() 
					#Put the center of the sphere into the camera coordinate system
					p3 = base.cam.getRelativePoint(i.node.getParent(), sphBounds.getCenter()) 
					#Check if p3 is in the view fustrum 
					p2 = Point2() 
					if base.camLens.project(p3, p2): 
						if (p2[0] >= fMouse_Lx) & (p2[0] <= fMouse_Rx) & (p2[1] >= fMouse_Ry) & (p2[1] <= fMouse_Ly):
							myGroup.addUnit(i)
		return Task.cont
	

class SelectionTool(DirectObject):

	updateTime = 0.015
	NO_SELECTION = 0
	CLICK_SELECTION = 1
	SELECTION = 2

	def __init__(self):
		self.selectionType = SelectionTool.NO_SELECTION
		self._notifySelection = False
		self.selectableUnit = []
		self.selectionUpdateTask = False
		
		cm = CardMaker('')
		cm.setFrame(0, 1, 0, 1)
		self.selectionRect = render2d.attachNewNode(cm.generate())
		self.selectionRect.setColor(0.5, 1, 0, 0.3) 
		self.selectionRect.setTransparency(1)
		self.selectionRect.hide()
		
		ls = LineSegs() 
		ls.setColor(0.5,1,0,1)
		ls.moveTo(0,0,0) 
		ls.drawTo(1,0,0) 
		ls.drawTo(1,0,1) 
		ls.drawTo(0,0,1) 
		ls.drawTo(0,0,0) 
		self.selectionRect.attachNewNode(ls.create())
		
		self.mousePos = False
		self.oldMousePos = False
		
		self.accept("mouse1", self.startSelection)
		self.accept("mouse1-up", self.stopSelection)
		self.accept("mouse3-up", self.rightSelection)
		
	def notifySelection(self, bool = False):
		self._notifySelection = bool
		
	def addSelectableUnit(self, unit):
		#if isinstance(unit, GameObject):
		self.selectableUnit.append(unit)
			
	def removeSelectableUnit(self, unit):
		if unit in self.selectableUnit:
			self.selectableUnit.remove(unit)
			
	def clear(self):
		self.selectableUnit = []
		
	def hasMouse(self):
		return base.mouseWatcherNode.hasMouse()
		
	def startSelection(self):
		self.mousePos = Mouse.queryScreenMousePosition()
		if not self.hasMouse() or self.selectionType != SelectionTool.NO_SELECTION or not self.mousePos:
			return
		self.selectionType = SelectionTool.CLICK_SELECTION
		self.oldMousePos = Point2(self.mousePos)
		if not self._notifySelection:
			self.selectionRect.setPos(self.mousePos[0], 1, self.mousePos[1])
			self.selectionRect.setScale(1e-3, 1, 1e-3)
			self.selectionType = SelectionTool.SELECTION
			self.selectionRect.show()
			self.selectionUpdateTask = taskMgr.add(self.updateSelection, "updateSel")
		
	def updateSelection(self, task):
		self.mousePos = Mouse.queryScreenMousePosition()
		if not self.hasMouse() or not self.mousePos:
			return task.cont
		mouseDiff = self.mousePos - self.oldMousePos
		self.selectionRect.setScale(mouseDiff[0] if mouseDiff[0] else 1e-3, 1, mouseDiff[1] if mouseDiff[1] else 1e-3)
		if abs(mouseDiff[0]) > 0.1 and abs(mouseDiff[1]) > 0.1:
			myGroup.clear()
			fMouse_Lx = min(self.oldMousePos[0], self.mousePos[0]) 
			fMouse_Ly = max(self.oldMousePos[1], self.mousePos[1]) 
			fMouse_Rx = max(self.oldMousePos[0], self.mousePos[0]) 
			fMouse_Ry = min(self.oldMousePos[1], self.mousePos[1])
			for unit in self.selectableUnit:
				camProj = base.cam.getRelativePoint(unit.getNode().getParent(), unit.getNode().getBounds().getCenter())
				screenProj = Point2()
				if base.camLens.project(camProj, screenProj):
					if screenProj[0] >= fMouse_Lx and screenProj[0] <= fMouse_Rx and screenProj[1] >= fMouse_Ry and screenProj[1] <= fMouse_Ly:
						myGroup.addUnit(unit)
		return task.cont
		
	def stopSelection(self):
		if self.selectionUpdateTask:
			self.selectionUpdateTask.remove()
			self.selectionUpdateTask = False
			self.selectionRect.hide()
		self.mousePos = Mouse.queryScreenMousePosition()
		if not self.hasMouse() or not self.mousePos:
			self.selectionType = SelectionTool.NO_SELECTION
			return
		if self.selectionType == SelectionTool.CLICK_SELECTION or self.selectionType == SelectionTool.SELECTION:
			self.selectionType = SelectionTool.NO_SELECTION
			if self._notifySelection:
				myGroup.leftButtonPressed()
				return
			mouseDiff = self.mousePos - self.oldMousePos
			if abs(mouseDiff[0]) < 0.1 and abs(mouseDiff[1]) < 0.1:
				for unit in self.selectableUnit:
					unitBBRadius = unit.getNode().getBounds().getRadius()
					x, y, z = base.cam.getRelativePoint(unit.getNode().getParent(), unit.getNode().getBounds().getCenter())
					distance = math.sqrt(x**2 + y**2 + z**2)
					print str(distance)
					print str(unitBBRadius)
					if distance - unitBBRadius < 0:
						myGroup.clear()
						myGroup.addUnit(unit)
						return
				myGroup.clear()
			return
		
	def rightSelection(self):
		if self._notifySelection:
			myGroup.rightButtonPressed()
			return
		myGroup.go()
