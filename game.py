import pygame
import sys
import time
import random
import math
from pygame.locals import *
from spritesheet_functions import SpriteSheet
from constants import *

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 320x240 sized screen
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

class Pointer(pygame.sprite.Sprite):
    def __init__(self):
        self.x_change = 0
        self.y_change = 0
        pygame.sprite.Sprite.__init__(self)
        self.image_poin = minesign_image.get_image(305, 8, 26.5, 24)
        self.rect = self.image_poin.get_rect()
        self.x_point, self.y_point = self.rect.topleft

    def xy_move(self):
        #print(self.rect.topleft)
        self.x_point += self.x_change
        self.y_point += self.y_change
        if (self.x_point <= 220):
           self.rect.topleft = (self.x_point, self.y_point)
        elif(self.x_point > 220):
           self.x_point = 220
           self.rect.topleft = (self.x_point, self.y_point)
        if (self.x_point >= 15):
           self.rect.topleft = (self.x_point, self.y_point)
        elif(self.x_point < 15):
           self.x_point = 15
           self.rect.topleft = (self.x_point, self.y_point)

        if (self.y_point <= 220):
           self.rect.topleft = (self.x_point, self.y_point)
        elif(self.y_point > 220):
           self.y_point = 220
           self.rect.topleft = (self.x_point, self.y_point)
        if (self.y_point >= 15):
           self.rect.topleft = (self.x_point, self.y_point)
        elif(self.y_point < 15):
           self.y_point = 15
           self.rect.topleft = (self.x_point, self.y_point)



class TimerDig(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def timer_sec(self):
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
    def update(self):
        #print(timeElapsed)
        xdig1, xdig2, xdig3, enti = self.timer_sec()
        self.image1 = minesign_image.get_image(xdig1, 7.5, 25, 45)
        self.image2 = minesign_image.get_image(xdig2, 7.5, 25, 45)
        self.image3 = minesign_image.get_image(xdig3, 7.5, 25, 45)

class BombCounter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.bombCount = BOMBCOUNT
    def changecount(self):
        return Pointer.rect.topleft
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
        self.blankImg = minesign_image.get_image(305, 32, 20, 20)
        self.blockImg = minesign_image.get_image(330, 32, 20, 20)
        self.flagImg = minesign_image.get_image(355, 32, 20, 20)
        self.bombImg = minesign_image.get_image(380, 32, 20, 20)
        self.endBombImg = minesign_image.get_image(405, 32, 20, 20)
        self.noBombImg = minesign_image.get_image(430, 32, 20, 20)
        self.bombCount = BOMBCOUNT
        self.ROWS = 9
        self.COLUMNS = 9
        self.pointerPos = (0, 0)
        self.gameStop = False

        #Define the defualt array for mineField, touchingField, and coverField.
        self.mineField = mineField
        self.touchingField = touchingField
        self.coverField = coverField
        self.mineField = self.placeBombs(self.bombCount)
        for blockY in range(self.ROWS):
             for blockX in range(self.COLUMNS):
                  self.searchSurrounding(blockX, blockY, self.ROWS, self.COLUMNS)
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
    def searchSurrounding(self,blockX,blockY, ROWS, COLUMNS):
        blockX = blockX
        blockY = blockY
        if self.mineField[blockY-1][blockX-1] == 1 and blockY > 0 and blockX > 0:
                self.touchingField[blockY][blockX] += 1

        if self.mineField[blockY-1][blockX] == 1 and blockY > 0:
                self.touchingField[blockY][blockX] += 1

        if blockX < COLUMNS-1 and self.mineField[blockY-1][blockX+1] == 1 and blockY > 0:
                self.touchingField[blockY][blockX] += 1

        if self.mineField[blockY][blockX-1] == 1 and blockX > 0:
                self.touchingField[blockY][blockX] += 1

        if blockX < COLUMNS-1 and self.mineField[blockY][blockX+1] == 1:
                self.touchingField[blockY][blockX] += 1

        if blockY < ROWS-1 and self.mineField[blockY+1][blockX-1] == 1 and blockX > 0:
                self.touchingField[blockY][blockX] += 1

        if blockY < ROWS-1 and self.mineField[blockY+1][blockX] == 1 :
                self.touchingField[blockY][blockX] += 1

        if blockY < ROWS-1 and blockX < COLUMNS-1 and self.mineField[blockY+1][blockX+1] == 1:
                self.touchingField[blockY][blockX] += 1


    #Returns displayable textSurface.get_rect().
    def textObjects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()
        #Display text object in gameDispay.
    def textDisplay(self, text, x, y, color, type):
        if type == "Block":
                numberText = pygame.font.Font("minesweeper.ttf", round(TILE_SIZE*(2/3)-4))
                textSurf, textRect = self.textObjects(text, numberText, color)
                #textRect.center = (x + TILE_SIZE/2, y + TILE_SIZE/2)
                textRect.center = (int(x + TILE_SIZE/2), int(y + TILE_SIZE/2))
                screen.blit(textSurf, textRect)
    #Draw the image as a number from touchingField or as a bomb from mineField.
    def numBlock(self, blockX, blockY):
        arrayRow = blockX
        arrayCol = blockY
        one = (0,0,255)
        two = (0,123,0)
        three = (255,0,0)
        four = (0,0,123)
        five = (123,0,0)
        six = (0,123,123)
        seven = (0,255,0)
        eight = (123,123,123)
        touchingBombs = str(self.touchingField[arrayRow][arrayCol])
        touchingBombsLabel = str(touchingBombs)
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

        if touchingBombsLabel != "0":
                return (touchingBombsLabel, labelColor)
                #self.textDisplay(touchingBombsLabel, blockX, blockY, labelColor, "Block")
        if touchingBombsLabel == "0":
                labelColor = "0",(0,0,0)
                return (touchingBombsLabel, labelColor)

    #Recursively uncover the blocks that are not a bomb, in layers outwards.
    def testSurrounding(self, cellColumn, cellRow):
        COLUMNS = 9
        ROWS = 9
        if self.mineField[cellRow][cellColumn] == 0 and self.touchingField[cellRow][cellColumn] == 0:
                #Test if edges are uncoverable.
                if cellRow > 0 and self.coverField[cellRow-1][cellColumn] == 0:
                        self.coverField[cellRow-1][cellColumn] = 5
                        self.testSurrounding(cellColumn, cellRow-1)

                if cellColumn > 0 and self.coverField[cellRow][cellColumn-1] == 0:
                        self.coverField[cellRow][cellColumn-1] = 5
                        self.testSurrounding(cellColumn-1, cellRow)

                if cellColumn < COLUMNS-1 and self.coverField[cellRow][cellColumn+1] == 0:
                        self.coverField[cellRow][cellColumn+1] = 5
                        self.testSurrounding(cellColumn+1, cellRow)

                if cellRow < ROWS-1 and self.coverField[cellRow+1][cellColumn] == 0:
                        self.coverField[cellRow+1][cellColumn] = 5
                        self.testSurrounding(cellColumn, cellRow+1)

                #Test if corners are uncoverable.
                if cellRow > 0 and cellColumn > 0 and self.coverField[cellRow-1][cellColumn-1] == 0:
                        self.coverField[cellRow-1][cellColumn-1] = 5
                        self.testSurrounding(cellColumn-1, cellRow-1)

                if cellColumn < COLUMNS-1 and cellRow > 0 and self.coverField[cellRow-1][cellColumn+1] == 0:
                        self.coverField[cellRow-1][cellColumn+1] = 5
                        self.testSurrounding(cellColumn+1, cellRow-1)

                if cellRow < ROWS-1 and cellColumn > 0 and self.coverField[cellRow+1][cellColumn-1] == 0:
                        self.coverField[cellRow+1][cellColumn-1] = 5
                        self.testSurrounding(cellColumn-1, cellRow+1)

                if cellRow < ROWS-1 and cellColumn < COLUMNS-1 and self.coverField[cellRow+1][cellColumn+1] == 0:
                        self.coverField[cellRow+1][cellColumn+1] = 5
                        self.testSurrounding(cellColumn+1, cellRow+1)

    def findCell(self):
        pointPosX, pointPosY = self.pointerPos
        xy = (9,9)
        if not self.gameStop:
           for arrayRow in range(0, ROWS):
               blockY = arrayRow * (TILE_SIZE + 5)
               blockY += PADDING
               if pointPosY > blockY and pointPosY < blockY + TILE_SIZE:
                  for arrayCol in range(0, COLUMNS):
                      blockX = arrayCol * (TILE_SIZE + 5)
                      blockX += PADDING
                      if pointPosX > blockX and pointPosX < blockX + TILE_SIZE:
                                      xy = (arrayRow, arrayCol)
        return (xy)

    def bombinCover(self):
        for arrayRow in range(0, ROWS):
            for arrayCol in range(0, COLUMNS):
                #print(self.mineField[arrayRow][arrayCol])
                if self.mineField[arrayRow][arrayCol] == 1 and self.coverField[arrayRow][arrayCol] == 0:
                   self.coverField[arrayRow][arrayCol] = 2
                if self.mineField[arrayRow][arrayCol] == 0 and self.coverField[arrayRow][arrayCol] == 1:
                   self.coverField[arrayRow][arrayCol] = 4
                   BombCounter.bombCount += 1


    def pressA(self):
        Row, Col = self.findCell()
        #print(Row, Col)
        if not Row == 9 and not Col == 9:
           if self.coverField[Row][Col] == 1:
              pass
           elif self.coverField[Row][Col] == 0 and self.mineField[Row][Col] == 1:
              self.coverField[Row][Col] = 3
              self.bombinCover()
              self.gameStop = True
              #BombCounter.bombCount += 1
           elif self.coverField[Row][Col] == 0 and self.mineField[Row][Col] == 0:
              self.coverField[Row][Col] = 5
        else:
            pass

    def pressB(self):
        Row, Col = self.findCell()
        #print(Row, Col)
        if not Row == 9 and not Col == 9:
           if self.coverField[Row][Col] == 0 and BombCounter.bombCount > 0:
              self.coverField[Row][Col] = 1
              BombCounter.bombCount -= 1
           elif self.coverField[Row][Col] == 1:
              self.coverField[Row][Col] = 0
              BombCounter.bombCount += 1
        else:
            pass

    def show(self):
        for arrayRow in range(0, ROWS):
            for arrayCol in range(0, COLUMNS):
                blockX = arrayCol * (TILE_SIZE + 5)
                blockY = arrayRow * (TILE_SIZE + 5)
                blockX += PADDING
                blockY += PADDING
                if self.coverField[arrayRow][arrayCol] == 0:
                   screen.blit(self.blockImg, (blockX, blockY))
                elif self.coverField[arrayRow][arrayCol] == 1:
                   screen.blit(self.flagImg, (blockX, blockY))
                elif self.coverField[arrayRow][arrayCol] == 2:
                   screen.blit(self.bombImg, (blockX, blockY))
                elif self.coverField[arrayRow][arrayCol] == 3:
                   screen.blit(self.endBombImg, (blockX, blockY))
                elif self.coverField[arrayRow][arrayCol] == 4:
                   screen.blit(self.noBombImg, (blockX, blockY))
                elif self.coverField[arrayRow][arrayCol] == 5:
                   screen.blit(self.blankImg, (blockX, blockY))
                   num1 , num2 = self.numBlock(arrayRow, arrayCol)
                   if num1 != "0":
                      self.textDisplay(num1, blockX, blockY, num2, "Block")
                   elif num1 == "0":
                      self.testSurrounding(arrayRow, arrayCol)
        #pass

    def update(self):
        #pointPosX, pointPosY = self.pointerPos
        #print(pointPosX, pointPosY)
        pass


all_sprites = pygame.sprite.Group()
TimerDig = TimerDig()
Pointer = Pointer()
Allfield = allfield()
BombCounter = BombCounter()
all_sprites.add(TimerDig,BombCounter,Allfield)
done = False

while not done:
    #clock.tick_busy_loop(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            if event.key == pygame.K_UP:
                Pointer.y_change = -3
            if event.key == pygame.K_DOWN:
                Pointer.y_change = 3
            if event.key == pygame.K_RIGHT:
                Pointer.x_change = 3
            if event.key == pygame.K_LEFT:
                Pointer.x_change = -3
            if event.key == pygame.K_a:
                Allfield.pointerPos = BombCounter.changecount()
                Allfield.pressA()
            if event.key == pygame.K_b:
                Allfield.pointerPos = BombCounter.changecount()
                Allfield.pressB()
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
    Allfield.show()
    screen.blit(Pointer.image_poin, (Pointer.rect))
    #timeElapsed += 16.66676
    timeElapsed += 40
    pygame.display.flip()
    clock.tick(30)


pygame.quit()
