# -*- coding: utf-8 -*-
from panda3d.core import *
from pandac.PandaModules import *
import sys,os
from random import Random

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
		
	def addBlackMatter(self, amount):
		self.blackMatter += amount
		
	def remove(self):
		for unit in self.unitList:
			unit.destroy()
		for structure in self.structureList:
			structure.destroy()
		self.unitList = []
		self.structureList = []
		self.node.remove()
		
	
class Group():
	def __init__(self, _unitList = []):
		self.unitList = _unitList
		for unit in self.unitList:
			unit.showHUD()
		self.finder = PathFinder("maps/burning_sun/burning_sun_nav.egg")
		self.random = Random()
		base.accept('right-click-on-selection', self.go)
		
	def addUnit(self, unit):
		unit.showHUD(True)
		self.unitList.append(unit)
		
	def removeUnit(self, unit):	
		unit.showHUD()
		self.unitList.remove(unit)
		
	def singleUnit(self):
		return len(self.unitList) == 1
		
	def emptySelection(self):
		return self.unitList == []
		
	def getSingleUnit(self):
		return self.unitList[0]
		
	def getUnitNumber(self):
		return len(self.unitList)
		
	def go(self):
		for unit in self.unitList:
			''' Temporarly disabled until I check for internal coherence
			if mySelection.underMouse):
				path = self.finder.pathFindToNode(mySelection.underMouse)
			else:
			'''
			path = self.finder.pathFindToMouse()
			lastWayPoint = path[len(path)-1]
			if len(self.unitList) > 1:
				path[len(path)-1] = Point3(lastWayPoint[0] + (self.random.random() -0.5) * 0.80, lastWayPoint[1] + (self.random.random() -0.5) * 0.80, lastWayPoint[2])
			unit.go(path)
		
	def stop(self):
		for unit in self.unitList:
			unit.stop()
			
	def clear(self):
		for unit in self.unitList:
			unit.showHUD()
		self.unitList = []
		