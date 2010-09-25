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
		self.legNode = render.attachNewNode("legions")
		
		self.setupStartUnits(pos)
	
	def setupStartUnits(self, start1):
		self.addUnit("base", start1.getX(),start1.getY(),start1.getZ())
	
	def addUnit(self, model, x, y, z):
		unit = Unit(model, x, y, z,self.color,self.legNode)
		if self.you == True:
			mySelection.listConsideration.append(unit)
		self.unitList.append(unit)
	
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

