
def process_hand(hand):
	
	# Jack == 11, Queen == 12, etc.
	face_card_dict = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
	# assign number values for face cards
	new_hand = []
	for card in hand:
		if card[0].isalpha():
			new_hand.append(face_card_dict[card[0]] + card[1:])
		else:
			new_hand.append(card)
	return new_hand

def sort_hand(hand):
	# get tuple (card_value, suit) for each hand
	temp = [(n[:-1], n[-1:]) for n in hand]
	# sort cards from highest to lowest based on card value, ignore suit
	sorted_hand = sorted(temp, key=lambda card: int(card[0]), reverse=True)
	# recombine tuples into strings
	# no don't do that
	# sorted_hand = [''.join(card) for card in sorted_hand]
	return sorted_hand

def straight(hand):
	biggest_card = int(hand[0][0])
	no_suits = [card[0] for card in hand]
	for card in hand[1:]:
		if not int(card[0]) == biggest_card - 1:
			return False
		else:
			biggest_card -= 1
	return ("STRAIGHT", no_suits)


def flush(hand):
	suits = [card[-1] for card in hand]
	no_suits = [card[0] for card in hand]
	if len(set(suits)) == 1:

		return ("FLUSH", no_suits)
	else:
		return False

def straight_flush(hand):
	# calls flush funcion
	# calls straight function
	pass


def find_duplicates(hand):
	dup_cards = {}
	for card in hand:
		if card in dup_cards:
			dup_cards[card] += 1
		else:
			dup_cards[card] = 1
	dupes = {card for card in dup_cards if dup_cards[card] > 1}  # order of pairs doesn't matter
	                                                             # screws up testing if I return a list here
	return dupes

def full_house_processing(hand):
	# just want the three of a kind part of 
	# the full house
	dup_cards = {}
	for card in hand:
		if card in dup_cards:
			dup_cards[card] += 1
		else:
			dup_cards[card] = 1
	return [max(dup_cards, key=dup_cards.get)]  # this is really dodgy


def wheel_straight(hand):
	wheel_straight_no_suits = ['14', '5', '4', '3', '2']
	no_suits = [card[0] for card in hand]
	if wheel_straight_no_suits == no_suits:
		# ensure wheel_straight always loses to every other straight
		wheel_straight_no_suits[0] = '1'
		return ("STRAIGHT", wheel_straight_no_suits) 


def pairs(hand):
	# after flush/straight-flush processing suits don't matter anymore right?
	no_suits = [card[0] for card in hand]
	unique_cards = set(no_suits)
	if len(unique_cards) == 2:  # four of a kind OR full house
		dupes = find_duplicates(no_suits)
		kickers = [card[0] for card in hand if card[0] not in dupes]
		if len(dupes) == 2: # full house
			# order matters for ranking full house
			full_house_type = full_house_processing(no_suits)
			#temp_dupes = [int(card) for card in dupes]
			#sorted_dupes = [str(card) for card in sorted(temp_dupes, reverse=True)]
			#full house have to return cards in correct order not descending order
			return ("FULL HOUSE", full_house_type, None) # full house has no kickers, need to
			                                          # return None because ranking function
			                                          # expects 3 element tuple

		else: # four of a kind
			return ("FOUR OF A KIND", dupes, kickers)

		
	elif len(unique_cards) == 3:  # three of a kind OR 2 pair
		dupes = find_duplicates(no_suits)
		kickers = [card[0] for card in hand if card[0] not in dupes] # kickers logic needs to be factored out
		if len(dupes) == 2: # two pair
			return ("TWO PAIR", dupes, kickers)
		else: # three of a kind
			return ("THREE OF A KIND", dupes, kickers)
		
		
	elif len(unique_cards) == 4:
		# one pair
		pair = find_duplicates(no_suits)
		# no suits needed for kickers right?
		kickers = [card[0] for card in hand if card[0] not in pair]
		return ('PAIR', pair, kickers)
	else:
		return False


def rank_hand(hand):

	ranking = {"STRAIGHT FLUSH": 8, "FOUR OF A KIND": 7, "FULL HOUSE": 6, 
		   "FLUSH": 5, "STRAIGHT": 4, "THREE OF A KIND": 3, "TWO PAIR": 2, 
	           "PAIR": 1, "HIGH CARD": 0}

	processed_hand = process_hand(hand)
	sorted_hand = sort_hand(processed_hand)

	is_flush = flush(sorted_hand)
	is_wheel_straight = wheel_straight(sorted_hand)
	is_straight = straight(sorted_hand)

	if is_flush and is_straight:
		return (ranking["STRAIGHT FLUSH"], is_flush[1])
	elif is_flush and is_wheel_straight:
		return (ranking["STRAIGHT FLUSH"], is_wheel_straight[1])	
	elif is_flush:
		return (ranking["FLUSH"], is_flush[1])
	elif is_straight:
		return (ranking["STRAIGHT"], is_straight[1])
	elif is_wheel_straight:
		return (ranking["STRAIGHT"], is_wheel_straight[1])
	is_pair = pairs(sorted_hand)
	if is_pair:
		return (ranking[is_pair[0]], is_pair[1], is_pair[2])
	else: # hand is merely high card
		no_suits = [card[0] for card in sorted_hand]
		return (ranking["HIGH CARD"], no_suits)


def break_tie(hand1_ranking, hand2_ranking):
	
	for a, b in zip(hand1_ranking[1], hand2_ranking[1]):
		if int(a) > int(b):
			return 1
		elif int(b) > int(a):
			return 2
	# do it again with 2nd tie breaker
	for a, b in zip(hand1_ranking[2], hand2_ranking[2]):
		if int(a) > int(b):
			return 1
		elif int(b) > int(a):
			return 2


	

def compare_hands(hand1_ranking, hand2_ranking):

	if hand1_ranking[0] > hand2_ranking[0]:
		return 1
	elif hand2_ranking[0] > hand1_ranking[0]:
		return 2
	else:
		# call tie breaking function
		return break_tie(hand1_ranking, hand2_ranking)  # double return?? this confuses me
		                                                # this function calls another function
		                                                # which returns to this function
		                                                # which returns to the mainloop?												

if __name__ == "__main__":

	all_da_hands = []
	with open('p054_poker.txt', 'r', encoding='utf-8') as f:
		temp = []
		for line in f:
			temp.append(line.split())

	assert len(temp) == 1000
	for line in temp:
		# good trick for iterating
		# can unpack tuple automatically when looping
		all_da_hands.append((line[:5], line[5:]))

	print("First hand pair is: {}".format(all_da_hands[0]))
	print("Last hand pair is {}".format(all_da_hands[-1]))


	hand1_wins = 0
	hand2_wins = 0
	for hand1, hand2 in all_da_hands:  
		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		winner = compare_hands(hand1_ranking, hand2_ranking)
		assert winner in (1, 2)
		if winner == 1:
			hand1_wins += 1
		else:
			hand2_wins += 1

	print(hand1_wins)
	#print("hand 2 wins: {}".format(hand2_wins))
	
	



