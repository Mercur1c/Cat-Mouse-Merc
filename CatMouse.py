import sys, os
import math
import pygame

pygame.init()

class Main:
	def __init__(self):
		self.screen = pygame.display.set_mode((640, 480))
		
	def mainLoop(self):
		player = Player((50,50))
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()
					sys.exit()
				
			self.screen.fill((0,0,0))
			
			player.draw(self.screen)
			player.update()
			
			pygame.display.flip()
					
			

class Entity(object):
	'''Basic entity, simply an x,y coordinate'''
	def __init__(self, (x,y)):
		self.x = x
		self.y = y

class ControlledEntity(Entity):
	'''An entity that is moved by a controller'''
	def __init__(self, (x,y), controller):
		Entity.__init__(self, (x,y))
		self.controller = controller((x,y), 1)
		
	def update(self):
		self.controller.update()
		self.x = self.controller.x
		self.y = self.controller.y				
		
class Player(ControlledEntity):
	'''The player's Mouse'''
	def __init__(self, (x, y)):	
		ControlledEntity.__init__(self, (x, y), MouseFollower)
		
		self.health = 100
		self.image = pygame.Surface((64,64))
		self.image.fill((255,255,255))
		
	def draw(self, screen):
		screen.blit(self.image, (self.x-32, self.y-32))
		
class Controller:
	'''Base controller class'''
	def __init__(self, (x,y)):
		self.x = x
		self.y = y
		
	def update(self):
		pass
		
class MouseController(Controller):
	'''Controller that moves itself to the mouse position'''
	def __init__(self, (x,y)):
		Controller.__init__(self, (x,y))
		
	def update(self):
		mousePos = pygame.mouse.get_pos()
		self.x = mousePos[0]
		self.y = mousePos[1]
		
class MouseFlee(Controller):
	'''Controller that moves away from the mouse'''
	def __init__(self, (x,y), speed):
		self.x = x
		self.y = y
		self.speed = speed
		self.direction = 0
		
	def update(self):
		mousePos = pygame.mouse.get_pos()
		self.direction = math.atan2(self.y-mousePos[1], self.x-mousePos[0])
		self.heading = (math.cos(self.direction), math.sin(self.direction))
		
		distanceToMouse = math.hypot(mousePos[0]-self.x, mousePos[1]-self.y)
		
		self.step = int(self.speed)# + math.sqrt(distanceToMouse))
		
		self.x += self.heading[0]*self.step
		self.y += self.heading[1]*self.step
		
class MouseFollower(Controller):
	'''Controller that follows the mouse'''
	def __init__(self, (x,y), speed):
		self.x = x
		self.y = y
		self.speed = speed
		self.direction = 0
		
		self.softDist = 2 #Stop the controlled sprite from jittering
		
	def update(self):
		mousePos = pygame.mouse.get_pos()
		self.direction = math.atan2(self.y-mousePos[1], self.x-mousePos[0])
		self.heading = (math.cos(self.direction), math.sin(self.direction))
		
		distanceToMouse = math.hypot(mousePos[0]-self.x, mousePos[1]-self.y)
		
		if distanceToMouse < self.softDist:
			pass
		
		else:
			self.step = int(self.speed + math.sqrt(distanceToMouse))
		
			self.x -= self.heading[0]*self.step
			self.y -= self.heading[1]*self.step
		

if __name__ == "__main__":
	main = Main()
	main.mainLoop()		
		

		