"""
Gridworld for reinforcement with GUI
Author: Wenbin Li

procedural programming atm, need to be formated into OOP
main reference: https://github.com/stober/gridworld/blob/master/src/gridworldgui.py
"""

import pygame
from pygame.locals import *

import numpy as np

grid_size = 100
n_row = n_col = 3  # grid size by row/column


# define state
state = np.zeros((n_row,n_col)) # initialization

# configure GUI
pygame.init()
pygame.display.set_mode((n_row * grid_size,n_col * grid_size)) # display surface
pygame.display.set_caption('Gridworld')

screen = pygame.display.get_surface() # get a reference to the currently set display surface

surface = pygame.Surface(screen.get_size())
bg = pygame.Surface(screen.get_size())

#screen.blit(surface,(0,0))

#screen = pygame.display.set_mode((n_row * grid_size,n_col * grid_size))
#screen.fill((0,0,0))
#pygame.display.set_caption('Gridworld')

"""
draw background
Update: add surface
"""
def draw_bg(surface,n_row,n_col,grid_size,start_state,goal_state,obstacle):
    for i in range(n_row):
        for j in range(n_col):
            y = i * grid_size
            x = j * grid_size
            coords = pygame.Rect(y,x,grid_size,grid_size)
            pygame.draw.rect(surface,(255,255,255),coords,1)
    
    # draw start state
    pygame.draw.circle(surface,(192,192,192),
                       (start_state[0] * grid_size + grid_size/2,
                        start_state[1] * grid_size + grid_size/2),
                        grid_size/4)
            
    # draw goal state
    pygame.draw.circle(surface,(102,204,0),
                       (goal_state[0] * grid_size + grid_size/2,
                        goal_state[1] * grid_size + grid_size/2),
                        grid_size/3)
                        
    # draw obastacles
    num_obs = len(obstacle)
    for i in range(num_obs):
        obs = obstacle[i]
        pygame.draw.circle(surface,(204,0,0),
                            (obs[0] * grid_size + grid_size/2,
                             obs[1] * grid_size + grid_size/2),
                             grid_size/3)
    #surface.fill((0,0,0))

"""
define iterative policy evaluation for equiprobable random policy

"""
def iterPolEvaRand(n_row,n_col,goal_pos,obs,n_iter):
    # initialize value function
    v = np.zeros((n_row,n_col))
    v_ = np.zeros((n_row,n_col)) # cache to store intermediate results
    
    def indVal(i,j,di,dj,n_row,n_col,obs): 
        # convert index to valid value
        #    1) (i,j) in corner/edge
        #    2) (i,j) near obstacles
        #    3) (i,j) is any normal state besides 1),2), what about goal?
        
        if  i + di < 0 or i + di == n_row or j + dj < 0 or j + dj == n_col or (i + di, j + dj) in obs:
            i = i
            j = j
        else:
            i = i + di
            j = j + dj
        
        return i,j

    for k in range(n_iter):
        for i in range(n_row):
            for j in range(n_col):
                # update v_, reward is -1 until reach the goal
                # if not((i,j) in obs):
                # import pdb;pdb.set_trace()
                v_[i,j] = 0.25 * (-1 + v[indVal(i,j,-1,0,n_row,n_col,obs)]) +  \
                          0.25 * (-1 + v[indVal(i,j,1,0,n_row,n_col,obs)]) + \
                          0.25 * (-1 + v[indVal(i,j,0,-1,n_row,n_col,obs)]) + \
                          0.25 * (-1 + v[indVal(i,j,0,1,n_row,n_col,obs)])
                          
                # for value iteration, change sum operator to get maximum          
                """
                v_[i,j] = max(0.25 * (-1 + v[indVal(i,j,-1,0,n_row,n_col,obs)]),  \
                              0.25 * (-1 + v[indVal(i,j,1,0,n_row,n_col,obs)]), \
                              0.25 * (-1 + v[indVal(i,j,0,-1,n_row,n_col,obs)]), \
                              0.25 * (-1 + v[indVal(i,j,0,1,n_row,n_col,obs)]))
                """                    
        v_[goal_pos[0],goal_pos[1]] = 0 # reset the value of goal state
        
        print "current value function:"
        
        print v_
        v = v_
        
    return v # return policy

"""
define agent with random move in the grid world

"""            
def random_move(n_row,n_col,grid_size,cur_pos,goal_pos,obs):
    x,y = cur_pos # get current pos
    
    # define update rule/policy
    # define goal state, if reach the state, then stop
    if cur_pos == goal_pos:
        next_pos = cur_pos
    else:
       # define random movement agent
       # Note, the agent has to stay in the gridworld; also avoid obstacle!!
       next_mov = np.random.randint(0,4) # only allow up/down/left/right
       
       # tmp solution, 0 for left , 1 for up, 2 for right, 3 for down
       if next_mov == 0:
           if x-1 < 0:
               x = x
           elif (x-1,y) in obs:
               print "cannot cross the obstacle"    
           else:
               x = x - 1
               print "move left"
       elif next_mov == 1:
           if y-1 < 0:
               y = y
           elif (x,y-1) in obs:
               print "cannot cross the obstacle"
           else:
               y = y - 1
               print "move up"
       elif next_mov == 2:
           if x+1 > n_col - 1:
               x = x
           elif (x+1,y) in obs:
               print "cannot cross the obstacle"
           else:
               x = x + 1
               print "move right"
       else:
           if y+1 > n_row - 1:
               y = y
           elif (x,y+1) in obs:
               print "cannot cross the obstacle"
           else:
               y = y + 1
               print "move down"
       
       next_pos = (x,y)
       
    return next_pos
    
    
cur_state = start_state = (0,0)

obstacle = [(1,1)] # make a list
goal_state = (n_row-1,n_col-1) # marked with cycle

n_iter = 2

iterPolEvaRand(n_row,n_col,goal_state,obstacle,n_iter)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # draw grid as bakground
    draw_bg(bg,n_row,n_col,grid_size,start_state,goal_state,obstacle)
    screen.blit(bg,(0,0))
    
    # draw the state of an agent
    surface.fill((0,0,0))
    
    cur_state = random_move(n_row,n_col,grid_size,cur_state,goal_state,obstacle) # random (policy) agent atm
    
    if cur_state != goal_state:
         pygame.draw.circle(surface,(255,255,255),
                         (cur_state[0] * grid_size + grid_size/2,
                          cur_state[1] * grid_size + grid_size/2),
                          grid_size/3)
    else:
        print "Goal reached"
        
                              
    bg.blit(surface,(0,0)) # draw a source into a surface: surface.blit(source, dest,...)
    
    pygame.display.flip()
    
    pygame.time.delay(1000)    
   
    
