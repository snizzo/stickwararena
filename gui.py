# -*- coding: utf-8 -*-
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import LerpHprInterval
import __builtin__, sys

class PopupBuilder():
	def __init__(self):
		pass
		
	def sendResponse(self, response):
		if(response):
			messenger.send("goToMainMenu", ['game'])
		self.dialog.cleanup()
		self.dialog.remove()
		
	def show(self):
		self.dialog = YesNoDialog(dialogName="exitPopup", text="Are you sure?", command=self.sendResponse)
		
	def hide(self):
		self.dialog.remove()

class MenuBuilder():
	def __init__(self):
		pass
		
	def show(self, type):
		if type == "main":
			self.mapNode = aspect2d.attachNewNode("mapNodeG")
			#background button
			self.background = loader.loadModel("images/background_main.egg")
			self.background.reparentTo(self.mapNode)
			
			#single player button (animated)
			self.spButtonGeom = loader.loadModel("images/beyourhero.egg")
			
			self.spButton = DirectButton(geom = (
			self.spButtonGeom.find('**/beyourhero_ready'),
			self.spButtonGeom.find('**/beyourhero_click'),
			self.spButtonGeom.find('**/beyourhero_rollover'),
			self.spButtonGeom.find('**/beyourhero_disabled')))
			self.spButton.resetFrameSize()
			
			self.spButton['relief'] = None
			self.spButton['command'] = messenger.send
			self.spButton['extraArgs'] = (['startSingle'])
			self.spButton.setX(-0.68)
			self.spButton.setZ(0.21)
			self.spButton.reparentTo(self.mapNode)
			
			#configuration button (animated)
			self.cfgButtonGeom = loader.loadModel("images/configure.egg")
			
			self.cfgButton = DirectButton(geom = (
			self.cfgButtonGeom.find('**/configure_ready'),
			self.cfgButtonGeom.find('**/configure_click'),
			self.cfgButtonGeom.find('**/configure_rollover'),
			self.cfgButtonGeom.find('**/configure_disabled')))
			self.cfgButton.resetFrameSize()
			
			self.cfgButton['relief'] = None
			self.cfgButton['command'] = sys.exit
			self.cfgButton.setX(0.68)
			self.cfgButton.setZ(0.21)
			self.cfgButton.reparentTo(self.mapNode)
			
			#multi player button (animated)
			self.mpButtonGeom = loader.loadModel("images/worldwidewar.egg")
			
			self.mpButton = DirectButton(geom = (
			self.mpButtonGeom.find('**/worldwidewar_ready'),
			self.mpButtonGeom.find('**/worldwidewar_click'),
			self.mpButtonGeom.find('**/worldwidewar_rollover'),
			self.mpButtonGeom.find('**/worldwidewar_disabled')))
			self.mpButton.resetFrameSize()
			
			self.mpButton['relief'] = None
			self.mpButton['command'] = sys.exit
			self.mpButton.setX(-0.64)
			self.mpButton.setZ(-0.55)
			self.mpButton.reparentTo(self.mapNode)
			
			#exit button (animated)
			self.exitButtonGeom = loader.loadModel("images/surrender.egg")
			
			self.exitButton = DirectButton(geom = (
			self.exitButtonGeom.find('**/surrender_ready'),
			self.exitButtonGeom.find('**/surrender_click'),
			self.exitButtonGeom.find('**/surrender_rollover'),
			self.exitButtonGeom.find('**/surrender_disabled')))
			self.exitButton.resetFrameSize()
			
			self.exitButton['relief'] = None
			self.exitButton['command'] = sys.exit
			self.exitButton.setX(0.64)
			self.exitButton.setZ(-0.55)
			self.exitButton.reparentTo(self.mapNode)
	
	def hide(self):
		self.mapNode.remove()

class HudBuilder():
	def __init__(self):
		self.pirulen = loader.loadFont("fonts/pirulen.ttf")
		self.miniImage = False
		
		base.accept("mouse-selection", self.updateCommanderSelection)
	
	def show(self):
		self.hudNode = aspect2d.attachNewNode("hudNode")
		self.bgImage = self.hudNode.attachNewNode("bgImage")
		
		self.mainCmd = loader.loadModel("images/stick_commander/commander.egg")
		self.mainCmd.setZ(-0.74)
		self.mainCmd.reparentTo(self.bgImage)
		
		self.displayInfo = self.hudNode.attachNewNode("displayInfo")
		self.dTL = TextNode("debugTextLine")
		self.dTL.setText("nothing selected")
		self.dTL.setFont(self.pirulen)
		self.dTL.setAlign(TextNode.ACenter)
		self.dTL_np = self.displayInfo.attachNewNode(self.dTL)
		self.dTL_np.setScale(0.05)
		self.dTL_np.setPos(-0.15,0,-0.55)
	
	def setText(self, title):
		self.dTL.setText(title)
	
	def hide(self):
		if(self.hudNode):
			self.hudNode.remove()
		
	
	def updateCommanderSelection(self):
		#nothing selected
		if len(mySelection.listSelected) == 0:
			self.setText("SCommander 1.0")
			if self.miniImage != False:
				self.miniImage.remove()
				self.miniImage = False
				
		#single element selected
		if len(mySelection.listSelected) == 1:
			obj = mySelection.listSelected[0]
			if obj.type == "GameUnit":
				if self.miniImage != False:																													 
					self.miniImage.remove()
					self.miniImage = False
				self.setText(obj.name)
				self.miniImage = loader.loadModel("models/base.egg")
				self.miniImage.setRenderModeWireframe()
				self.miniImage.setPos(-0.55,0,-0.82)
				self.miniImage.setP(16)
				self.miniImage.setScale(0.2)
				self.miniImage.reparentTo(self.displayInfo)
				self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
				#base button order :)
				#TODO
			if obj.type == "BlackMatter":
				if self.miniImage != False:																													 
					self.miniImage.remove()
					self.miniImage = False
				self.setText(obj.name)
				self.miniImage = loader.loadModel("models/blob/blob.egg")
				self.miniImage.setRenderModeWireframe()
				self.miniImage.setPos(-0.55,0,-0.82)
				self.miniImage.setP(16)
				self.miniImage.setScale(0.09)
				self.miniImage.reparentTo(self.displayInfo)
				self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
				
		if len(mySelection.listSelected) > 1:
			self.setText(str(len(mySelection.listSelected)) + " selected units")
	
	'''
	def damageUnit(self):
		unitNode = objSelectionTool.listSelected[0]
		uobj = unitNode.getPythonTag("unitobj")
		uobj.giveDamage(10)
	
	def changeText(self, text):
		self.dTL.setText(text)
	
	def destroyCommander(self):
		self.mainCmd.remove()
		self.displayInfo.remove()
	'''
