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


class PathDrawer:
	def __init__(self, name = None):
		self.points = []
		self.name = name
		
		self.np = render.attachNewNode("np")
		#self.np.setPos(0,0,1)
		self.np.reparentTo(render)
		self.decalVec = Vec3(0,0,0.1)
		maxParticles = 500
		self.generator = MeshDrawer()
		self.generator.setBudget(maxParticles)
		self.generatorNode = self.generator.getRoot()
		self.generatorNode.reparentTo(self.np)
		self.generatorNode.setDepthWrite(False)
		self.generatorNode.setTransparency(True)
		self.generatorNode.setTwoSided(True)
		self.generatorNode.setTexture(loader.loadTexture("white2.png"))
		self.generatorNode.setBin("fixed",0)
		self.generatorNode.setLightOff(True)
		
		self.generatorNode.node().setBounds(BoundingSphere((0, 0, 0), 10000000))
		self.generatorNode.node().setFinal(True)
		
		self.startDraw()
		
	def addPoint(P):
		self.points.append(Vec3(P))

	def delPoint(n):
		try:
			del self.points[n]
		except:
			print "Impossible to remove point number %s" % (n)
		
	def clear(self):
		self.stopDraw()
		self.points = []
		
	def startDraw(self):
		#if (not(taskMgr.hasTaskNamed("drawTrail"))):
		if self.name!=None:
			self.generatorNode.reparentTo(render)
			taskMgr.add(self.drawTask, self.name)
		else:
			print "Error : draw task has not been given a name."
		
			
	def stopDraw(self):
		if (taskMgr.hasTaskNamed(self.name)):
			taskMgr.remove(self.name)
		self.generatorNode.detachNode()
		
	def drawTask(self, task):
		#dt = globalClock.getFrameTime()
		#dt = globalClock.getDt()
		#print "HPR = ", self.generatorNode.getHpr()
		if len(self.points)>=2:
			self.generator.begin(base.cam,render)
			self.generator.linkSegment(Vec3(self.points[0]+self.decalVec),1,0.2,Vec4(1,0,0,1))# because of the weird bug for second point
			for n in range(len(self.points)):
				self.generator.linkSegment(Vec3(self.points[n]+self.decalVec),1,0.2,Vec4(1,0,0,1))
			self.generator.linkSegmentEnd(1,Vec4(1,0,0,1))
			self.generator.end()
		return Task.cont
		
	def destroy(self):
		self.stopDraw()
