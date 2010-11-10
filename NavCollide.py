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

class MouseCollider:
	def __init__(self):
		# collision handler
		self.picker = CollisionTraverser()
		self.pq     = CollisionHandlerQueue()
	
		self.pickerNode = CollisionNode('mouseRay')
		self.pickerNode.setIntoCollideMask(BitMask32.allOff())
		self.pickerNP = camera.attachNewNode(self.pickerNode)
		self.pickerRay = CollisionRay()
		self.pickerNode.addSolid(self.pickerRay)
		self.picker.addCollider(self.pickerNP, self.pq)
		#self.picker.showCollisions(render)
		
	def collide(self):
		if base.mouseWatcherNode.hasMouse():
			mpos = base.mouseWatcherNode.getMouse()
		else:
			return None
		self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

		nearPoint = render.getRelativePoint(camera, self.pickerRay.getOrigin())
		nearVec = render.getRelativeVector(camera, self.pickerRay.getDirection())
	
		self.picker.traverse(render)
		if self.pq.getNumEntries() > 0:
			self.pq.sortEntries()
			'''
			for n in range(self.pq.getNumEntries()):
				#print "Mouse Collision entry %s ---------------------" % (n)
				#print self.pq.getEntry(n)
				print "Mouse into node name = %s" % (self.pq.getEntry(n).getIntoNode().getName())
				print self.pq.getEntry(n).getSurfacePoint(render)
			'''
			return self.pq.getEntry(0).getSurfacePoint(render)
		return None

	def hasMouse(self):
		return base.mouseWatcherNode.hasMouse()
		
		
class GroundCollider:
	def __init__(self):
		self.picker = CollisionTraverser()
		self.pq     = CollisionHandlerQueue()
		
		self.model = render.attachNewNode("groundColNodePath")
		
		self.colRay = CollisionRay()
		self.colRay.setOrigin(0,0,5)
		self.colRay.setDirection(0,0,-1)
		
		self.modelCollider = self.model.attachNewNode(CollisionNode("ground"))
		self.modelCollider.node().setIntoCollideMask(BitMask32.allOff())
		self.modelCollider.node().addSolid(self.colRay)
		
		self.picker.addCollider(self.modelCollider, self.pq)
		#self.picker.showCollisions(render)
		
		self.A = None
		self.B = None
		
	def collide(self, pos):
		#print "Call to GC COLLIDE!"
		self.model.setPos(pos)
		self.picker.traverse(render)
		if self.pq.getNumEntries() > 0:
			self.pq.sortEntries()
			
			
			#for n in range(self.pq.getNumEntries()):
				#print "Ground Collision entry %s ---------------------" % (n)
				#print self.pq.getEntry(n)
				#print "Ground collider into node name = %s" % (self.pq.getEntry(n).getIntoNode().getName())
				#print self.pq.getEntry(n).getSurfacePoint(render)
			
			return self.pq.getEntry(0).getSurfacePoint(render)
		'''
		else:
			print "FAIL!!! no collision from ground!"
			pass
		'''
		return None
		
	def getPoints(self, A, B, step=0.01):
		points = []
		v = B-A
		AB = v.length()
		nb = int(AB / step)
		for i in range(nb):
			fac = (float(i)+1)/nb
			p = A + v/(1.0/fac)
			points.append(p)
		return points
		
		
		
	def hasLine(self, A, B, step=0.01):
		for p in self.getPoints(A, B, step):
			if self.collide(p) == None:
				return False
			'''
			else:
				m = loader.loadModelCopy("fleche.egg")
				m.setScale(0.1)
				m.setPos(self.collide(p))
				m.reparentTo(render)
			'''
		return True

