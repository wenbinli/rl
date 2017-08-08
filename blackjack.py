# blackjace experiment
# version: each player competes independently against the dealer
import numpy as np

# a game episode
def game():

	def init():
		# deal two cards to both player and the dealer
		dealer_cards.append(deal())
		dealer_cards.append(deal())
		player_cards.append(deal())
		player_cards.append(deal())

		return dealer_cards, player_cards

	def deal():
		# deal a card
		card = np.random.randint(1,14)
		return card

	def win_or_loss(dealer_cards, player_cards):
		# decide current result

		# convert cards to sum
		dealer_cards_sum = 0
		for card in dealer_cards:
			if card > 10:
				dealer_cards_sum += 10
			else:
				dealer_cards_sum += card


		if sum(dealer_cards) == 21:
			r = -1
			terminal = True
			info = "player loses!!! --> dealer hits 21"
		elif sum(dealer_cards) > 21:
			r = 1
			terminal = True
			info = 'player wins!!! --> dealer busts'
		elif sum(player_cards) == 21:
			r = 1
			terminal = True
			info = "player wins!!! --> player hits 21"
		elif sum(player_cards) > 21:
			r = -1
			terminal = True
			info = "player loses!!! --> player busts"
		else:
			r = 0
			terminal = False
			info = ""

		return r, terminal, info

	r = 0
	terminal = False
	info = ""

	dealer_cards, player_cards = init()

	if sum(player_cards) == 12:

	r, terminal, info = evalute_result(player_cards, dealer_cards)

	print "=============== Game ==============="
	
	while not terminal:
		# play a round
		dec = policyP(player_cards)
		if dec == 1:
			player_cards.append(deal())
		else:
			dealer_cards.append(deal())

		player_dec = policyP(player_cards)
		dealer_dec = policyD(dealer_cards)

		# decision for current round
		if player_dec == 0 and dealer_dec == 0: # player and dealer stick
			if sum(player_cards) > sum(dealer_cards):
				r = 1
				terminal = True
				info = "player wins!!! --> player larger than dealer"
			elif sum(player_cards) == sum(dealer_cards):
				r = 0
				terminal = True
				info = "player ties!!! --> player ties with dealer"
			elif sum(player_cards) < sum(dealer_cards):
				r = -1
				terminal = True
				info = "player loses!!! --> player smaller than dealer"

		if player_dec == 0 and dealer_dec == 1: # player sticks and dealer hits
			dealer_cards.append(deal())

		if player_dec == 1 and dealer_dec == 0: # player hits and dealer sticks
			player_cards.append(deal())

		if player_dec == 1 and dealer_dec == 1: # player hits and dealer hits
			player_cards.append(deal())

		r, terminal, info = evalute_result(player_cards, dealer_cards)

	print "dealer's cards: "
	print dealer_cards
	print "player's cards:"
	print player_cards
	print info

	# return result

def policyD(dealer_cards):
	dealer_current_sum = sum(dealer_cards)
	if dealer_current_sum >= 17:
		decision = 0 # stick
	else:
		decision = 1 # hit
	return decision

def policyP(player_cards):
	player_current_sum = sum(player_cards)
	if player_current_sum == 20 or player_current_sum == 21:
		decision = 0 # stick
	else:
		decision = 1 # hit
	return decision

def game():
	# new definition of a game
	# 1) first deal two cards to both player and dealer
	# 2) decide if game stops here:
	# 		if game stops
	#			decide winner
	#			game over
	#		else
	# 			continue to 3) player's turn
	# 3) player's turn
	#		if player sticks
	#			then go to dealer's turn
	#		if player hits
	#			if player busts
	#				player loses
	#				game over
	#			else
	#				continue to 3)
	# 4) dealer's turn
	#		if dealer sticks
	#			decide winner
	#			game over
	#		if dealer hits
	#			if dealer busts
	#				dealer loses
	#				game over
	#			else
	#				continue to 4)

# simulation
N = 10
for i in range(N):
	game()
