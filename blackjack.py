# blackjace experiment
# version: each player competes independently against the dealer
import numpy as np

# a game episode
# def game():

# 	def init():
# 		# deal two cards to both player and the dealer
# 		dealer_cards.append(deal())
# 		dealer_cards.append(deal())
# 		player_cards.append(deal())
# 		player_cards.append(deal())

# 		return dealer_cards, player_cards

# 	def deal():
# 		# deal a card
# 		card = np.random.randint(1,14)
# 		return card

# 	def win_or_loss(dealer_cards, player_cards):
# 		# decide current result

# 		# convert cards to sum
# 		dealer_cards_sum = 0
# 		for card in dealer_cards:
# 			if card > 10:
# 				dealer_cards_sum += 10
# 			else:
# 				dealer_cards_sum += card


# 		if sum(dealer_cards) == 21:
# 			r = -1
# 			terminal = True
# 			info = "player loses!!! --> dealer hits 21"
# 		elif sum(dealer_cards) > 21:
# 			r = 1
# 			terminal = True
# 			info = 'player wins!!! --> dealer busts'
# 		elif sum(player_cards) == 21:
# 			r = 1
# 			terminal = True
# 			info = "player wins!!! --> player hits 21"
# 		elif sum(player_cards) > 21:
# 			r = -1
# 			terminal = True
# 			info = "player loses!!! --> player busts"
# 		else:
# 			r = 0
# 			terminal = False
# 			info = ""

# 		return r, terminal, info

# 	r = 0
# 	terminal = False
# 	info = ""

# 	dealer_cards, player_cards = init()

# 	if sum(player_cards) == 12:

# 	r, terminal, info = evalute_result(player_cards, dealer_cards)

# 	print "=============== Game ==============="
	
# 	while not terminal:
# 		# play a round
# 		dec = policyP(player_cards)
# 		if dec == 1:
# 			player_cards.append(deal())
# 		else:
# 			dealer_cards.append(deal())

# 		player_dec = policyP(player_cards)
# 		dealer_dec = policyD(dealer_cards)

# 		# decision for current round
# 		if player_dec == 0 and dealer_dec == 0: # player and dealer stick
# 			if sum(player_cards) > sum(dealer_cards):
# 				r = 1
# 				terminal = True
# 				info = "player wins!!! --> player larger than dealer"
# 			elif sum(player_cards) == sum(dealer_cards):
# 				r = 0
# 				terminal = True
# 				info = "player ties!!! --> player ties with dealer"
# 			elif sum(player_cards) < sum(dealer_cards):
# 				r = -1
# 				terminal = True
# 				info = "player loses!!! --> player smaller than dealer"

# 		if player_dec == 0 and dealer_dec == 1: # player sticks and dealer hits
# 			dealer_cards.append(deal())

# 		if player_dec == 1 and dealer_dec == 0: # player hits and dealer sticks
# 			player_cards.append(deal())

# 		if player_dec == 1 and dealer_dec == 1: # player hits and dealer hits
# 			player_cards.append(deal())

# 		r, terminal, info = evalute_result(player_cards, dealer_cards)

# 	print "dealer's cards: "
# 	print dealer_cards
# 	print "player's cards:"
# 	print player_cards
# 	print info

# 	# return result

# def policyD(dealer_cards):
# 	dealer_current_sum = sum(dealer_cards)
# 	if dealer_current_sum >= 17:
# 		decision = 0 # stick
# 	else:
# 		decision = 1 # hit
# 	return decision

# def policyP(player_cards):
# 	player_current_sum = sum(player_cards)
# 	if player_current_sum == 20 or player_current_sum == 21:
# 		decision = 0 # stick
# 	else:
# 		decision = 1 # hit
# 	return decision

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
	if 1 in player_cards and sum(player_cards) >= 11:
		if 1 in dealer_cards and sum(dealer_cards) >= 11:
			r = 0
			info = "Both player and dealer get natural, ties!"
			return r, info, player_cards, dealer_cards
		else:
			r = 1
			info = "Player gets natural, player wins!"
			return r, info, player_cards, dealer_cards
	else:
		if 1 in dealer_cards and sum(dealer_cards) >= 11:
			r = -1
			info = "Dealer get natural, player loses!"
			return r, info, player_cards, dealer_cards

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
			else:
				player_cards.append(new_card)

			if sum(player_cards) > 21:
				r = -1
				info = "Player busts, player loses"
				return r, info, player_cards, dealer_cards


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
				return r, info, player_cards, dealer_cards

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

	return r, info, player_cards, dealer_cards

# simulation
N = 10
for i in range(N):
	print "========== Game " + str(i) + " =========="
	r, info, player_cards, dealer_cards = game()
	print player_cards
	print dealer_cards
	print info
