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
import copy

from NavCollide import *

#-----------------------------------------------------------------------
# point inside a triangle
#-----------------------------------------------------------------------

def SameSide(p1,p2,A,B):
	cp1 = (B-A).cross(p1-A)
	cp2 = (B-A).cross(p2-A)
	if cp1.dot(cp2)>= 0: return True
	return False

def PointInTriangle(p,A,B,C):
	if SameSide(p,A,B,C) and SameSide(p,B,A,C) and SameSide(p,C,A,B):
		vecNorm = (A-B).cross(A-C)
		if (p-A).dot(vecNorm)< 0.001:
			return True
	return False

#-----------------------------------------------------------------------
# egg data processing
#-----------------------------------------------------------------------

def processGeomNode(geomNode):
	for i in range(geomNode.getNumGeoms()):
		geom = geomNode.getGeom(i)
		state = geomNode.getGeomState(i)
		#print "Geom : ", geom
		#print "State : ", state
		return processGeom(geom)
	#print "#------- end of processGeomNode ---------"	
	
def processGeom(geom):
	vdata = geom.getVertexData()
	prim = geom.getPrimitive(0)
	return processPrimitive(prim, vdata)
	
	'''
	#print vdata
	#self.processVertexData(vdata)
	n = 0
	for i in range(geom.getNumPrimitives()):
		prim = geom.getPrimitive(i)
		#print prim
		processPrimitive(prim, vdata)
		print "primitive %s done" % (n)
		n=n+1
	'''
	#print "#------- end of processGeom ---------"


def processVertexData(self, vdata):
	vertex = GeomVertexReader(vdata, 'vertex')
	texcoord = GeomVertexReader(vdata, 'texcoord')
	while not vertex.isAtEnd():
		v = vertex.getData3f()
		try:t = texcoord.getData2f()
		except : t = "grosse erreur de texcoord.getData2f()"
		print "v = %s, t = %s" % (repr(v), repr(t))


def processPrimitive(prim, vdata, scale = 1):
	prims = {}
	vertex = GeomVertexReader(vdata, 'vertex')
	prim = prim.decompose()
	for p in range(prim.getNumPrimitives()):
		s = prim.getPrimitiveStart(p)
		e = prim.getPrimitiveEnd(p)
		vertexList = []
		for i in range(s, e):
			
			vi = prim.getVertex(i)
			vertex.setRow(vi)
			v = vertex.getData3f()
			v = VBase3(v[0]*scale, v[1]*scale, v[2]*scale)
			vertexList.append(v)
			
			#print "prim %s has vertex %s: %s" % (p, vi, v)
		prims[p]=vertexList
	return prims



#-----------------------------------------------------------------------
# NavMesh initial functions
#-----------------------------------------------------------------------

'''

def loadNavMesh(modelPath):
	decor = loader.loadModel(modelPath)
	geomNodeCollection = decor.findAllMatches('**/+GeomNode')
	for nodePath in geomNodeCollection:
		geomNode = nodePath.node()
		#processGeomNode(geomNode)
		#print geomNode
		return processGeomNode(geomNode)

def getPointsList(modelPath):
	prims = loadNavMesh(modelPath)
	liste = []
	for P in prims.values():
		for p in P:
			if not(p in liste):
				liste.append(p)
	return liste

def getNeighbours(modelPath):
	dico = {}
	prims = loadNavMesh(modelPath)
	
	#liste = getPointsList(modelPath)
	liste = []
	for P in prims.values():
		for p in P:
			if not(p in liste):
				liste.append(p)
	
	for point in liste:
		if not dico.has_key(point):
			dico[point] = []
		for prim in prims.values():
			if point in prim:
				for n in prim:
					if (n != point) and not (n in dico[point]):
						dico[point].append(n)
	return dico
	
def getGrid(modelPath):
	NeighDic = getNeighbours(modelPath)
	centerDic = {}
	for p, nList in NeighDic.items():
		for n in nList:
			center = (p+n)/2.0
			if not centerDic.has_key(center):
				centerDic[center]=[p,n]
				
	for p in NeighDic.keys():
		if not centerDic.has_key(p):
			centerDic[p] = NeighDic[p]
		for center, Nlist in centerDic.items():
			if p in Nlist and not center in centerDic[p]:
				centerDic[p].append(center)
				
	# TODO : ajouter aux centres des edges les autres voisins des edges à côté
				
	return centerDic
	

		
		
def getPrimsNeighbours(prims):
	primNeighbours = {}
	for prim, vertList in prims.items():
		neighbours = []
		for prim2, vertList2 in prims.items():
			nbSameVert = 0
			for v in vertList:
				for v2 in vertList2:
					if v == v2:
						nbSameVert +=1
			if nbSameVert == 2:
				neighbours.append(prim2)
		primNeighbours[prim] = neighbours
	return primNeighbours

'''

def getCost(path):
	cost = 0
	for n in range(len(path)-1):
		cost = cost + (path[n+1]-path[n]).length()
	return cost
	
#-----------------------------------------------------------------------
# NavMesh
#-----------------------------------------------------------------------

class NavMesh:
	def __init__(self, modelPath=None):
		if modelPath!=None:
			# dico de la forme : {n1 : [p1, p2, p3],...},
			#où prim est un polygon, p des VBase3
			self.prims = self.load(modelPath)
			self.points = self.getPointsList()
			self.primsFull = self.addCenters()
			self.pointsNeighboursDic = self.getNeighbours()
			self.primsNeighboursDic = self.getPrimsNeighbours()
			
			
			
		else:
			self.prims = {}
			self.points = []
			self.primsFull = {}
			self.pointsNeighboursDic = {}
			self.primsNeighboursDic = {}
		
		self.gc = GroundCollider()
		
		self.paths = []
		self.primPaths = []
		
		self.step = 0
		self.targetList = []
		
		self.pointToSet = 1
		self.startPoint = None
		self.endPoint = None
		
		self.startPrim = None
		self.endPrim = None
		
	def initSearch(self, A, B):
		self.startPos = A
		self.endPos = B
		
		primA = self.getPrim(A)
		if primA == None:
			print "Error : %s not in NavMesh" % (A)
			return False
		primB = self.getPrim(B)
		if primB == None:
			print "Error : %s not in NavMesh" % (B)
			return False
		if primA == primB:
			return [primA]
		
		if primB in self.primsNeighboursDic[primA]:
			return [primA, primB]
			
		#print "primA : %s, primB : %s" % (primA, primB)
		
		self.primPaths = []
		
		self.startPrim = primA
		self.endPrim = primB
		
		for n in self.primsNeighboursDic[primA]:
			self.primPaths.append([primA, n])
		self.step = 2
		for i in range(len(self.prims.keys())):
			self.primDig()
			path = self.checkIfPrimPathFound()
			if path != False:
				#print "Prim path found! %s" % (path)
				return path
		#print "Path not found :("
		#print "primPaths : %s" % (self.primPaths)
		return None
		
	def findPath(self, A, B):
		primPath = self.initSearch(A, B)
		if primPath != None:
			wayPoints = []
			wayPoints.append(self.startPos)
			
			for n in range(len(primPath)-1):
				A = primPath[n]
				B = primPath[n+1]
				p = self.getCommonEdgeCenter(A, B)
				wayPoints.append(p)
			wayPoints.append(self.endPos)
			return wayPoints
			
		return None
		
	def smoothPath(self, path, step=0.25):
		if(len(path)<3):
			return path
			
		newPath = []
		pathLeft = []
		
		
		#print "----------------------------------------------"
		#print "Initial Path : %s" % (path)
		#print "longueur : %s" % (len(path))
		
		for i in path:
			pathLeft.append(i)
		
		newPath.append(pathLeft.pop(0))
		
		while(len(pathLeft)>1):
			if self.gc.hasLine(newPath[-1], pathLeft[1], step):
				pathLeft.pop(0)
			else:
				newPath.append(pathLeft.pop(0))
		
		newPath.append(pathLeft.pop(0))
		
		#print "Smoothed path trouvé : %s" % (newPath)
		return newPath
		
		
	def primDig(self):
		#print "digging : step = %s" % (self.step)
		pathList = self.primPaths
		
		newPrimPaths = []
		
		for path in pathList:
			lastPrim = path[-1]
			neighbours = self.primsNeighboursDic[lastPrim]
			tmpPathList = []
			for n in neighbours:
				if not n in path:
					tmpPath = []
					tmpPath.extend(path)
					tmpPath.append(n)
					tmpPathList.append(tmpPath)
			newPrimPaths.extend(tmpPathList)
		self.primPaths.extend(newPrimPaths)
		#print "digging : new prim paths found : %s" % (newPrimPaths)
		self.cleanPrimPaths()
		
		
	def cleanPrimPaths(self):
		liste = []
		for path in self.primPaths:
			if len(path) != self.step:
				liste.append(path)
				#print "cleaning : keeping %s" % (path)
			'''
			else:
				print "cleaning : removing %s" % (path)
			'''
		self.primPaths = liste
		self.step = self.step + 1
		
	def checkIfPrimPathFound(self):
		for path in self.primPaths:
			if path[-1]==self.endPrim:
				return path
		return False
	
	
	def load(self, modelPath):
		decor = loader.loadModel(modelPath)
		geomNodeCollection = decor.findAllMatches('**/+GeomNode')
		for nodePath in geomNodeCollection:
			geomNode = nodePath.node()
			#processGeomNode(geomNode)
			#print geomNode
			return processGeomNode(geomNode)
			
	def getPointsList(self):
		liste = []
		for P in self.prims.values():
			for p in P:
				if not(p in liste):
					liste.append(p)
		return liste

	def getPrim(self, pt):
		for k, v in self.prims.items():
			if PointInTriangle(pt, v[0], v[1], v[2]):
				#print "le point %s est dans le chemin. Prim = %s, vertices = %s" % (pt, k, v)
				return k
		return None
		
	def addCenters(self):
		primsFull = {}
		
		for k, v in self.prims.items():
			c1 = (v[0]+v[1])/2.0
			c2 = (v[0]+v[2])/2.0
			c3 = (v[2]+v[1])/2.0
			if c1 not in self.points:self.points.append(c1)
			if c2 not in self.points:self.points.append(c2)
			if c3 not in self.points:self.points.append(c3)
			primsFull[k] = []
			for i in v:
				primsFull[k].append(i)
			primsFull[k].append(c1)
			primsFull[k].append(c2)
			primsFull[k].append(c3)
			
		return primsFull
		
		
	def getNeighbours(self):
		NeighboursDic = {}
		for point in self.points:
			if not NeighboursDic.has_key(point):
				NeighboursDic[point] = []
			for primPoints in self.primsFull.values():
				if point in primPoints:
					for n in primPoints:
						if not n in NeighboursDic[point] and point != n:
							NeighboursDic[point].append(n)
		return NeighboursDic
							
	def getPrimsNeighbours(self):
		primNeighbours = {}
		for prim, vertList in self.prims.items():
			neighbours = []
			for prim2, vertList2 in self.prims.items():
				nbSameVert = 0
				for v in vertList:
					for v2 in vertList2:
						if v == v2:
							nbSameVert +=1
				if nbSameVert == 2:
					neighbours.append(prim2)
			primNeighbours[prim] = neighbours
		return primNeighbours
		
	def getCommonPoints(self, prim1, prim2):
		liste = []
		for p1 in self.primsFull[prim1]:
			for p2 in self.primsFull[prim2]:
				if p1 == p2:
					liste.append(p1)
		return liste

	def getCommonEdgeCenter(self, prim1, prim2):
		commonVertices = []
		for pt in self.prims[prim1]:
			for pt2 in self.prims[prim2]:
				if pt == pt2:
					commonVertices.append(pt)
		if len(commonVertices) == 2:
			P = (commonVertices[0]+commonVertices[1])/2
			return Point3(P)
		return None
		
	
