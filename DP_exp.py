# DP experiment with gridworld

from gridWorld import GridWorld

grid_h = 4
grid_w = 4

goal_loc = [(0,0),(grid_h-1, grid_w-1)]
theta = 0.01 # threshold of iteration stopping criteria
num_action = 4
discount = 1. # undiscount

env = GridWorld(grid_h,grid_w,goal_loc,theta, num_action, discount)

# policy evaluation for random policy
# loop over all states/in-place update

while True:

	# done = env.v_eval()
	done = env.value_itr()
	if done == True:
		break