# -*- coding: utf-8 -*-
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import LerpHprInterval
import sys

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

					
#fuckin' oop

class Hud():

	titlePosition = Vec3(0,0,-0.60)
	firstRowPosition = Vec3(-0.14,0,-0.70)
	secondRowPosition = Vec3(-0.14,0,-0.78)
	thirdRowPosition = Vec3(-0.14,0,-0.86)
	
	mainGui = False
	topGui = False
	
	@staticmethod
	def showGuiBackground(bool = False):
		if not Hud.mainGui:
			Hud.mainGui = DirectFrame(frameColor=(0, 0, 0, .9),frameSize=(-1, 1, -1, -0.5))
			Hud.mainGui.reparentTo(render2d)
		if not Hud.topGui:
			Hud.topGui = DirectFrame(frameColor=(0, 0, 0, .9),frameSize=(-1, 1, 0.95, 1))
			Hud.topGui.reparentTo(render2d)
		if bool:
			Hud.mainGui.show()
			Hud.topGui.show()
		else:
			Hud.mainGui.hide()
			Hud.topGui.hide()

	def __init__(self):
		self.font = loader.loadFont("fonts/pirulen.ttf")
		self.miniImage = False
		self.itemList = {}
		self.buttonList = {}
		
		self.actualMeshPath = ""
		
		self.hudNode = aspect2d.attachNewNode("unitHudNode")
		self.bgImage = render2d.attachNewNode("unitBgImage")
		self.displayInfo = self.hudNode.attachNewNode("displayInfo")
		self.buttons = self.hudNode.attachNewNode("buttons")
		
		#make standard hud
		self.setGrid()
		
		self.addTextLine("titleString", "", Hud.titlePosition, 0.05, TextNode.ACenter)
		self.addTextLine("healthString", "", Hud.firstRowPosition, 0.04)
		
		self.hide()
		
	def setGrid(self, columns = 3, cellsize = 0.1, padding = 2, xoff = 0.70, yoff = -0.57):
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
		elif listLen > 0:
			cellRelXNumber = cellNumber % self.gridX
			cellRelYNumber = int(cellNumber / self.gridX)
			if cellNumber / self.gridX > cellRelYNumber:
				cellRelYNumber += 1
			x = (self.cellSize + self.gridPadding) * cellRelXNumber
			y = (self.cellSize + self.gridPadding) * cellRelYNumber
		return Vec3(x,0,y)
		
	def addTextLine(self, name, text, pos, scale, align = TextNode.ALeft):
		tl = TextNode(name)
		tl.setText(text)
		tl.setFont(self.font)
		tl.setAlign(align)
		tlnp = self.displayInfo.attachNewNode(tl)
		tlnp.setScale(scale)
		tlnp.setPos(pos)
		self.itemList[name] = tlnp
	
	def setTitle(self, parent):
		self.itemList['titleString'].getNode(0).setText(parent.getType())
	
	def setTextLine(self, parent):
		self.setTitle(parent)
		s = "life: " + str(parent.getHealthBar().getCurrentHealth()) + "/" + str(parent.getHealthBar().getTotalHealth())
		self.itemList['healthString'].getNode(0).setText(s)
		
	def loadImage(self, model, scale, z):
		if self.actualMeshPath != model:
			if self.miniImage:
				self.miniImage.remove()
			self.miniImage = False
			self.actualMeshPath = model
			self.miniImage = loader.loadModel(self.actualMeshPath)
			self.miniImage.setRenderModeWireframe()
			self.miniImage.setPos(-0.55,0,z)
			self.miniImage.setP(16)
			self.miniImage.setScale(scale)
			self.miniImage.reparentTo(self.displayInfo)
			self.miniImage.hprInterval(10, Vec3(360,16,0)).loop()
		
	def show(self, parent = False, scale = 1.0, z = 0.0):
		if parent:
			self.loadImage(parent.getMeshPath(), scale, z)
			self.setTextLine(parent)
		self.hudNode.show()
		self.bgImage.show()
		
	def hide(self):
		self.hudNode.hide()
		self.bgImage.hide()
		
		
class MultipleHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		
	def show(self, unitNumber):
		self.itemList['titleString'].getNode(0).setText(str(unitNumber) + " units selected")
		Hud.show(self) 
	
		
class WorkerHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		self.addTextLine("attackString", "", Hud.secondRowPosition, 0.04)
		self.addTextLine("armorString", "", Hud.thirdRowPosition, 0.04)
		
		btg = loader.loadModel("images/stick_commander/worker_button.egg")
		bt = DirectButton(geom = (
		btg.find('**/worker'),
		btg.find('**/worker'),
		btg.find('**/worker'),
		btg.find('**/worker')))
		bt.resetFrameSize()
		bt.setScale(0.1)
		bt.reparentTo(self.buttons)
		#getting next cell position from directives
		pos = self.getNextCell()
		bt.setPos(pos)
		bt['relief'] = None
		bt['command'] = None
		bt['extraArgs'] =  None
		self.buttonList['base'] = bt
		
		for key, button in self.buttonList.iteritems():
			x = button.getX()
			y = button.getZ()
			button.setX(x+self.xOffset)
			button.setZ(y+self.yOffset)
		
	def setTextLine(self, parent):
		Hud.setTextLine(self, parent)
		s = "attack: " + str(parent.getAttack())
		self.itemList['attackString'].getNode(0).setText(s)
		s = "armor: " + str(parent.getArmor())
		self.itemList['armorString'].getNode(0).setText(s)
		
	def show(self, parent, scale, z):
		if parent.isOwner():
			self.buttons.show()
			self.setButton(parent)
		else:
			self.buttons.hide()
		self.setTextLine(parent)
		Hud.show(self, parent, scale, z)
		
	def setButton(self, parent):
		self.buttonList['base']['command'] = parent.buildStructure
		self.buttonList['base']['extraArgs'] = ([parent.getStructureType().base])
		
class SoldierHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		self.addTextLine("attackString", "", Hud.secondRowPosition, 0.04)
		self.addTextLine("armorString", "", Hud.thirdRowPosition, 0.04)
		
		for key, button in self.buttonList.iteritems():
			x = button.getX()
			y = button.getZ()
			button.setX(x+self.xOffset)
			button.setZ(y+self.yOffset)
		
	def setTextLine(self, parent):
		Hud.setTextLine(self, parent)
		s = "attack: " + str(parent.getAttack())
		self.itemList['attackString'].getNode(0).setText(s)
		s = "armor: " + str(parent.getArmor())
		self.itemList['armorString'].getNode(0).setText(s)
		
	def show(self, parent, scale, z):
		self.setTextLine(parent)
		Hud.show(self, parent, scale, z)
		
class BlackMatterHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		self.addTextLine("resourceString", "", Hud.firstRowPosition, 0.04)
		
	def setTextLine(self, parent):
		self.setTitle(parent)
		s = "resource: " + str(parent.getResource()) + "/" + str(parent.getTotalResource())
		self.itemList['resourceString'].getNode(0).setText(s)
		
	def show(self, parent, scale, z):
		self.setTextLine(parent)
		Hud.show(self, parent, scale, z)

class BaseHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		
		self.addTextLine("armorString", "", Hud.thirdRowPosition, 0.04)
		
		btg = loader.loadModel("images/stick_commander/worker_button.egg")
		bt = DirectButton(geom = (
		btg.find('**/worker'),
		btg.find('**/worker'),
		btg.find('**/worker'),
		btg.find('**/worker')))
		bt.resetFrameSize()
		bt.setScale(0.1)
		bt.reparentTo(self.buttons)
		#getting next cell position from directives
		pos = self.getNextCell()
		bt.setPos(pos)
		bt['relief'] = None
		bt['command'] = None
		bt['extraArgs'] =  None
		self.buttonList['worker'] = bt
		
		for key, button in self.buttonList.iteritems():
			x = button.getX()
			y = button.getZ()
			button.setX(x+self.xOffset)
			button.setZ(y+self.yOffset)
		
	def setTextLine(self, parent):
		Hud.setTextLine(self, parent)
		s = "armor: " + str(parent.getArmor())
		self.itemList['armorString'].getNode(0).setText(s)
		
	def show(self, parent, scale, z):
		if parent.isOwner():
			self.buttons.show()
			self.setButton(parent)
		else:
			self.buttons.hide()
		self.setTextLine(parent)
		Hud.show(self, parent, scale, z)
		
	def setButton(self, parent):
		self.buttonList['worker']['command'] = parent.addUnitToCreationQueue
		self.buttonList['worker']['extraArgs'] = ([parent.getUnitType().worker])
		
