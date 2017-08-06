# blackjace experiment
# version: each player competes independently against the dealer
import numpy as np

# deal a card
def deal():
	card = np.random.randint(1,14)
	return card

# a game episode
def game():
	def evalute_result(player_cards, dealer_cards):
		# decide current result
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

	dealer_cards = []
	player_cards = []
	r = 0
	terminal = False
	info = ""

	# first 2 cards
	dealer_cards.append(deal())
	dealer_cards.append(deal())
	player_cards.append(deal())
	player_cards.append(deal())

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

# simulation
N = 10
for i in range(N):
	game()
