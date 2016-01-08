import math
import sys
from collections import defaultdict


def quitProcessing(event):
    print "Done!"
    sys.exit(0)

Env.addHotkey(Key.ESC, KeyModifier.SHIFT, quitProcessing)
               
def getTileIndex(x, y):
    index = (int((x - leftX) / tileW), int((y - leftY) / tileH))
    return index

def findTilePositions(tileType, tileImg):
    parseMatches(puzRegion.findAll(tileImg), tileType)

def parseMatches(matches, tileType):
    while matches.hasNext():
        tileData = matches.next()
        #tileData.highlight()
        tileData = tileData.getTarget()
        tileIndex = getTileIndex(tileData.getX(), tileData.getY())
        prevValue = 0
        if tileType in puzzleTiles[tileIndex[1]]:
            prevValue = puzzleTiles[tileIndex[1]][tileType]
        else:
            puzzleTiles[tileIndex[1]][tileType] = 0
        puzzleTiles[tileIndex[1]][tileType] = prevValue | (1 << tileIndex[0])

def clickAtRegion(action):
    puzRegion.mouseMove(action)
    puzRegion.mouseDown(Button.LEFT)
    puzRegion.mouseUp(Button.LEFT)

def getPosOfSetBit(bit):
    if bit == 0:
        return 0
    return int(math.log(bit)/math.log(2))

print "A bot to play 3-Match!"
print "Python version %s" % (sys.version)

# Define the puzzle region
windowTopLeft = find("1452210177625.png").getTarget()
windowBottomRight = find("1452210191657.png").getTarget()
leftX = windowTopLeft.getX()
leftY = windowTopLeft.getY()
rightX = windowBottomRight.getX()
rightY = windowBottomRight.getY()
width = rightX - leftX
height = rightY - leftY
puzRegion = Region(leftX, leftY, width, height)
Settings.MinSimilarity = 0.95

# Print some data about the puzzle
print "=Puzzle Region=" 
print "Pos: %d, %d" % (leftX, leftY)
print "Bounds: %d, %d" % (width, height)
tileW = width / 8
tileH = height / 8
print "=Tile Data="
print "Size: %d, %d" % (tileW, tileH)
tileTypes = {0: "1452210238386.png", 1: "1452210253817.png", 2: "1452210263737.png", 3: "1452211649479.png", 4: "1452210282937.png", 5: "1452210297009.png", 6: "1452210319985.png"}
print tileTypes

# Build the gamestate
puzzleTiles = defaultdict(dict)
for key in tileTypes:
    findTilePositions(key, tileTypes[key])
print "Puzzle State: "
print puzzleTiles

# Give the Game Window focus
clickAtRegion(puzRegion)
clickAtRegion(puzRegion)

matchFound = 0
#while(matchFound == 1):
 #   matchFound = 0
for key in puzzleTiles:
    curRow = puzzleTiles[key]
    if matchFound == 1:
        break
    for tileType in curRow:
        if matchFound == 1:
            break
        marks = curRow[tileType]
        xox = marks & (marks << 2)
        xx = marks & (marks << 1)
        binCount = bin(marks).count("1")
        if key == 2 and tileType == 2:
            print "XOX %d, XX %d" % (getPosOfSetBit(xox), getPosOfSetBit(xx))
        delta = getPosOfSetBit(xox) - getPosOfSetBit(xx)
        if binCount >= 3 and delta > 0 and delta < 3:
            print "Key %d, Type %d, Val %d" % (key, tileType, marks)
            print "Found! Checking for deceit..."
            if getPosOfSetBit(xx) == 0 and curRow[getPosOfSetBit(xx)] != tileType:
                continue
            
            print "XOX %d, XX %d" % (xox, xx)
            col = getPosOfSetBit(xox >> 1)
            print "Col %d" % (col)
            action = Region(col * tileW + leftX, key * tileH + leftY, tileW, tileH)
            action.highlight(1)
            action.setX(action.getX())
            clickAtRegion(action)
            if xx > xox:
                action.setX(action.getX() - tileW)
            else:
                action.setX(action.getX() + tileW)
            clickAtRegion(action)
            #puzRegion.mouseDown(Button.LEFT)
            #puzRegion.mouseUp(Button.LEFT)
            matchFound = 1

if matchFound == 0:
    print "Found no matches, make me better :("
