# ai.py


import population
import numpy as np
from random import choice


class AI( object ):

    def __init__( self, grid, score, grapher, exp, height):
        self.height = height
        self.grid = grid
        self.score = score
        self.population = population.Population( )
        self.currentGeneration = 0
        self.currentGenome = 0
        self.grapher = grapher
        self.backupGrid = np.zeros( [ 10, 20 ], dtype=np.uint8 )
        self.backupTile = [ 0, 0, 0 ]
        # ===================================================================== 
        self.state = np.zeros( [ self.height, 10 ], dtype=np.uint8 )
        if exp != {}:
            self.exp = exp
        else:
            self.exp = {}    
        self.storeExp = {}
        self.count = 0
        self.gamma = 0.8
        self.alpha = 0.2
        self.totalReward = 0
        # =====================================================================

    """
    def update(self, tile, bestMove, bestRotate , gameover):
        self.grid.realAction = True
        self.grid.grid = np.copy( self.backupGrid )

        if gameover:
            self.population.generations[ self.currentGeneration ].genomes[ self.currentGenome ].score = self.score.getScore( )
            if self.currentGenome == 39:
                self.grapher.appendDataSet( [ x.score for x in self.population.generations[ self.currentGeneration ].genomes ] )
                self.currentGenome = 0
                self.population.nextGen( )
                self.currentGeneration += 1
            else:
                self.currentGenome += 1

        for i in range( 0, bestRotate ):
            tile.rotCW( )
        if bestMove<0:
            for i in range( 0, -bestMove ):
                tile.decX( )
        if bestMove>0:
            for i in range( 0, bestMove ):
                tile.incX( )
        tile.drop( )


    def makeMove( self, tile ):
        self.backupGrid = np.copy( self.grid.grid )
        self.grid.realAction = False
        self.backupTile = [ tile.psX, tile.psY, tile.rot ]

        # =====================================================================
        count = 0
        test = [1,1,1,1,1,1,1,1,1,1]
        for i in self.backupGrid.transpose():
            if count > 15:
                break
            elif i.T.dot(test) == 0:
                count += 1
            else:
                break

        # self.state = np.copy( self.grid.grid.transpose()[count:count+self.height] )
        # self.state[self.state > 0] = 1
       
        self.state = self.calculateState()
        curStateWithTile = self.state + [tile.identifier]
        # =====================================================================
        initH = self.grid.lastMaxHeight
        bestRating = -10000000000000
        bestMove = 0
        bestRotate = 0

        for move in range( -5, 6 ):
            for rotate in range( 0, 3 ):
                for i in range( 0, rotate ):
                    tile.rotCW( )
                if move<0:
                    for i in range( 0, -move ):
                        tile.decX( )
                if move>0:
                    for i in range( 0, move ):
                        tile.incX( )

                tile.drop( )
                tile.apply( )
                self.grid.removeCompleteRows( )
                newH = self.grid.lastMaxHeight

                # if self.rateMove( )[ 0 ] > bestRating:
                #     bestMove = move
                #     bestRotate = rotate
                #     bestRating, gameover = self.rateMove( )

                # =====================================================================
                count = 0
                for i in self.grid.grid.transpose():
                    if count > 15:
                        break
                    elif i.T.dot(test) == 0:
                        count += 1
                    else:
                        break
                alpha = 0.2
                gamma = 0.9
                reward, gameover = self.getReward(initH, newH)
                key = tuple(self.state+[tile.identifier, move, rotate])
                
                
                nextState = self.calculateState()
                nextStateWithTile = nextState + [tile.identifier]
                
                if key not in self.exp:
                    Q = alpha * reward
                    #self.exp[key] = (reward, nextState, Q)
                    print("new %f, %f, %f" % (Q, move, rotate))
                elif key in self.exp:
                    Q = self.exp[key][2]
                    Q += alpha * (reward + gamma * self.getMaxQ(nextStateWithTile)[0] - Q)
                    #self.exp[key] = (reward, nextState, Q)
                    print("old %f, %f, %f" % (Q, move, rotate))

                print(self.state)
                print(nextState)
                print(reward)
                print(Q)
                input()
                # print(move, rotate, Q)
                # input()
                # print(Q)
                # self.state = np.copy( self.grid.grid.transpose()[count:count+4] )
                # print("%f, %f \n" % (move, rotate))
                # print(self.state)
                # input()
                # =====================================================================

                tile.psX, tile.psY, tile.rot = self.backupTile
                self.grid.grid = np.copy( self.backupGrid )
        # =====================================================================
        # print(self.state.flatten().tolist())
        # Q = self.getMaxQ(self.state.flatten().tolist(), alpha, reward)[0]
        # print(Q)
        # bestAction = self.getMaxQ(self.state.flatten().tolist(), alpha, reward)[1]
        Q, bestAction = self.getMaxQ(curStateWithTile)
        bestMove, bestRotate = bestAction[0], bestAction[1]
        key = curStateWithTile + [bestMove, bestRotate]
        self.exp[key] = ()
        # print(bestAction)
        # input()
        # print(self.getMaxQ(self.state.flatten().tolist()))
        # input()
        
        # print(bestAction)
        # input()
        self.update(tile, bestMove, bestRotate, gameover)
        # =====================================================================

        return bestMove, bestRotate, bestRating

    def rateMove( self ):
        gameover = False
        cGenome = self.population.generations[ self.currentGeneration ].genomes[ self.currentGenome ]
        rating = 0
        rating += self.grid.lastRowsCleared * cGenome.weightRowsCleared
        rating += self.grid.lastMaxHeight * cGenome.weightMaxHeight
        rating += self.grid.lastSumHeight * cGenome.weightSumHeight
        rating += self.grid.lastRelativeHeight * cGenome.weightRelativeHeight
        rating += self.grid.lastAmountHoles * cGenome.weightAmountHoles
        rating += self.grid.lastRoughness * cGenome.weightRoughness
        if self.grid.checkForGameOver( ):
            rating -= 500
            gameover = True
        return rating, gameover
    """
    # =====================================================================

    def train(self, tile):
        if self.count > 100:
            self.count = 0
            self.exp = self.storeExp
        bestMove, bestRotate = self.chooseBestAction(tile)
        self.update(tile, bestMove, bestRotate)
        self.count += 1

    def update(self, tile, bestMove, bestRotate):
        self.grid.realAction = True
        self.grid.grid = np.copy( self.backupGrid )
        initH = self.grid.lastMaxHeight
        value1 = self.fitness()
        self.state = self.calculateState()
        curStateWithTile = tuple(self.state + [tile.identifier])
        # curStateKey = tuple(curStateWithTile + [bestMove, bestRotate])

        for i in range( 0, bestRotate ):
            tile.rotCW( )
        if bestMove<0:
            for i in range( 0, -bestMove ):
                tile.decX( )
        if bestMove>0:
            for i in range( 0, bestMove ):
                tile.incX( )
        tile.drop( )
        tile.apply( )
        self.grid.removeCompleteRows( )

        newH = self.grid.lastMaxHeight
        value2 = self.fitness()
        nextState = self.calculateState()
        nextStateWithTile = tuple(nextState + [tile.identifier])
        # nextStateKey = tuple(nextStateWithTile + [bestMove, bestRotate])
        # print(curStateKey)
        # print(nextStateKey)
        # input()
        reward = self.getReward(value1, value2)
        self.totalReward += value2
        ####UPDATE Q!!!!
        if curStateWithTile not in self.exp:
            self.exp[curStateWithTile] = 0
        
        self.storeExp[curStateWithTile] = (1 - self.alpha) * self.exp[curStateWithTile] + self.alpha * (reward + self.gamma * self.exp[nextStateWithTile])
        # print(self.grid.grid.transpose())
        # print(curStateWithTile)
        # # print(self.exp[curStateKey])
        # input()
        self.grid.grid = np.copy( self.backupGrid )
        tile.drop()

    
    def chooseBestAction(self, tile):
        self.backupGrid = np.copy( self.grid.grid )
        self.grid.realAction = False
        self.backupTile = [ tile.psX, tile.psY, tile.rot ]
        self.state = self.calculateState()

        old = False
        initH = self.grid.lastMaxHeight
        value1 = self.fitness()
        maxQ = float('-inf')
        bestAction = []
        for move in range( -5, 6 ):
            for rotate in range( 0, 3 ):
                for i in range( 0, rotate ):
                    tile.rotCW( )
                if move<0:
                    for i in range( 0, -move ):
                        tile.decX( )
                if move>0:
                    for i in range( 0, move ):
                        tile.incX( )

                tile.drop( )
                tile.apply( )
                self.grid.removeCompleteRows( )

                newH = self.grid.lastMaxHeight
                value2 = self.fitness()
                reward = self.getReward(value1, value2)

                nextState = self.calculateState()
                nextStateWithTile = tuple(nextState + [tile.identifier])
                # nextStateKey = tuple(nextStateWithTile + [move, rotate])
                
                if nextStateWithTile not in self.exp:
                    old = False
                    self.exp[nextStateWithTile] = 0
                elif self.exp[nextStateWithTile] != 0:                    
                    old = True
                    
                Q = self.exp[nextStateWithTile]
                if (reward + self.gamma * Q) > maxQ:
                    newQ = self.exp[nextStateWithTile]
                    maxQ = reward + self.gamma * Q
                    bestAction = [[move, rotate]]
                elif (reward + self.gamma * Q) == maxQ:
                    bestAction.append([move, rotate])
                # print('next H: %d, cur H: %d' % (newH, initH))
                # print(self.state)
                # print(nextState)
                # print(Q)
                # print(move, rotate)

                tile.psX, tile.psY, tile.rot = self.backupTile
                self.grid.grid = np.copy( self.backupGrid )
        
            # input()
        # print('bestAction: (%d, %d)' % (bestMove, bestRotate))
        # print('Max Q:', maxQ)
        #input()
        if len(bestAction) > 1:
            oneBestAction = choice(bestAction)

        else:
            oneBestAction = bestAction[0]

        if old:
            print("old %f, %f, %f, %f" % (maxQ, newQ, oneBestAction[0], oneBestAction[1]))
        return oneBestAction[0], oneBestAction[1]

    def getReward(self, value1, value2):
        #print('next H: %d, cur H: %d' % (h2, h1))

        # reward = 0
        # reward += self.grid.lastRowsCleared * 4.760666
        # reward += self.grid.lastMaxHeight * -1.510066
        # reward += self.grid.lastSumHeight * 0.0
        # reward += self.grid.lastRelativeHeight * -1.0
        # reward += self.grid.lastAmountHoles * -0.35663
        # reward += self.grid.lastAmountHoles * -5.35663
        # reward += self.grid.lastRoughness * -0.184483
        # # reward = (-100) * (h2-h1)
        # return reward

        #reward = (-100) * (h2-h1)
        """
        reward = self.grid.lastRowsCleared * 4.7
        reward += self.grid.lastMaxHeight * -1.51
        #reward += self.grid.lastSumHeight * 0.0
        #reward += self.grid.lastRelativeHeight * -1.0
        reward += self.grid.lastAmountHoles * -5.35
        reward += self.grid.lastRoughness * -0.184483
        """
        return value2-value1

    def fitness(self):
        value = self.grid.lastRowsCleared * 0.76
        value += self.grid.lastSumHeight / 10 * -0.51
        value += self.grid.lastAmountHoles * -0.36
        value += self.grid.lastRoughness * -0.18
        return value

    def calculateState(self):
        count = 0
        test = [1,1,1,1,1,1,1,1,1,1]
        for i in self.backupGrid.transpose():
            if count > 15:
                break
            elif i.T.dot(test) == 0:
                count += 1
            else:
                break

        state = []
        for item in self.grid.grid:
            # print(item)
            # input()
            state_count = 0
            while state_count < 20 and item[state_count] == 0:
                state_count += 1
                pass
            state += [20 - state_count]

        state_diff=[]
        for i in range(len(state)-1):
            state_diff.append(state[i+1] - state[i])

        return state_diff

    """
    def getMaxQ( self , nextState, reward):
        maxQ = -1000000
        best_set = []
        bestAction=()
        found = False
        key_set = []
        for k in self.exp:
            # print(k[:-2])
            # print("\n")
            # print(nextState)
            # input()
            equal = 0
            for a, b in zip(k[:-2], nextState):
                if a != b:
                    equal = 0
                    break
                equal = 1
            if equal:
                found = True
                if self.exp[k][2] > maxQ:
                    maxQ = self.exp[k][2]
                    best_set = [k[-2:]]
                    key_set.append(k)
                    # bestAction = k[-2:]
                    # print("> %f" % maxQ)
                elif self.exp[k][2] == maxQ:
                    best_set += [k[-2:]]
                    key_set.append(k)
                    # print("== %f" % maxQ)
        if not found:
            maxQ = 0
            bestAction = (np.random.random_integers( -5, 5 ), np.random.random_integers( 0, 2 ))
            key_set.append()
            # R = self.getReward
                # self.exp[tuple(nextState +[bestAction[0], bestAction[1]])] = (reward, )
                    # print("< %f" % maxQ)
        # print(self.exp[k][2], maxQ)
        # input()
        if len(best_set) > 1:
            bestAction = choice(best_set)
            bestKey = choice(key_set)
        elif len(best_set) == 1:
            bestAction = best_set[0]
            bestKey = key_set[0]
        else:
            bestKey = ()

        return bestKey
    
    def getReward( self, h1, h2):
        gameover = False
        if self.grid.checkForGameOver( ):
            gameover = True
        reward = 0
        print('next H: %d, cur H: %d' % (h2, h1))
        reward += (-100) * (h2-h1)
        # reward += self.grid.lastRowsCleared * 4.760666
        # reward += self.grid.lastMaxHeight * -1.510066
        # reward += self.grid.lastSumHeight * 0.0
        # reward += self.grid.lastRelativeHeight * -1.0
        # # reward += self.grid.lastAmountHoles * -0.35663
        # reward += self.grid.lastAmountHoles * -5.35663
        # reward += self.grid.lastRoughness * -0.184483
        #reward += self.grid.lastRowsCleared * 500
        # reward += self.grid.lastMaxHeight * -5
        # reward += self.grid.lastSumHeight * -1
        # reward += self.grid.lastRelativeHeight * -1
        # reward += self.grid.lastAmountHoles * -1
        # reward += self.grid.lastRoughness * -1
        #reward += gameover * (-500)
        return reward, gameover
    """
    # =====================================================================
