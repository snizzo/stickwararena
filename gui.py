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
		
	def show(self, type):
		if type == "main":
			self.mapNode = aspect2d.attachNewNode("mapNodeG")
			#background button
			self.background = DirectFrame(frameColor=(1, 1, 1, 1),frameSize=(-1, 1, -1, 1),)
			self.background['geom'] = loader.loadModel("images/background_main.egg")
			self.background['geom_scale'] = 2
			self.background.resetFrameSize()
			self.background.reparentTo(render2d)
			
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
		self.background.remove()
		self.mapNode.remove()

class HudBuilder():
	def __init__(self):
		self.pirulen = loader.loadFont("fonts/pirulen.ttf")
		self.miniImage = False
	
	def show(self):
		#looking for who you are
		
		for legion in myLegion:
			if legion.you == True:
				self.myLegion = legion
		
		self.hudNode = aspect2d.attachNewNode("hudNode")
		self.bgImage = render2d.attachNewNode("bgImage")
		
		self.displayInfo = self.hudNode.attachNewNode("displayInfo")
		
		self.resTL = TextNode("resTextLine")
		self.resTL.setText("nothing selected")
		self.resTL.setFont(self.pirulen)
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
		
		#initial res
		self.updateRes()
		
		#res text line should be present just before :)
		self.resTL_np.show()
		
		self.dTL = TextNode("debugTextLine")
		self.dTL.setText("nothing selected")
		self.dTL.setFont(self.pirulen)
		self.dTL.setAlign(TextNode.ACenter)
		self.dTL_np = self.displayInfo.attachNewNode(self.dTL)
		self.dTL_np.setScale(0.05)
		self.dTL_np.setPos(-0.15,0,-0.55)
		
		self.attTL = TextNode("attackTextLine")
		self.attTL.setFont(self.pirulen)
		self.attTL.setText("ccc")
		self.attTL_np = self.displayInfo.attachNewNode(self.attTL)
		self.attTL_np.setScale(0.04)
		self.attTL_np.setPos(-0.14,0,-0.81)
		self.attTL_np.hide()
		
		self.defTL = TextNode("defenceTextLine")
		self.defTL.setFont(self.pirulen)
		self.defTL.setText("defTL")
		self.defTL_np = self.displayInfo.attachNewNode(self.defTL)
		self.defTL_np.setScale(0.04)
		self.defTL_np.setPos(-0.14,0,-0.73)
		self.defTL_np.hide()
		
		self.hpTL = TextNode("healthTextLine")
		self.hpTL.setFont(self.pirulen)
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
	
	def setText(self, title):
		self.dTL.setText(title)
	
	def hide(self):
			self.bgImage.remove()
			self.hudNode.remove()
		
	def clear(self):
		self.OneButton.hide()
		self.setText("SCommander 1.0")
		self.hpTL_np.hide()
		self.attTL_np.hide()
		self.defTL_np.hide()
		if self.miniImage != False:
			self.miniImage.remove()
			self.miniImage = False
	
	def updateCommanderSelection(self):
		y = base.mouseWatcherNode.getMouseY()
		if y < -0.5:
			return
		#nothing selected
		if len(mySelection.listSelected) == 0:
			self.clear()
				
		#single element selected
		if len(mySelection.listSelected) == 1:
			obj = mySelection.listSelected[0]
			if obj.type == "GameUnit":
				#base hud
				if obj.uname == "base":
					self.clear()
					
					#loading miniImage Hud
					if self.miniImage != False:
						self.miniImage.remove()
						self.miniImage = False
					self.miniImage = loader.loadModel(obj.model)
					self.miniImage.setRenderModeWireframe()
					self.miniImage.setPos(-0.55,0,-0.82)
					self.miniImage.setP(16)
					self.miniImage.setScale(0.2)
					self.miniImage.reparentTo(self.displayInfo)
					self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
					
					#organizing other hud stuff
					self.setText(obj.name)
					#gathering information about current selected unit
					tLife = obj.totalLife
					cLife = obj.node.getPythonTag("hp")
					attack = obj.node.getPythonTag("att")
					defence = obj.node.getPythonTag("def")
					
					self.hpTL.setText("life: "+str(cLife)+"/"+str(tLife))
					self.hpTL_np.show()
					self.attTL.setText("damage: "+str(attack))
					self.attTL_np.show()
					self.defTL.setText("armor: "+str(defence))
					self.defTL_np.show()
					
					#base button order :)
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
					
					self.OneButton['relief'] = None
					self.OneButton['command'] = self.myLegion.buildUnit
					self.OneButton['extraArgs'] = (['worker'])
					self.OneButton.reparentTo(self.hudNode)
					
				if obj.uname == "worker":
					self.clear()
					
					#loading miniImage Hud
					if self.miniImage != False:
						self.miniImage.remove()
						self.miniImage = False
					self.miniImage = loader.loadModel(obj.model)
					self.miniImage.setRenderModeWireframe()
					self.miniImage.setPos(-0.55,0,-0.82)
					self.miniImage.setP(16)
					self.miniImage.setScale(0.2)
					self.miniImage.reparentTo(self.displayInfo)
					self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
					
					#organizing other hud stuff
					self.setText(obj.name)
					#gathering information about current selected unit
					tLife = obj.totalLife
					cLife = obj.node.getPythonTag("hp")
					attack = obj.node.getPythonTag("att")
					defence = obj.node.getPythonTag("def")
					
					self.hpTL.setText("life: "+str(cLife)+"/"+str(tLife))
					self.hpTL_np.show()
					self.attTL.setText("damage: "+str(attack))
					self.attTL_np.show()
					self.defTL.setText("armor: "+str(defence))
					self.defTL_np.show()
				
			if obj.type == "BlackMatter":
				#updating amount infos
				self.clear()
				later = obj.node.getPythonTag("amountT")
				now = obj.node.getPythonTag("amount")
				self.hpTL.setText("Res: "+str(now)+"/"+str(later))
				self.hpTL_np.show()
				#miniImage
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
			
	
	def updateRes(self):
			self.resTL.setText(str(self.myLegion.blackMatter))
	
	def update(self, what, obj):
		#base matter
		if what == "base":
			if len(mySelection.listSelected) > 0:
				if mySelection.listSelected[0] == obj:
					later = obj.totalLife
					now = obj.node.getPythonTag("hp")
					self.hpTL.setText("life: "+str(now)+"/"+str(later))
					
		if what == "resources":
			if len(mySelection.listSelected) > 0:
				if mySelection.listSelected[0] == obj:
					later = obj.node.getPythonTag("amountT")
					now = obj.node.getPythonTag("amount")
					self.hpTL.setText("Res: "+str(now)+"/"+str(later))
