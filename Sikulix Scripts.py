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
    matches = puzRegion.findAll(tileImg)
    while matches.hasNext():
        tileData = matches.next()
        tileData = tileData.getTarget()
        tileIndex = getTileIndex(tileData.getX(), tileData.getY())
        prevValue = 0
        if tileType in puzzleTiles[tileIndex[1]]:
            prevValue = puzzleTiles[tileIndex[1]][tileType]
        else:
            puzzleTiles[tileIndex[1]][tileType] = 0
        puzzleTiles[tileIndex[1]][tileType] = prevValue | (1 << tileIndex[0])

print "A bot to play Puzzle Pirates!"

# Define the puzzle region
windowTopLeft = find("topLeftCorner.png").getTarget()
windowBottomRight = find("bottomRightCorner.png").getTarget()
leftX = windowTopLeft.getX()
leftY = windowTopLeft.getY()
rightX = windowBottomRight.getX()
rightY = windowBottomRight.getY()
width = rightX - leftX
height = rightY - leftY
puzRegion = Region(leftX, leftY, width, height)

# Print some data about the puzzle
print "=Puzzle Region=" 
print "Pos: %d, %d" % (leftX, leftY)
print "Bounds: %d, %d" % (width, height)
tileW = width / 6
tileH = height / 12
print "=Tile Data="
print "Size: %d, %d" % (tileW, tileH)
tileTypes = {0: "blueSquare.png", 1: "blueCircle.png", 2: "whiteCircle.png", 3: "bigOctagon.png", 4: "smallOctagon.png"}
print tileTypes

# Build the gamestate
puzzleTiles = defaultdict(dict)
for key in tileTypes:
    findTilePositions(key, tileTypes[key])
print
print "Puzzle State: "
print puzzleTiles

def convertBitMaskToCount(i):
    i = i - ((i >> 1) & 0x55555555);
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333);
    return (((i + (i >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24;

def getPosOfSetBit(bit):
    if bit == 1:
        return 0
    elif bit == 2:
        return 1
    elif bit == 4:
        return 2
    elif bit == 8:
        return 3
    elif bit == 16:
        return 4
    elif bit == 32:
        return 5

matchFound = 0
for key in puzzleTiles:
    curRow = puzzleTiles[key]
    for tileType in curRow:
        marks = curRow[tileType]
        xox = marks & (marks << 2)
        xx = marks & (marks << 1)
        if convertBitMaskToCount(marks) > 2 and (xox - xx) > 0:
            print "Key %d, Type %d, Val %d" % (key, tileType, marks)
            print "XOX %d, XX %d" % (xox, xx)
            col = getPosOfSetBit(xox >> 1)
            action = Region(col * tileW + leftX, key * tileH + leftY, tileW, tileH)
            action.highlight(1)
            action.setX(action.getX() + 5)
            puzRegion.mouseMove(action)
            puzRegion.mouseDown(Button.LEFT)
            puzRegion.mouseUp(Button.LEFT)
            matchFound = 1

if matchFound == 0:
    print "Found no matches, make me better :("
