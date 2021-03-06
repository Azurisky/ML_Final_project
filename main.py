# main.py


import timeController
import scoreController
import gridController
import tileController

import grapher

import ai
import time
import viewController

timeStart = time.time()

timeController = timeController.TimeController( 1 )
scoreController = scoreController.ScoreController( )
gridController = gridController.GridController( scoreController )
tileController = tileController.TileController( gridController )

grapher = grapher.Grapher( scoreController )

ai = ai.AI( gridController, scoreController, grapher, {}, 20)

viewController = viewController.ViewController( gridController, timeController, scoreController, ai, grapher )

index = 0

# =====================================================================
cTile = tileController.getTile( index )
index += 1
nTile = tileController.getTile( index )
# =====================================================================


# cTile = tileController.getRandomTile( )
# nTile = tileController.getRandomTile( )
viewController.setTile( cTile, nTile )

"""
while not viewController.abort:
    if timeController.timeEvent( ):
        if viewController.aiState:
            #move, rotate, rating =  ai.makeMove( cTile )
            ai.train(cTile)
        if not cTile.incY( ):
            cTile.apply( )

            if not gridController.checkForGameOver( ):
                scoreController.tileReleased( )
                cTile = nTile
                index += 1
                nTile = tileController.getTile( index )
                viewController.setTile( cTile, nTile )
            else:
                index = 0
                cTile = tileController.getTile( index )
                index += 1
                nTile = tileController.getTile( index )
                viewController.setTile( cTile, nTile )
    viewController.updateEverything( )
"""

for j in range(5):
    times = 0
    index = 0
    ai.totalReward = 0
    for i in range(10000):
        if timeController.timeEvent( ):
            if viewController.aiState:
                #move, rotate, rating =  ai.makeMove( cTile )
                ai.train(cTile)
            if not cTile.incY( ):
                cTile.apply( )

                if not gridController.checkForGameOver( ):
                    scoreController.tileReleased( )
                    cTile = nTile
                    index += 1
                    nTile = tileController.getTile( index )
                    viewController.setTile( cTile, nTile )
                else:
                    times += 1
                    cTile = tileController.getTile( index )
                    index += 1
                    nTile = tileController.getTile( index )
                    viewController.setTile( cTile, nTile )
        viewController.updateEverything( )
    time_cost = time.time()
    print('Evaluation : %f, gameover %d times, cost %f sec' % (ai.totalReward, times, time_cost-timeStart))

timeEnd = time.time()
print("It cost %f sec" % (timeEnd - timeStart))