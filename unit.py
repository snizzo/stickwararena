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
import sys,os,string

class Unit():
	def __init__(self, model, x, y, z,color,owner):
		self.type = "GameUnit"
		if model == "base":
			self.name = "Main Base"
			#meshdrawer lifebar
			self.lifebar = False
			self.lifebarnode = False
			
			self.main = owner.attachNewNode("unit")
			self.main.setPos(x,y,z)
			
			self.node = loader.loadModel("models/base.egg")
			self.node.reparentTo(self.main)
			self.node.setTag("type", model)
			
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
			self.node.setPythonTag("unitobj", self)
			
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
		self.myLifeBarNode.setY(-bradius/2-0.35)
		self.myLifeBar.end()
		#end building lifebar
			
	def updateBarLife(self):
		currentLife = self.node.getPythonTag("hp")
		lifeColor = currentLife*100/self.totalLife
		#draw red life because unit is near death
		if lifeColor <= 25:
			self.myLifeBar.begin(base.cam,render)
			for i in range(currentLife/10):
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0.5,0,0.5,0.5),0.035,Vec4(1,1,1,1))
			for e in range(self.totalLife/10-currentLife/10):
				i += 1;
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			self.myLifeBar.end()
			
		if lifeColor > 25 and lifeColor < 50 :
			self.myLifeBar.begin(base.cam,render)
			for i in range(currentLife/10):
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0.5,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			for e in range(self.totalLife/10-currentLife/10):
				i += 1;
				self.myLifeBar.billboard(Vec3(i*0.07,0,+0.15),Vec4(0,0.5,0.5,0.5),0.035,Vec4(1,1,1,1))
			self.myLifeBar.end()
		if lifeColor >= 50:
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
		if(self in mySelection.listSelected):
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
			mySelection.listSelected.remove(self)
		if self in mySelection.listLastSelected:
			mySelection.listLastSelected.remove(self)
		self.main.remove()
		
		
