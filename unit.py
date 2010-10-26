# -*- coding: utf-8 -*-
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.interval.IntervalGlobal import *
from direct.interval.FunctionInterval import Wait
from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from panda3d.core import TextNode
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import Point3,Vec3,Vec4
from panda3d.core import Filename
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.ai import *
from PathFind import *
import sys,os,string,math

class BaseEvents():
	def __init__(self):
		self.finder = PathFinder("maps/burning_sun/burning_sun_nav.egg")
		base.accept("mouse-order", self.go)
	
	def go(self):
		if len(mySelection.listSelected) == 1:
			obj = mySelection.listSelected[0]
			if len(mySelection.underMouse) == 1:
				toobj = mySelection.underMouse[0]
				if toobj.type == "BlackMatter":
					obj.gather(toobj.node)
				else:
					obj.go(toobj.node)
			else:
				path = self.finder.pathFindToMouse()
				obj.go(path)
	
	def stop(self, obj):
		obj.stop()

class MainBase():
	def __init__(self, x, y, z,color,owner,parentLegion):
		
		self.myLegion = parentLegion
		
		self.type = "GameUnit"
		self.model = "models/mainbase/base.egg"
		self.uname = "base"
		self.name = "Main Base"
		#meshdrawer lifebar
		self.lifebar = False
		self.lifebarnode = False
		
		self.main = owner.attachNewNode("unit")
		self.main.setPos(x,y,z)
		
		self.origx = x
		self.origy = y
		
		self.n = self.main.attachNewNode("np")
		
		self.node = loader.loadModel(self.model)
		self.node.reparentTo(self.n)
		self.node.setTag("type", self.uname)
		
		
		self.colorFlag = self.node.find("**/colorFlagObj")
		self.materialFlag = Material("materialFlag")
		self.materialFlag.setDiffuse(color)
		self.colorFlag.setMaterial(self.materialFlag,1)
		self.colorFlag.setColor(Vec4(0.5,0.5,0.5,1))
		
		self.bradius = bradius = self.node.getBounds().getRadius()
		
		self.otherN = self.node.attachNewNode("otherThings")
		self.selector = loader.loadModel("images/selector.egg")
		self.selector.setLightOff()
		self.selector.reparentTo(self.otherN)
		self.selector.setZ(0.1)
		self.selector.setP(270)
		self.selector.setScale(bradius)
		self.otherN.hide()
		
		##unit properties
		#life
		self.totalLife = 400
		self.node.setPythonTag("hp", 400)
		self.node.setPythonTag("att", 0)
		self.node.setPythonTag("def", 1)
		
		#building lifebar
		amount = self.node.getPythonTag("hp")
		self.myLifeBar = MeshDrawer()
		self.myLifeBar.setBudget(amount/5)
		self.myLifeBarNode = self.myLifeBar.getRoot()
		self.myLifeBarNode.reparentTo(self.otherN)
		self.myLifeBarNode.setTexture(loader.loadTexture("images/stick_commander/lifebar.png"))
		self.myLifeBarNode.setLightOff(True)
		self.myLifeBar.begin(base.cam,render)
		for i in range(amount/10):
			self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0,0.5,0.5),0.035,Vec4(1,1,1,1))
		self.barBound = barBound = self.myLifeBarNode.getBounds().getRadius()
		self.myLifeBarNode.setX(-barBound+0.06)
		self.myLifeBarNode.setY(-bradius/2-0.35)
		self.myLifeBar.end()
		#end building lifebar
		
		#specific lists of unit build
		self.buildingUnit = False
		self.buildCurrent = False
		self.buildList = []
		
		self.costList = {
		"worker" : 50
		}
		
		self.timeList = {
		"worker" : 2
		}
		
		#AI object avoidance
		#aiWorld.addObstacle(self.main)
		
	def buildUnit(self, unit):
		#try to build a worker unit
		if self.myLegion.blackMatter >= self.costList[unit]:
			if self.buildingUnit == True:
				print unit+" ordered in sublist!"
				self.myLegion.addBM(self.costList[unit]*-1)
				self.buildList.append(unit)
			if self.buildingUnit == False:
				print unit+" ordered!"
				self.myLegion.addBM(self.costList[unit]*-1)
				task = taskMgr.doMethodLater(self.timeList[unit], self.createUnit, "ct", extraArgs = [unit])
				self.buildingUnit = True
	
	def createUnit(self, what):
		x = self.origx-self.barBound+0.06
		y = self.origy-self.bradius/2-0.35
		self.myLegion.addUnit(what,x,y)
		if len(self.buildList)>=1:
			what = self.buildList.pop(0)
			task = taskMgr.doMethodLater(self.timeList[what], self.createUnit, "ct", extraArgs=[what])
		if len(self.buildList)<1:
			self.buildingUnit = False
			self.buildCurrent = False
	
	def updateBarLife(self):
		currentLife = self.node.getPythonTag("hp")
		lifeColor = currentLife*100/self.totalLife
		#draw red life because unit is near death
		if lifeColor <= 33:
			self.myLifeBar.begin(base.cam,render)
			for i in range(currentLife/10):
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0.5,0,0.5,0.5),0.035,Vec4(1,1,1,1))
			for e in range(self.totalLife/10-currentLife/10):
				i += 1;
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			self.myLifeBar.end()
			
		if lifeColor > 33 and lifeColor < 66 :
			self.myLifeBar.begin(base.cam,render)
			for i in range(currentLife/10):
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0.5,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			for e in range(self.totalLife/10-currentLife/10):
				i += 1;
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			self.myLifeBar.end()
		if lifeColor >= 66:
			self.myLifeBar.begin(base.cam,render)
			for i in range(currentLife/10):
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0,0.5,0.5),0.035,Vec4(1,1,1,1))
			for e in range(self.totalLife/10-currentLife/10):
				i += 1;
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			self.myLifeBar.end()
	
	def giveDamage(self,amount):
		life = self.node.getPythonTag("hp")
		newlife = life - amount
		if newlife <= 0:
			#explosion sequence and remove
			int1 = Func(self.animDeath)
			int2 = Func(self.remove)
			seq1 = Sequence(int1,Wait(3.0),int2)
			seq1.start()
		else:
			self.node.setPythonTag("hp", newlife)
			messenger.send("commander-update", [self.uname, self])
			self.updateBarLife()
	
	def giveHeal(self,amount):
		life = self.node.getPythonTag("hp")
		newlife = life + amount
		if newlife >= self.totalLife:
			newlife = self.totalLife
		self.node.setPythonTag("hp", newlife)
		self.updateBarLife()
	
	def animDeath(self):
		#avoiding crashes when clearing scene and something is selected/not removed
		if self in mySelection.listConsideration:
			mySelection.listConsideration.remove(self)
		if(self in mySelection.listSelected):
			if len(mySelection.listSelected) == 1:
				myHudBuilder.clear()
			mySelection.listSelected.remove(self)
		if(self in mySelection.listLastSelected):
			mySelection.listLastSelected.remove(self)
		self.node.remove()
		
		self.p = ParticleEffect()
		self.p.loadConfig(Filename("images/fx/explosionSmoke.ptf"))
		self.p.setZ(3)
		self.p.setY(-2)
		self.p.setScale(self.bradius*0.5)
		self.p.start(self.main)
		
		
	def remove(self):
		if self in mySelection.listConsideration:
			mySelection.listConsideration.remove(self)
		if self in mySelection.listSelected:
			if len(mySelection.listSelected) == 1:
				myHudBuilder.clear()
			mySelection.listSelected.remove(self)
			
		if self in mySelection.listLastSelected:
			mySelection.listLastSelected.remove(self)
		#aiWorld.removeObstacle(self.node)
		self.main.remove()
		
class StickWorker():
	def __init__(self, x, y, z,color,owner,parentLegion):
		
		self.myLegion = parentLegion
		
		self.type = "GameUnit"
		self.model = "models/ometto/ometto.egg"
		self.uname = "worker"
		self.name = "Stick Worker"
		#meshdrawer lifebar
		self.lifebar = False
		self.lifebarnode = False
		
		self.main = owner.attachNewNode("unit")
		self.main.setPos(x,y,z)
		
		self.node = Actor (self.model, {
			'idle':'models/ometto/ometto-idle.egg',
			'run':'models/ometto/ometto-run.egg'
		})
		self.node.reparentTo(self.main)
		self.node.setTag("type", self.uname)
		
		self.materialFlag = Material("materialFlag")
		self.materialFlag.setDiffuse(color)
		self.node.setMaterial(self.materialFlag,1)
		
		self.bradius = bradius = self.node.getBounds().getRadius()
		
		#other things must have normal material and not reddish one
		self.normalFlag = Material("normalFlag")
		self.normalFlag.setDiffuse(Vec4(1,1,1,1))
		
		self.otherN = self.node.attachNewNode("otherThings")
		self.otherN.setMaterial(self.normalFlag,1)
		self.otherN.setCompass()
		self.selector = loader.loadModel("images/selector.egg")
		self.selector.setLightOff()
		self.selector.reparentTo(self.otherN)
		self.selector.setZ(0.1)
		self.selector.setP(270)
		self.selector.setScale(bradius-0.35)
		self.otherN.hide()
		
		##unit properties
		#life
		self.totalLife = 60
		self.node.setPythonTag("hp", 60)
		self.node.setPythonTag("att", 5)
		self.node.setPythonTag("def", 0)
		
		#building lifebar
		amount = self.node.getPythonTag("hp")
		self.myLifeBar = MeshDrawer()
		self.myLifeBar.setBudget(amount/5)
		self.myLifeBarNode = self.myLifeBar.getRoot()
		self.myLifeBarNode.reparentTo(self.otherN)
		self.myLifeBarNode.setTexture(loader.loadTexture("images/stick_commander/lifebar.png"))
		self.myLifeBarNode.setLightOff(True)
		self.myLifeBar.begin(base.cam,render)
		for i in range(amount/10):
			self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0,0.5,0.5),0.035,Vec4(1,1,1,1))
		barBound = self.myLifeBarNode.getBounds().getRadius()
		self.myLifeBarNode.setX(-barBound+0.06)
		self.myLifeBarNode.setY(-bradius/2)
		self.myLifeBar.end()
		#end building lifebar
		
		#currentstatus
		self.node.play('idle')
		
		#AI setting
		self.aiChar = AICharacter("aiunit"+str(self.node.getKey()), self.main, 50, 2, 4)
		aiWorld.addAiChar(self.aiChar)
		self.aiBe = self.aiChar.getAiBehaviors()
		
		self.waylist = []
		self.isFollowing = False
		
		self.isWalking = False
		self.isGathering = False
		self.isGatheringToBm = False
		self.isGatheringToBase = False
		self.hasRes = False
		self.bm = False
		self.nb = False
		
		taskMgr.add(self.update, "unitupdate")
		
	def debug(self):
		print "Unit debug info:"
		print "isWalking = " + str(self.isWalking)
		print "isGathering = " + str(self.isGathering)
		print "isGatheringToBm = " + str(self.isGatheringToBm)
		print "isGatheringToBase = " + str(self.isGatheringToBase)
		print "hasRes = " + str(self.hasRes)
		print "path state = " + self.aiBe.behaviorStatus("seek")
		
	def getNearestBase(self):
		ulist = self.myLegion.selectNameUnits("base")
		for unit in ulist:
			dist = math.sqrt(math.pow(unit.node.getX()+self.bm.getX(),2)+math.pow(unit.node.getY()+self.bm.getY(),2))
			if self.nb == False:
				self.nb = unit
			else:
				if dist < self.nb:
					self.nb = unit
		
	def updateBarLife(self):
		currentLife = self.node.getPythonTag("hp")
		lifeColor = currentLife*100/self.totalLife
		#draw red life because unit is near death
		if lifeColor <= 33:
			self.myLifeBar.begin(base.cam,render)
			for i in range(currentLife/10):
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0.5,0,0.5,0.5),0.035,Vec4(1,1,1,1))
			for e in range(self.totalLife/10-currentLife/10):
				i += 1;
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			self.myLifeBar.end()
			
		if lifeColor > 33 and lifeColor < 66 :
			self.myLifeBar.begin(base.cam,render)
			for i in range(currentLife/10):
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0.5,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			for e in range(self.totalLife/10-currentLife/10):
				i += 1;
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			self.myLifeBar.end()
		if lifeColor >= 66:
			self.myLifeBar.begin(base.cam,render)
			for i in range(currentLife/10):
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0,0.5,0.5),0.035,Vec4(1,1,1,1))
			for e in range(self.totalLife/10-currentLife/10):
				i += 1;
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			self.myLifeBar.end()
	
	def giveDamage(self,amount):
		life = self.node.getPythonTag("hp")
		newlife = life - amount
		if newlife <= 0:
			#explosion sequence and remove
			int1 = Func(self.animDeath)
			int2 = Func(self.remove)
			seq1 = Sequence(int1,Wait(3.0),int2)
			seq1.start()
		else:
			self.node.setPythonTag("hp", newlife)
			messenger.send("commander-update", [self.uname, self])
			self.updateBarLife()
	
	def giveHeal(self,amount):
		life = self.node.getPythonTag("hp")
		newlife = life + amount
		if newlife >= self.totalLife:
			newlife = self.totalLife
		self.node.setPythonTag("hp", newlife)
		self.updateBarLife()
	
	def animDeath(self):
		#avoiding crashes when clearing scene and something is selected/not removed
		if self in mySelection.listConsideration:
			mySelection.listConsideration.remove(self)
		if(self in mySelection.listSelected):
			if len(mySelection.listSelected) == 1:
				myHudBuilder.clear()
			mySelection.listSelected.remove(self)
		if(self in mySelection.listLastSelected):
			mySelection.listLastSelected.remove(self)
		self.node.remove()
		
		#TODO: death effect
	
	def gather(self, bm):
		self.bm = bm
		self.getNearestBase()
		self.go(bm)
		print "status: " + self.aiBe.behaviorStatus("pathfollow")
		self.isGathering = True
		self.isGatheringToBm = True
		
	def go(self,waylist):
		self.waylist = waylist
		print str(self.waylist)
		if len(waylist)==2:
			self.aiBe.removeAi("seek")
			self.aiBe.seek(self.waylist.pop(1))
		if len(waylist)>2:
			self.aiBe.removeAi("seek")
			self.aiBe.seek(self.waylist.pop(1))
			self.isFollowing = True
		if self.isWalking != True:
			self.node.loop("run")
		self.isWalking = True
	
	def move(self,way):
		self.aiBe.removeAi("seek")
		self.aiBe.seek(way)
		self.node.loop("run")
	
	def stop(self):
		self.node.pose("idle", 1)
	
	def update(self, task):
		action = False
		
		if self.isGathering == True:
			if self.aiBe.behaviorStatus("seek") == "done" or self.aiBe.behaviorStatus("seek") == "paused":
				if self.isGatheringToBm == True:
					if self.hasRes == False:
						if self.aiBe.behaviorStatus("seek") == "paused":
							self.aiBe.resumeAi("seek")
						self.hasRes = True
						self.isGatheringToBm = False
						self.isGatheringToBase = True
						self.go(self.nb.node)
						#just performed an action - do not do more
						action = True
				if self.isGatheringToBase == True and action == False:
					if self.hasRes == True:
						if self.aiBe.behaviorStatus("seek") == "paused":
							self.aiBe.resumeAi("seek")
						self.myLegion.addBM(5)
						self.hasRes = False
						self.isGatheringToBm = True
						self.isGatheringToBase = False
						self.go(self.bm)
		
		if self.isFollowing == True:
			if self.aiBe.behaviorStatus("seek") == "done":
				if len(self.waylist) >= 2:
					self.move(self.waylist.pop(1))
				if len(self.waylist) <= 1:
					self.waylist = []
					self.isFollowing = False
		
		if self.isWalking == True:
			if self.aiBe.behaviorStatus("seek") == "done":
				myEventManager.stop(self)
				self.isWalking = False
		if self.isWalking == False:
			if self.aiBe.behaviorStatus("seek") == "active":
				self.node.loop("run")
				self.isWalking = True
		return Task.cont
		
	def remove(self):
		if self in mySelection.listConsideration:
			mySelection.listConsideration.remove(self)
		if self in mySelection.listSelected:
			if len(mySelection.listSelected) == 1:
				myHudBuilder.clear()
			mySelection.listSelected.remove(self)
			
		if self in mySelection.listLastSelected:
			mySelection.listLastSelected.remove(self)
		
		#other
		aiWorld.removeAiChar("aiunit"+str(self.node.getKey()))
		self.main.remove()

