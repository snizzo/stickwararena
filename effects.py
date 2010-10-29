# -*- coding: utf-8 -*-
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.interval.FunctionInterval import Wait
from direct.interval.LerpInterval import LerpHprInterval
from direct.filter.CommonFilters import CommonFilters
import __builtin__, sys

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
	
