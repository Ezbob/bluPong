# Assisting definisions for the pong game
# By Anders Busch 2014

import pygame

global FUN_COUNTER,RED,GREEN,BLUE,WHITE,BLACK,HORIZONTAL,VERTICAL,LEFT_PLAYER,RIGHT_PLAYER,MAXIMUM_BALL_SPEED,MINIMUM_BALL_SPEED
global MAIN_MENU,START_SCREEN,GAME_SCREEN_TIME,GAME_SCREEN_GOAL,GAME_SCREEN_INF,COUNTER_PANEL_HEIGHT,COUNTER_UPPER_LIMIT,COUNTER_LOWER_LIMIT
global DEFAULT_BALL_SPEED,DEFAULT_BALL_RADIUS,DEFAULT_BAT_WIDTH,DEFAULT_BAT_LENGTH,DEFAULT_FPS_RATE,DEFAULT_CENTERLINE_WIDTH 
global Ball,Bat,MUSIC_LOOP,MUSIC_VOLUME,SOUND_EFFECT_VOLUME

# some constants
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)
WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
HORIZONTAL = 0
VERTICAL = 1
LEFT_PLAYER = 0
RIGHT_PLAYER = 1
START_SCREEN = 0
MAIN_MENU = 1
GAME_MODE_TIME = 1
GAME_MODE_GOAL = 2
GAME_MODE_INF = 3
FUN_COUNTER = 4
MENU_SPACING = 20
MUSIC_LOOP = 1
MUSIC_VOLUME = 1
SOUND_EFFECT_VOLUME = 1
MAXIMUM_BALL_SPEED = 9
MINIMUM_BALL_SPEED = -MAXIMUM_BALL_SPEED
DEFAULT_BALL_SPEED = 5
DEFAULT_BALL_RADIUS = 10
DEFAULT_BAT_SPEED = 5
DEFAULT_FPS_RATE = 60
DEFAULT_BAT_LENGTH = 80
DEFAULT_BAT_WIDTH = 15
DEFAULT_CENTERLINE_WIDTH = 10
COUNTER_PANEL_HEIGHT = 100
COUNTER_UPPER_LIMIT = 999
COUNTER_LOWER_LIMIT = 0

class Ball:
	def __init__(self,position,size):
		self.x = position[0]
		self.y = position[1]
		self.randCounter = 0
		self.size = size
	# direction 0: x-axis 1: y-axis
	def move(self,direction,length): 
		if(direction == 0):
			self.x = self.x + length
		elif (direction == 1):
			self.y = self.y + length
	# returns a tuple with the position of the ball
	def getPosition(self):
		return (self.x,self.y)
	def setPosition(self,position):
		self.x = position[0]
		self.y = position[1]
	def getRandomCounter(self):
		return self.randCounter
	def incrementRandomCounter(self):
		self.randCounter += 1
	def resetRandomCounter(self):
		self.randCounter = 0

class Bat:
	def __init__(self,position,idNumb):
		self.x = position[0]
		self.y = position[1]
		self.id = idNumb
		self.width = DEFAULT_BAT_WIDTH
		self.length = DEFAULT_BAT_LENGTH
	def move(self,direction,length): 
		if(direction == 0):
			self.x = self.x + length
		elif (direction == 1):
			self.y = self.y + length
	def getParameters(self):
		return (self.x,self.y,self.width,self.length)
	def getAreal(self):
		return width*length
	def setWidthLength(self,width,length):
		self.width = width
		self.length = length
	def setPosition(self,position):
		self.x = position[0]
		self.y = position[1]