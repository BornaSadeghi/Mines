from pygame import *
from gui import SimpleText, Button
import random, spritesheet, sys, timer

sys.setrecursionlimit(20000)

SIZE = 800,592
screen = display.set_mode(SIZE)
clock = time.Clock()

BEIGE = 240,240,230
RED = 255,0,0
sprites = spritesheet.sheetToSpriteArray("minesheet.png", (16,16))

topMenuHeight = 64
gridW, gridH = 20,16
cellSize = min(SIZE[0]//gridW, (SIZE[1]-topMenuHeight)//gridH)

coveredSprite = transform.scale(sprites[0], (cellSize, cellSize))
discoveredSprite = transform.scale(sprites[1], (cellSize, cellSize))
mineSprite = transform.scale(sprites[3], (cellSize, cellSize))
flagSprite = transform.scale(sprites[2], (cellSize, cellSize))
numSprites = [transform.scale(sprites[i], (cellSize, cellSize)) for i in range (3,12)]

gameIcon = image.load("icon.ico")

display.set_icon(gameIcon)
display.set_caption("Mines")

numMines = 50

class Tile:
    def __init__(self, x=0, y=0):
        self.x, self.y = x,y
        self.rect = Rect(x*cellSize,topMenuHeight+y*cellSize,cellSize,cellSize)
        
        self.numSprite = None
        self.mines = 0 # adj mines
        
        self.covered = True
        self.mine = False
        self.flag = False
        
    def updateNumber(self):
        if self.mine:
            return
        self.mines = self.countAdjMines()
        if self.mines > 0:
            self.numSprite = numSprites[self.mines]
    
    def countAdjMines(self):
        count = 0
        for x in range (self.x-1, self.x+2, 1):
            for y in range (self.y-1, self.y+2, 1):
                if 0 <= x < gridW and 0 <= y < gridH and tiles[x][y].mine:
                    count += 1
        return count    
    
    def draw(self):
        x,y = self.rect[:2]
        if self.covered:
            if hoveredTile == self and mouseHold:
                screen.blit(discoveredSprite, (x,y))
            else:
                screen.blit(coveredSprite, (x,y))
            if self.flag:
                screen.blit(flagSprite, (x,y))
        else:
            screen.blit(discoveredSprite, (x,y))
            if self.mine:
                screen.blit(mineSprite, (x,y))
            elif self.mines > 0:
                screen.blit(self.numSprite, (x,y))

def inRect(pos, rect):
    x, y = pos
    rX, rY, rW, rH = rect
    
    if rX < x < rX + rW:
        if rY < y < rY + rH:
            return True
    return False

hoveredTile = None
def getHovered(): # find which tile is hovered
    for x in range (gridW):
        for y in range (gridH):
            if inRect((mouseX, mouseY), tiles[x][y].rect):
                return tiles[x][y]

def discover (curX,curY): # use dfs to chain uncover tiles
    tile = tiles[curX][curY]
    tile.covered = False
    
    if tile.mine:
        endGame()
        return
    
    if tile.mines == 0:
        for x in range (curX-1, curX+2, 1):
            for y in range (curY-1, curY+2, 1):
                if 0 <= x < gridW and 0 <= y < gridH and tiles[x][y].covered and not tiles[x][y].mine:
                    discover (x,y)

def countCovered ():
    count = 0
    for x in range (gridW):
        for y in range (gridH):
            if tiles[x][y].covered:
                count += 1
    return count

def discoverAll():
    for x in range (gridW):
        for y in range (gridH):
            tiles[x][y].covered = False

def flagAll():
    for x in range (gridW):
        for y in range (gridH):
            tiles[x][y].flag = True

def setMines():
    for i in range (numMines): # set mines
        pos = random.choice(safeTiles)
        safeTiles.remove(pos)
        tiles[pos[0]][pos[1]].mine = True
        
    for x in range (gridW):
        for y in range (gridH):
            tiles[x][y].updateNumber()

def startGame():
    global firstClick
    firstClick = False
    safeTiles.remove((hoveredTile.x, hoveredTile.y)) # make sure that first click is not a mine
    setMines()
    timer.unpause()
    
def endGame(win=False):
    if win:
        flagAll()
    else:
        discoverAll()
    timer.pause()
    
def checkWin():
    if countCovered() == numMines:
        endGame(True)
    
def resetMines():
    global safeTiles, numFlags
    for x in range (gridW):
        for y in range (gridH):
            tiles[x][y].mine = False
            tiles[x][y].flag = False
            tiles[x][y].covered = True
            
    numFlags = 0
    safeTiles = [(x,y) for x in range (gridW) for y in range (gridH)]

def reset():
    global firstClick
    resetMines()
    timer.stop()
    firstClick = True

def genTiles():
    for x in range (gridW): # gen tiles
        tiles.append([])
        for y in range (gridH):
            tiles[x].append(Tile(x,y))

safeTiles = [(x,y) for x in range (gridW) for y in range (gridH)]
tiles = []
timer = timer.Timer()
genTiles()

numFlags = 0

resetButton = Button((0,0,topMenuHeight, topMenuHeight), reset, sprite=sprites[12])
timerUI = SimpleText((topMenuHeight,0,topMenuHeight,topMenuHeight), "%.3f" %timer.getTime(), 60)
flagCountUI = SimpleText((topMenuHeight*6, 0,topMenuHeight, topMenuHeight), "%d" %(numMines-numFlags), 60, RED)

firstClick = True # first discovery generates the field
mouseHold = False
run = True

while run:
    screen.fill(BEIGE)
    mouseX, mouseY = mouse.get_pos()
    hoveredTile = getHovered()
    
    resetButton.draw()
    timer.update()
    timerUI.update("%.3f" %timer.getTime())
    timerUI.draw()
    flagCountUI.update("%d" %(numMines-numFlags))
    flagCountUI.draw()
    
    for x in range (gridW):
        for y in range (gridH):
            tiles[x][y].draw()
    
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1: # LMB
                mouseHold = True
            elif e.button == 3: # RMB
                if hoveredTile != None and hoveredTile.covered:
                        hoveredTile.flag = not hoveredTile.flag
                        numFlags += 1 if hoveredTile.flag else -1
                
        elif e.type == MOUSEBUTTONUP:
            mouseHold = False
            resetButton.getHovered((mouseX, mouseY), True)
            
            if hoveredTile != None:
                if e.button == 1 and not hoveredTile.flag: # left click on unflagged square
                    if firstClick:
                        startGame()
                    discover(hoveredTile.x, hoveredTile.y)
                    checkWin()
        elif e.type == MOUSEMOTION:
            resetButton.getHovered((mouseX, mouseY))
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False

        elif e.type == QUIT:
            run = False
            
    display.update()
    clock.tick(60)
quit()
