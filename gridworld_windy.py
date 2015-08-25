# solve windy gridworld with Sarsa (on-policy TD control)
# from the example in the book, introduction to reinforcement learning
# author: Wenbin Li

import pygame
from pygame.locals import *
import numpy as np


# numeric backend

grid_size = 100
n_row = 7
n_col = 10
state = np.zeros((n_row * grid_size, n_col * grid_size)) 
step_size = 0.5
epsilon = 0.1 # parameter for epislon-greedy
N_actions = 4 # number of actions {left,up,right,down}
N_episodes = 170 # number of episodes
N_steps = 8000 # number of total steps, not sure which to use n/n_step
# as suggested by the book, reach optimality by 8000 time steps
# constant rewards of -1 until the goal state is reached

# specify goal location
goal_r = 3
goal_c = 7
# specify start location
start_r = 3
start_c = 0

# define wind 
#    [:,3:5,8] str = 1
#    [:,6:7] str = 2

# initialize state-action value function
q = np.zeros((7,10,4)) # num_row by num_col by num_states
# Note: Q(terminal-state,.) = 0

# undiscounted and episodic task
n_steps = 0
n_episodes = 0


# epsilon-greedy strategy
def ep_greedy(epsilon,num_actions,q,i,j):
    roll = np.random.uniform(0,1)
        
    # epsilon-greedy strategy
    if roll < epsilon: # exploration
        a = np.random.randint(0,num_actions)
    else:              # exploitation
        a = np.argmax(q[i,j,:])
        
    return a

# translate action into state-change
# note since there is cross-wind in the gridworld
# hence it's not directly mapping
def action2state(i,j,a):
    # Note: coordintate system start from the upper-left corner and 
    #       right/downwards are the positive direction
    if   a == 0: # to left
        i_next = i
        j_next = j - 1
    elif a == 1: # upwards
        i_next = i - 1
        j_next = j
    elif a == 2: # to right
        i_next = i
        j_next = j + 1
    else:        # downwards
        i_next = i + 1
        j_next = j
    
    # add wind effect, a bit counter-intuitive, affect row reading
    if j == 3 or j == 4 or j == 5 or j == 8:
        i_next = i_next -1
    elif j == 6 or j == 7:
        i_next = i_next - 2
        
    return i_next,j_next
    
while n_steps < N_steps:

    # begin of an episode
    i = start_r
    j = start_c
    
    # end of an episode
    n_episodes += 1
    print "episode ",str(n_episodes),"..."
    
    while True:
        n_steps += 1
        # print "    step ",str(n_steps),"..."
        # choose A from S using policy derived from Q (epsilon-greedy)
        a = ep_greedy(epsilon,N_actions,q,i,j)
        
        # translate action into state-change with windy effect
        i_next,j_next = action2state(i,j,a)
        
        # update the state-action value function
        #     state transitions end in the goal state
        #     state should be in the range of the gridworld    
        if i_next == goal_r and j_next == goal_c: # reach the goal position
            #q[i,j] = q[i,j] + step_size * (0 + q[i_next,j_next] - q[i,j])
            q[i,j] = q[i,j] + step_size * (0 + 0 - q[i,j]) #the Q(terminal,.) = 0
            break
        # keep in mind of different wind strength of the boundary condition    
        elif i_next < 0:
            i_next = 0
        elif i_next > n_row - 1:
            i_next = n_row - 1
            
        elif j_next < 0 or j_next > n_col - 1:
            j_next = j
            
        a_next = ep_greedy(epsilon,N_actions,q,i_next,j_next)
        
        q[i,j,a] = q[i,j,a] + step_size * (-1 + q[i_next,j_next,a_next] - q[i,j,a])
        
        i = i_next
        j = j_next

# visualize the solution
# plot the gridworld as background
#     (optional) mark wind direction
pygame.init()
pygame.display.set_mode((n_col * grid_size,n_row * grid_size))
pygame.display.set_caption('Windy Gridworld')
 
screen = pygame.display.get_surface()
surface = pygame.Surface(screen.get_size())
bg = pygame.Surface(screen.get_size())
 
 
def draw_bg(surface,n_row,n_col,grid_size,start_r,start_c,goal_r,goal_c):
    for i in range(n_col):
        for j in range(n_row):
            x = i * grid_size
            y = j * grid_size
            coords = pygame.Rect(x,y,grid_size,grid_size)
            pygame.draw.rect(surface,(255,255,255),coords,1)

    # draw start state
    pygame.draw.circle(surface,(192,192,192),(start_c * grid_size + grid_size/2,
                                              start_r * grid_size + grid_size/2),grid_size/4)

    # draw goal state         
    pygame.draw.circle(surface,(102,204,0),(goal_c * grid_size + grid_size/2,
                                            goal_r * grid_size + grid_size/2),grid_size/4)
                                            
# use state-action function to find one-step optimal policy
def step_q(q,s_r,s_c,n_row,n_col):
    print "state-action value:"
    print q[s_r,s_c,:]
    a = np.argmax(q[s_r,s_c,:]) # greedy only
    
    # display debug
    if   a == 0:
        print "move left"
    elif a == 1:
        print "move upward"
    elif a == 2:
        print "move right"
    else:
        print "move downwards" 
    
    s_r_next,s_c_next = action2state(s_r,s_c,a) 
    
    # keep in mind of different wind strength of the boundary condition
    # since the wind blow only in vertical direction    
    if s_r_next < 0:
        s_r_next = 0
    elif s_r_next > n_row -1:
        s_r_next = n_row - 1
    
    elif s_c_next < 0 or s_c_next > n_col - 1:
        s_c_next = s_c
        
    return s_r_next,s_c_next

s_r = start_r
s_c = start_c
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
             
    # draw gridworld background
    draw_bg(bg,n_row,n_col,grid_size,start_r,start_c,goal_r,goal_c)
    screen.blit(bg,(0,0))
    
    # draw the state of the agent, i.e. the path (start --> end) as the foreground   
    surface.fill((0,0,0))
    
    # use state-action function to find a optimal policy
    #    in the loop, should provide a step function
    #print (s_r,s_c)
    s_r_next,s_c_next = step_q(q,s_r,s_c,n_row,n_col)
    #print (s_r_next,s_c_next)
    if s_r_next != goal_r or s_c_next != goal_c:
        pygame.draw.circle(surface,(255,255,255),(s_c_next * grid_size + grid_size/2,
                                                  s_r_next * grid_size + grid_size/2),grid_size/4)
     
    bg.blit(surface,(0,0))
    pygame.display.flip() # update
    pygame.time.delay(1000)
    
    s_r,s_c = s_r_next,s_c_next # update coordinate

