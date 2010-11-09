#!/usr/bin/python
# -*- coding: utf8 -*-

from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from direct.showbase.DirectObject import DirectObject
#import direct.directbase.DirectStart
from direct.actor.Actor import Actor
from direct.stdpy import thread
import math, sys, time, Queue, collections, copy

from NavMesh import *
#from NavDrawer import *

#-------------------------------------------------------------------------------
# PathFinder
#-------------------------------------------------------------------------------	

class PathFinderPool:
	def __init__(self, slotNum, modelPath):
		self.pathFindTask = collections.deque()
		self.slotNum = slotNum
		self.pathFindQueue = Queue.Queue(50)
		#for i in range(slotNum):
		#	self.pathFindTask.append(PathFinder(modelPath))
		self.pathFindTask.append(PathFinder(modelPath))
		for i in range(1, self.slotNum):
			self.pathFindTask.append(copy.copy(self.pathFindTask[0]))
		taskMgr.setupTaskChain("pathFinderChain", numThreads = slotNum, tickClock = None, threadPriority = None, frameBudget = -1, frameSync = False, timeslicePriority = False)
		
	def addPathFindTask(self, unit, army):
		if not self.pathFindQueue.full():
			self.pathFindQueue.put(unit)
			taskMgr.add(self.createNewTask, "createTask", extraArgs=[unit, army], appendTask = True, taskChain = "pathFinderChain")
			return True
		return False
		
	def createNewTask(self, unit, army, task):
		for i in range(self.slotNum):
			print "checking pathFinder n. " + str(i)
			if self.pathFindTask[i].isFree():
				print "using pathFinder n. " + str(i)
				self.pathFindTask[i].setIsFree(False)
				path = self.pathFindTask[i].pathFindToMouse(self.pathFindQueue.get())
				self.pathFindTask[i].setIsFree(True)
				army.onPathComplete(unit, path)
				return task.done
		return task.cont
	

class PathFinder:
	def __init__(self, modelPath):
		self.node = NavMesh(modelPath)
		self.model = loader.loadModel(modelPath)
		self.model.setTwoSided(True)
		self.model.reparentTo(render)
		self.model.hide()
		self.z = 0
		self.setz = False
		self.mc = MouseCollider()
		self.bIsFree = True
		taskMgr.setupTaskChain("pathfinderChain", numThreads = 2, tickClock = None, threadPriority = None, frameBudget = -1, frameSync = False, timeslicePriority = False)
	
	def getZ(self):
		if self.setz == False:
			P = self.mc.collide()
			if P!=None:
				GCP = self.node.gc.collide(P+Vec3(0,0,0.5))
				if GCP != None:
					prim = self.node.getPrim(GCP)
					if prim!=None:
						self.z = GCP.getZ()
						self.setz = True
						return self.z
		else:
			return self.z
	'''
	def pathFindToMouse(self, unit, army):
		taskMgr.add(self.pftmTask, "pathfindTask", extraArgs=[unit, army], appendTask = True, taskChain = "pathfinderChain")
						
	def pftmTask(self, unit, army, task):
		P = self.mc.collide()
		if P!=None:
			GCP = self.node.gc.collide(P+Vec3(0,0,0.5))
			if GCP != None:
				prim = self.node.getPrim(GCP)
				if prim!=None:
					startPoint = unit.getPos()
					endPoint = GCP
					startPoint.setZ(self.getZ())
					path = self.node.findPath(startPoint, endPoint)
					if path != None:
						path2 = self.node.smoothPath(path)
						army.onPathComplete(unit, path2)
		return task.done
	'''
	def pathFindToMouse(self, unit):
		self.bIsFree = False
		P = self.mc.collide()
		if P!=None:
			GCP = self.node.gc.collide(P+Vec3(0,0,0.5))
			if GCP != None:
				prim = self.node.getPrim(GCP)
				if prim!=None:
					startPoint = unit.getPos()
					endPoint = GCP
					startPoint.setZ(self.getZ())
					path = self.node.findPath(startPoint, endPoint)
					if path != None:
						path2 = self.node.smoothPath(path)
						self.bIsFree = True
						return path2
		
	def isFree(self):
		return self.bIsFree
		
	def setIsFree(self, bool = True):
		self.bIsFree = bool
	
	def pathFindBake(self,start,unit):
		startPoint = start.node.getPos(render)
		startPoint.setZ(self.getZ())
		endPoint = unit.node.getPos(render)
		endPoint.setZ(self.getZ())
		path = self.node.findPath(startPoint, endPoint)
		if path != None:
			path2 = self.node.smoothPath(path)
			return path2
	
	def pathFindToNode(self,unit):
		startPoint = myGroup.getSingleUnit().getPos()
		startPoint.setZ(self.getZ())
		endPoint = unit.node.getPos(render)
		endPoint.setZ(self.getZ())
		path = self.node.findPath(startPoint, endPoint)
		if path != None:
			path2 = self.node.smoothPath(path)
			return path2
