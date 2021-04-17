import sys, pygame
import math
import time
import random
from pygame.locals import *

pygame.init()
pygame.joystick.init()
screenWidth = 1000
screenHeight = 750

gameDisplay = pygame.display.set_mode((screenWidth,screenHeight))

icon = pygame.image.load('cookie.png') #sets the icon for the game
pygame.display.set_icon(icon)
pygame.display.set_caption('Chase') #sets the name for the game window
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55) #default font for in-game text

def text_objects(text,color): #function to render text objects
    textSurface = font.render(text,True,color)
    return textSurface, textSurface.get_rect()

def updateScore(score): #renders the score to the top left of the screen
    text = pygame.font.SysFont("comicsansms",55).render("Score: " + str(score),True,(255,0,0))
    gameDisplay.blit(text,[0,0])

def gameIntro(): #game loop for the game's start screen
    intro = True
    while intro:
        for event in pygame.event.get(): #event handler for quitting the game, starting the game, and closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                    gameLoop()
                elif event.key == pygame.K_q:
                    pygame.quit()


        gameDisplay.fill((255,255,255))
        screenMessage("C H A S E",(122,232,12),-100)
        screenMessage("(Eat the Cookies and Avoid the UFO)",(0,0,0),120)
        screenMessage("Press Space to Play or Q to Quit",(0,0,0),210)
        screenMessage("Arrow Keys or WASD to Move and Space to Pause",(0,0,0),300)
        #start screen text

        pygame.display.update()
        clock.tick(5) #runs start screen at 5 fps

def pause(): #pause loop function
    paused = True
    while paused:
        for event in pygame.event.get(): #event handler to handle resuming the game, quitting the game, and closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    paused = False
                elif event.key == K_q:
                    gameIntro()
        gameDisplay.fill((255,255,255))
        screenMessage("PAUSED",(255,0,0),-100)
        screenMessage("Press Space to Unpause or Q to Quit",(255,0,0),25)
        pygame.display.update()
        clock.tick(5)

def screenMessage(message,color,y_displace=0): #displays a message to the screen
    textSurf, textRect = text_objects(message,color)
    textRect.center = (screenWidth//2), (screenHeight/2) + y_displace
    gameDisplay.blit(textSurf,textRect)

def detectCollision(xCoor1,xCoor2,yCoor1,yCoor2,width1,width2,height1,height2): #function that uses the coordinates and dimensions for two objects to detect if they collide
    if xCoor1 > xCoor2 and xCoor1 < xCoor2 + width2 or xCoor1 + width1 > xCoor2 and xCoor1 + width1 < xCoor2 + width2:
        if yCoor1 > yCoor2 and yCoor1 < yCoor2 + height2 or yCoor1 + height1 > yCoor2 and yCoor1 + height1 < yCoor2 + height2:
            return True
        elif yCoor1 + height1 > yCoor2 and yCoor1 + height1 < yCoor2 + height2:
            return True
    elif xCoor2 > xCoor1 and xCoor2 < xCoor1 + width1 or xCoor2 + width2 > xCoor1 and xCoor2 + width2 < xCoor1 + width1:
        if yCoor2 > yCoor1 and yCoor2 < yCoor1 + height1 or yCoor2 + height2 > yCoor1 and yCoor2 + height2 < yCoor1 + height1:
            return True
        elif yCoor2 + height2 > yCoor1 and yCoor2 + height2 < yCoor1 + height1:
            return True

def disablePowerups(): #disables all the powerups
    powerupFreeze = False
    powerupSpeedUp = False
    powerupSpeedDown = False
    powerupReverse = False
    powerupDizzy = False

def gameLoop(): #resets all of the game variables whenever the game is restarted and runs while the game is being played
    gameExit = False
    gameOver = False

    mysteryBoxOnScreen = False
    powerupOnScreen = False

    powerupSpeedUp = False
    powerupSpeedUpTime = 0
    powerupSpeedDown = False
    powerupSpeedDownTime = 0
    powerupFreeze = False
    powerupFreezeTime = 0
    powerupReverse = False
    powerupReverseTime = 0
    powerupDizzy = False
    powerupDizzyTime = 0
    #resets all the powerups to off and the activation times to 0

    score = 0

    charWidth = int(screenHeight/15)
    charHeight = int(screenHeight/15)
    enemyWidth = int(screenHeight/15)
    enemyHeight = int(screenHeight/15)
    randCookieWidth = int(screenHeight/15)
    randCookieHeight = int(screenHeight/15)
    mysteryBoxWidth = int(screenHeight/10)
    mysteryBoxHeight = int(screenHeight/10)
    icecreamWidth = int(screenHeight/7.5)
    icecreamHeight = int(screenHeight/7.5)
    chiliWidth = int(screenHeight/7.5)
    chiliHeight = int(screenHeight/7.5)
    tacoWidth = int(screenHeight/7.5)
    tacoHeight = int(screenHeight/7.5)
    turtleWidth = int(screenHeight/7.5)
    turtleHeight = int(screenHeight/7.5)
    dizzyWidth = int(screenHeight/7.5)
    dizzyHeight = int(screenHeight/7.5)
    #sets the heights and widths for each game object based on the screen's resolution

    playerSpeed = int(screenHeight/94)
    enemySpeed = int(screenHeight/375)
    #starting speeds for the player and the enemy

    counter1 = 0
    counter2 = 0
    immunityTime = 0
    mysteryBoxOpenTime = 0
    powerupOpenTime = 0
        
    mainchar = pygame.image.load('mainchar.png')
    mainchar = pygame.transform.scale(mainchar,(charWidth,charHeight))
    mysteryBoxChar = pygame.image.load('mysterybox.png')
    mysteryBoxChar = pygame.transform.scale(mysteryBoxChar,(mysteryBoxWidth,mysteryBoxHeight))
    icecreamchar = pygame.image.load("icecream.png")
    icecreamchar = pygame.transform.scale(icecreamchar,(icecreamWidth,icecreamHeight))
    chilichar = pygame.image.load("chili.png")
    chilichar = pygame.transform.scale(chilichar,(chiliWidth,chiliHeight))
    turtlechar = pygame.image.load("turtle.png")
    turtlechar = pygame.transform.scale(turtlechar,(turtleWidth,turtleHeight))
    tacochar = pygame.image.load("taco.png")
    tacochar = pygame.transform.scale(tacochar,(tacoWidth,tacoHeight))
    dizzychar = pygame.image.load("dizzy.png")
    dizzychar = pygame.transform.scale(dizzychar,(dizzyWidth,dizzyHeight))
    enemychar = pygame.image.load('enemy.png')
    enemychar = pygame.transform.scale(enemychar,(enemyWidth,enemyHeight))
    background = pygame.image.load('background.jpeg')
    cookiechar = pygame.image.load('cookie.png')
    cookiechar = pygame.transform.scale(cookiechar,(randCookieWidth,randCookieHeight))
    background = pygame.transform.scale(background,(screenWidth,screenHeight))
    #imports images from the their file locations and scales them based off of their already defined width and height variables

    headLeftChange = 0
    headRightChange = 0
    headUpChange = 0
    headDownChange = 0

    headX = 300
    headY = 300
    randCookieX = random.randrange(0,screenWidth - randCookieWidth)
    randCookieY = random.randrange(0,screenHeight - randCookieHeight)
    mysteryBoxX = 5000
    mysteryBoxY = 5000
    icecreamX = 5000
    icecreamY = 5000
    chiliX = 5000
    chiliY = 5000
    tacoX = 5000
    tacoY = 5000
    enemyX = random.randrange(0,screenWidth - enemyWidth)
    enemyY = random.randrange(0,screenHeight - enemyHeight)
    #sets the starting coordinates for each of the objects

    while not gameExit:

        while gameOver: #loop that runs when the player loses
            gameDisplay.fill((78,0,255))
            screenMessage("Game Over!",(255,255,255),-100)
            screenMessage("Score: " + str(score),(255,255,255),100)
            screenMessage("Press R to restart the game or Q to quit.",(255,255,255),200)
            pygame.display.update()

            for event in pygame.event.get(): #handles the player's choice of restarting the game, quitting to the main menu, or closing the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameIntro()
                        gameOver = False
                    elif event.key == pygame.K_r:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN: #handles events for the game for arrow keys, wasd, or pausing the game
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    headLeftChange = playerSpeed*-1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    headRightChange = playerSpeed
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    headUpChange = playerSpeed*-1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    headDownChange = playerSpeed
                elif event.key == pygame.K_SPACE:
                    pause()
            if event.type == pygame.KEYUP: #makes sure that when the player releases the arrow keys that there is no change in location until more keys are pressed
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    headLeftChange = 0
                    headRightChange = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    headUpChange = 0
                    headDownChange = 0

        if headX <= 0: #makes sure the player cannot exit the screen boundaries
            headLeftChange = 0
        elif headX >= screenWidth - charWidth:
            headRightChange = 0
        if headY <= 0:
            headUpChange = 0
        elif headY >= screenHeight - charHeight:
            headDownChange = 0
        
        headX += headLeftChange #updates the location based off of the keys pressed
        headX += headRightChange
        headY += headUpChange
        headY += headDownChange

        if headX > enemyX: #has the enemy move towards the player coordinates based off of the coordinates of the player and the coordinates of the enemy
            enemyX += enemySpeed
        elif headX < enemyX:
            enemyX -= enemySpeed
        if headY > enemyY:
            enemyY += enemySpeed
        elif headY < enemyY:
            enemyY -= enemySpeed

        gameDisplay.blit(background,(0,0))
        powerupDisplay = pygame.Surface((100,100))
        powerupDisplay.fill((128,128,128,128))
        gameDisplay.blit(powerupDisplay,((screenWidth/2)-50,0))
        if (powerupSpeedUp):
            gameDisplay.blit(chilichar,((screenWidth/2)-50,0))
        elif (powerupSpeedDown):
            gameDisplay.blit(turtlechar,((screenWidth/2)-50,0))
        elif (powerupReverse):
            gameDisplay.blit(tacochar,((screenWidth/2)-50,0))
        elif (powerupFreeze):
            gameDisplay.blit(icecreamchar,((screenWidth/2)-50,0))
        elif (powerupDizzy):
            gameDisplay.blit(dizzychar,((screenWidth/2)-50,0))
        #puts a square at the top of the screen and puts a powerup icon for the current powerup being used

        gameDisplay.blit(cookiechar,(randCookieX,randCookieY))
        gameDisplay.blit(mainchar,(headX,headY))
        gameDisplay.blit(enemychar,(enemyX,enemyY))
        gameDisplay.blit(mysteryBoxChar,(mysteryBoxX,mysteryBoxY))
        gameDisplay.blit(icecreamchar,(icecreamX,icecreamY))
        gameDisplay.blit(chilichar,(chiliX,chiliY))
        gameDisplay.blit(tacochar,(tacoX,tacoY))
        updateScore(score)
        #displays the game's objects

        pygame.display.update()

        if detectCollision(headX,randCookieX,headY,randCookieY,mainchar.get_width(),randCookieWidth,mainchar.get_height(),randCookieHeight): #checks if the player collides with a cookie and increases the player size and the score
            randCookieX = random.randrange(0,screenWidth - randCookieWidth)
            randCookieY = random.randrange(0,screenHeight - randCookieHeight)
            mainchar = pygame.transform.scale(mainchar,(mainchar.get_width()+10,mainchar.get_height()+10))
            charWidth += 10
            charHeight += 10
            score += 100
        
        if detectCollision(headX,enemyX,headY,enemyY,charWidth,enemyWidth,charHeight,enemyHeight) and immunity == False: #checks if the player collides with the enemy and shrinks the player and makes the player invisible temporarily
            if powerupReverse:
                enemychar = pygame.transform.scale(enemychar,(enemyWidth-10,enemyHeight-10))
                enemyWidth -= 10
                enemyHeight -= 10
                mainchar = pygame.transform.scale(mainchar,(charWidth+10,charHeight+10))
                charWidth += 10
                charHeight += 10
            else:
                mainchar = pygame.transform.scale(mainchar,(mainchar.get_width()-10,mainchar.get_height()-10))
                charWidth -= 10
                charHeight -= 10
            immunity = True
            immunityTime = pygame.time.get_ticks()    

        if detectCollision(headX,mysteryBoxX,headY,mysteryBoxY,charWidth,mysteryBoxWidth,charHeight,mysteryBoxHeight):
            mysteryBoxOpenTime = pygame.time.get_ticks()
            mysteryBoxOnScreen = False
            mysteryBoxX = 5000
            mysteryBoxY = 5000
            powerup = random.randrange(1,6)
            if powerup == 1:
                disablePowerups()
                tempSpeedUpSpeed = playerSpeed
                playerSpeed = playerSpeed + 5
                powerupSpeedUp = True
                powerupSpeedUpTime = pygame.time.get_ticks()
            elif powerup == 2:
                disablePowerups()
                tempSpeedDownSpeed = playerSpeed
                playerSpeed = enemySpeed + 1
                powerupSpeedDown = True
                powerupSpeedDownTime = pygame.time.get_ticks()
            elif powerup == 3:
                disablePowerups()
                tempFreezeSpeed = enemySpeed
                enemySpeed = 1
                powerupFreeze = True
                powerupFreezeTime = pygame.time.get_ticks()
            elif powerup == 4:
                disablePowerups()
                tempReverseSpeed = enemySpeed
                enemySpeed *= -1
                powerupReverse = True
                powerupReverseTime = pygame.time.get_ticks()
            elif powerup == 5:
                disablePowerups()
                tempDizzySpeed = playerSpeed
                playerSpeed = 0
                powerupDizzy = True
                powerupDizzyTime = pygame.time.get_ticks()

        if detectCollision(headX,icecreamX,headY,icecreamY,charWidth,icecreamWidth,charHeight,icecreamHeight):
            disablePowerups()
            powerupOpenTime = pygame.time.get_ticks()
            powerupFreezeTime = pygame.time.get_ticks()
            powerupOnScreen = False
            icecreamX = 5000
            icecreamY = 5000
            tempFreezeSpeed = enemySpeed
            enemySpeed = 1
            powerupFreeze = True
            powerupFreezeTime = pygame.time.get_ticks()

        if detectCollision(headX,chiliX,headY,chiliY,charWidth,chiliWidth,charHeight,chiliHeight):
            disablePowerups()
            powerupOpenTime = pygame.time.get_ticks()
            powerupSpeedUpTime = pygame.time.get_ticks()
            powerupOnScreen = False
            chiliX = 5000
            chiliY = 5000
            tempSpeedUpSpeed = playerSpeed
            playerSpeed = playerSpeed * 2
            powerupSpeedUp = True

        if detectCollision(headX,tacoX,headY,tacoY,charWidth,tacoWidth,charHeight,tacoHeight):
            disablePowerups()
            powerupOpenTime = pygame.time.get_ticks()
            powerupReverseTime = pygame.time.get_ticks()
            powerupOnScreen = False
            tacoX = 5000
            tacoY = 5000
            tempReverseSpeed = enemySpeed
            enemySpeed *= -1
            powerupReverse = True

        if enemyWidth < 30:
            disablePowerups()
            enemychar = pygame.transform.scale(enemychar,(30,30))
            enemyWidth = 30
            enemyHeight = 30
        #makes sure the enemy doesn't get too small when the reverse powerup is active

        if charWidth < 50 and charHeight < 50: #ends the game when the player becomes smaller than its original size
            gameOver = True

        if pygame.time.get_ticks() - immunityTime > 500: #makes sure that the player isn't invisible for more than half a second (500 milliseconds)
            immunity = False 

        if pygame.time.get_ticks() - powerupSpeedUpTime > 6000 and powerupSpeedUp:
            playerSpeed = screenHeight/94
            powerupSpeedUp = False
            powerupSpeedUpTime = 0

        if pygame.time.get_ticks() - powerupSpeedDownTime > 6000 and powerupSpeedDown:
            playerSpeed = screenHeight/94
            powerupSpeedDown = False
            powerupSpeedDownTime = 0

        if pygame.time.get_ticks() - powerupFreezeTime > 4000 and powerupFreeze:
            enemySpeed = tempFreezeSpeed
            powerupFreeze = False
            powerupFreezeTime = 0

        if pygame.time.get_ticks() - powerupReverseTime > 4000 and powerupReverse:
            enemySpeed = tempReverseSpeed
            powerupReverse = False
            powerupReverseTime = 0
        
        if pygame.time.get_ticks() - powerupDizzyTime > 3000 and powerupDizzy:
            playerSpeed = tempDizzySpeed
            powerupDizzy = False
            powerupDizzyTime = 0

        if score > 0 and score % 500 == 0 and score / 500 != counter1:
            enemychar = pygame.transform.scale(enemychar,(enemychar.get_width()+10,enemychar.get_height()+10))
            enemyWidth += 10
            enemyHeight += 10
            counter1 += 1 #counter that makes sure the enemy doesn't grow every frame that the score stays the same
        
        if score > 0 and score % 1000 == 0 and score / 1000 != counter2 and enemySpeed < 4: #makes the enemy 1 unit faster every 1000 points until it reaches a speed of 4 pixels per second
            enemySpeed += 1
            counter2 += 1 #counter that makes sure that the speed doesn't increase every frame that the score stays the same

        powertype = random.randrange(1,3)
        if powertype == 1 and not(powerupOnScreen):
            if not(mysteryBoxOnScreen) and pygame.time.get_ticks() - mysteryBoxOpenTime > 30000:
                mysteryBoxOnScreen = True
                mysteryBoxX = random.randrange(0,screenWidth - mysteryBoxWidth)
                mysteryBoxY = random.randrange(0,screenHeight - mysteryBoxHeight)
                mysteryBoxOpenTime = 0
        elif powertype == 2 and not(mysteryBoxOnScreen):
            if not(powerupOnScreen) and pygame.time.get_ticks() - powerupOpenTime > 12000:
                choice = random.randrange(1,3)
                if choice == 1:
                    icecreamX = random.randrange(0,screenWidth - icecreamWidth)
                    icecreamY = random.randrange(0,screenHeight - icecreamHeight)
                elif choice == 2:
                    chiliX = random.randrange(0,screenWidth - chiliWidth)
                    chiliY = random.randrange(0,screenHeight - chiliHeight)
                elif choice == 3:
                    tacoX = random.randrange(0,screenWidth - tacoWidth)
                    tacoY = random.randrange(0,screenHeight - tacoHeight)
                powerupOnScreen = True
                powerupOpenTime = 0
        #chooses a random powerup or mystery box to appear on the screen

        clock.tick(60) #runs the game at 60 fps

    pygame.quit()
    quit()

gameIntro()
gameLoop()