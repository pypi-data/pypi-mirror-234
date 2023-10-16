import pygame as p

from realms import display

class Realm:

	def __init__(self, title="My Realm", width=800, height=600):
		p.init()
		p.display.set_mode((width, height))
		p.display.set_caption(title)
	
	def update(self):
		pass
		
