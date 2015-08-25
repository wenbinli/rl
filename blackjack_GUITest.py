""" 
blackjack problem with Monte Carlo prediction (policy evaluation)

Author: Wenbin Li
"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import numpy.random as npr
import time

# generate samples for MC

# generate the card shown from the dealer
# Note: the face down card for the dealer should be counted and is not visible!
# though it is not counted as a state

# IMPORTANT: updating the table for state-value V-function 
def one_round(dealer_card_show,player_sum_cur):    

    # TODO modify the model for reward, currently seems to treat the whole action in a round a state
    
    # state
    #dealer_card_show = npr.randint(1,11) # randint , lower bound inclusive, upper bound exclusive
    #player_sum_cur = npr.randint(12,22)
    
    # generate the face down card for the dealer
    dealer_card_facedown = npr.randint(1,12)
    
    dealer_sum_cur = dealer_card_facedown # hidden state ?
    
    # player's policy: sticks if the sum is 20 or 21, otherwise hits
    while player_sum_cur < 20:
        card_hit = npr.randint(1,11) # no usable ace
        player_sum_cur += card_hit # action!
        if player_sum_cur > 21:
            reward = -1
            return reward

    # done with the player's round, hit till sum is 17
    while dealer_sum_cur < 17:
        card_hit = npr.randint(1,11) # also no usable ace 
        dealer_sum_cur += card_hit
        if dealer_sum_cur > 21:
            reward = 1
            return reward
    
    # compare the sum if necessary
    if player_sum_cur > dealer_card_show:
        reward = 1
    elif player_sum_cur == dealer_card_show:
        reward = 0
    else:
        reward = -1
            
    return reward

# plot function
def sim(N):
    # N = 5000
    states = {}
    for i in range(N):
        dealer_card_show = npr.randint(1,11) # randint , lower bound inclusive, upper bound exclusive
        player_sum_cur = npr.randint(12,22)

        reward = one_round(dealer_card_show,player_sum_cur)
    
        if (dealer_card_show,player_sum_cur) in states:
            states[(dealer_card_show,player_sum_cur)] = \
                (states[(dealer_card_show,player_sum_cur)][0]+reward,
                 states[(dealer_card_show,player_sum_cur)][1]+1)
        else:
            states[(dealer_card_show,player_sum_cur)] = (reward,1)

    # average and plot
    states_reward_avg = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            # note the dealer card show ranges from 1 to 10
            #      the player sum ranges from 12 to 21
            if (i+1,j+1+11) in states:
                states_reward_avg[i,j] = states[(i+1,j+1+11)][0]*1./states[(i+1,j+1+11)][1]

    return states_reward_avg
    

# made animation
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.set_xlabel('Dealer showing')
ax.set_ylabel('Player sum')

# use the pause to do the animation trick
axis_dealer_card_show = np.arange(1,11)
axis_player_sum_cur = np.arange(12,22)
x,y = np.meshgrid(axis_dealer_card_show,axis_player_sum_cur)

wframe = None
#tstart = time.time()
for i in range(100):
    n_samples = 5000 + i * 5000
    z = sim(n_samples)
    
    oldcol = wframe
    
    wframe = ax.plot_wireframe(x,y,z)
    
    if oldcol is not None:
        ax.collections.remove(oldcol)
    
    plt.pause(.05)   
    
#print('FPS: %f' %(100/(time.time() - tstart)))
