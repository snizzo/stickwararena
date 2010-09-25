# -*- coding: utf-8 -*-

from pandac.PandaModules import *
import sys,os

from legion import *

class Map():
	def __init__(self):
		pass
	
	def setupInitMap(self):
		startPosNode = self.mapNode.findAllMatches("**/start_p**")
		i = 0
		for pos in startPosNode:
			#color declaration
			if i==0:
				color = Vec4(1,0,0,1)
				you = True
			if i==1:
				color = Vec4(0,1,0,1)
				you = False
			if i==2:
				color = Vec4(0,0,1,1)
				you = False
			if i==3:
				color = Vec4(1,1,0,1)
				you = False
			legion = Legion(pos,color,you)
			myLegion.append(legion)
			i = i+1
		resPosNode = self.mapNode.findAllMatches("**/r**")
		for pos in resPosNode:
			myResources.addResource(pos)
	
	def loadMap(self, url):
		self.mapNode = render.attachNewNode("mapNode")
		# "maps/burning_sun/burning_sun.egg" demo map name
		self.map = loader.loadModel(url)
		self.map.reparentTo(self.mapNode)
	
	def unloadMap(self):
		self.mapNode.remove()
	
	def setupMap(self):
		#carico la skybox e riparento
		self.skybox = loader.loadModel("maps/data/skybox.egg")
		self.skybox.setScale(16)
		self.skybox.reparentTo(render)
			
	def destroyMap(self):
		self.skybox.remove()
		
