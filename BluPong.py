# My take on the Pong game
# Created with pygame 
# By Anders Busch 2014

import pygame,math,sys,random
from ass_def import *
from pygame.locals import *
from screen_def import *

# Version 1.00 - GAMMA release... Finally!

pygame.init()
pygame.mixer.init()

# variables that change over gameplay
windowResolution = [800,600]
ballDirectionSpeed = [0,0]
currentGameState = GAME_MODE_TIME 
scoreList = [0,0]
counter = 0
timeLimit = 0
mSecAfterStart = 0
debug = ''
isNewGame = True

# variables that don't change over gameplay
fpsClock = pygame.time.Clock()
music = pygame.mixer.music
windowSurface = pygame.display.set_mode(windowResolution)
pygame.display.set_caption('BluPong')
hugeFont = pygame.font.Font('fonts/PressStart2P.ttf',48)
bigFont = pygame.font.Font('fonts/PressStart2P.ttf',32)
titleFont = pygame.font.Font('fonts/PressStart2P.ttf',75)
debugFont = pygame.font.Font('fonts/PressStart2P.ttf',24)
authorFont = pygame.font.Font('fonts/PressStart2P.ttf',10)
wallHitSound = pygame.mixer.Sound('sounds/bounce1.wav')
batHitSound = pygame.mixer.Sound('sounds/batBounce.wav')
scoreSound = pygame.mixer.Sound('sounds/score.wav')
startSound = pygame.mixer.Sound('sounds/start.wav')
noSound = pygame.mixer.Sound('sounds/no.wav')
musicPlayList = ['sounds/8bitNo5-2.mp3','sounds/8bitMozNo40-4.mp3']
currentMusic = 0

# player bats and ball initial positions
startPositionBall = (windowResolution[HORIZONTAL]/2, windowResolution[VERTICAL]/2)
startPositionBat1 = (50, (windowResolution[VERTICAL]/2)-(DEFAULT_BAT_LENGTH/2))
startPositionBat2 = (windowResolution[HORIZONTAL]-50, (windowResolution[VERTICAL]/2)-(DEFAULT_BAT_LENGTH/2))

# making the players and the ball
ball = Ball(startPositionBall,DEFAULT_BALL_RADIUS)
bat1 = Bat(startPositionBat1,1) # left bat
bat2 = Bat(startPositionBat2,2) # right bat

# The different screens
startScreen = StartMenu(windowSurface,[(90,200),(90,350)],BLUE, [titleFont, bigFont, authorFont])
mainMenu = MainMenu(windowSurface,[(windowResolution[0]/2,10),(90,350)],BLUE, [bigFont, debugFont])

def setupSound():
	global music
	wallHitSound.set_volume(SOUND_EFFECT_VOLUME)
	scoreSound.set_volume(SOUND_EFFECT_VOLUME)
	startSound.set_volume(SOUND_EFFECT_VOLUME)
	musicLoader()
	
def musicLoader():
	global music,musicPlayList,currentMusic
	if isNewGame:
		music.set_volume(MUSIC_VOLUME)
	if not music.get_busy():
		music.load(musicPlayList[currentMusic])
		currentMusic = (currentMusic+1) % len(musicPlayList)
		music.play(MUSIC_LOOP) 

def setBackground():
	global windowSurface,currentGameState
	if currentGameState == GAME_MODE_INF:
		windowSurface.fill(BLUE)
		centerlineX = windowResolution[0]/2-DEFAULT_CENTERLINE_WIDTH/2
		pygame.draw.rect(windowSurface,WHITE,(centerlineX,0,DEFAULT_CENTERLINE_WIDTH,windowResolution[1]))
		setScores(windowSurface)
		setDebug(windowSurface)
	elif currentGameState == GAME_MODE_GOAL or currentGameState == GAME_MODE_TIME:
		windowSurface.fill(BLUE)
		centerlineX = windowResolution[0]/2-DEFAULT_CENTERLINE_WIDTH/2
		pygame.draw.rect(windowSurface,WHITE,(centerlineX,COUNTER_PANEL_HEIGHT,DEFAULT_CENTERLINE_WIDTH,windowResolution[1]-COUNTER_PANEL_HEIGHT))
		setScores(windowSurface)
		setCounter(windowSurface)
		setDebug(windowSurface)
	else:
		print "Error: no game mode or invalid game mode choosen"

def setDebug(windowSurfaceObj):
	debugObj = bigFont.render(debug,False,WHITE)
	windowSurfaceObj.blit(debugObj,(0,0))

def setCounter(windowSurfaceObj):
	counterSurface = hugeFont.render(str(counter),False,WHITE)
	windowSurfaceObj.blit(counterSurface, ((windowResolution[0]/2)-(counterSurface.get_width()/2),COUNTER_PANEL_HEIGHT/2-COUNTER_PANEL_HEIGHT/4))

def setScores(windowSurfaceObj):
	scoreSurfaces = []
	for score in scoreList:
		scoreSurfaces.append(bigFont.render(str(score),False,WHITE))
	count = 0
	for scoreSurface in scoreSurfaces:
		centerXMsg = (windowResolution[HORIZONTAL]/2)-scoreSurface.get_rect().centerx
		windowSurfaceObj.blit(scoreSurface,(count*centerXMsg+centerXMsg/2,windowResolution[VERTICAL]/12))
		count += 1

def setMovingParts():
	global windowSurface
	pygame.draw.circle(windowSurface,WHITE,ball.getPosition(),ball.size)
	pygame.draw.rect(windowSurface,WHITE,bat1.getParameters())
	pygame.draw.rect(windowSurface,WHITE,bat2.getParameters())

def setWinningText(text,font):
	global windowSurface,windowResolution
	renderedText = font.render(text,False,WHITE)
	textBackground = renderedText.get_rect()
	positionOfText = ((windowResolution[HORIZONTAL]/2)-(textBackground.width/2),(windowResolution[VERTICAL]/2)-(textBackground.height/2))
	backgroundFill = pygame.draw.rect(windowSurface, BLUE,(positionOfText[0],positionOfText[1],textBackground.width,textBackground.height))
	windowSurface.blit(renderedText,positionOfText)

def keyListing():
	keysPressed = pygame.key.get_pressed()
	if(keysPressed[K_ESCAPE] and bat2.y >= 0):
		pygame.event.post(pygame.event.Event(QUIT))
	if(keysPressed[K_UP] and bat2.y >= 0):
		bat2.move(VERTICAL,-DEFAULT_BAT_SPEED)
	if(keysPressed[K_DOWN] and (bat2.y+bat2.length) <= windowResolution[VERTICAL]):
		bat2.move(VERTICAL,DEFAULT_BAT_SPEED)
	if(keysPressed[K_a] and bat1.y >= 0):
		bat1.move(VERTICAL,-DEFAULT_BAT_SPEED)
	if(keysPressed[K_z] and (bat1.y+bat1.length) <= windowResolution[VERTICAL]):
		bat1.move(VERTICAL,DEFAULT_BAT_SPEED)

def eventHandler():
	global counter,debug
	for event in pygame.event.get():
		if event.type == QUIT: # for quitting the game
			pygame.quit()
			sys.exit()

#collision width top and bottom edges
def edgeBallCollisionHandler():
	if (ball.y+ball.size) > windowResolution[VERTICAL] or (ball.y-ball.size) < 0:
		wallHitSound.play()
		ballDirectionSpeed[VERTICAL] = (-ballDirectionSpeed[VERTICAL])
	if ballDirectionSpeed[HORIZONTAL] == 0:
		ballDirectionSpeed[HORIZONTAL] = random.randint(-1,1)*DEFAULT_BALL_SPEED

# has a collision occured ? if so True is returned
def batCollisionDetection(bat):
	circleDistanceX = math.fabs(ball.x - (bat.width/2 + bat.x))
	circleDistanceY = math.fabs(ball.y - (bat.length/2 + bat.y))
	if (bat.width/2 + ball.size/2) > circleDistanceX and (bat.length/2 + ball.size/2) > circleDistanceY:
		return True
	cornerDistanceSq = (circleDistanceX - bat.width/2)**2 + (circleDistanceY - bat.length/2)**2
	if cornerDistanceSq < ball.size**2:
		return True
	return False

def batCollisionHandling(bats,determ_limit):
	for playerBat in bats:
		if batCollisionDetection(playerBat):
			if (playerBat.id == 2 and ballDirectionSpeed[HORIZONTAL] > 0) or (playerBat.id == 1 and ballDirectionSpeed[HORIZONTAL] < 0):
				if ballDirectionSpeed[HORIZONTAL] < MAXIMUM_BALL_SPEED and ballDirectionSpeed[HORIZONTAL] > MINIMUM_BALL_SPEED:
					ballDirectionSpeed[HORIZONTAL] = ballDirectionSpeed[HORIZONTAL]+random.randint(0,1)
				ballDirectionSpeed[HORIZONTAL] = -ballDirectionSpeed[HORIZONTAL]
				batHitSound.play()
			keysPressed = pygame.key.get_pressed()
			if keysPressed[K_a] or keysPressed[K_UP] and ballDirectionSpeed[VERTICAL] > 0:
				ballDirectionSpeed[VERTICAL] += random.randint(1,2)
			elif keysPressed[K_a] or keysPressed[K_UP] and ballDirectionSpeed[VERTICAL] < 0:
				ballDirectionSpeed[VERTICAL] -= random.randint(1,2)
			elif keysPressed[K_z] or keysPressed[K_DOWN] and ballDirectionSpeed[VERTICAL] < 0:
				ballDirectionSpeed[VERTICAL] += random.randint(1,2)
			elif keysPressed[K_z] or keysPressed[K_DOWN] and ballDirectionSpeed[VERTICAL] > 0:
				ballDirectionSpeed[VERTICAL] -= random.randint(1,2)
			if ballDirectionSpeed[VERTICAL] == 0:
				ballDirectionSpeed[VERTICAL] += random.randint(-1,1)

# returns 1 if ball has crossed left edge, 2 if right edge, 
# 0 if neither edge has been crossed  
def crossedScoringEdge():
	if ball.x < -DEFAULT_BAT_LENGTH:
		return 1
	if ball.x > windowResolution[HORIZONTAL]+DEFAULT_BAT_LENGTH:
		return 2
	return 0

def resetPositions():
	bat1.setPosition(startPositionBat1)
	bat2.setPosition(startPositionBat2)
	ball.setPosition(startPositionBall)

def scoreHandler():
	if crossedScoringEdge() != 0:
		if crossedScoringEdge() == 1:
			scoreList[1] += 1 
		elif crossedScoringEdge() == 2:
			scoreList[0] += 1
		scoreSound.play()
		resetPositions()
		ballDirectionSpeed[VERTICAL] = random.randint(-1,1)*DEFAULT_BALL_SPEED
		ballDirectionSpeed[HORIZONTAL] = random.randint(-1,1)*DEFAULT_BALL_SPEED

def drawUpdate(rectangleList = None):
	if(rectangleList == None):
		pygame.display.update()
	else:
		pygame.display.update(rectangleList)

def setFPS(fpsRate = DEFAULT_FPS_RATE):
	global mSecAfterStart,currentGameState,mainMenu,debug
	if mainMenu.isPlaying and currentGameState == GAME_MODE_TIME:
		mSecAfterStart += fpsClock.tick(fpsRate)
	else:
		fpsClock.tick(fpsRate)

def counterHandler():
	global counter,currentGameState,mSecAfterStart,debug
	if currentGameState == GAME_MODE_TIME:
		counter =  (timeLimit-mSecAfterStart/1000)

def firstGame():
	if isNewGame:
		global startScreen,currentGameState,counter,mainMenu,pygame,timeLimit,debug
		startScreen.reset()
		currentGameState = mainMenu.getSelectedCounter()[0]
		counter = mainMenu.getSelectedCounter()[1]
		timeLimit = mainMenu.getSelectedCounter()[1]
		ballDirectionSpeed[VERTICAL] = DEFAULT_BALL_SPEED
		setupSound() 

def beforePlaying():
	global startScreen,mainMenu,currentGameState,debug
	if not startScreen.isMenu:
		startScreen.showStartScreen('BluPong','Press Enter To Start')
		startScreen.listingForKeyPressed(startSound)
	else:
		mainMenu.showMainMenu('Choose Game Mode',['Time Attack','Goal','Infinity'])
		mainMenu.setCursor()
		mainMenu.listingForKeyPressed([startSound,noSound])

def nowPlaying():
	global mainMenu,isNewGame,ball
	if mainMenu.isPlaying:
		firstGame()
		counterHandler()
		setBackground()
		setMovingParts()
		scoreHandler()
		eventHandler()
		ball.move(VERTICAL,ballDirectionSpeed[VERTICAL])
		ball.move(HORIZONTAL,ballDirectionSpeed[HORIZONTAL])
		batCollisionHandling([bat1,bat2],DEFAULT_BALL_SPEED)
		edgeBallCollisionHandler()
		keyListing()
		isNewGame = False
		musicLoader()
		winHandler()

def returnToStart():
	global mainMenu,startScreen,isNewGame,music,counter,ballDirectionSpeed,currentGameState,scoreList,timeLimit,mSecAfterStart,debug
	mainMenu.reset()
	startScreen.reset()
	isNewGame = True
	music.stop()
	music.rewind()
	counter = 0
	ballDirectionSpeed = [0,0]
	currentGameState = GAME_MODE_TIME
	scoreList = [0,0]
	timeLimit = 0
	mSecAfterStart = 0
	debug = ''
	beforePlaying()
	

def winHandler():
	global currentGameState,counter,scoreList,bigFont
	if currentGameState == GAME_MODE_GOAL and mainMenu.isPlaying:
		if scoreList[0] == counter: # Left player has won
			setWinningText('Left player won!',bigFont)
			drawUpdate()
			pygame.time.wait(3000)
			returnToStart()
		elif scoreList[1] == counter: # Right player has won
			setWinningText('Right player won!',bigFont)
			drawUpdate()
			pygame.time.wait(3000)
			returnToStart()
	if currentGameState == GAME_MODE_TIME and mainMenu.isPlaying:
		if scoreList[0] > scoreList[1] and counter == 0: # Left player has won
			setWinningText('Left player won!',bigFont)
			drawUpdate()
			pygame.time.wait(3000)
			returnToStart()
		elif scoreList[0] < scoreList[1] and counter == 0: # Right player has won
			setWinningText('Right player won!',bigFont)
			drawUpdate()
			pygame.time.wait(3000)
			returnToStart()
		elif scoreList[0] == scoreList[1] and counter == 0: # Tie
			setWinningText('Tie! :(',bigFont)
			drawUpdate()
			pygame.time.wait(3000)
			returnToStart()

while True: # main game loop
	beforePlaying()
	nowPlaying()
	drawUpdate()
	setFPS()