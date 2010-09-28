# -*- coding: utf-8 -*-

#dichiarazioni di panda3d
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
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
fullscreen 1
win-size 1280 800
text-encoding utf8
show-frame-rate-meter 1
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
		
		#introVideo = VideoClip("video/intro.mpg", "video/menutheme.mp3")
		#introVideo.play()
		self.mainMenu("intro")
		
		base.accept("startSingle", self.startSingle)
		base.accept("goToMainMenu", self.mainMenu)
		myShader.setBloomed()
		
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

n = Navigator()

n.run()
