# -*- coding: utf-8 -*-

from PathFind import *
from direct.showbase.DirectObject import DirectObject
from random import Random
import sys,os,string,math, Queue
from gui import *
from enumeration import ReverseEnumeration
		
#fuckin' OOP
#health bar class
class HealthBar():

	fullLifeFrame = Vec4(0,0,0.5,0.5)
	halfLifeFrame = Vec4(0.5,0.5,0.5,0.5)
	lowLifeFrame = Vec4(0.5,0,0.5,0.5)
	noLifeFrame = Vec4(0,0.5,0.5,0.5)

	def __init__(self, health, _owner, _yOffset = 0.0):
		self.totalHealth = health
		self.currentHealth = health
		self.owner = _owner
		self.mesh = MeshDrawer()
		self.mesh.setBudget(self.totalHealth / 5)
		self.node = self.mesh.getRoot()
		self.node.reparentTo(self.owner)
		self.node.setTexture(loader.loadTexture("images/stick_commander/lifebar.png"))
		self.node.setLightOff(True)
		self.node.setCompass()
		self.material = Material("normalFlag")
		self.material.setDiffuse(Vec4(1,1,1,1))
		self.node.setMaterial(self.material,1)
		self.yOffset = _yOffset
		
		self.draw(HealthBar.fullLifeFrame)
		self.show()
		
	def draw(self, frame):
		self.mesh.begin(base.cam, render)
		for i in range(self.currentHealth / 10):
			self.mesh.billboard(Vec3(i*0.07,0,+0.15),frame,0.035,Vec4(1,1,1,1))
		for e in range(self.totalHealth / 10 - self.currentHealth / 10):
			i += 1
			self.mesh.billboard(Vec3(i*0.07,0,+0.15), HealthBar.noLifeFrame, 0.035, Vec4(1,1,1,1))
		barBound = self.node.getBounds().getRadius()
		self.node.setX(-barBound+0.06)
		self.node.setY(-self.owner.getBounds().getRadius() / 2 + self.yOffset)
		self.mesh.end()
				
	def show(self):
		self.node.show()
	
	def hide(self):
		self.node.hide()
	
	def getTotalHealth(self):
		return self.totalHealth
		
	def getCurrentHealth(self):
		return self.currentHealth
		
	def update(self, amount):
		self.currentHealth += amount
		print str(self.currentHealth)
		if self.currentHealth > self.totalHealth:
			self.currentHealth = self.totalHealth
		if self.currentHealth < 0:
			self.owner.destroy()
		percHealth = self.currentHealth * 100 / self.totalHealth
		if percHealth < 33:
			frame = HealthBar.lowLifeFrame
		elif percHealth < 66:
			frame = HealthBar.halfLifeFrame
		else:
			frame = HealthBar.fullLifeFrame
		self.draw(frame)
			
	def setHealth(self, amount):
		self.totalHealth = amount
		self.currentHealth = amount
		self.draw(HealthBar.fullLifeFrame)
		

class Selector():
		def __init__(self, _owner, scaleFactor = 1.0, xOffset = 0.0, yOffset = 0.0):
			self.owner = _owner
			self.radius = self.owner.getBounds().getRadius() * scaleFactor
			
			self.node = loader.loadModel("images/selector.egg")
			self.node.setLightOff(True)
			self.node.reparentTo(self.owner)
			if xOffset != 0.0:
				self.node.setX(self.node.getX() + xOffset)
			if yOffset != 0.0:
				self.node.setY(self.node.getY() + yOffset)
			self.node.setZ(0.1)
			self.node.setP(270)
			self.node.setScale(self.radius)
			
		def show(self):
			self.node.show()
			
		def hide(self):
			self.node.hide()
	
		
#basic game entity class, not for Instantiation
class GameObject(DirectObject):

	multipleHud = MultipleHud()

	def __init__ (self, x, y, z, _army):
		self.army = _army
		self.node = self.army.getNode().attachNewNode("gameobject")
		self.node.setPos(x, y, z)
		
	def isOwner(self):
		return self.army.getIsPlayer()
		
	def getType(self):
		return self.type
		
	def getMainType(self):
		return self.mainType
		
	def getMeshPath(self):
		return self.meshPath
		
	def leftButtonNotify(self):
		pass
		
	def rightButtonNotify(self):
		pass
	
	#set the health of the game object to <amount> and update the healthbar consistently
	def setHealth(self, amount):
		self.healthBar.setHealth(amount)
		
	#print on the standard output various debug information
	def debug(self):
		print "position:  x = " + str(self.node.getX()) + "    y = " + str(self.node.getY()) + "     z = " + str(self.node.getZ())
		
	#return the main node of the game object
	def getNode(self):
		return self.node
		
	def getPos(self):
		return self.node.getPos()
		
	#return the current health of the game object
	def getHealth(self):
		return self.healtBar.getHealth()
	
	#apply <amount> damage to the game object and update the health bar consistently
	def damage(self, amount):
		self.healthBar.update(-amount)
		
	def heal(self, amount):
		self.healthBar.update(amount)
		
	def getHealthBar(self):
		return self.healthBar
		
	def showHealthBar(self, bool = False):
		if bool:
			self.healthBar.show()
		else:
			self.healthBar.hide()
			
	def showSelector(self, bool = False):
		if bool:
			self.selector.show()
		else:
			self.selector.hide()
	
	def showGui(self, bool = False):
		pass
	
	def showHUD(self, bool = False):
		self.showGui(bool)
		self.showHealthBar(bool)
		self.showSelector(bool)
		
	#update the game object status
	def update(self, task):
		return task.cont
		
	def getArmor(self):
		return self.armor
		
	#remove the game object from the game
	def destroy(self):
		self.node.remove()
		
#basic structure class, not for Instantiation
class Structure(GameObject):

	random = Random()

	def __init__(self, x, y, z, _army):
		self.spawnPoint = x + 2, y + 2, z
		self.mainType = "structure"
		self.creationQueue = Queue.Queue(5)
		self.queueBusy = False
		GameObject.__init__(self, x, y, z, _army)
		self.unitCreationTask = False
		
	#create a new unit of type <unitType> at location <spawnPoint> (note: <spawnPoint> is an instance variable)
	def createUnit(self, unitType):
		pass
		
	def createUnitDelayed(self, unitType, task):
		return task.done
		
	def addUnitToCreationQueue(self, unitType):
		if not self.creationQueue.full():
			self.creationQueue.put(unitType)
			if not self.unitCreationTask:
				self.unitCreationTask = taskMgr.add(self.update, "creationQueue")
			return True
		else:
			return False
		
	def update(self, task):
		if not self.creationQueue.empty() and not self.queueBusy:
			self.createUnit(self.creationQueue.get())
			self.queueBusy = True
		if self.creationQueue.empty():
			self.unitCreationTask = False
			return task.done
		return task.cont
		
	#set the unit spawn point to <x, y>
	def setSpawnPoint(self, x, y):
		self.spawnPoint = x, y, self.spawnPoint[2]
	
		
#basic unit class, not for Instantiation
class Unit(GameObject):
	def __init__(self, x, y, z, _army):
		GameObject.__init__(self, x, y, z, _army)
		self.movementTask = False
		self.mainType = "unit"
	
	#move to object from the actual position to the last waypoint in <waylist> passing through all the waypoint
	def go(self, wayList):
		self.wayList = wayList
		if self.movementTask:
			taskMgr.remove(self.movementTask)
		self.movementTask = False
		self.model.loop('run')
		self.currentWayList = wayList
		self.currentWayList.pop(0)
		if len(self.currentWayList) > 0:
			self.currentTarget = self.currentWayList.pop(0)
			self.rotateTo(self.currentTarget)
			self.currentDir = self.node.getPos() - self.currentTarget
			self.currentDir.normalize()
			self.currentDir[2] = 0.0
			self.targetReached = False
			self.movementTask = taskMgr.add(self.moveTo, "moveTo")
	
	#make unit face his target smoothly
	def rotateTo(self, point):
		nodeRotation = self.node.getH()
		#avoiding accumulation of degrees problems
		if nodeRotation > 180:
			nodeRotation = nodeRotation - 360
			self.node.setH(nodeRotation)
		if nodeRotation < -180:
			nodeRotation = nodeRotation + 360
			self.node.setH(nodeRotation)
		#get the needed angle
		requiredRotation = self.getSteeringAngle(point)
		#make the angle working with the -180° / 0° / 180° degrees system
		if nodeRotation >= 0 and requiredRotation < 0:
			hlerp = abs(nodeRotation) + abs(requiredRotation)
			if hlerp > 180:
				requiredRotation = nodeRotation + (360 - hlerp)
		if nodeRotation < 0 and requiredRotation > 0:
			hlerp = abs(nodeRotation) + abs(requiredRotation)
			if hlerp > 180:
				requiredRotation = nodeRotation - (360 - hlerp)
		#play a small interval lasting <0.2> seconds, <to angle>, <from angle>
		self.node.hprInterval(0.2, Vec3(requiredRotation,0,0), Vec3(nodeRotation,0,0)).start()
		
	#return needed node's angle to turn and face <point> target
	def getSteeringAngle(self, point):
		x = self.node.getX() - point.getX()
		y = self.node.getY() - point.getY()
		d = math.sqrt(x*x + y*y)
		if d != 0:
			h = 90 + math.degrees(math.asin(y / d))
		else:
			h = 90
		if x < 0:
			h = -h
		return h
	
	def moveTo(self, task):
		#get clock delta time to make movement frame-rate indipendent
		dt = globalClock.getDt()
		#movement task
		if abs(self.node.getX() - self.currentTarget[0]) > 0.1 or abs(self.node.getY() - self.currentTarget[1]) > 0.1:
			if len(self.currentWayList) == 0:
				self.targetReached = True
			if abs(self.node.getX() - self.currentTarget[0]) > 0.1:
				self.node.setX(self.node.getX() - self.currentDir[0] * dt * 2)
			if abs(self.node.getY() - self.currentTarget[1]) > 0.1:
				self.node.setY(self.node.getY() - self.currentDir[1] * dt * 2)
			return task.cont
		else:
			if self.targetReached:
				self.stop()
				return task.done
			else:
				if len(self.currentWayList) == 0:
					self.stop()
					return task.done
				self.currentTarget = self.currentWayList.pop(0)
				self.rotateTo(self.currentTarget)
				self.currentDir = self.node.getPos() - self.currentTarget
				self.currentDir.normalize()
				self.currentDir[2] = 0.0
				return task.cont
	
	#stop the game unit canceling all the current actions
	def stop(self):
		if self.movementTask:
			taskMgr.remove(self.movementTask)
		self.model.pose('idle', 1)
		
	def getAttack(self):
		return self.attack

		
#specialized structure class
class Base(Structure):

	hud = BaseHud()

	def __init__(self, x, y, z, _army):
		Structure.__init__(self, x, y, z, _army)
		self.type = "base"
		self.unitType = ReverseEnumeration("unit", [("worker", 4), ("soldier", 5)])
		
		self.armor = 100
		
		#load the model
		self.meshPath = "models/mainbase/base.egg"
		self.model = loader.loadModel(self.meshPath)
		self.model.reparentTo(self.node)
		
		#set the material properties
		self.colorFlag = self.node.find("**/colorFlagObj")
		self.materialFlag = Material("materialFlag")
		self.materialFlag.setDiffuse(self.army.getColor())
		self.colorFlag.setMaterial(self.materialFlag,1)
		self.colorFlag.setColor(Vec4(0.5,0.5,0.5,1))
		
		#create the healthbar
		self.healthBar = HealthBar(400, self.model, -0.35)
		self.healthBar.hide()
		
		#create the selector
		self.selector = Selector(self.model, 0.75)
		self.selector.hide()
		
		#create the gui
		#self.hud = Hud(self)
	
	def createUnit(self, unitType):
		if unitType == self.unitType.worker:
			taskMgr.doMethodLater(self.unitType.__getattr__("worker"), self.createUnitDelayed, 'createUnit', extraArgs=[unitType], appendTask=True)
		elif unitType == self.unitType.soldier:
			taskMgr.doMethodLater(self.unitType.__getattr__("soldier"), self.createUnitDelayed, 'createUnit', extraArgs=[unitType], appendTask=True)
			
	def createUnitDelayed(self, unitType, task):
		if unitType == self.unitType.worker:
			self.army.addUnit(Worker(self.spawnPoint[0] + (Base.random.random() - 0.5), self.spawnPoint[1] + (Base.random.random() - 0.5), self.spawnPoint[2], self.army))
		elif unitType == self.unitType.soldier:
			self.army.addUnit(Soldier(self.spawnPoint[0] + (Base.random.random() - 0.5), self.spawnPoint[1] + (Base.random.random() - 0.5), self.spawnPoint[2], self.army))
		self.queueBusy = False
		return task.done
			
	def getUnitType(self):
		return self.unitType
		
	def showGui(self, bool = False):
		if bool:
			Base.hud.show(self, 0.2, -0.82)
		else:
			Base.hud.hide()
		

#specialized unit class	
class Worker(Unit):

	hud = WorkerHud()

	def __init__(self, x, y, z, _army):
		Unit.__init__(self, x, y, z, _army)
		self.type = "worker"
		self.unitType = ReverseEnumeration("structure", [("Base", 40)])
		
		#unit params
		self.attack = 5
		self.armor = 0
		
		#load the model and the animation
		self.meshPath = "models/ometto/ometto.egg"
		self.model = Actor (self.meshPath, {
			'idle':'models/ometto/ometto-idle.egg',
			'run':'models/ometto/ometto-run.egg'
		})
		self.model.setH(180)
		self.model.reparentTo(self.node)
		
		#set the material properties
		self.materialFlag = Material("materialFlag")
		self.materialFlag.setDiffuse(self.army.getColor())
		self.model.setMaterial(self.materialFlag,1)
		
		#create the health bar
		self.healthBar = HealthBar(60, self.model, 0)
		self.healthBar.hide()
		
		#create the selector
		self.selector = Selector(self.model, 0.5)
		self.selector.hide()
		
		#play the basic animation
		self.model.play('idle')
		
		#call the update coroutine
		taskMgr.add(self.update, "unitupdate")
		
	#send the worker to gather the indicated <blackMatter> through the route indicated by <wayList>
	def gather(self, blackMatter, wayList):
		pass
		
	def buildStructure(self, structureType):
		pass
		
	def showGui(self, bool = False):
		if bool:
			Worker.hud.show(self, 0.4, -0.89)
		else:
			Worker.hud.hide()
		

class Soldier(Unit):

	hud = SoldierHud()

	def __init__(self, x, y, z, _army):
		Unit.__init__(self, x, y, z, _army)
		self.type = "soldier"
		
		#load the model and the animation
		self.meshPath = "models/ometto/ometto.egg"
		self.model = Actor (self.meshPath, {
			'idle':'models/ometto/ometto-idle.egg',
			'run':'models/ometto/ometto-run.egg'
		})
		self.model.setH(180)
		self.model.reparentTo(self.node)
		
		#set the material properties
		self.materialFlag = Material("materialFlag")
		self.materialFlag.setDiffuse(self.army.getColor())
		self.model.setMaterial(self.materialFlag,1)
		
		#create the health bar
		self.healthBar = HealthBar(60, self.model, 0)
		self.healthBar.hide()
		
		#create the selector
		self.selector = Selector(self.model, 0.5)
		self.selector.hide()
		
		#play the basic animation
		self.model.play('idle')
		
		#call the update coroutine
		taskMgr.add(self.update, "unitupdate")
		
	def showGui(self, bool = False):
		if bool:
			Soldier.hud.show(self, 0.4, -0.89)
		else:
			Soldier.hud.hide()
			
