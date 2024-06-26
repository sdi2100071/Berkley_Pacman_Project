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
import random, util, sys

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        from util import manhattanDistance
        
        ghostpos = successorGameState.getGhostPositions()       
        for pos in ghostpos:
            #if pacman's next move collisions on ghosts position and not scared return a very small num to avoid that
            if (newPos == ghostpos or manhattanDistance(pos, newPos) < 2) and not newScaredTimes: 
                return -sys.maxsize 
            #else return a smaller than the previous num but still small cause its not preferable
            elif (newPos == ghostpos or manhattanDistance(pos, newPos) < 2) and  newScaredTimes:               
                return -sys.maxsize / 2                            
            
        currentfood = currentGameState.getFood()
        foodlist = currentfood.asList()
        fooddist = []
        fooddist.append(sys.maxsize)
        #find the closest food to pacman  and return the score - min distance because we prefer the state with the state were pacman is closer
        # score - min(minfooddistance) more preferable --> return value larger
        for f in foodlist:
            fooddist.append(manhattanDistance(f, newPos))
            
        return successorGameState.getScore() - min(fooddist)
                  
            
            
            
def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
     
        "*** YOUR CODE HERE ***"
        
        #maximazer--->pacman = 0
        #minimazers-->ghosts >= 1
        
        #pacman plays first      
        pacman = 0    
        optimalAction, opteval = self.minimax(gameState, 0, pacman) #call the minimax with depth 0 
        return optimalAction
    
        
    def minimax(self, gameState, depth, agent):
        
        pacman = 0
        agentnum = gameState.getNumAgents()
        
        #if we explored all agents --> 
        if agent == agentnum: 
            depth += 1      #go deeper
            agent = pacman  #start from pacman    
        
        if gameState.isWin() or gameState.isLose() or  depth == self.depth:
            return Directions.STOP,self.evaluationFunction(gameState)
        
        if agent == pacman:   
                                                
            actions = gameState.getLegalActions(0)
            opteval = - sys.maxsize  #optimal evaluation value      
            for action in actions:   
                
                nextState = gameState.generateSuccessor(agent, action)
                #call minimazer               
                bestAction,eval = self.minimax(nextState, depth, agent + 1)                
                opteval = max(eval, opteval)    #select max evaluation value of minimazers options
                if  eval == opteval:
                    optimalAction = action  #keep actions that leed to the max evaluation val
        else:
            
            opteval = sys.maxsize 
            actions = gameState.getLegalActions(agent)                
            for action in actions:
               
                nextstate = gameState.generateSuccessor(agent, action) 
                bestaction,eval = self.minimax(nextstate, depth, agent + 1)
                opteval = min(eval, opteval)
               
                if  eval == opteval:
                    optimalAction = action
            
        return optimalAction,opteval
               
          
        
                
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pacman = 0
        optimalAction, opteval = self.alpha_beta(gameState, -float('inf'), float('inf'), 0, pacman) 
        return optimalAction
        
    def alpha_beta(self, gameState, alpha,beta,  depth, agent):
    
        pacman = 0
        agentnum = gameState.getNumAgents()
        if agent == agentnum:
            depth += 1
            agent = pacman
        
        if gameState.isWin() or gameState.isLose() or  depth == self.depth:
            return Directions.STOP,self.evaluationFunction(gameState)
        
        if agent == pacman:   
                                                
            actions = gameState.getLegalActions(0)
            opteval = - sys.maxsize                   
            for action in actions:   
                                
                nextState = gameState.generateSuccessor(agent, action)
                bestAction,eval = self.alpha_beta(nextState, alpha, beta, depth, agent + 1)
                opteval = max(eval, opteval)
                if  eval == opteval:
                    optimalAction = action                     
                alpha = max(alpha, opteval)
                
                if alpha > beta:
                    return optimalAction,opteval
        else:
            
            opteval = sys.maxsize
            actions = gameState.getLegalActions(agent)                
            for action in actions:
                
                nextstate = gameState.generateSuccessor(agent, action) 
                bestaction,eval = self.alpha_beta(nextstate,alpha, beta, depth, agent + 1)
                opteval = min(eval, opteval)
                
                if  eval == opteval:
                    optimalAction = action                   
                beta = min(beta, opteval)
               
                if alpha > beta:
                    return optimalAction,opteval
            
        return optimalAction,opteval
            

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacman = 0       
        optimalAction, opteval = self.expectimax(gameState, 0, pacman) 
        return optimalAction
    
        
    def expectimax(self, gameState, depth, agent):
        
        pacman = 0
        agentnum = gameState.getNumAgents()
        if agent == agentnum:
            depth += 1
            agent = pacman
        
        if gameState.isWin() or gameState.isLose() or  depth == self.depth:
            return Directions.STOP,self.evaluationFunction(gameState)
        
        if agent == pacman:                                        
            actions = gameState.getLegalActions(0)
            opteval = - sys.maxsize  
    
            for action in actions:                              
                
                nextState = gameState.generateSuccessor(agent, action)
                bestAction,eval = self.expectimax(nextState, depth, agent + 1)
                opteval = max(eval, opteval)
               
                if  eval == opteval:
                    optimalAction = action  
        else:
            
            opteval = 0.0
            actions = gameState.getLegalActions(agent) 
            if len(actions) != 0:  
                probability = 1.0 / len(actions)    # probability -= 1 / number of actions                
               
                for action in actions:
                    nextstate = gameState.generateSuccessor(agent, action) 
                    bestaction,eval = self.expectimax(nextstate, depth, agent + 1)
                    opteval += eval * probability
                    optimalAction = action                 
            else:                        
                opteval = 0.0
                optimalAction = Directions.STOP        
            
        return optimalAction,opteval
        

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    from util import manhattanDistance
    
    #objects that affect my evaluation value
    pos = currentGameState.getPacmanPosition()
    ghostpos = currentGameState.getGhostPositions()
    food = currentGameState.getFood()
    foodList = food.asList()
    capsules = currentGameState.getCapsules()  
    
    ghostStates = currentGameState.getGhostStates()
    eval = currentGameState.getScore()
    
    if currentGameState.isWin() :
        return float('inf')
    if currentGameState.isLose() :
        return - float('inf')
    
    #prefer state with more capsules
    eval += -1.5 * len(capsules)
    
    # scaredGhosts: list of scared ghosts
    scaredGhosts = [ghostState.scaredTimer for ghostState in ghostStates]
    # scaredGhosts: list of non scared ghosts
    notscaredGhosts = [not ghostState.scaredTimer for ghostState in ghostStates]
    
    # prefere states with less scared ghosts 
    eval += -3.5 * len(scaredGhosts) 
    eval += -3* len(notscaredGhosts)
    
    #prefer states with more food
    eval += -0.5 * len(foodList)
    
    #prefer states were pacman is closer to food
    fooddist = []
    fooddist.append(sys.maxsize)
    for f in foodList:
        fooddist.append(manhattanDistance(f, pos))
        mindist = min(fooddist)
    eval += - 0.3* mindist
    
    return eval
    
    
    
    
# Abbreviation
better = betterEvaluationFunction
