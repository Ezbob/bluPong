import pygame,sys
from ass_def import *
from pygame.locals import *
#from BluPong import debug

class StartMenu:
	def __init__(self,windowSurfaceObj,textPos,backgroundcolour, Fonts):
		self.titleTextPosition = textPos[0]
		self.mainSurface = windowSurfaceObj
		self.subTitleTextPos = textPos[1]
		self.menuBackgroundColour = backgroundcolour
		self.isMenu = False
		self.titleFontObj = Fonts[0]
		self.selectionFontObj = Fonts[1]
		self.authorFontObj = Fonts[2]
	def reset(self):
		self.isMenu = False
	def showStartScreen(self,title,subtitle):
		self.mainSurface.fill(self.menuBackgroundColour)
		self.mainSurface.blit(self.titleFontObj.render(title,False,WHITE),self.titleTextPosition) 
		self.mainSurface.blit(self.selectionFontObj.render(subtitle,False,WHITE),self.subTitleTextPos)
		authorText = self.authorFontObj.render('by Anders Busch 2014',False,WHITE)
		self.mainSurface.blit(authorText,(570,570))
	def enterMenu(self):
		self.isMenu = True
		pygame.time.wait(1000)
	def listingForKeyPressed(self,startSound):
		for event in pygame.event.get(): 
			if event.type == QUIT: # for quitting the game
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN: # for single event key pressing
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))
				if event.key == K_RETURN:
					startSound.play()
					self.enterMenu()
class MainMenu:
	def __init__(self,windowSurfaceObj,textPos,backgroundcolour, Fonts):
		self.mainSurface = windowSurfaceObj
		self.titleTextPosition = textPos[0]
		self.menuTextPosition = textPos[1]
		self.menuBackgroundColour = backgroundcolour
		self.isPlaying = False
		self.titleFontObj = Fonts[0]
		self.selectionFontObj = Fonts[1]
		self.currentCursorOption = GAME_MODE_TIME
		self.selectionCounters = [0,0]
		self.optionRectangleHeight = 0
		self.cursor = Bat((textPos[1][0]-MENU_SPACING,(self.mainSurface.get_height()/3)),-1)
	def reset(self):
		self.isPlaying = False
		self.selectionCounters = [0,0]
		self.currentCursorOption = GAME_MODE_TIME
		self.cursor = Bat((self.menuTextPosition[0]-MENU_SPACING,(self.mainSurface.get_height()/3)),-1)
	def setCursor(self):
		self.cursor.length = self.selectionFontObj.get_height()
		pygame.draw.rect(self.mainSurface,WHITE,self.cursor.getParameters()) 
	def showMainMenu(self,title,menuOptions):
		self.mainSurface.fill(self.menuBackgroundColour)
		titleRendered = self.titleFontObj.render(title,False,WHITE)
		self.mainSurface.blit(titleRendered,((self.mainSurface.get_width()/2)-(titleRendered.get_width()/2),100))
		offsetcount = 0
		for optionText in menuOptions:
			renderedOptionText = self.selectionFontObj.render(optionText,False,WHITE)
			self.optionRectangleHeight = renderedOptionText.get_height()+MENU_SPACING
			Yposition = (self.mainSurface.get_height()/3)+(self.optionRectangleHeight)*offsetcount
			self.mainSurface.blit(renderedOptionText,(self.menuTextPosition[0], Yposition))
			if offsetcount <= 1:
				renderedCounterText = self.selectionFontObj.render(str(self.selectionCounters[offsetcount]),False,WHITE)
				self.mainSurface.blit(renderedCounterText,((self.mainSurface.get_width()-self.menuTextPosition[0])-(renderedCounterText.get_width()/2), Yposition))
			offsetcount += 1
	def getSelectedCounter(self):
		if self.currentCursorOption != GAME_MODE_INF:
			return (self.currentCursorOption,self.selectionCounters[self.currentCursorOption-1])
		else:
			return (self.currentCursorOption,-1) 
	def listingForKeyPressed(self,sounds):
		for event in pygame.event.get(): 
			if event.type == QUIT: # for quitting the game
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN: # for single event key pressing
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))
				if event.key == K_RETURN:
					if self.currentCursorOption == GAME_MODE_INF or self.currentCursorOption <= 2 and self.selectionCounters[self.currentCursorOption-1] != 0:
						self.isPlaying = True
						if sounds != []:
							sounds[0].play()
						pygame.time.wait(1000)
					else:
						if sounds != []:
							sounds[1].play()
				if event.key == K_DOWN:
					if self.currentCursorOption >= GAME_MODE_TIME and self.currentCursorOption <= GAME_MODE_INF and self.currentCursorOption+1 <= GAME_MODE_INF:
						self.currentCursorOption += 1
						self.cursor.move(VERTICAL,self.optionRectangleHeight)
				if event.key == K_UP:
					if self.currentCursorOption >= GAME_MODE_TIME and self.currentCursorOption <= GAME_MODE_INF and self.currentCursorOption-1 >= GAME_MODE_TIME:
						self.currentCursorOption -= 1
						self.cursor.move(VERTICAL,-(self.optionRectangleHeight))
				if event.key == K_LEFT:
					if self.currentCursorOption != GAME_MODE_INF:
						if self.selectionCounters[self.currentCursorOption-1] >= COUNTER_LOWER_LIMIT and self.selectionCounters[self.currentCursorOption-1] <= COUNTER_UPPER_LIMIT:
							if self.selectionCounters[self.currentCursorOption-1]-1 >= COUNTER_LOWER_LIMIT:
								if self.currentCursorOption == GAME_MODE_TIME:
									self.selectionCounters[self.currentCursorOption-1] -= 5
								else:
									self.selectionCounters[self.currentCursorOption-1] -= 1
				if event.key == K_RIGHT:
					if self.currentCursorOption != GAME_MODE_INF:
						if self.selectionCounters[self.currentCursorOption-1] >= COUNTER_LOWER_LIMIT and self.selectionCounters[self.currentCursorOption-1] <= COUNTER_UPPER_LIMIT:
							if self.selectionCounters[self.currentCursorOption-1]+1 <= COUNTER_UPPER_LIMIT:
								if self.currentCursorOption == GAME_MODE_TIME:
									self.selectionCounters[self.currentCursorOption-1] += 5
								else:
									self.selectionCounters[self.currentCursorOption-1] += 1