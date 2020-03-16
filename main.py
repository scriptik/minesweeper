import pygame
import sys
import time
import random
import math
from pygame.locals import *
from spritesheet_functions import SpriteSheet
#from mainfield import mainfield

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

MAX_TIME = 180
BOMBCOUNT = 20
timeElapsed = 0
timeEnd = False

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([320, 240])

# This sets the name of the window
pygame.display.set_caption('minesweeper')

clock = pygame.time.Clock()

# Before the loop, load the sounds:
#click_sound = pygame.mixer.Sound("laser5.ogg")

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics.
background_image = pygame.image.load("minebg.png").convert()
minesign_image = SpriteSheet("minesign.png")

def timer_sec():
    global timeElapsed
    global seconds
    #timeElapsed += 16.66676
    seconds = round(timeElapsed / 1000)
    #print(180-seconds)

    if MAX_TIME-seconds >= 0:
       global timeEnd
       rem_sec = str(MAX_TIME-seconds)
       dig_pos = {"0":5,"1":35,"2":65,"3":95,"4":125,"5":155,"6":185,"7":215,"8":245,"9":275}
       if len(rem_sec) == 3:
          x1_dig = dig_pos[rem_sec[0]]
          x2_dig = dig_pos[rem_sec[1]]
          x3_dig = dig_pos[rem_sec[2]]
       elif len(rem_sec) == 2:
          x1_dig = dig_pos["0"]
          x2_dig = dig_pos[rem_sec[0]]
          x3_dig = dig_pos[rem_sec[1]]
       elif len(rem_sec) == 1:
          x1_dig = dig_pos["0"]
          x2_dig = dig_pos["0"]
          x3_dig = dig_pos[rem_sec[0]]
       return(x1_dig,x2_dig,x3_dig,timeEnd)
    else:
       dig_pos = {"0":5,"1":35,"2":65,"3":95,"4":125,"5":155,"6":185,"7":215,"8":245,"9":275}
       print("Time END")
       x1_dig = dig_pos["0"]
       x2_dig = dig_pos["0"]
       x3_dig = dig_pos["0"]
       timeEnd = True
       return(x1_dig,x2_dig,x3_dig,timeEnd)

class Pointer(pygame.sprite.Sprite):
    def __init__(self,x_change,y_change):
        self.x_change = x_change
        self.y_change = y_change
        pygame.sprite.Sprite.__init__(self)
        self.image_poin = minesign_image.get_image(305, 8, 26.5, 24)
        self.rect = self.image_poin.get_rect()
        self.x_point, self.y_point = self.rect.topleft

    def xy_move(self):
        #print(self.rect.topleft)
        self.x_point += self.x_change
        self.y_point += self.y_change
        if (self.x_point <= 210):
           self.rect.topleft = (self.x_point, self.y_point)
        elif(self.x_point > 210):
           self.x_point = 210
           self.rect.topleft = (self.x_point, self.y_point)
        if (self.x_point >= 0):
           self.rect.topleft = (self.x_point, self.y_point)
        elif(self.x_point < 0):
           self.x_point = 0
           self.rect.topleft = (self.x_point, self.y_point)

        if (self.y_point <= 220):
           self.rect.topleft = (self.x_point, self.y_point)
        elif(self.y_point > 220):
           self.y_point = 220
           self.rect.topleft = (self.x_point, self.y_point)
        if (self.y_point >= 0):
           self.rect.topleft = (self.x_point, self.y_point)
        elif(self.y_point < 0):
           self.y_point = 0
           self.rect.topleft = (self.x_point, self.y_point)



class TimerDig(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        #print(timeElapsed)
        xdig1, xdig2, xdig3, enti = timer_sec()
        self.image1 = minesign_image.get_image(xdig1, 7.5, 25, 45)
        self.image2 = minesign_image.get_image(xdig2, 7.5, 25, 45)
        self.image3 = minesign_image.get_image(xdig3, 7.5, 25, 45)

class BombCounter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.bombCount = BOMBCOUNT
    def changecount(self):
        #self.x_point, self.y_point = Pointer.rect.topleft
        print(Pointer.rect.topleft)
        if self.bombCount > 0:
           self.bombCount -= 1
        elif self.bombCount == 0:
           self.bombCount = 0
    def update(self):
        self.dig_pos = {"0":5,"1":35,"2":65,"3":95,"4":125,"5":155,"6":185,"7":215,"8":245,"9":275}
        self.bombCountDig = str(self.bombCount)
        if self.bombCount >= 10:
           self.bombCountDig1 = self.dig_pos[self.bombCountDig[0]]
           self.bombCountDig2 = self.dig_pos[self.bombCountDig[1]]
        elif self.bombCount < 10:
           self.bombCountDig1 = self.dig_pos["0"]
           self.bombCountDig2 = self.dig_pos[self.bombCountDig[0]]
        self.image1 = minesign_image.get_image(self.bombCountDig1, 7.5, 25, 45)
        self.image2 = minesign_image.get_image(self.bombCountDig2, 7.5, 25, 45)
        #print(timeElapsed)



class allfield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_cover = minesign_image.get_image(305, 32, 20, 20)
        self.bombCount = BOMBCOUNT
        self.ROWS = 9
        self.COLUMNS = 9

        #Define the defualt array for mineField, touchingField, and coverField.
        self.mineField = [
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             ]
        self.touchingField = [
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             ]
        self.coverField = [
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             ]
        self.mineField = self.placeBombs(self.bombCount)
        for blockY in range(self.ROWS):
             for blockX in range(self.COLUMNS):
                  self.searchSurrounding(blockX, blockY, self.ROWS, self.COLUMNS, self.mineField, self.touchingField)
        print(self.touchingField)
    #Randomly place bombs in mineField.
    def placeBombs(self,bombCount):
        mineField = [
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,0],
             ]
        #bombCount = 15
        COLUMNS = 9
        ROWS = 9

        bombpos =[]
        answerSize = 0
        #Randomly generate mine coordinates withing the array.

        while answerSize < bombCount:
             tempX = str(random.randrange(0, COLUMNS))
             tempY = str(random.randrange(0, ROWS))
             pos = tempX+tempY
             if pos not in bombpos:
                 answerSize += 1
                 bombpos.append(pos)

        for pos in bombpos:
            tempX = int(pos[0])
            tempY = int(pos[1])
            mineField[tempX][tempY] = 1

        print(bombpos)
        print(len(bombpos))
        print(mineField)
        return mineField

    #Determine the amount of surrounding bombs for the given index in touchingField.	
    def searchSurrounding(self,blockX,blockY, ROWS, COLUMNS, mineField,touchingField):
        blockX = blockX
        blockY = blockY
        mineField = mineField
        touchingField = touchingField
        if mineField[blockY-1][blockX-1] == 1 and blockY > 0 and blockX > 0:
                touchingField[blockY][blockX] += 1

        if mineField[blockY-1][blockX] == 1 and blockY > 0:
                touchingField[blockY][blockX] += 1

        if blockX < COLUMNS-1 and mineField[blockY-1][blockX+1] == 1 and blockY > 0:
                touchingField[blockY][blockX] += 1

        if mineField[blockY][blockX-1] == 1 and blockX > 0:
                touchingField[blockY][blockX] += 1

        if blockX < COLUMNS-1 and mineField[blockY][blockX+1] == 1:
                touchingField[blockY][blockX] += 1

        if blockY < ROWS-1 and mineField[blockY+1][blockX-1] == 1 and blockX > 0:
                touchingField[blockY][blockX] += 1

        if blockY < ROWS-1 and mineField[blockY+1][blockX] == 1 :
                touchingField[blockY][blockX] += 1

        if blockY < ROWS-1 and blockX < COLUMNS-1 and mineField[blockY+1][blockX+1] == 1:
                touchingField[blockY][blockX] += 1
    #Display text object in gameDispay.
    def textDisplay(text, x, y, color, type):
        if type == "Block":
                numberText = pygame.font.Font("Media/minesweeper.ttf", round(TILE_SIZE*(2/3)-1))
                textSurf, textRect = textObjects(text, numberText, color)
                textRect.center = (x + TILE_SIZE/2, y + TILE_SIZE/2)
                screen.blit(textSurf, textRect)
    #Draw the image as a number from touchingField or as a bomb from mineField.
    def bombBlock(arrayCol, arrayRow):
        blockX = arrayCol * TILE_SIZE
        blockY = arrayRow * TILE_SIZE

        touchingBombs = str(touchingField[arrayRow][arrayCol])
        print(touchingBombs)
        touchingBombsLabel = str(touchingBombs)
        print(touchingBombsLabel)

        #Change the block coordinates to center the sprites in gameDisplay.
        blockX += PADDING
        blockY += MARGIN*2 + PADDING*2

        blockType = "Blank"

        one = (0,0,255)
        two = (0,123,0)
        three = (255,0,0)
        four = (0,0,123)
        five = (123,0,0)
        six = (0,123,123)
        seven = (0,255,0)
        eight = (123,123,123)
        #labelColors = {"1":"one","2":"two","3":"three","4":"four","5":"five","6":"six","7":"seven","8":"eight"}

        #If the position in mineField is 1, this block is a bomb instead of a label.
        if mineField[arrayRow][arrayCol] == 1:
                blockType = "Bomb"

        #labelColor = labelColors[touchingBombsLabel]

        if touchingBombsLabel == "1":
                labelColor = one
        elif touchingBombsLabel == "2":
                labelColor = two
        elif touchingBombsLabel == "3":
                labelColor = three
        elif touchingBombsLabel == "4":
                labelColor = four
        elif touchingBombsLabel == "5":
                labelColor = five
        elif touchingBombsLabel == "6":
                labelColor = six
        elif touchingBombsLabel == "7":
                labelColor = seven
        elif touchingBombsLabel == "8":
                labelColor = eight

        if blockType == "Blank" and coverField[arrayRow][arrayCol] == 1:
                screen.blit(blankImg, (blockX, blockY))
                if touchingBombsLabel != "0" and coverField[arrayRow][arrayCol] == 1:
                        textDisplay(touchingBombsLabel, blockX, blockY, labelColor, "Block")
        elif blockType == "Bomb" and coverField[arrayRow][arrayCol] == 1:
                screen.blit(bombImg, (blockX, blockY))


    def update(self):
        #print(MAX_TIME-seconds)
        pass



all_sprites = pygame.sprite.Group()
TimerDig = TimerDig()
Pointer = Pointer(0,0)
Allfield = allfield()
BombCounter = BombCounter()
all_sprites.add(TimerDig,BombCounter,Allfield)
done = False

while not done:
    clock.tick_busy_loop(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            if event.key == pygame.K_UP:
                Pointer.y_change = -2
            if event.key == pygame.K_DOWN:
                Pointer.y_change = 2
            if event.key == pygame.K_RIGHT:
                Pointer.x_change = 2
            if event.key == pygame.K_LEFT:
                Pointer.x_change = -2
            if event.key == pygame.K_a:
                BombCounter.changecount()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Pointer.x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                   Pointer.y_change = 0
        #elif event.type == pygame.MOUSEBUTTONDOWN:
        #    click_sound.play()



    Pointer.xy_move()
    all_sprites.update()
    # Copy image to screen:
    screen.blit(background_image, background_position)
    screen.blit(TimerDig.image1, (235,40))
    screen.blit(TimerDig.image2, (260,40))
    screen.blit(TimerDig.image3, (285,40))
    screen.blit(BombCounter.image1, (260,115))
    screen.blit(BombCounter.image2, (285,115))
    #screen.blit(Pointer.image_poin, (Pointer.x_point,Pointer.y_point))
    for i in range(0,10):
        for j in range(0,10):
            screen.blit(Allfield.image_cover, (3+(23*i), 3+(23*j)))
    screen.blit(Pointer.image_poin, (Pointer.rect))
    timeElapsed += 16.66676
    pygame.display.flip()
    #clock.tick(30)


pygame.quit()
