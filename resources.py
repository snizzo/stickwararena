# -*- coding: utf-8 -*-
from panda3d.core import *
from pandac.PandaModules import *
from random import randint
import sys,os, math


from unit import GameObject, Selector
from gui import BlackMatterHud

class Resources():
	def __init__(self):
		self.resourceList = []
		self.node = render.attachNewNode("resources")
	
	def addResource(self, node):
		bm = BlackMatter(node.getX(), node.getY(), node.getZ(), self)
		mySelection.listConsideration.append(bm)
		self.resourceList.append(bm)
		
	def getNode(self):
		return self.node
		
	def getIsPlayer(self):
		return False
	
	def removeResource(self, resource):
		mySelection.listConsideration.remove(resource)
		self.resourceList.remove(resource)
		resource.destroy()
	
	#function that i use to remove all my RTS's units from the main units list.
	def remove(self):
		for res in self.resourceList:
			self.resourceList.remove(res)
			res.destroy()
			

class Resource(GameObject):
	def __init__(self, x, y, z, _army):
		GameObject.__init__(self, x, y, z, _army)
		self.mainType = "resource"
		
	def showHealthBar(self, bool = False):
		pass
		
	def setHealth(self, amount):
		pass
		
	def getHealth(self):
		pass
		
	def damage(self, amount):
		pass
		
	def heal(self, amount):
		pass
			
			
class BlackMatter(Resource):
	
	hud = BlackMatterHud()
	
	def __init__(self, x, y, z, _army):
		Resource.__init__(self, x, y, z, _army)
		self.type = "blackmatter"
		self.name = "Black Matter Pool"
		self.meshPath = "models/blob/blob.egg"
		#initializing
		self.model = loader.loadModel(self.meshPath)
		self.model.setH(randint(0, 359))
		self.model.reparentTo(self.node)
		#set amount of black matter
		self.resCurrent = 18000
		self.resTotal = self.resCurrent

		self.selector = Selector(self.model, 1.0, 0.75)
		self.selector.hide()
	
	def getTotalResource(self):
		return self.resTotal
	
	def getResource(self):
		return self.resCurrent
	
	def getX(self):
		return self.node.getX()
	
	def getY(self):
		return self.node.getY()
	
	def getZ(self):
		return self.node.getZ()
	
	def setResource(self, res):
		n = self.resCurrent - 5
		if n > 0:
			self.resCurrent = n
			#TODO: update blackmatter
		else:
			#TODO: remove blackmatter, maybe scale animation...
			pass
	
	def showGui(self, bool = False):
		if bool:
			BlackMatter.hud.show(self, 0.12, -0.79)
		else:
			BlackMatter.hud.hide()
