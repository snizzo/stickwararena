# -*- coding: utf-8 -*-
'''
#from direct.showbase.DirectObject import DirectObject
#from panda3d.core import *
#from pandac.PandaModules import *

#from direct.particles.Particles import Particles
#from direct.particles.ParticleEffect import ParticleEffect
#from direct.interval.IntervalGlobal import *
#from direct.interval.FunctionInterval import Wait
#from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
#from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
#from panda3d.physics import LinearNoiseForce,DiscEmitter
#from panda3d.core import TextNode
#from panda3d.core import AmbientLight,DirectionalLight
#from panda3d.core import Point3,Vec3,Vec4
#from panda3d.core import Filename
#from direct.particles.Particles import Particles
#from direct.particles.ParticleEffect import ParticleEffect
#from direct.particles.ForceGroup import ForceGroup
#from direct.gui.OnscreenText import OnscreenText
#from direct.task import Task
#from direct.actor.Actor import Actor
#from panda3d.ai import *
'''
from PathFind import *

import sys,os,string,math, Queue#, copy

from enumeration import Enumeration
'''
class BaseEvents():
	def __init__(self):
		self.finder = PathFinder("maps/burning_sun/burning_sun_nav.egg")
		base.accept("mouse-order", self.go)
	
	def go(self):
		#if a unit is selected
		if len(mySelection.listSelected) == 1:
			#get the unit
			obj = mySelection.listSelected[0]
			#if currently under the mouse is there something like a NodePath (right-click selection)
			if len(mySelection.underMouse) == 1:
				to = mySelection.underMouse[0]
				#if the target is a blackmatter and the unit is a worker
				if to.type == "BlackMatter" and obj.uname == "worker":
					path = self.finder.pathFindToNode(to)
					obj.gather(to,path)
				else:
					path = self.finder.pathFindToNode(to)
					obj.go(path)
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
	
	def gather(self, bm, waylist):
		self.bm = bm
		self.getNearestBase()
		self.go(waylist)
		self.isGathering = True
		self.isGatheringToBm = True
		
	def go(self,waylist):
		self.waylist = waylist
		
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
						path = myEventManager.finder.pathFindBake(self,self.nb)
						self.go(path)
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
						path = myEventManager.finder.pathFindBake(self,self.bm)
						self.go(path)
		
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
'''
		
		
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

class Hud():

	def __init__(self, parent):
		self.parent = parent
		self.font = loader.loadFont("fonts/pirulen.ttf")
		#list of all buttons
		self.miniImage = False
		self.itemList = {}
		self.buttonList = {}
		
		self.hudNode = aspect2d.attachNewNode("unitHudNode")
		self.bgImage = render2d.attachNewNode("unitBgImage")
		self.displayInfo = self.hudNode.attachNewNode("displayInfo")
		
		#make standard hud
		self.setGrid()
	
	def setGrid(self, columns=3,cellsize=0.1,padding=2,xoff=0.70,yoff=-0.57):
		self.gridX = columns
		self.cellSize = cellsize
		self.gridPadding = padding
		self.xOffset = xoff
		self.yOffset = yoff
	
	def getNextCell(self):
		listLen = len(self.buttonList)
		cellNumber = listLen + 1
		if listLen == 0:
			x = 0
			y = 0
			pos = Vec3(x,0,y)
			return pos
		elif listLen > 0:
			cellRelXNumber = cellNumber % self.gridX
			cellRelYNumber = int(cellNumber / self.gridX)
			if cellNumber / self.gridX > cellRelYNumber:
				cellRelYNumber += 1
			x = (self.cellSize + self.gridPadding) * cellRelXNumber
			y = (self.cellSize + self.gridPadding) * cellRelYNumber
			pos = Vec3(x,0,y)
			return pos
	
	def showGrid(self):
		for button in self.buttonList:
			x = button.getX()
			z = button.getZ()
			button.setX(x+self.xOffset)
			button.setZ(z+self.zOffset)
	
	def loadImage(self, model, scale,z):
		self.miniImage = loader.loadModel(model)
		self.miniImage.setRenderModeWireframe()
		self.miniImage.setPos(-0.55,0,z)
		self.miniImage.setP(16)
		self.miniImage.setScale(scale)
		self.miniImage.reparentTo(self.displayInfo)
		self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
	
	def addTextLine(self,name,text,pos,scale,align=TextNode.ALeft):
		tl = TextNode(name)
		tl.setText(text)
		tl.setFont(self.font)
		tl.setAlign(align)
		tlnp = self.displayInfo.attachNewNode(tl)
		tlnp.setScale(scale)
		tlnp.setPos(pos)
		self.itemList[name] = tlnp
	
	def addButton(self,name):
		btg = loader.loadModel("images/stick_commander/"+name+"_button.egg")
		bt = DirectButton(geom = (
		btg.find('**/'+name),
		btg.find('**/'+name),
		btg.find('**/'+name),
		btg.find('**/'+name)))
		bt.resetFrameSize()
		self.bt.setScale(0.1)
		#getting nent cell position from directives
		pos = self.getNextCell()
		self.bt.setPos(pos)
		self.buttonList[name] = bt
		bt.hide()
	
	def addTitle(self, text):
		self.addTextLine("title", text, Vec3(-0.15,0,-0.55), 0.05, TextNode.ACenter)
	
	def makeStandard(self,scale,z):
		#adding title hud
		self.addTitle(self.parent.type)
		#print life string
		l = "life: " + str(self.parent.healthBar.getCurrentHealth()) + "/" + str(self.parent.healthBar.getTotalHealth())
		self.addTextLine("lifeString", l, Vec3(-0.14,0,-0.65),0.04)
		#print attack string
		a = "attack: " + str(self.parent.attack)
		self.addTextLine("attackString", a,Vec3(-0.14,0,-0.73),0.04)
		#print defence string
		d = "armor: " + str(self.parent.armor)
		self.addTextLine("armorString", d,Vec3(-0.14,0,-0.81),0.04)
		#image
		self.loadImage(self.parent.meshPath,scale,z)
	
	def show(self):
		#build button grid
		self.showGrid()
		self.hudNode.show()
		self.bgImage.show()
	
	def hide(self):
		for name, button in self.buttonList.iteritems():
			button.remove()
		for name, item in self.itemList.iteritems():
			item.remove()
		if self.miniImage:
			self.miniImage.remove()
			self.miniImage = False
		self.hudNode.hide()
		self.bgImage.hide()

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
class GameObject():
	def __init__ (self, x, y, z, _army):
		self.army = _army
		self.node = self.army.getNode().attachNewNode("gameobject")
		self.node.setPos(x, y, z)
		
	def isOwner(self):
		return self.army.getIsPlayer()
	
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
		if bool:
			self.showObjectHud()
			self.hud.show()
		else:
			self.hud.hide()
	
	def showHUD(self, bool = False):
		self.showGui(bool)
		self.showHealthBar(bool)
		self.showSelector(bool)
		
	#update the game object status
	def update(self, task):
		return task.cont
		
	#remove the game object from the game
	def destroy(self):
		#self.army.removeUnit(self)
		self.node.remove()
		
#basic structure class, not for Instantiation
class Structure(GameObject):
	def __init__(self, x, y, z, _army):
		self.spawnPoint = x, y, z
		self.mainType = "structure"
		self.creationQueue = Queue.Queue(5)
		self.queueBusy = False
		GameObject.__init__(self, x, y, z, _army)
		taskMgr.add(self.update, "creationQueue")
		
	#create a new unit of type <unitType> at location <spawnPoint> (note: <spawnPoint> is an instance variable)
	def createUnit(self, unitType):
		pass
		
	def addUnitToCreationQueue(self, unitType):
		if not self.creationQueue.full():
			self.creationQueue.put(unitType)
			#print str(unitType) + " added to queue"
			return True
		else:
			return False
		
	def update(self, task):
		if not self.creationQueue.empty() and not self.queueBusy:
			#print "started unit creation"
			self.createUnit(self.creationQueue.get())
			self.queueBusy = True
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
		#self.currentWayList = copy.copy(wayList)
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
		self.node.hprInterval(0.2, Vec3(requiredRotation,0,0),Vec3(nodeRotation,0,0)).start()
		
	#return needed node's angle to turn and face <point> target
	def getSteeringAngle(self, point):
		x = self.node.getX() - point.getX()
		y = self.node.getY() - point.getY()
		d = math.sqrt(x*x+y*y)
		if d != 0:
			h = 90 + math.degrees(math.asin(y/d))
		else:
			h = 90
		if x < 0:
			h = h * -1
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
		
#specialized structure class
class Base(Structure):
	def __init__(self, x, y, z, _army):
		Structure.__init__(self, x, y, z, _army)
		self.type = "base"
		self.unitType = Enumeration("unit", [("worker",5), ("soldier",5)])
		
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
		self.hud = Hud(self)
		
		#call the update coroutine
		#taskMgr.add(self.update, "structureupdate")
	
	def showObjectHud(self):
		print "specific hud"
	
	def hideObjectHud(self):
		print "specific hud"
	
	def createUnit(self, unitType):
		if unitType == self.unitType.worker:
			taskMgr.doMethodLater(self.unitType.__getattr__("worker"), self.createUnitDelayed, 'createUnit', extraArgs=[unitType], appendTask=True)
		elif unitType == self.unitType.soldier:
			taskMgr.doMethodLater(self.unitType.__getattr__("soldier"), self.createUnitDelayed, 'createUnit', extraArgs=[unitType], appendTask=True)
			
	def createUnitDelayed(self, unitType, task):
		if unitType == self.unitType.worker:
			self.army.addUnit(Worker(self.node.getX()+2, self.node.getY()+2, self.node.getZ(), self.army))
		elif unitType == self.unitType.soldier:
			self.army.addUnit(Soldier(self.node.getX()+2, self.node.getY()+2, self.node.getZ(), self.army))
		#print "unit created"
		self.queueBusy = False
		return task.done
			
	def getUnitType(self):
		return self.unitType

#specialized unit class	
class Worker(Unit):
	def __init__(self, x, y, z, _army):
		Unit.__init__(self, x, y, z, _army)
		self.type = "worker"
		self.unitType = Enumeration("structure", [])
		
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
		
		#create the gui
		self.hud = Hud(self)
		#creating
		
		#play the basic animation
		self.model.play('idle')
		
		#call the update coroutine
		taskMgr.add(self.update, "unitupdate")
	
	def showObjectHud(self):
		'''
		#adding title hud
		self.hud.addTitle(self.type)
		#print life string
		l = "life: " + str(self.healthBar.getCurrentHealth()) + "/" + str(self.healthBar.getTotalHealth())
		self.hud.addTextLine("lifeString", l, Vec3(-0.14,0,-0.65),0.04)
		#print attack string
		a = "attack: " + str(self.attack)
		self.hud.addTextLine("attackString", a,Vec3(-0.14,0,-0.73),0.04)
		#print defence string
		d = "armor: " + str(self.armor)
		self.hud.addTextLine("armorString", d,Vec3(-0.14,0,-0.81),0.04)
		'''
		self.hud.makeStandard(0.4,-0.89)
		
	#send the worker the gather the indicated <blackMatter> through the route indicated by <wayList>
	def gather(self, blackMatter, wayList):
		pass
		
	def buildStructure(self, structureType):
		pass
		

class Soldier(Unit):
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
		
	def showObjectHud(self):
		print "specific hud"
	
	def hideObjectHud(self):
		print "specific hud"
