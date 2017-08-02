# DP experiment with gridworld

from gridworld import GridWorld

start_loc = (0,0)
goal_loc = (9,9)
grid_h = 10
grid_l = 10

env = GridWorld(10,10,start_loc,goal_loc)

# policy evaluation for random policy
