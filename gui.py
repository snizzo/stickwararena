# -*- coding: utf-8 -*-
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.LerpInterval import LerpHprInterval
from direct.interval.IntervalGlobal import *
from camera import Mouse
import sys, __builtin__

class Message():
	def __init__(self, title, message = "", duration = 5.0):
		self.title = title
		self.message = message
		self.duration = duration
		
	def getTitle(self):
		return self.title
		
	def getMessage(self):
		return self.message
	
	def getDuration(self):
		return self.duration

class Messages():
	
	defaultXPos = 0.95
	defaultYPos = 0.85
	maxYPos = 10
	defaultXInc = -0.2
	defaultYInc = -0.13
	fadeInTime = 1
	fadeOutTime = 1
	
	def __init__(self):
		self.node = render2d.attachNewNode("messagesNode")
		self.font = loader.loadFont("fonts/freesans.ttf")
		self.XPosition = 0
		self.YPosition = 0
		self.messages = []
		
	def addMessage(self, _message):
		node = self.node.attachNewNode("message")
		node.hide()
		node.setScale(0.05)
		
		title = TextNode("title")
		title.setFont(self.font)
		title.setAlign(TextNode.ARight)
		titlePath = node.attachNewNode(title)
		title.setText(_message.getTitle())
		titlePath.setScale(0.9)
		
		message = TextNode("message")
		message.setFont(self.font)
		message.setAlign(TextNode.ARight)
		messagePath = node.attachNewNode(message)
		message.setText(_message.getMessage())
		messagePath.setZ(messagePath.getZ() - 1)
		messagePath.setScale(0.8)
		
		if title.getWidth() >= message.getWidth():
			title.setFrameAsMargin(0.2,0.3,1.2,-0.3)
			title.setFrameColor(0, 0, 0, 0.5)
			title.setCardColor(0, 0, 0, 0.5)
			title.setCardAsMargin(0.2,0.3,1.2,-0.3)
			title.setCardDecal(True)
			messagePath.setY(-1)
		else:
			message.setFrameAsMargin(0.2,0.3,0.2,1)
			message.setFrameColor(0, 0, 0, 0.5)
			message.setCardColor(0, 0, 0, 0.5)
			message.setCardAsMargin(0.2,0.3,0.2,1)
			message.setCardDecal(True)
			titlePath.setY(-1)

		self.messages.append(node)
		node.show()
		taskMgr.add(self.showMessage, "sequence", extraArgs = [_message, node], appendTask = True)
		self.update()
		
	def update(self):
		self.XPosition = 0
		self.YPosition = 0
		for message in self.messages:
			message.setPos(self.getNextPosition())
			
	def showMessage(self, message, node, task):
		if task.time < Messages.fadeInTime:
			node.setAlphaScale(task.time / Messages.fadeInTime)
		elif task.time < Messages.fadeInTime + message.getDuration():
			node.setAlphaScale(1.0)
		elif task.time < Messages.fadeInTime + message.getDuration() + Messages.fadeOutTime:
			node.setAlphaScale(1 - (task.time - message.getDuration() - Messages.fadeInTime) / Messages.fadeOutTime)
		else:
			self.removeMessage(node)
			return task.done
		return task.cont

	def removeMessage(self, message):
		message.hide()
		self.messages.remove(message)
		self.update()
		message.remove()
		
	def getNextPosition(self):
		xPos = Messages.defaultXPos + self.XPosition * Messages.defaultXInc
		yPos = Messages.defaultYPos + self.YPosition * Messages.defaultYInc
		self.YPosition = (self.YPosition + 1) % Messages.maxYPos
		return Vec3(xPos, 0, yPos)
			

class Popup():

	TOPLEFT = 0
	TOPRIGHT = 1
	BOTTOMLEFT = 2
	BOTTOMRIGHT = 3
	font = loader.loadFont("fonts/freesans.ttf")
	
	def __init__(self, message, position = 1, xOffset = 0.01, yOffset = 0.01):
		self.node = render2d.attachNewNode("popup")
		if isinstance(message, str):
			text = TextNode("popup")
			text.setFont(Popup.font)
			text.setAlign(TextNode.ALeft)
			textPath = self.node.attachNewNode(text)
			text.setText(message)
			text.setFrameAsMargin(0.2,0.3,0.3,0)
			text.setFrameColor(0, 0, 0, 0.5)
			text.setCardColor(0, 0, 0, 0.5)
			text.setCardAsMargin(0.2,0.3,0.3,0)
			text.setCardDecal(True)
		else:
			y = 0.0
			for line in message:
				text = TextNode("popup")
				if y == 0.0:
					text.setFrameAsMargin(0.2,0.3,0.2 + 1 * (len(message) - 1),-0.3)
					text.setFrameColor(0, 0, 0, 0.5)
					text.setCardColor(0, 0, 0, 0.5)
					text.setCardAsMargin(0.2,0.3,0.2 + 1 * (len(message) - 1),-0.3)
					text.setCardDecal(True)
				text.setFont(Popup.font)
				text.setAlign(TextNode.ALeft)
				textPath = self.node.attachNewNode(text)
				text.setText(line)
				textPath.setZ(textPath.getZ() - y)
				y += 1
				yOffset += 0.04
			yOffset -= 0.04
		self.node.setScale(0.040)
		
		mp = Mouse.queryScreenMousePosition()
		if mp:
			if position == Popup.TOPLEFT:
				self.node.setPos(mp[0] + xOffset, 0.0, mp[1] + yOffset)
			elif position == Popup.TOPRIGHT:
				self.node.setPos(mp[0] + xOffset, 0.0, mp[1] + yOffset)
			elif position == Popup.BOTTOMLEFT:
				self.node.setPos(mp[0] + xOffset, 0.0, mp[1] + yOffset)
			elif position == Popup.BOTTOMRIGHT:
				self.node.setPos(mp[0] + xOffset, 0.0, mp[1] + yOffset)
			else:
				self.node.setPos(0.95,0,0.85)
		else:
			self.node.setPos(0.95,0,0.85)
		
	def remove(self):
		self.node.remove()

class PopupBuilder():
	def __init__(self):
		pass
		
	def sendResponse(self, response):
		if(response):
			messenger.send("goToMainMenu", ['game'])
			mySelection.clear()
			myGroup.clear()
			for army in myLegion:
				for unit in army.getUnitList():
					unit.showHUD(False)
				for unit in army.getStructureList():
					unit.showHUD(False)
				army.remove()
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
		
	def setGrid(self, columns = 4, cellsize = 0.1, padding = 0.01, xoff = 0.70, yoff = -0.57):
		self.gridX = columns
		self.cellSize = cellsize
		self.gridPadding = padding
		self.xOffset = xoff
		self.yOffset = yoff
		
	def getNextCell(self):
		cellNumber = len(self.buttonList)
		cellRelXNumber = cellNumber % self.gridX
		cellRelY = cellNumber / self.gridX
		cellRelYNumber = int(cellNumber / self.gridX)
		if cellRelY > cellRelYNumber:
			cellRelYNumber += 1
		x = (self.cellSize + self.gridPadding) * cellRelXNumber
		y = -(self.cellSize + self.gridPadding) * cellRelYNumber
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
		
		#Base button
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
		
		#Barrack button
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
		self.buttonList['barrack'] = bt
		
		#Armory button
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
		self.buttonList['armory'] = bt
		
		#Laboratory button
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
		self.buttonList['lab'] = bt
		
		#Factory button
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
		self.buttonList['factory'] = bt
		
		#Airbase button
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
		self.buttonList['airbase'] = bt
		
		#Bunker button
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
		self.buttonList['bunker'] = bt
		
		#Turret button
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
		self.buttonList['turret'] = bt
		
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
		self.buttonList['barrack']['command'] = parent.buildStructure
		self.buttonList['barrack']['extraArgs'] = ([parent.getStructureType().barrack])
		self.buttonList['armory']['command'] = parent.buildStructure
		self.buttonList['armory']['extraArgs'] = ([parent.getStructureType().armory])
		self.buttonList['lab']['command'] = parent.buildStructure
		self.buttonList['lab']['extraArgs'] = ([parent.getStructureType().lab])
		self.buttonList['factory']['command'] = parent.buildStructure
		self.buttonList['factory']['extraArgs'] = ([parent.getStructureType().factory])
		self.buttonList['airbase']['command'] = parent.buildStructure
		self.buttonList['airbase']['extraArgs'] = ([parent.getStructureType().airbase])
		self.buttonList['bunker']['command'] = parent.buildStructure
		self.buttonList['bunker']['extraArgs'] = ([parent.getStructureType().bunker])
		self.buttonList['turret']['command'] = parent.buildStructure
		self.buttonList['turret']['extraArgs'] = ([parent.getStructureType().turret])
		
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
		
		
class BarrackHud(Hud):
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
		self.buttonList['soldier'] = bt
		
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
		self.buttonList['soldier']['command'] = parent.addUnitToCreationQueue
		self.buttonList['soldier']['extraArgs'] = ([parent.getUnitType().soldier])
		
		
class ArmoryHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		
		self.addTextLine("armorString", "", Hud.thirdRowPosition, 0.04)
		
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
		pass
		

class LabHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		
		self.addTextLine("armorString", "", Hud.thirdRowPosition, 0.04)
		
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
		pass
		
class FactoryHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		
		self.addTextLine("armorString", "", Hud.thirdRowPosition, 0.04)
		
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
		pass
		
		
class AirbaseHud(Hud):
	def __init__(self):
		Hud.__init__(self)
		
		self.addTextLine("armorString", "", Hud.thirdRowPosition, 0.04)
		
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
		pass
		
		
class BunkerHud(Hud):
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
		if parent.isOwner():
			self.buttons.show()
			self.setButton(parent)
		else:
			self.buttons.hide()
		self.setTextLine(parent)
		Hud.show(self, parent, scale, z)
		
	def setButton(self, parent):
		pass
		
		
class TurretHud(Hud):
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
		if parent.isOwner():
			self.buttons.show()
			self.setButton(parent)
		else:
			self.buttons.hide()
		self.setTextLine(parent)
		Hud.show(self, parent, scale, z)
		
	def setButton(self, parent):
		pass
		