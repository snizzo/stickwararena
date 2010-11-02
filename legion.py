# -*- coding: utf-8 -*-
from panda3d.core import *
from pandac.PandaModules import *
import sys,os
from random import Random
from unit import Unit

from unit import *
'''
class Legion():
	def __init__(self, pos, color, you):
		self.you = you
		#creating main list
		self.unitList = []
		self.color = color
		self.blackMatter = 100
		self.legNode = render.attachNewNode("legions")
		self.army = Army(self.color)
		
		self.setupStartUnits(pos)
	
	def cameraOnFirstBuilding(self):
		#myCamera.placeOnUnit(self.unitList[0])
		pass
	
	def buildUnit(self, what):
		if len(mySelection.listSelected)==1:
			#if mySelection.listSelected[0].uname == "base":
			if mySelection.listSelected[0].type == "base":
				mySelection.listSelected[0].createUnit(mySelection.listSelected[0].unitType.worker)
	
	def addBM(self, amount):
		self.blackMatter += amount
		if self.you == True:
			messenger.send("res-updated")
	
	def setupStartUnits(self, start1):
		#self.addUnit("base", start1.getX(),start1.getY(),start1.getZ())
		unit = Worker(start1.getX()+5, start1.getY(), start1.getZ(), self.army)
		mySelection.listConsideration.append(unit)
		structure = Base(start1.getX(), start1.getY(), start1.getZ(), self.army)
		mySelection.listConsideration.append(structure)
	
	def addUnit(self, model, x=0, y=0, z=0):
		if model == "base":
			unit = MainBase(x, y, z, self.color, self.legNode, self)
		if model == "worker":
			unit = StickWorker(x,y,z, self.color, self.legNode, self)
			print "Worker created!"
		if self.you == True:
			mySelection.listConsideration.append(unit)
		self.unitList.append(unit)
	
	def selectNameUnits(self, uname):
		ulist = []
		for unit in self.unitList:
			if unit.uname == uname:
				ulist.append(unit)
		return ulist
	
	def removeUnit(self, unit):
		self.unitList.remove(unit)
		unit.remove()
	
	#function that i use to remove all my RTS's units from the main units list.
	def remove(self):
		for unit in self.unitList[:]:
			unit.remove()
			self.unitList.remove(unit)
		self.legNode.remove()
'''

#fuckin' OOP
class Army():
	def __init__(self, startUpPos, _color, _player):
		self.unitList = []
		self.structureList = []
		self.blackMatter = 200
		self.color = _color
		self.player = _player
		self.node = render.attachNewNode("army")
		self.addStructure(Base(startUpPos.getX(), startUpPos.getY(), startUpPos.getZ(), self))
		
	def getNode(self):
		return self.node
		
	def getColor(self):
		return self.color
		
	def getIsPlayer(self):
		return self.player
		
	def getUnitAt(self, i):
		return self.unitList[i]
		
	def getStructureAt(self, i):
		return self.structureList[i]
		
	def addUnit(self, unit):
		self.unitList.append(unit)
		mySelection.listConsideration.append(unit)
		
	def removeUnitAt(self, i):
		unit = self.unitList.pop(i)
		mySelection.listConsideration.remove(unit)
		unit.destroy()
		
	def removeUnit(self, unit):
		self.unitList.remove(unit)
		mySelection.listConsideration.remove(unit)
		unit.destroy()
		
	def addStructure(self, structure):
		self.structureList.append(structure)
		mySelection.listConsideration.append(structure)
		
	def removeStructureAt(self, i):
		structure = self.structureList.pop(i)
		mySelection.listConsideration.remove(structure)
		structure.destroy()
		
	def removeStructure(self, structure):
		self.structureList.remove(structure)
		mySelection.listConsideration.remove(structure)
		structure.destroy()
		
	def alterBlackMatter(self, amount):
		self.blackMatter += amount
		
	def remove(self):
		for unit in self.unitList:
			unit.destroy()
		for structure in self.structureList:
			structure.destroy()
		self.unitList = []
		self.structureList = []
		self.node.remove()
		
	
class Group(DirectObject):
	def __init__(self, _unitList = []):
		#self.unitList = _unitList
		self.singleObject = False
		self.multipleObject = _unitList
		for unit in self.multipleObject:
			unit.showHUD(True)
		self.finder = PathFinder("maps/burning_sun/burning_sun_nav.egg")
		self.random = Random()
		self.accept('right-click-on-selection', self.go)
		
	def addUnit(self, unit):
		#self.unitList.append(unit)
		if unit.isOwner() and isinstance(unit, Unit):
			self.multipleObject.append(unit)
			#print "append " + str(unit) + " to multiple"
			if self.singleObject:
				#print "remove " + str(self.singleObject) + " from single"
				self.singleObject.showHUD()
				self.singleObject = False
				#print "remove " + str(unit) + " to multiple"
		elif len(self.multipleObject) == 0 and not self.singleObject:
			self.singleObject = unit
			#print "append " + str(unit) + " to single"
		else:
			return
		unit.showHUD(True)
		
	def removeUnit(self, unit):	
		unit.showHUD()
		#self.unitList.remove(unit)
		if unit == self.singleObject:
			#print "remove " + str(unit) + " from single"
			self.singleOjbect = False
		else:
			#print "remove " + str(unit) + " from multiple"
			self.multipleObject.remove(unit)
		
	def notifyRightClick(self):
		mySelection.notifyRightClick(True)
		print "notify requested"
		
	def notifyLeftClick(self):
		mySelection.notifyLeftClick(True)
		
	def abortLeftClickNotify(self):
		mySelection.notifyLeftClick(False)
	
	def abortRightClickNotify(self):
		mySelection.notifyRightClick(False)
		
	def leftButtonPressed(self):
		if self.singleObject:
			self.singleObject.leftButtonNotify()
		else:
			for unit in self.multipleObject:
				unit.leftButtonNotify()
		
	def rightButtonPressed(self):
		if self.singleObject:
			self.singleObject.rightButtonNotify()
		else:
			for unit in self.multipleObject:
				unit.rightButtonNotify()
		
	def singleUnit(self):
		#return len(self.unitList) == 1
		return self.singleObject
		
	def emptySelection(self):
		#return self.unitList == []
		return self.multipleObject == [] and not self.singleObject
		
	def getSingleUnit(self):
		#return self.unitList[0]
		return self.singleObject
		
	def getUnitNumber(self):
		#return len(self.unitList)
		if self.singleObject:
			return 1
		else:
			len(self.multipleObject)
		
	def go(self):
		#for unit in self.unitList:
		for unit in self.multipleObject:
			''' Temporarly disabled until I check for internal coherence
			if mySelection.underMouse):
				path = self.finder.pathFindToNode(mySelection.underMouse)
			else:
			'''
			path = self.finder.pathFindToMouse(unit)
			#if len(self.unitList) > 1:
			if len(self.multipleObject) > 1:
				lastWayPoint = path[len(path)-1]
				path[len(path)-1] = Point3(lastWayPoint[0] + (self.random.random() -0.5) * 0.80, lastWayPoint[1] + (self.random.random() -0.5) * 0.80, lastWayPoint[2])
			unit.go(path)
		
	def stop(self):
		#for unit in self.unitList:
		#	unit.stop()
		if self.singleObject:
			self.singleObject.stop()
		else:
			for unit in self.multipleObject:
				unit.stop()
			
	def clear(self):
		#for unit in self.unitList:
		#	unit.showHUD()
		#self.unitList = []
		if self.singleObject:
			#print "remove " + str(self.singleObject) + " from single"
			self.singleObject.showHUD()
			self.singleObject = False
		for unit in self.multipleObject:
			unit.showHUD()
			#print "remove " + str(unit) + " from multiple"
		self.multipleObject = []
		mySelection.notifyLeftClick(False)
		mySelection.notifyRightClick(False)
		