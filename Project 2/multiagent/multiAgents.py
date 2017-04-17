# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import sys
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        v = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == v]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
        # Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		# print successorGameState
		# print "successorGameState"
		newPos = successorGameState.getPacmanPosition()
		# print "newPos"
		# print newPos
		newFood = successorGameState.getFood()
		# print "newFood"
		# print newFood.asList()
		newGhostStates = successorGameState.getGhostStates()
		# print "newGhostStates"
		# for i in newGhostStates:
			# print i
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		# print "newScaredTimes"
		# print newScaredTimes
		newGhostPositions = successorGameState.getGhostPositions()
		foodList = newFood.asList()
		minFood = 9999
		minGhost = 9999
		for i in foodList:
			if util.manhattanDistance(newPos,i) < minFood:
				minFood = util.manhattanDistance(newPos,i)
		for i in newGhostPositions:
			if util.manhattanDistance(newPos,i) < minGhost:
				minGhost = util.manhattanDistance(newPos,i)	
		# print minFood
		# print minGhost
		if currentGameState.getPacmanPosition() == newPos:
			return -9999
		inversefood = 0
		if minFood is not 0:
				inversefood = 1/minFood
		# if minFood 
		if(minGhost>1):				
			# return (2*minGhost/(minGhost+minFood)) * ((inversefood)**2)	+ successorGameState.getScore()
			return ((minGhost+inversefood)/(minGhost-inversefood))**2 + successorGameState.getScore()
		else:
			return -9999
		# else:
			# return 9999
		

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

			gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		"*** YOUR CODE HERE ***"
		
		def maxValue(gameState,depth):
			if self.depth == depth:
				return(self.evaluationFunction(gameState),None)	
			actions = gameState.getLegalActions(0)
			betterAction = None
			v = -sys.maxint
			if len(actions) == 0:
				return(self.evaluationFunction(gameState),None)
			for a in actions:
				newState = gameState.generateSuccessor(0,a)
				betterscore = minValue(newState,1,depth)[0]
				if betterscore > v:
					v = betterscore
					betterAction = a
					# print "betterAction"
					# print betterAction
			return (v,betterAction)
			
		def minValue(gameState,agentIndex,depth):	
			actions = gameState.getLegalActions(agentIndex)
			betterAction = None
			v = sys.maxint
			if len(actions) == 0:
				return(self.evaluationFunction(gameState),None)
			for a in actions:
				# print a
				newState = gameState.generateSuccessor(agentIndex,a)
				if (agentIndex + 1 == gameState.getNumAgents()):
					betterscore = maxValue(newState, depth + 1)[0]
				else:
					betterscore = minValue(newState,agentIndex+1,depth)[0]
					
				if betterscore < v:
					v = betterscore
					betterAction = a
			return (v,betterAction)	
		return maxValue(gameState,0)[1]
		util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		def maxValue(gameState, depth, alpha, beta):
			if depth == self.depth:
				return (self.evaluationFunction(gameState), None)

			actions = gameState.getLegalActions(0)
			v = -sys.maxint
			betterAction = None

			if len(actions) == 0:
				return (self.evaluationFunction(gameState), None)

			for a in actions:
				newState = gameState.generateSuccessor(0, a)
				betterScore = minValue(newState, 1, depth, alpha, beta)[0]
				if (betterScore > v):
					v = betterScore
					betterAction = a
				if (v > beta):
					return (v, betterAction)	
				if (betterScore > alpha):
					alpha = betterScore
			return (v, betterAction)



		def minValue(gameState, ID, depth, alpha, beta):
			actions = gameState.getLegalActions(ID)
			v = sys.maxint
			bestAction = None

			if len(actions) == 0:
				return (self.evaluationFunction(gameState), None)

			for a in actions:
				newState = gameState.generateSuccessor(ID, a)
				if (ID == gameState.getNumAgents() - 1):
					betterScore = maxValue(newState, depth + 1, alpha, beta)[0]
				else:
					betterScore = minValue(newState, ID + 1, depth, alpha, beta)[0]

				if (betterScore < v):
					v = betterScore
					bestAction = a
				if (betterScore < alpha):
					return (v, bestAction)	
				if (betterScore < beta):
					beta = betterScore
			return (v, bestAction)

		return maxValue(gameState, 0, -sys.maxint, sys.maxint)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
		"""
		Returns the expectimax action using self.depth and self.evaluationFunction

		All ghosts should be modeled as choosing uniformly at random from their
		legal moves.
		"""
		"*** YOUR CODE HERE ***"
		def maxValue(gameState, depth):
			if depth == self.depth:
				return (self.evaluationFunction(gameState), None)

			actions = gameState.getLegalActions(0)
			v = - sys.maxint - 1
			bestAction = None

			if len(actions) == 0:
				return (self.evaluationFunction(gameState), None)

			for a in actions:
				newState = gameState.generateSuccessor(0, a)
				betterScore = randomValue(newState, 1, depth)[0]
				if (betterScore > v):
					v = betterScore
					bestAction = a
			return (v, bestAction)



		def randomValue(gameState, ID, depth):
			actions = gameState.getLegalActions(ID)
			totalScore = 0
			bestAction = None

			if len(actions) == 0:
				return (self.evaluationFunction(gameState), None)

			for a in actions:
				newState = gameState.generateSuccessor(ID, a)
				if (ID == gameState.getNumAgents() - 1):
					betterScore = maxValue(newState, depth + 1)[0]
				else:
					betterScore = randomValue(newState, ID + 1, depth)[0]
				totalScore += betterScore/len(actions)
			return (totalScore, bestAction)

		return maxValue(gameState, 0)[1]
		util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 5).

	DESCRIPTION: <write something here so we know what you did>
	Here, I am taking into account features such as distance to closest food, amount of food left, 
	amount of food capsules, scared ghosts and ghosts which are not scared.
	"""
	currPos = currentGameState.getPacmanPosition()
	
	newFood = currentGameState.getFood()
	newGhostStates = currentGameState.getGhostStates()
	newGhostPositions = currentGameState.getGhostPositions()
	foodList = newFood.asList()
	minFoodDistance = 9999
	for i in foodList:
			if util.manhattanDistance(currPos,i) < minFoodDistance:
				minFoodDistance = util.manhattanDistance(currPos,i)
	notScaredGhost=9999
	scaredGhost=9999
	for ghost in newGhostStates:
		if ghost.scaredTimer:
			m = util.manhattanDistance(currPos,ghost.getPosition())
			if m<scaredGhost:
					scaredGhost = m
			m = scaredGhost	
			# print m
		else:
			m = util.manhattanDistance(currPos,ghost.getPosition())
			if m<notScaredGhost:
					notScaredGhost = m
			m = notScaredGhost
			# print m
	powerupsleft = len(currentGameState.getCapsules())
	foodleft = len(foodList)	
	# if newScaredTimes:
	
	#Evaluation function
	return currentGameState.getScore()+(1/minFoodDistance)*10 - 1.5 * powerupsleft - 1.5 * foodleft - 1/(scaredGhost*2 - notScaredGhost*2)
	if currentGameState.isWin():
		return 9999
		
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

