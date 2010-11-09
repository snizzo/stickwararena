# -*- coding: utf-8 -*-

#dichiarazioni di panda3d
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from panda3d.ai import *
from PathFind import *
import sys,os,__builtin__
#my import
from gui import Hud
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
sync-video #t
""")

class Navigator(ShowBase):
	def __init__(self):
		#ShowBase.__init__(self)
		
		self.appRunner = base.appRunner
		self.taskMgr = base.taskMgr
		base.setFrameRateMeter(True)
		
		#declaration on built-in objects
		#that can be called nearly everywhere
		__builtin__.myShader = ShaderManager()
		__builtin__.myMap = Map()
		__builtin__.myMenuBuilder = MenuBuilder()
		__builtin__.myPopupBuilder = PopupBuilder()
		__builtin__.myResources = Resources()
		__builtin__.myLegion = []
		__builtin__.myGroup = Group()
		__builtin__.myCamera = Camera()
		__builtin__.mySelection = clSelectionTool()
		__builtin__.myMessages = Messages()
		__builtin__.myAudio = Audio()
		
		# used to force fullscreen
		# uncomment to use
		#myCamera.setFullscreen(True)
		
		# uncomment following line to see intro
		#introVideo = VideoClip("video/intro.mpg", "video/menutheme.mp3")
		#introVideo.play()
		self.mainMenu("intro")
		
		base.accept("startSingle", self.startSingle)
		base.accept("goToMainMenu", self.mainMenu)
		base.accept("exitGame", self.exitGame)
		
		#shader and effects function
		#want to run very fast and with intel based gc
		myShader.setBloomed()
		myAudio.playSoundtrack()
	
	#function called when creating a new single player game
	def startSingle(self):
		#hide every gui present in the screen
		myMenuBuilder.hide()
		#load pre-baked map
		myMap.loadMap("maps/burning_sun/burning_sun.egg")
		#setup players, starting structures and resources
		myMap.setupInitMap()
		#show game hud
		Hud.showGuiBackground(True)
		#make mouse selection tool active
		mySelection.setActive()
		
		#phase specific event handling
		#used to show a popup if you want to exit
		base.accept("escape", myPopupBuilder.show)
	
	#function called for showing main Menu
	# args: f = from where are you returning (eg. game, just started..)
	def mainMenu(self,f):
		#set mouse selection tool inactive
		mySelection.setIdle()
		#avoid showing the popup to return to main menu
		base.ignore("escape")
		#if you're seeing main menu once closed a game unload map and remove everything from scene
		if(f=="game"):
			myMap.unloadMap()
			Hud.showGuiBackground()
			for legion in myLegion:
				legion.remove()
			myResources.remove()
		
		#show main menu
		myMenuBuilder.showMainMenu()
	
	#function called to exit the application in any time
	#called from event "exitApp"
	def exitGame(self):
		sys.exit()

n = Navigator()
n.run()
