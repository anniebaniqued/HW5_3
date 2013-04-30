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
"""def ex_strategy_one(randAction, maxAction):
  randomNum = throw.ranf()
  if randomNum < 0.1:
    return randAction
  else: 
    return maxAction"""

def ex_strategy_one():
  randomNum = throw.ranf()
  if randomNum < 0.05:
    return True
  return False

# Exploration/exploitation strategy two.
# BOLTZMANN
def ex_strategy_two(iterations, inQ, numActions, s):
  tau = 100.0*(1.0/5.0)**(iterations)
  probabilities = []
  for a in range(numActions):
    Qvalue = inQ[s][a]
    print "Qvalue: " + str(Qvalue)
    print "tau: " + str(tau)
    probabilities.append(math.exp(Qvalue/tau))
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

      #E-greedy
      """
      to_explore = ex_strategy_one()
      if to_explore:
        # explore
        a = random.randint(0, len(actions)-1)
        action = actions[a]
      else:
        # exploit
        a = pi_star[s]
        action = actions[a] 
        """


      #a = ex_strategy_one(randAction, maxAction)
      a = ex_strategy_two(numiterations, Q, len(actions), s)
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


