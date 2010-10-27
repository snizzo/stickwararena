# -*- coding: utf-8 -*-
from panda3d.core import *
from pandac.PandaModules import *
import sys,os

from unit import *

class Legion():
	def __init__(self, pos, color, you):
		self.you = you
		#creating main list
		self.unitList = []
		self.color = color
		self.blackMatter = 100
		self.legNode = render.attachNewNode("legions")
		
		self.setupStartUnits(pos)
	
	def cameraOnFirstBuilding(self):
		myCamera.placeOnUnit(self.unitList[0])
	
	def buildUnit(self, what):
		if len(mySelection.listSelected)==1:
			if mySelection.listSelected[0].uname == "base":
				obj = mySelection.listSelected[0]
				obj.buildUnit(what)
	
	def addBM(self, amount):
		self.blackMatter += amount
		if self.you == True:
			messenger.send("res-updated")
	
	def setupStartUnits(self, start1):
		self.addUnit("base", start1.getX(),start1.getY(),start1.getZ())
	
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
		print "legion.remove() called"
		for unit in self.unitList[:]:
			unit.remove()
			self.unitList.remove(unit)
		self.legNode.remove()


#fuckin' OOP
class Army():
	def __init__(self, _color):
		self.unitList = []
		self.structureList = []
		self.blackMatter = 0
		self.color = _color
		
	def addUnit(self, unit):
		self.unitList.append(unit)
		
	def removeUnitAt(self, i):
		self.unitList.pop(i)
		
	def removeUnit(self, unit):
		self.unitList.remove(unit)
		
	def addStructure(self, structure):
		self.structureList.append(structure)
		
	def removeStructureAt(self, i):
		self.structureList.pop(i)
		
	def removeStructure(self, structure):
		self.structureList.remove(structure)
		
	def addBlackMatter(self, amount):
		self.blackMatter += amount
		
	
class Group():
	def __init__(self, _unitList):
		self.unitList = _unitList
		
	def go(self, wayList):
		for unit in self.unitList:
			unit.go(wayList)
			
