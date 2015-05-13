import math

def quitProcessing(event):
    print "Done!"
def getTileIndex(x, y):
    index = (math.floor((x - leftX) / tileW), math.floor((y - leftY) / tileH))
    return index

def findTilePositions(tileType, tileImg):
    matches = puzRegion.findAll(tileImg)
    while matches.hasNext():
        tileData = matches.next()
        tileData = tileData.getTarget()
        tileIndex = getTileIndex(tileData.getX(), tileData.getY())
        puzzleTiles[tileIndex[0]][tileIndex[1]] = tileType
    
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
puzzleTiles = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
for key in tileTypes:
    findTilePositions(key, tileTypes[key])
print
print "Puzzle State: "
print puzzleTiles