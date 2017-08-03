import numpy as np

class GridWorld(object):
    def __init__(self, grid_h, grid_w, goal_loc, theta, num_action, discount):
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.goal_loc = goal_loc
        self.theta = theta
        self.num_action = num_action
        self.discount = discount

        self.v_est = np.zeros((grid_h, grid_w))

    def step(self, cur_r, cur_c, action):
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

        return nxt_r, nxt_c

    def v_eval(self):
        done = False
        delta = 0

        for i in range(self.grid_h):
            for j in range(self.grid_w):

                if (i,j) not in self.goal_loc:

                    v = self.v_est[i,j]

                    V = 0
                    for k in range(self.num_action):

                        nxt_r, nxt_c = self.step(i,j,k)
                        V += 1./self.num_action * (self.discount * self.v_est[nxt_r, nxt_c] - 1)

                    self.v_est[i,j] = V
                    delta = max(delta, abs(v - V))
                    print 'current delta: ' + str(delta)
                    
                    if delta < self.theta:
                        done = True
                        print self.v_est
                        return done
        print self.v_est
        
        return done