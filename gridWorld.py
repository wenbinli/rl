import numpy as np

class GridWorld(object):
    def __init__(self, grid_h, grid_l, start_loc, goal_loc):
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.start_loc = start_loc
        self.goal_loc = goal_loc
        self.v_est = np.zeros((grid_h, grid_l))

    def step(cur_r, cur_c, action):
        if action == 0: # left
            nxt_r = cur_r
            nxt_c = cur_c - 1
        elif action == 1: # right
            nxt_r = cur_r
            nxt_c = cur_c + 1
        elif action == 2: # up
            nxt_r = cur_r - 1
            nxt_c = cur_c
        elif action == 3: # down
            nxt_r = cur_r + 1
            nxt_c = cur_c

        # action takes the agent off the grid will leave the state unchanged
        if nxt_c < 0 or nxt_c > self.grid_w - 1:
            nxt_c = cur_c

        if nxt_r < 0 or nxt_r > self.grid_h - 1:
            nxt_r = cur_r

        # reward and terminal signal
        if (nxt_r, nxt_c) == self.goal_loc:
            reward = 0
        else:
            reward = -1

        return nxt_r, nxt_c, reward