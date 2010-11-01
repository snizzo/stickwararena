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
		self.dialog = YesNoDialog(dialogName="exitPopup", text="Are you sure?", command=self.sendResponse, fadeScreen = True)
		
	def hide(self):
		self.dialog.remove()

class MenuBuilder():
	def __init__(self):
		pass
	
	#function used to fast make a button from a predrawn set of images
	def makeBigButton(self, name, message, x,z,parent):
		buttonGeom = loader.loadModel("images/"+name+".egg")
		
		button = DirectButton(geom = (
		buttonGeom.find('**/'+name+'_ready'),
		buttonGeom.find('**/'+name+'_click'),
		buttonGeom.find('**/'+name+'_rollover'),
		buttonGeom.find('**/'+name+'_disabled')))
		button.resetFrameSize()
		
		button['relief'] = None
		#command executed when pressed the button
		button['command'] = messenger.send
		button['extraArgs'] = ([message])
		button.setX(x)
		button.setZ(z)
		button.reparentTo(parent)
	
	def showMainMenu(self):
		self.mapNode = aspect2d.attachNewNode("mapNodeG")
		#background button
		self.background = DirectFrame(frameColor=(1, 1, 1, 1),frameSize=(-1, 1, -1, 1),)
		self.background['geom'] = loader.loadModel("images/background_main.egg")
		self.background['geom_scale'] = 2
		self.background.resetFrameSize()
		self.background.reparentTo(render2d)
		
		#building buttons
		# (name, event sent via messenger, x, z, parent node)
		self.makeBigButton("beyourhero", "startSingle", -0.68, 0.21, self.mapNode)
		self.makeBigButton("configure", "exitGame", 0.68, 0.21, self.mapNode)
		self.makeBigButton("worldwidewar", "exitGame", -0.64, -0.55, self.mapNode)
		self.makeBigButton("surrender", "exitGame", 0.64, -0.55, self.mapNode)
	
	def hide(self):
		self.background.remove()
		self.mapNode.remove()

class HudBuilder():
	def __init__(self):
		#loading HUD specific font
		self.font = loader.loadFont("fonts/pirulen.ttf")
		#image used to show what you have selected
		self.loadedImage = False
		self.lastSelectedObj = False
	
	def show(self):
		#looking for who you are
		
		for legion in myLegion:
			if legion.getIsPlayer():
				self.myLegion = legion
		
		self.hudNode = aspect2d.attachNewNode("hudNode")
		self.bgImage = render2d.attachNewNode("bgImage")
		
		self.displayInfo = self.hudNode.attachNewNode("displayInfo")
		
		self.resTL = TextNode("resTextLine")
		self.resTL.setText("nothing selected")
		self.resTL.setFont(self.font)
		self.resTL.setAlign(TextNode.ALeft)
		self.resTL_np = self.displayInfo.attachNewNode(self.resTL)
		self.resTL_np.setScale(0.037)
		self.resTL_np.setPos(-0.25,0,0.965)
		self.resTL_np.hide()
		
		base.accept("mouse-selection", self.updateCommanderSelection)
		base.accept("commander-update", self.update)
		base.accept("res-updated", self.updateRes)
		
		self.mainCmd = DirectFrame(frameColor=(0, 0, 0, .9),frameSize=(-1, 1, -1, -0.5))
		self.mainCmd.reparentTo(self.bgImage)
		
		self.topBar = DirectFrame(frameColor=(0, 0, 0, .9),frameSize=(-1, 1, 0.95, 1))
		self.topBar.reparentTo(self.bgImage)
		
		#resources
		self.resourceIcon = loader.loadModel("images/stick_commander/blackmatter.egg")
		self.resourceIcon.setScale(0.04)
		self.resourceIcon.setX(-0.3)
		self.resourceIcon.setZ(0.975)
		self.resourceIcon.reparentTo(self.hudNode)
		
		#update initial resources
		self.updateRes()
		
		#res text line should be present just before :)
		self.resTL_np.show()
		
		self.dTL = TextNode("debugTextLine")
		self.dTL.setText("nothing selected")
		self.dTL.setFont(self.font)
		self.dTL.setAlign(TextNode.ACenter)
		self.dTL_np = self.displayInfo.attachNewNode(self.dTL)
		self.dTL_np.setScale(0.05)
		self.dTL_np.setPos(-0.15,0,-0.55)
		
		self.attTL = TextNode("attackTextLine")
		self.attTL.setFont(self.font)
		self.attTL.setText("ccc")
		self.attTL_np = self.displayInfo.attachNewNode(self.attTL)
		self.attTL_np.setScale(0.04)
		self.attTL_np.setPos(-0.14,0,-0.81)
		self.attTL_np.hide()
		
		self.defTL = TextNode("defenceTextLine")
		self.defTL.setFont(self.font)
		self.defTL.setText("defTL")
		self.defTL_np = self.displayInfo.attachNewNode(self.defTL)
		self.defTL_np.setScale(0.04)
		self.defTL_np.setPos(-0.14,0,-0.73)
		self.defTL_np.hide()
		
		self.hpTL = TextNode("healthTextLine")
		self.hpTL.setFont(self.font)
		self.hpTL.setText("hpTL")
		self.hpTL_np = self.displayInfo.attachNewNode(self.hpTL)
		self.hpTL_np.setScale(0.04)
		self.hpTL_np.setPos(-0.14,0,-0.65)
		self.hpTL_np.hide()
		
		#hud buttons
		self.OneButtonGeom = loader.loadModel("images/stick_commander/worker_button.egg")
		
		self.OneButton = DirectButton(geom = (
		self.OneButtonGeom.find('**/worker'),
		self.OneButtonGeom.find('**/worker'),
		self.OneButtonGeom.find('**/worker'),
		self.OneButtonGeom.find('**/worker')))
		self.OneButton.resetFrameSize()
		self.OneButton.hide()
		
		self.TwoButtonGeom = loader.loadModel("images/stick_commander/worker_button.egg")
		
		self.TwoButton = DirectButton(geom = (
		self.TwoButtonGeom.find('**/worker'),
		self.TwoButtonGeom.find('**/worker'),
		self.TwoButtonGeom.find('**/worker'),
		self.TwoButtonGeom.find('**/worker')))
		self.TwoButton.resetFrameSize()
		self.TwoButton.hide()
	
	def loadImage(self, model, scale):
		#do not load it twice
		white = Material()
		#white.setShininess(5.0) #Make this material shiny
		white.setAmbient(VBase4(1,1,1,1)) #Make this material blue
		
		if self.loadedImage == False:
			self.clear()
			#load it
			self.miniImage = loader.loadModel(model)
			self.miniImage.setRenderModeWireframe()
			self.miniImage.setPos(-0.55,0,-0.82)
			self.miniImage.setP(16)
			self.miniImage.setScale(scale)
			self.miniImage.clearTexture()
			self.miniImage.setColor(1,1,1,1)
			self.miniImage.setMaterial(white)
			self.miniImage.reparentTo(self.displayInfo)
			self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
			self.loadedImage = True
			#store last selected object
			#self.lastSelectedObj = mySelection.getSingleSelected()
			self.lastSelectedObj = myGroup.getSingleUnit()
			
		#if self.lastSelectedObj != mySelection.getSingleSelected():
		if self.lastSelectedObj != myGroup.getSingleUnit():
			#clear
			self.clear()
			#load it
			if self.loadedImage != False:
				self.miniImage.remove()
			self.miniImage = loader.loadModel(model)
			self.miniImage.setRenderModeWireframe()
			self.miniImage.setPos(-0.55,0,-0.82)
			self.miniImage.setP(16)
			self.miniImage.setScale(scale)
			self.miniImage.clearTexture()
			self.miniImage.setMaterial(white)
			self.miniImage.reparentTo(self.displayInfo)
			self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
			self.loadedImage = True
			#store last selected object
			#self.lastSelectedObj = mySelection.getSingleSelected()
			self.lastSelectedObj = myGroup.getSingleUnit()
	
	def setText(self, title):
		self.dTL.setText(title)
	
	def hide(self):
			self.bgImage.remove()
			self.hudNode.remove()
		
	def clear(self):
		self.OneButton.hide()
		self.TwoButton.hide()
		self.setText("SCommander 1.0")
		self.hpTL_np.hide()
		self.attTL_np.hide()
		self.defTL_np.hide()
		if self.loadedImage == True:
			self.miniImage.remove()
			self.loadedImage = False
	
	def updateCommanderSelection(self):
		#getting 2D coordinate
		y = base.mouseWatcherNode.getMouseY()
		#if mouse is in the HUD don't selected and load selection
		if y < -0.5:
			return
		'''
		#if nothing selected clear HUD
		if len(mySelection.listSelected) == 0:
			self.clear()
			mySelection.group.clear()
				
		#if one single element selected
		if len(mySelection.listSelected) == 1:
			obj = mySelection.getSingleSelected()
			if obj.type == "base":
				self.makeBaseHud()
			if obj.type == "worker" or obj.type == "soldier":
				self.makeWorkerHud()
		
		#if more than one is selected
		if len(mySelection.listSelected) > 1:
			self.setText(str(len(mySelection.listSelected)) + " selected units")
		'''
		if myGroup.emptySelection():
			self.clear()
		elif myGroup.singleUnit():
			unit = myGroup.getSingleUnit()
			if unit.type == "base":	
				self.makeBaseHud()
			elif unit.type == "worker" or unit.type == "soldier":
				self.makeWorkerHud()
			else:
				self.setText(str(myGroup.getUnitNumber()) + " selected units")
		
	def makeResourceHud(self):
		obj = mySelection.getSingleSelected()
		#updating amount infos
		later = obj.node.getPythonTag("amountT")
		now = obj.node.getPythonTag("amount")
		self.hpTL.setText("Res: "+str(now)+"/"+str(later))
		self.hpTL_np.show()
		#setting main text
		self.setText(obj.name)
		#load image
		self.loadImage("models/blob/blob.egg", 0.09)
	
	def makeWorkerHud(self):
		#obj = mySelection.getSingleSelected()
		obj = myGroup.getSingleUnit()
		#loading miniImage Hud
		self.loadImage(obj.meshPath,0.2)
		
		#organizing other hud stuff
		self.setText("Stick Worker")
		#gathering information about current selected unit
		tLife = obj.healthBar.getTotalHealth()
		cLife = obj.healthBar.getCurrentHealth()
		attack = "5"   #to define it in UNIT class lately
		defence = "1"  #to define it in UNIT class lately
		
		self.hpTL.setText("life: "+str(cLife)+"/"+str(tLife))
		self.hpTL_np.show()
		self.attTL.setText("damage: "+str(attack))
		self.attTL_np.show()
		self.defTL.setText("armor: "+str(defence))
		self.defTL_np.show()
	
	def makeBaseHud(self):
		#obj = mySelection.getSingleSelected()
		obj = myGroup.getSingleUnit()
		#loading miniImage Hud
		self.loadImage(obj.meshPath,0.2)
		
		#organizing other hud stuff
		self.setText("Main Base")
		#gathering information about current selected unit
		tLife = obj.healthBar.getTotalHealth()
		cLife = obj.healthBar.getCurrentHealth()
		attack = "0"   #to define it in UNIT class lately, anyway not used in structure
		defence = "1"  #to define it in UNIT class lately
		
		self.hpTL.setText("life: "+str(cLife)+"/"+str(tLife))
		self.defTL.setText("armor: "+str(defence))
		self.hpTL_np.show()
		self.defTL_np.show()
		
		#base button construction
		self.OneButtonGeom = loader.loadModel("images/stick_commander/worker_button.egg")
		
		self.OneButton = DirectButton(geom = (
		self.OneButtonGeom.find('**/worker'),
		self.OneButtonGeom.find('**/worker'),
		self.OneButtonGeom.find('**/worker'),
		self.OneButtonGeom.find('**/worker')))
		self.OneButton.resetFrameSize()
		self.OneButton.setScale(0.1)
		self.OneButton.setX(0.75)
		self.OneButton.setZ(-0.57)
		self.OneButton.show()
		
		#send myLegion specific build command:
		self.OneButton['relief'] = None
		base = self.myLegion.getStructureAt(0)
		self.OneButton['command'] = base.addUnitToCreationQueue
		self.OneButton['extraArgs'] = ([base.getUnitType().worker])
		self.OneButton.reparentTo(self.hudNode)
		
		#soldier button construction
		self.TwoButtonGeom = loader.loadModel("images/stick_commander/worker_button.egg")
		
		self.TwoButton = DirectButton(geom = (
		self.TwoButtonGeom.find('**/worker'),
		self.TwoButtonGeom.find('**/worker'),
		self.TwoButtonGeom.find('**/worker'),
		self.TwoButtonGeom.find('**/worker')))
		self.TwoButton.resetFrameSize()
		self.TwoButton.setScale(0.1)
		self.TwoButton.setX(0.85)
		self.TwoButton.setZ(-0.57)
		self.TwoButton.show()
		
		#send myLegion specific build command:
		self.TwoButton['relief'] = None
		base = self.myLegion.getStructureAt(0)
		self.TwoButton['command'] = base.addUnitToCreationQueue
		self.TwoButton['extraArgs'] = ([base.getUnitType().soldier])
		self.TwoButton.reparentTo(self.hudNode)
	
	def updateRes(self):
			self.resTL.setText(str(self.myLegion.blackMatter))
	
	def update(self, what, obj):
		#base
		if what == "base":
			if len(mySelection.listSelected) > 0:
				if mySelection.listSelected[0] == obj:
					later = obj.totalLife
					now = obj.node.getPythonTag("hp")
					self.hpTL.setText("life: "+str(now)+"/"+str(later))
		#blackmatter
		if what == "resources":
			if len(mySelection.listSelected) > 0:
				if mySelection.listSelected[0] == obj:
					later = obj.node.getPythonTag("amountT")
					now = obj.node.getPythonTag("amount")
					self.hpTL.setText("Res: "+str(now)+"/"+str(later))
