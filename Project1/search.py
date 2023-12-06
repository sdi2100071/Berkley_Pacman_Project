# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in: 

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    
    print("Start's successors:", problem.getSuccessors(problem.getStartState())) """
    
    
    "*** YOUR CODE HERE ***"
    
    from util import Stack 
     
    #stack : ( (x,y) , path[] )
    my_stack = Stack()
     
    #visited : (x , y)
    visited = []
    
    #[west/north/.../...]
    path = []
    
    if problem.isGoalState(problem.getStartState()) :
        return[]
    
    #start state 
    start_node = problem.getStartState()
    my_stack.push( (start_node , []) )   
    
    while  not my_stack.isEmpty() :
            
        popped_elem = my_stack.pop() 
        #append at the list the visited elem --> (x,y)
        visited.append(popped_elem[0])
        
        #if its not the start node 
        if not (popped_elem[1] == [] ) :
            path = popped_elem[1]
       
        if problem.isGoalState(popped_elem[0]):
            return path     
                    
        successors = problem.getSuccessors(popped_elem[0])   
        for state in successors :          
            if state[0] not in visited  :
                new_path = path + [state[1]]
                my_stack.push( (state[0] , new_path) )
        
    return path
                

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    from util import Queue
    
    # my_queue : ( (x,y)  , path )
    my_queue = Queue()
    
    #list of visited nodes : [(x,y)]
    visited = []
    
    #path : [west / ...]
    path = []
    
    start_node = problem.getStartState()    
    if problem.isGoalState(start_node) :
        return[]
    
    my_queue.push( (start_node , []) )   
    while not my_queue.isEmpty():
        
        popped_elem = my_queue.pop()
        visited.append( popped_elem[0] )
        
        #if its not the start node 
        if not (popped_elem[1] == [] ) :
            path = popped_elem[1]
        
        if problem.isGoalState( popped_elem[0] ):
            return path
        
        #succesors of the visited node 
        successors = problem.getSuccessors( popped_elem[0] )
        
        #creating a list of the first element of the tupples in the queue [ (x , y) ]
        list_queue = []
        for i in  my_queue.list :
            list_queue.append(i[0]) 
        
        #if successor not visited AND not already in queue --> push   
        for state in successors : 
            if state[0] not in visited and state[0] not in list_queue:
                new_path = path + [state[1]]
                my_queue.push((state[0] , new_path ))
               
    return path

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue

    #pqueue : [ (x,y) , path ]
    pqueue = PriorityQueue()
    
    #[( x , y )]
    visited = []
    
    #path: [west / ...]
    path = []
       
    start_node = problem.getStartState()
    if problem.isGoalState( start_node ): 
        return []
    
    pqueue.push((start_node , []) , problem.getCostOfActions(path))
    
    while not pqueue.isEmpty() :
        
        popped_elem = pqueue.pop()
        
        #if not the first element
        if (popped_elem[1] != []):
            path = popped_elem[1]
            
        if problem.isGoalState( popped_elem[0] ):
            return path
          
        if popped_elem[0] not in visited:
            successors = problem.getSuccessors(popped_elem[0]) 
            visited.append(popped_elem[0])
            for state in successors :          
                new_path = path + [ state[1] ] 
                pqueue.push((state[0] , new_path), problem.getCostOfActions(new_path))
                                            
    return path
    
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue
    
    #pqueue : [ (x,y) , path ]
    pqueue = PriorityQueue()
    
    #[( x , y )]
    visited = []
    
    #path: [west / ...]
    path = []
       
    start_node = problem.getStartState()
    if problem.isGoalState(start_node): 
        return []
     
    cost = problem.getCostOfActions(path)
    pqueue.push((start_node , path) , cost)
    
    while not pqueue.isEmpty() :
        
        popped_elem = pqueue.pop()
        path = popped_elem[1]
            
        if problem.isGoalState(popped_elem[0]):
            return path
              
        if popped_elem[0] not in visited:
                       
            successors = problem.getSuccessors(popped_elem[0]) 
            visited.append(popped_elem[0]) 
               
            for state in successors :
                heur_value = heuristic(state[0] , problem)
                new_path = path + [state[1]] 
                cost = problem.getCostOfActions( new_path )
                priority = cost +  heur_value
                pqueue.push( (state[0] , new_path), priority )
        
    return path
    

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
