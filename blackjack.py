# blackjace experiment
# version: each player competes independently against the dealer
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

def game():
	# new definition of a game
	def deal():
		# deal a card
		card = np.random.randint(1,14)
		if card > 10:
			card = 10
		return card

	player_cards = []
	dealer_cards = []
	usable_ace = False # mark if there is a usable ace in player's card

	# 1) first deal two cards to both player and dealer
	player_cards.append(deal())
	player_cards.append(deal())
	dealer_cards.append(deal())
	dealer_cards.append(deal())

	# 2) decide if game stops here:
	# 		if game stops
	#			decide winner
	#			game over
	#		else
	# 			continue to 3) player's turn

	# game stops situations
	#	if player gets natural and dealer does not have natural
	#		player wins
	#		game over
	#	if player gets natural and dealer gets natural
	#		player ties
	#		game over
	#	if player does not get natural and dealer gets natural
	#		player loses
	#		game over
	if 1 in player_cards and sum(player_cards) == 11:
		if 1 in dealer_cards and sum(dealer_cards) == 11:
			r = 0
			info = "Both player and dealer get natural, ties!"
			usable_ace = True
			return r, info, player_cards, dealer_cards, usable_ace
		else:
			r = 1
			info = "Player gets natural, player wins!"
			usable_ace = True
			return r, info, player_cards, dealer_cards, usable_ace
	else:
		if 1 in dealer_cards and sum(dealer_cards) == 11:
			r = -1
			info = "Dealer get natural, player loses!"
			return r, info, player_cards, dealer_cards, usable_ace

	# 3) player's turn ~ player's policy
	#		if player sticks
	#			then go to dealer's turn
	#		if player hits
	#			if player busts
	#				player loses
	#				game over
	#			else
	#				continue to 3)

	# player's policy
	# if cards count to 20 or 21 
	#	player sticks

	# usable ace
	if 1 in player_cards and sum(player_cards) + 10 <= 21:
		i = 0
		while player_cards[i] != 1: # first ace in the player's cards
			i += 1
		player_cards[i] = 11

	player_stick = False
	while not player_stick:
	
		player_sum = sum(player_cards)

		if player_sum == 20 or player_sum == 21:
			player_stick = True
		else:
			new_card = deal()
			# usable ace
			if new_card == 1 and sum(player_cards) + 11 <= 21:
				player_cards.append(11)
				usable_ace = True
			else:
				player_cards.append(new_card)

			if sum(player_cards) > 21:
				r = -1
				info = "Player busts, player loses"
				return r, info, player_cards, dealer_cards, usable_ace


	# 4) dealer's turn ~ dealer's policy
	#		if dealer sticks
	#			decide winner
	#			game over
	#		if dealer hits
	#			if dealer busts
	#				dealer loses
	#				game over
	#			else
	#				continue to 4)

	# dealer's policy
	# if cards count more than 17
	#	dealer sticks

	# usable ace
	if 1 in dealer_cards and sum(player_cards) + 10 <= 21:
		i = 0
		while dealer_cards[i] != 1: # first ace in the player's cards
			i += 1
		player_cards[i] = 11

	dealer_stick = False
	while not dealer_stick:

		dealer_sum = sum(dealer_cards)

		if dealer_sum >= 17:
			dealer_stick = True
		else:
			new_card = deal()
			# usable ace
			if new_card == 1 and sum(dealer_cards) + 11 <= 21:
				dealer_cards.append(11)
			else:
				dealer_cards.append(new_card)

			if sum(dealer_cards) > 21:
				r = 1
				info = "Dealer busts, player wins"
				return r, info, player_cards, dealer_cards, usable_ace

	# 5) both player and dealer stick, check result
	if sum(player_cards) > sum(dealer_cards):
		r = 1
		info = "Player's cards > dealer's cards, player wins"
	elif sum(player_cards) == sum(dealer_cards):
		r = 0
		info = "Player's cards = dealer's cards, player ties"
	else:
		r = -1
		info = "Player's cards < dealer's cards, player loses"

	return r, info, player_cards, dealer_cards, usable_ace

def v_update(r, player_cards, dealer_cards, v):
	dealer_show = dealer_cards[1]
	num_player_cards = len(player_cards)
	for i in range(1,num_player_cards):
		player_sum = sum(player_cards[:i+1])
		if player_sum >= 12 and player_sum <= 21:
			# import ipdb;ipdb.set_trace()
			# print dealer_show
			# print player_sum
			v[dealer_show-1,player_sum-12] += r
	return v

# init state-value estimate
V_Usable = np.zeros((10,10)) # dealer_show X player_sum
V_noUsable = np.zeros((10,10))
# MC simulation
N = 10000
N_Usable = 0
N_noUsable = 0

for i in range(N):
	print "========== Game " + str(i) + " =========="
	r, info, player_cards, dealer_cards, usable_ace = game()
	if usable_ace == True:
		V_Usable = v_update(r, player_cards, dealer_cards, V_Usable)
		N_Usable += 1
	else:
		V_noUsable = v_update(r, player_cards, dealer_cards, V_noUsable)
		N_noUsable += 1
	print player_cards
	print dealer_cards
	print info

V_Usable = 1. * V_Usable/N_Usable
V_noUsable = 1. * V_noUsable/N_noUsable

x = np.linspace(1,10,10)
y = np.linspace(12,21,10)
X,Y = np.meshgrid(x,y)

# plot results
fig = plt.figure()
ax = fig.add_subplot(2,1,1, projection='3d')
ax.plot_wireframe(X, Y, V_Usable, rstride=1, cstride=1)
ax.set_zlim(-1,1)
ax.set_zticks([-1,1])
ax.tick_params(axis='x',labelsize=7)
ax.tick_params(axis='y',labelsize=7)
ax.set_title('Usable ace')

ax = fig.add_subplot(2,1,2, projection='3d')
ax.plot_wireframe(X, Y, V_noUsable, rstride=1, cstride=1)
ax.set_zlim(-1,1)
ax.set_zticks([-1,1])
ax.tick_params(axis='x',labelsize=7)
ax.tick_params(axis='y',labelsize=7)
ax.set_title('No usable ace')
ax.set_xlabel('Dealer showing')
ax.set_ylabel('Player sum')


fig = plt.gcf()
fig.set_size_inches(4,8)
plt.tight_layout()
out_path = 'MCES_blackjack_itr_' + str(N) + '.png' 
plt.savefig(out_path,dpi=180)