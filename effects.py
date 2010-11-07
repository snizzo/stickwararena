# -*- coding: utf-8 -*-
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.interval.FunctionInterval import Wait
from direct.interval.LerpInterval import LerpHprInterval
from direct.filter.CommonFilters import CommonFilters
from direct.task import Task
import __builtin__, sys,os,string

class ShaderManager():
	def __init__(self):
		#needed for physics and particle system
		base.enableParticles()
		render.setShaderAuto()
	
	def setBloomed(self):
		#setupfilters and shaders
		self.filters = CommonFilters(base.win, base.cam)
		#self.filters.setCartoonInk(separation=1.0)
		self.filters.setBloom(size="small")
		#self.filters.setVolumetricLighting(myCamera.cameraLightNode)
		render.setAttrib(LightRampAttrib.makeHdr0())
		pass
	
class Audio():
	def __init__(self):
		self.audioList = []
		self.audioList = self.getAudioTracks()
		
		self.currentTrack = 0
		self.lenghtTrack = len(self.audioList)
		
	def getAudioTracks(self):
		tracks = os.listdir("sounds/music")
		for i in range(len(tracks)):
			tracks[i] = "sounds/music/" + tracks[i]
		return tracks
	
	def playSoundtrack(self):
		self.sound = loader.loadSfx(self.audioList[0])
		self.sound.play()
		myMessages.showBaloon(self.getBName(self.audioList[0]), 5)
		taskMgr.add(self.playMusic,"soundtrack")
	
	def stopSoundtrack(self):
		self.currentTrack = -1
		self.sound.stop()
	
	def playMusic(self,task):
		if self.sound.status() == AudioSound.PLAYING:
			return Task.cont
		self.currentTrack += 1
		if self.currentTrack > len(self.audioList)-1:
			self.currentTrack = 0
		self.sound.stop()
		self.sound = loader.loadSfx(self.audioList[self.currentTrack])
		self.sound.play()
		myMessages.showBaloon(self.getBName(self.audioList[self.currentTrack]), 5)	
		
		return Task.cont
	
	def getBName(self,name):
		name = self.audioList[self.currentTrack].split("/")
		name = name.pop()
		name = name.split(".")
		name.pop()
		sname = ""
		for n in name:
			sname += n
		return sname
		
		
'''
class VideoClip():
	def __init__(self,videourl,addsound=""):
		self.props = WindowProperties()
		self.props.setCursorHidden(True) 
		base.win.requestProperties(self.props)
		self.tex = loader.loadTexture(videourl)
		self.cm = CardMaker("VideoIntro");
		self.cm.setFrameFullscreenQuad()
		self.cm.setUvRange(self.tex)
		self.card = NodePath(self.cm.generate())
		self.card.setTexture(self.tex)
		self.mySound = base.loader.loadSfx(addsound)
		
		self.videoNode = render2d.attachNewNode("video")
		self.card.reparentTo(self.videoNode)
		
		self.videoNode.hide()
		
	def stop(self):
		#remove card and movie
		self.tex.stop()
		self.card.remove()
		#re-enabling mouse
		self.props.setCursorHidden(False) 
		base.win.requestProperties(self.props)
		messenger.send("goToMainMenu", ['intro'])
	
	def play(self):
		#disabling mouse when playing
		
		self.videoNode.show()
		int1 = Func(self.tex.play)
		int2 = Func(self.stop)
		self.mySound.play()
		seq1 = Sequence(int1,Wait(27.0),int2)
		seq1.start()
		
	def remove(self):
		self.videoNode.remove()
'''
