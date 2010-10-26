# -*- coding: utf-8 -*-

#dichiarazioni di panda3d
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from panda3d.ai import *
import sys,os,__builtin__
#my import
from gui import *
from map import *
from effects import *
from unit import *
from legion import *
from resources import *
from camera import *

#fullscreen e grandezza finestra
loadPrcFileData("","""
fullscreen 0
win-size 800 600
text-encoding utf8
show-frame-rate-meter 1
sync-video #f
""")

class Navigator(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		
		#declaration on built-in objects
		#that can be called nearly everywhere
		__builtin__.myShader = ShaderManager()
		__builtin__.myMap = Map()
		__builtin__.myMenuBuilder = MenuBuilder()
		__builtin__.myHudBuilder = HudBuilder()
		__builtin__.myCamera = Camera()
		__builtin__.objKeyBoardModifiers = clKeyBoardModifiers()
		__builtin__.mySelection = clSelectionTool()
		__builtin__.myPopupBuilder = PopupBuilder()
		__builtin__.myResources = Resources()
		__builtin__.myLegion = []
		__builtin__.aiWorld = AIWorld(render)
		__builtin__.myEventManager = BaseEvents()
		
		#introVideo = VideoClip("video/intro.mpg", "video/menutheme.mp3")
		#introVideo.play()
		self.mainMenu("intro")
		self.full = False
		self.displayModes = []
		self.getSupportedDisplayRes()
		
		base.accept("startSingle", self.startSingle)
		base.accept("goToMainMenu", self.mainMenu)
		base.accept("f", self.toggleFullscreen)
		base.accept("d", self.debug)
		myShader.setBloomed()
		
		#ai update setting
		taskMgr.add(self.aiUpdate,"AIUpdate")
	
	def debug(self):
		if len(mySelection.listSelected) == 1:
			obj = mySelection.listSelected[0]
			obj.debug()
	
	def aiUpdate(self,task):
		aiWorld.update()
		return Task.cont
	
	def startSingle(self):
		#hide normalgui
		myMenuBuilder.hide()
		myMap.loadMap("maps/burning_sun/burning_sun.egg")
		#build hud
		myMap.setupInitMap()
		myHudBuilder.show()
		mySelection.setActive()
		
		#TODO: add event class handler
		
		#phase specific event handling
		base.accept("escape", myPopupBuilder.show)
	
	#def givedamage(self,
	
	# used to remove all exiting and rejoining...
	def mainMenu(self,f):
		mySelection.setIdle()
		base.ignore("escape")
		if(f=="game"):
			mySelection.setIdle()
			myMap.unloadMap()
			myHudBuilder.hide()
			for legion in myLegion:
				legion.remove()
			myResources.remove()
		
		#build main menu
		myMenuBuilder.show("main")
	
	def exitGame(self):
		sys.exit()
		
	def getSupportedDisplayRes(self):
		di = base.pipe.getDisplayInformation()
		wp = WindowProperties()
		for index in range(di.getTotalDisplayModes()):
			if abs(float(di.getDisplayModeWidth(index)) / float(di.getDisplayModeHeight(index)) - (16. / 9.)) < 0.001:
				self.displayModes.append([di.getDisplayModeWidth(index), di.getDisplayModeHeight(index)]) 
		
	def toggleFullscreen(self):
		print "called fullscreen toggle"
		wp = WindowProperties()
		if self.full == True:
			wp.setSize(self.displayModes[0][0], self.displayModes[0][1])
			wp.setFullscreen(False)
			self.full = False
		else:
			wp.setSize(self.displayModes[len(self.displayModes) - 1][0], self.displayModes[len(self.displayModes) - 1][1])
			wp.setFullscreen(True)
			self.full = True
		base.win.requestProperties(wp)

n = Navigator()

n.run()
