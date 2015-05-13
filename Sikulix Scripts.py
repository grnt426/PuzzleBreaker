import math
from collections import defaultdict

def quitProcessing(event):
    print "Done!"
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
    
Env.addHotkey(Key.ESC, KeyModifier.SHIFT, quitProcessing)

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

# Find a simple match
typeRow = puzzleTiles[7][2]
xox = typeRow & (typeRow << 2)
xx = typeRow & (typeRow << 1)
print xox
print xx
if xox - xx >= 0:
    action = Region(3 * tileW + leftX, 7 * tileH + leftY, tileW, tileH)
    action.highlight()
    puzRegion.mouseMove(action)