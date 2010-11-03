# -*- coding: utf-8 -*-
from panda3d.core import *
from pandac.PandaModules import *
import sys,os
from random import Random
from unit import *
from PathFind import PathFinder

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
		self.singleObject = False
		self.multipleObject = _unitList
		for unit in self.multipleObject:
			unit.showHUD(True)
		self.finder = PathFinder("maps/burning_sun/burning_sun_nav.egg")
		self.random = Random()
		self.accept('right-click-on-selection', self.go)
		
	def addUnit(self, unit):
		if unit.isOwner() and isinstance(unit, Unit):
			self.multipleObject.append(unit)
			if self.singleObject:
				self.singleObject.showHUD()
				self.singleObject = False
		elif len(self.multipleObject) == 0 and not self.singleObject:
			self.singleObject = unit
		else:
			return
		if len(self.multipleObject) > 0:
			if len(self.multipleObject) > 1:
				for unit in self.multipleObject:
					unit.showGui()
				GameObject.multipleHud.show(len(self.multipleObject))
			else:
				unit.showGui(True)
			unit.showHealthBar(True)
			unit.showSelector(True)
		else:
			unit.showHUD(True)
		
	def removeUnit(self, unit):	
		unit.showHUD()
		if unit == self.singleObject:
			self.singleOjbect = False
		else:
			self.multipleObject.remove(unit)
		
	def notifyRightClick(self):
		mySelection.notifyRightClick(True)
		
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
		return self.singleObject
		
	def emptySelection(self):
		return self.multipleObject == [] and not self.singleObject
		
	def getSingleUnit(self):
		return self.singleObject
		
	def getUnitNumber(self):
		if self.singleObject:
			return 1
		else:
			len(self.multipleObject)
		
	def go(self):
		for unit in self.multipleObject:
			''' Temporarly disabled until I check for internal coherence
			if mySelection.underMouse:
				path = self.finder.pathFindToNode(mySelection.underMouse)
			else:
			'''
			path = self.finder.pathFindToMouse(unit)
			if len(self.multipleObject) > 1:
				lastWayPoint = path[len(path)-1]
				path[len(path)-1] = Point3(lastWayPoint[0] + (self.random.random() -0.5) * 0.80, lastWayPoint[1] + (self.random.random() -0.5) * 0.80, lastWayPoint[2])
			unit.go(path)
		
	def stop(self):
		if self.singleObject:
			self.singleObject.stop()
		else:
			for unit in self.multipleObject:
				unit.stop()
			
	def clear(self):
		if self.singleObject:
			self.singleObject.showHUD()
			self.singleObject = False
		for unit in self.multipleObject:
			unit.showHUD()
		self.multipleObject = []
		mySelection.notifyLeftClick(False)
		mySelection.notifyRightClick(False)
		