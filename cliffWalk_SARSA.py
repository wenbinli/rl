# solve cliff-walking task with Sarsa
# original example problem from the book, introduction for reinforcement learning
# Author: Wenbin Li 

# numeric backend
import pygame
from pygame.locals import *
import numpy as np

grid_size = 100
n_row = 4
n_col = 12
state = np.zeros((n_row * grid_size, n_col * grid_size)) 
step_size = 0.5
epsilon = 0.1 # parameter for epislon-greedy
N_actions = 4 # number of actions {left,up,right,down}

N_episodes = 600 # number of episodes
# as suggested by the book, reach optimality by 8000 time steps
# rewards of -1 until the goal state is reached
#            -100 for entering cliff region and instantly return to starting position 

# specify goal location
goal_r = 3
goal_c = 11
# specify start location
start_r = 3
start_c = 0

# initialize state-action value function
q = np.zeros((n_row,n_col,N_actions)) # num_row by num_col by num_states
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
        
    return i_next,j_next

# Sarsa method
while n_episodes < N_episodes:

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
        
        # update the state-action value function with Sarsa/Q-Learning of choice
        #     state transitions end in the goal state
        #     state should be in the range of the gridworld    
        if i_next == goal_r and j_next == goal_c: # reach the goal position
            # q[i,j] = q[i,j] + step_size * (-1 + 0 - q[i,j]) #the Q(terminal,.) = 0
            q[i,j,a] = q[i,j,a] + step_size * (-1 + 0 - q[i,j,a]) #the Q(terminal,.) = 0
            # Note, transition from noterminal to terminal also gets reward of -1 in this case
                
            break
            
        # different reward/consequence when entering the cliff region
        elif i_next == 3 and j_next > 1 and j_next < n_col - 1:
            i_next = start_r
            j_next = start_c
            r = -100 
        elif i_next < 0 or i_next > n_row -1:
            i_next = i
            r = -1
        elif j_next < 0 or j_next > n_col - 1:
            j_next = j
            r = -1
        else:
            r = -1
            
        a_next = ep_greedy(epsilon,N_actions,q,i_next,j_next)
        
        q[i,j,a] = q[i,j,a] + step_size * (r + q[i_next,j_next,a_next] - q[i,j,a])
        
        i = i_next
        j = j_next
        
# visualize the solution/GUI-backend
# plot the gridworld as background
#     (optional) mark wind direction

pygame.init()
pygame.display.set_mode((n_col * grid_size,n_row * grid_size))
pygame.display.set_caption('Cliff Walking')
 
screen = pygame.display.get_surface()
surface = pygame.Surface(screen.get_size())
bg = pygame.Surface(screen.get_size())

# draw background, with mark on start/end states & cliff region 
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
           
    # draw cliff region
    x = 1 * grid_size
    y = 3 * grid_size
    coords = pygame.Rect(x,y,grid_size*10,grid_size)
    pygame.draw.rect(surface,(192,192,192),coords)
                                            
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
    
    # define rules especially when the agent enter the cliff region
    if s_r_next == 3 and s_c_next > 1 and s_c_next < n_col - 1:
        s_r_next = start_r
        s_c_next = start_c
        # in theory, the produced optimal policy should not enter this branch
    elif s_r_next < 0 or s_r_next > n_row -1:
        s_r_next = s_r
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
