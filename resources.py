# -*- coding: utf-8 -*-
from panda3d.core import *
from pandac.PandaModules import *
from random import randint
import sys,os, math


from unit import GameObject, Selector

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
			mySelection.listConsideration.remove(res)
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
		self.node.setPythonTag("amountT", 18000)
		self.node.setPythonTag("amount", 18000)

		self.selector = Selector(self.model, 1.0, 0.75)
		self.selector.hide()
	
	def getX(self):
		return self.node.getX()
	
	def getY(self):
		return self.node.getY()
	
	def getZ(self):
		return self.node.getZ()
	
	def subResource(self, res):
		amount = self.node.getPythonTag("amount")
		n = amount - 5
		if n > 0:
			self.node.setPythonTag("amount", n)
			messenger.send("commander-update", ['resources', res])
		else:
			self.army.remove(self)
