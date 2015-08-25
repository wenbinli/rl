# rl
some of my python scripts for reinforcement learning

## Overview
So far most scripts are for the examples from Barto and Sutton's book (2nd edition) http://webdocs.cs.ualberta.ca/~sutton/book/the-book.html

## Dependency
Python 2.X + {pygame,matplotlib} tested on Ubuntu 14.04

## List (so far)
1. gridworld.py: a GUI example (random policy) and DP demo                               
![alt text](https://github.com/wenbinli/rl/raw/master/screenshot/gridworld.png)
2. blackjack_GUITest.py: a demo for plotting the animation plot of the learned value function.
![alt text](https://github.com/wenbinli/rl/raw/master/screenshot/blackjack_gui.png)
2. blackjack_sol.py: a demo for the blackjack example, MC with Exploring Start and animation plot of the learned policy function. Somehow,the policy does not match the book's description, to be fixed.
3. gridworld_windy.py: a GUI demo for the gridworld with crosswind, Sarsa                   
![alt text](https://github.com/wenbinli/rl/raw/master/screenshot/gridworld_windy.png)
4. cliffWalk_QL/SARSA.py: GUI demos for gridworld with cliff, Q-Learning and Sarsa
![alt text](https://github.com/wenbinli/rl/raw/master/screenshot/cliff_walking.png)

## Note
Jeremy Stober provides more general codes on RL & robotics https://github.com/stober
