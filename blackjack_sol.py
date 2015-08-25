""" 
Solve blackjack problem with Monte Carlo with Exploring Start
Author: Wenbin Li

"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import numpy.random as npr
import time

# Update the estimation of action value, return, policy 
def one_sample(Q,R,P):

    # initial state
    dealer_card_facedown = npr.randint(1,11)
    dealer_card_show = npr.randint(1,11)
    player_sum_cur = npr.randint(12,22)
    
    # if the player gets a natural
    if player_sum_cur == 21:
        up_state_0 = R[player_sum_cur - 12,dealer_card_show - 1,0]
        up_state_1 = R[player_sum_cur - 12,dealer_card_show - 1,1]

        # if the dealer also gets a natural, then it's a draw
        if (dealer_card_facedown == 1 and dealer_card_show == 10) or \
           (dealer_card_facedown == 10 and dealer_card_show == 1): 
            # udpate the return function
            R[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state_0[0]+0,up_state_0[1]+1) # +0 for draw
            R[player_sum_cur - 12,dealer_card_show - 1,1] = (up_state_1[0]+0,up_state_1[1]+1) # +0 for draw
            # udpate action value function, but the player doesn't do any actions?
            Q[player_sum_cur -  12,dealer_card_show - 1,0] = (up_state_0[0]+0)/(up_state_0[1] + 1) # draw->reward 0,regardless of the action???
            Q[player_sum_cur -  12,dealer_card_show - 1,1] = (up_state_1[0]+0)/(up_state_1[1] + 1)
            print "player draw with natural"
        # if the dealer does not get a natural, then the player won
        else:
            # udpate the return function
            R[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state_0[0]+1,up_state_0[1]+1) # +1 for win
            R[player_sum_cur - 12,dealer_card_show - 1,1] = (up_state_1[0]+0,up_state_1[1]+1) # +0 for draw
            # udpate action value function, but the player doesn't do any actions?
            Q[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state_0[0]+1)/(up_state_0[1] + 1) # draw->reward 0,regardless of the action???
            Q[player_sum_cur - 12,dealer_card_show - 1,1] = (up_state_1[0]+1)/(up_state_1[1] + 1)
            print "player win with natural"
            
        # update policy
        P[player_sum_cur - 12,dealer_card_show - 1] = np.argmax(Q[player_sum_cur - 12,dealer_card_show - 1])
                    
        # return updates and end this round simulation
        return Q,R,P

    # if the player does not have a natural, then the game moves on
    else:
        # so we need to compute the working sum of the dealer's initial two cards 
        if dealer_card_facedown == 1 and dealer_card_show == 1: # 2 aces
            dealer_sum_cur = 11 + 1
        elif dealer_card_facedown == 1: # 1 ace for facedown
            dealer_sum_cur = dealer_card_show + 10
        elif dealer_card_show == 1:     # 1 ace for show
            dealer_sum_cur = dealer_card_facedown + 10
        else:                           # no ace
            dealer_sum_cur = dealer_card_facedown + dealer_card_show
                
        # separate the case of usable aces and no usable aces
        # use the current policy to generate a sample
        running = True
        num_player_actions = 0 # counter for the player's action {hit,stick}
        # continue to hits with respect to the current policy until 
        #    1) lose or 2) the decision of stick
        while running:
            # take action according to the policy
            action = P[player_sum_cur - 12,dealer_card_show - 1]
            num_player_actions += 1

            if action == 0: # if the player stick
                # it's dealer's turn to finish the round !
                # 1) dealer sticks, compare the value
                # 2) dealer goes bust, player wins
                while dealer_sum_cur < 17:
                    card_hit = npr.randint(1,11)
                    dealer_sum_cur += card_hit
                
                up_state = R[player_sum_cur - 12,dealer_card_show - 1,0]

                # wrap up the card number
                if dealer_sum_cur > 21: # dealer goes bust
                    
                    # update return function NOTE: R should be of (s,a) not (s)
                    R[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state[0] + 1 * num_player_actions,up_state[1]+1)
                    # update action value function
                    Q[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state[0] + 1 * num_player_actions) / (up_state[1] + 1)

                    print "player win"
                    
                else: # dealer does not go bust,then compare card number
                    if dealer_sum_cur > player_sum_cur:
                        R[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state[0] - 1 * num_player_actions,up_state[1]+1)
                        Q[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state[0] - 1 * num_player_actions) / (up_state[1] + 1)
                        print "player lose"
                    elif dealer_sum_cur == player_sum_cur:
                        R[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state[0] + 0 * num_player_actions,up_state[1]+1)
                        Q[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state[0] + 0 * num_player_actions) / (up_state[1] + 1)
                        print "player draw"
                    else:
                        R[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state[0] + 1 * num_player_actions,up_state[1]+1)
                        Q[player_sum_cur - 12,dealer_card_show - 1,0] = (up_state[0] + 1 * num_player_actions) / (up_state[1] + 1)
                        print "player win"

                # update policy
                P[player_sum_cur - 12,dealer_card_show - 1] = np.argmax(Q[player_sum_cur - 12,dealer_card_show - 1])
                # return updates and end this round simulation
                return Q,R,P

            else: # if the player hits, stop till
                # 1) policy stop then the code goes to the upper if branch # TODO check the validatity for different situation
                # 2) player goes bust
                card_hit = npr.randint(1,11)

                if card_hit + player_sum_cur > 21:  # player goes bust

                    up_state = R[player_sum_cur - 12,dealer_card_show - 1,1]
                    # update return function
                    R[player_sum_cur - 12,dealer_card_show - 1,1] = (up_state[0] -1 * num_player_actions,up_state[1]+1)
                    # update action value function
                    Q[player_sum_cur - 12,dealer_card_show - 1,1] = (up_state[0] - 1 * num_player_actions)/(up_state[1] + 1)
                    # update policy
                    P[player_sum_cur - 12,dealer_card_show - 1] = np.argmax(Q[player_sum_cur - 12,dealer_card_show - 1])
                    print "player lose"
                    # return updates and end this round simulation
                    return Q,R,P
                else:
                    # if the player does not go bust, then we need to consider *delayed reward*
                    #   to cope this, we only update the counter
                    player_sum_cur += card_hit

                    up_state = R[player_sum_cur - 12,dealer_card_show - 1,1]
                    # update return function
                    R[player_sum_cur - 12,dealer_card_show - 1,1] = (up_state[0],up_state[1]+1)
                    # update action value function
                    Q[player_sum_cur - 12,dealer_card_show - 1,1] = (up_state[0])/(up_state[1] + 1)
                    # update policy
                    P[player_sum_cur - 12,dealer_card_show - 1] = np.argmax(Q[player_sum_cur - 12,dealer_card_show - 1])
                    # continue to other branch to end this round simulation

# main script to run simulation
N = 50000
# initialization
q = np.zeros((10,10,2)) # 200 pairs? s = 10x10, a = 2
# init policy if player_sum_cur = 20 or 21 sticks otherwise hits
# regarding the policy, it's a mapping from states to action

# store in a table/array
# each row for the same player's current sum
# 1 for stick, 0 for hit
pi = np.zeros((10,10)) 
pi[8,:] = 1
pi[9,:] = 1 

# return is a list, we use a dict to store the value
# for consistency, we convert the range of key to 0-9
r = {}
for i in range(10):
    for j in range(10):
        r[i,j,0] = (0,0)
        r[i,j,1] = (0,0)

for i in range(N):
    print "itr. ",str(i)
    q,r,pi = one_sample(q,r,pi)
    
    #if i % 500 == 0:
    #    print pi

plt.matshow(pi)
plt.show()

print pi
