# -*- coding: utf-8 -*-
from panda3d.core import *
from pandac.PandaModules import *
from random import randint
import sys,os


from unit import *

class Resources():
	def __init__(self):
		#creating main list
		self.resList = []
		self.legNode = render.attachNewNode("resources")
	
	def addResource(self, node):
		res = BlackMatter(node, self.legNode)
		self.resList.append(res)
	
	#function that i use to remove all my RTS's units from the main units list.
	def remove(self):
		print "resources.remove() called"
		for res in self.resList[:]:
			res.remove()
			self.resList.remove(res)

#creating this Black matter class just to follow the "standard" of selection class...
#maybe fix in future... or maybe not...
class BlackMatter():
	def __init__(self, pos, owner):
		self.type = "BlackMatter"
		self.name = "Black Matter Pool"
		#initializing
		self.node = loader.loadModel("models/blob/blob.egg")
		self.node.setX(pos.getX())
		self.node.setY(pos.getY())
		self.node.setZ(pos.getZ())
		self.node.setH(randint(0, 359))
		self.node.reparentTo(owner)
		#set amount of black matter
		self.node.setPythonTag("amount", 18000)
		#adding to selectable unit list
		mySelection.listConsideration.append(self)
	
	def subResource(self, res):
		amount = self.node.getPythonTag("amount")
		n = amount - 5
		if n > 0:
			self.node.setPythonTag("amount", n)
			messenger.send("commanderUpdate", ['resources'])
		else:
			self.remove()
	
	def remove(self):
		if self in mySelection.listSelected:
			mySelection.listSelected.remove(self)
		if self in mySelection.listLastSelected:
			mySelection.listLastSelected.remove(self)
		mySelection.listConsideration.remove(self)
		self.node.remove()
