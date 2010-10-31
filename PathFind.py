#!/usr/bin/python
# -*- coding: utf8 -*-

from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from direct.showbase.DirectObject import DirectObject
import direct.directbase.DirectStart
from direct.actor.Actor import Actor

import math
import sys
import time

from NavMesh import *
from NavDrawer import *

#-------------------------------------------------------------------------------
# PathFinder
#-------------------------------------------------------------------------------	
class PathFinder:
	def __init__(self, modelPath):
		self.node = NavMesh(modelPath)
		self.model = loader.loadModel(modelPath)
		self.model.setTwoSided(True)
		self.model.reparentTo(render)
		self.model.hide()
		self.z = 0
		self.setz = False
		#self.pd2 = PathDrawer("triangle2")
		self.mc = MouseCollider()
	
	def getZ(self):
		if self.setz == False:
			P = self.mc.collide()
			if P!=None:
				#self.pd2.clear()
				GCP = self.node.gc.collide(P+Vec3(0,0,0.5))
				if GCP != None:
					prim = self.node.getPrim(GCP)
					if prim!=None:
						self.z = GCP.getZ()
						self.setz = True
						return self.z
		else:
			return self.z
	
	def pathFindToMouse(self, unit):
		P = self.mc.collide()
		if P!=None:
			#self.pd2.clear()
			GCP = self.node.gc.collide(P+Vec3(0,0,0.5))
			if GCP != None:
				prim = self.node.getPrim(GCP)
				if prim!=None:
					#print "listSelected: " + str(mySelection.listSelected[0].main.getPos())
					#startPoint = mySelection.listSelected[0].node.getPos(render)
					startPoint = unit.getPos()
					endPoint = GCP
					startPoint.setZ(self.getZ())
					#print "calling pathfinding with s: " + str(startPoint) + " | f:" + str(endPoint)
					path = self.node.findPath(startPoint, endPoint)
					if path != None:
						path2 = self.node.smoothPath(path)
						#path2 contains the true path
						#self.pd2.points = path2
						#self.pd2.startDraw()
						#print "path2: " +str(path2)
						return path2
	
	def pathFindBake(self,start,unit):
		#print "listSelected: " + str(mySelection.listSelected[0].main.getPos())
		startPoint = start.node.getPos(render)
		startPoint.setZ(self.getZ())
		endPoint = unit.node.getPos(render)
		endPoint.setZ(self.getZ())
		#print "calling pathfinding with s: " + str(startPoint) + " | f:" + str(endPoint)
		path = self.node.findPath(startPoint, endPoint)
		if path != None:
			path2 = self.node.smoothPath(path)
			#path2 contains the true path
			#self.pd2.points = path2
			#self.pd2.startDraw()
			#print "path2: " +str(path2)
			return path2
	
	def pathFindToNode(self,unit):
		#print "listSelected: " + str(mySelection.listSelected[0].main.getPos())
		#startPoint = mySelection.listSelected[0].node.getPos(render)
		startPoint = myGroup.getSingleUnit().getPos()
		startPoint.setZ(self.getZ())
		endPoint = unit.node.getPos(render)
		endPoint.setZ(self.getZ())
		#print "calling pathfinding with s: " + str(startPoint) + " | f:" + str(endPoint)
		path = self.node.findPath(startPoint, endPoint)
		if path != None:
			path2 = self.node.smoothPath(path)
			#path2 contains the true path
			#self.pd2.points = path2
			#self.pd2.startDraw()
			#print "path2: " +str(path2)
			return path2
