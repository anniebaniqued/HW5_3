# Components of a darts player. #

# 
 # Modify the following functions to produce a player.
 # The default player aims for the maximum score, unless the
 # current score is less than or equal to the number of wedges, in which
 # case it aims for the exact score it needs.  You can use this
 # player as a baseline for comparison.
 #

from random import *
import throw
import darts

# make pi global so computation need only occur once
PI = {}
EPSILON = .001


# actual
def start_game(gamma):

  infiniteValueIteration(gamma)
  #for ele in PI:
    #print "score: ", ele, "; ring: ", PI[ele].ring, "; wedge: ", PI[ele].wedge
  
  return PI[throw.START_SCORE]

def get_target(score):

  return PI[score]

# define transition matrix/ function
def T(a, s, s_prime):
  # takes an action a, current state s, and next state s_prime
  # returns the probability of transitioning to s_prime when taking action a in state s
  aRing = a.ring
  aWedge = a.wedge
  target = s - s_prime

  probs = [0.4, 0.2, 0.1]

  probability = 0
  for i in range (-2, 3):
    w = (throw.wedges.index(a.wedge) + i) % len(throw.wedges)
    wedge = throw.wedges[w]
    for j in range(-2, 3):
      ring = min(abs(aRing + j), 6)
      loc = throw.location(ring, wedge)
      score = throw.location_to_score(loc)
      if target == score:
        probability += probs[abs(i)] * probs[abs(j)]

  return probability

"""
  possiblePoints = []


  return probability
      if i + aRing < 0:
        # two cases, in the center, and outside

        possiblePoints.append(throw.location_to_score(throw.location((aRing+i, (aWedge+j) % 5)))

      else:
        possiblePoints.append(throw.location_to_score(throw.location((aRing+i) % 5, (aWedge+j) % 5)))

  try:
    targetIndex = possiblePoints.index(target)
  except ValueError:
    return 0

  probs = [0.4, 0.2, 0.1]
  

  ringIndex = targetIndex / 5 - 5
  wedgeIndex = targetIndex % 5 - 5

  return probs[abs(ringIndex)] * probs[abs(wedgeIndex)]  

  for i in range (-2, 3):
    for j in range(-2, 3):




  allLocs = []


  for i in range(-2, 3):
    for 



  wedgeDistDict = {0:0.4, 1:0.2, -1:0.2, -2:0.1, 2:0.1}
  regionDistDict = {0:0.4, 1:0.2, -1:0.2, -2:0.1, 2:0.1}

  if target == 50:
    try:
      return regionDistDict[aRing - 0]
    except KeyError:
  
  if target == 25:
    try: 
      return regionDistDict[aRing - 1]
    except KeyError:

  wedgeProb = 0.4
  for i in range(-2, 3):
    return wedgeProb*



  return 0


  possiblePoints = []

  for i in range 

  if wedge 
  dartScore = throw.location_to_score(a)
  if s - dartScore == s_prime:
    return 0.4
  elif s - 
"""

def infiniteValueIteration(gamma):
  # takes a discount factor gamma and convergence cutoff epislon
  # returns

  V = {}
  Q = {}
  V_prime = {}
  
  states = darts.get_states()
  actions = darts.get_actions()

  notConverged = True

  # intialize value of each state to 0
  for s in states:
    V[s] = 0
    Q[s] = {}

  # until convergence is reached
  while notConverged:

    # store values from previous iteration
    for s in states:
      V_prime[s] = V[s]

    # update Q, pi, and V
    for s in states:
      for a in actions:

        # given current state and action, sum product of T and V over all states
        summand = 0
        for s_prime in states:
          summand += T(a, s, s_prime)*V_prime[s_prime]

        # update Q
        Q[s][a] = darts.R(s, a) + gamma*summand

      # given current state, store the action that maximizes V in pi and the corresponding value in V
      PI[s] = actions[0]
      V[s] = Q[s][PI[s]]  
      for a in actions:
        if V[s] <= Q[s][a]:
          V[s] = Q[s][a]
          PI[s] = a

    notConverged = False
    for s in states:
      if abs(V[s] - V_prime[s]) > EPSILON:
        notConverged = True
        
  