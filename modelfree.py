import random
import throw
import darts
import math
 
# The default player aims for the maximum score, unless the
# current score is less than the number of wedges, in which
# case it aims for the exact score it needs. 
#  
# You may use the following functions as a basis for 
# implementing the Q learning algorithm or define your own 
# functions.

def start_game():

  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES)) 

def get_target(score):

  if score <= throw.NUM_WEDGES: return throw.location(throw.SECOND_PATCH, score)
  
  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES))


# Exploration/exploitation strategy one.
# This one is random purely with some probability
# decreasing epsilon greedy by passing in numiterations
def ex_strategy_one(numgames, currgame, randAction, maxAction):
  randomNum = random.random()
  change = 0.8 * numgames
  if currgame < change: # fill out the Q table by exploring often
    epsilon = 1
    if random.uniform(0,1) < epsilon:
      return randAction
    else: 
      return maxAction
  else:
    epsilon = 0.5 * change / float(currgame)
    if random.uniform(0,1) < epsilon:
      return randAction
    else: 
      return maxAction


# Exploration/exploitation strategy two.
# BOLTZMANN
def ex_strategy_two(numgames, gameNo, inQ, numActions, s):
  tau = float(numgames - gameNo)
  probabilities = []
  for a in range(numActions):
    Qvalue = inQ[s][a]
    probabilities.append(math.exp(Qvalue/(tau+1)))
  choice = random.uniform(0, sum(probabilities))
  probSoFar = 0.0
  for i in range(len(probabilities)):
    if probSoFar <= choice <= probSoFar + probabilities[i]:
      return i
    else:
      probSoFar += probabilities[i]

# The Q-learning algorithm:
def Q_learning(gamma, numRounds, alpha):
  states = darts.get_states()
  actions = darts.get_actions()
  Q = {}
  for s in states:
  	Q[s] = [0] * len(actions)

  totaliter = 0
  for i in range(numRounds):
    s = throw.START_SCORE
    numiterations = 0
    while s > 0:
      randAction = random.randint(0, len(actions) - 1)
      maxAction = Q[s].index(max(Q[s]))

      a = ex_strategy_one(numRounds, i, randAction, maxAction)
      #a = ex_strategy_two(numRounds, i, Q, len(actions), s)
      action = actions[a]

      s_prime = s - throw.location_to_score(action)
      if s_prime < 0:
        s_prime = s
      maxQ = 0.0
      for a_prime in range(len(actions)):
        if Q[s_prime][a_prime] > maxQ:
          maxQ = Q[s_prime][a_prime]
      Q[s][a] = Q[s][a] + alpha * (darts.R(s, actions[a]) + (gamma * maxQ) - Q[s][a])
      s = s_prime
      numiterations += 1
    totaliter += numiterations

  print "Average number of throws: " + str(float(totaliter) / numRounds)


