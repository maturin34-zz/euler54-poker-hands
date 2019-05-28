import unittest
from euler54 import *

class TestCardRanking(unittest.TestCase):

	
	FLUSH           = ['8C', 'KC', '7C', 'TC', '2C'] 
	STRAIGHT        = ['8S', '6H', 'TD', '7C', '9C']  # watch out with the namespaceing!
	ONE_PAIR        = ['AS', 'AH', '8D', 'JH', '6C']
	TWO_PAIR        = ['KH', 'AH', 'KS', '2D', '2C']
	THREE_OF_A_KIND = ['5H', '4H', '5S', 'TD', '5C']
	FOUR_OF_A_KIND  = ['8H', '8D', '8S', 'TD', '8C']
	FULL_HOUSE      = ['AH', 'KD', 'AS', 'AD', 'KC']
	RANDOM_HAND     = ['8C', 'TS', 'KC', '9H', '4S']
    

	def test_straight(self):
		processed_hand = process_hand(self.STRAIGHT)   
		sorted_hand = sort_hand(processed_hand)
		
		expected_result = ('STRAIGHT', ['10', '9', '8', '7', '6'])
		self.assertEqual(straight(sorted_hand), expected_result)

	def test_flush(self):
		processed_hand = process_hand(self.FLUSH)
		sorted_hand = sort_hand(processed_hand)

		expected_result = ('FLUSH', ['13', '10', '8', '7', '2'])
		self.assertEqual(flush(sorted_hand), expected_result)

	def test_one_pair(self):
		processed_hand = process_hand(self.ONE_PAIR)  # factor this out obviously
		sorted_hand = sort_hand(processed_hand)

		expected_result = ('PAIR', {'14'}, ['11', '8', '6'])
		self.assertEqual(pairs(sorted_hand), expected_result)

	def test_two_pair(self):
		processed_hand = process_hand(self.TWO_PAIR) 
		sorted_hand = sort_hand(processed_hand)

		expected_result = ('TWO PAIR', {'13', '2'}, ['14'])
		self.assertEqual(pairs(sorted_hand), expected_result)

	def test_threeofakind(self):
		processed_hand = process_hand(self.THREE_OF_A_KIND) 
		sorted_hand = sort_hand(processed_hand)

		expected_result = ("THREE OF A KIND", {'5'}, ['10', '4'])
		self.assertEqual(pairs(sorted_hand), expected_result)

	def test_fourofakind(self):
		processed_hand = process_hand(self.FOUR_OF_A_KIND) 
		sorted_hand = sort_hand(processed_hand)

		expected_result = ("FOUR OF A KIND", {'8'}, ['10'])
		self.assertEqual(pairs(sorted_hand), expected_result)

	def test_full_house(self):
		processed_hand = process_hand(self.FULL_HOUSE) 
		sorted_hand = sort_hand(processed_hand)
		# full house function returns list instead of set, and no kickers
		expected_result = ("FULL HOUSE", ['14'], None) 
		self.assertEqual(pairs(sorted_hand), expected_result)

	def test_high_card(self):
		# totally different test, probably should be in new test class
		expected_result = (0, ['13','10','9','8','4']) 
		self.assertEqual(rank_hand(self.RANDOM_HAND), expected_result)


class TestBreakTies(unittest.TestCase):
	

	def test_high_card_vs_high_card(self):
		hand1 = ['8C', 'TS', 'KC', '9H', '4S'] 
		hand2 = ['7D', '2S', '5D', '3S', 'AC']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 2
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_flush_vs_flush(self):
		hand1 = ['5C', 'KC', '5C', 'AC', '6C'] 
		hand2 = ['JD', '9D', 'QD', '9D', 'TD']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 1
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_two_pair_vs_two_pair(self):  # remember always has to begin with 'test'
		hand1 = ['5D', '6C', '5C', 'AC', '6D'] 
		hand2 = ['TS', '9D', 'QD', 'QH', 'TD']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 2
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_full_house_vs_full_house(self):
		hand1 = ['TD', 'TC', 'TS', 'AC', 'AD'] 
		hand2 = ['JS', 'JD', 'JH', '2H', '2D']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 2
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_straight_flush_vs_straight_flush(self):
		hand1 = ['AD', 'KD', 'TD', 'JD', 'QD'] 
		hand2 = ['KS', 'QS', '10S', '9S', 'JS']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 1
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)


	def test_pair_vs_pair(self):
		hand1 = ['AD', 'QD', 'AS', 'JC', '2H'] 
		hand2 = ['AH', 'KS', '10D', 'AC', '7C']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 2
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_straight_vs_straight(self):
		hand1 = ['AC', 'TS', 'KC', 'JH', 'QS'] 
		hand2 = ['KD', '10S', 'JD', 'QH', '9C']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 1
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

class CompareDifferentHands(unittest.TestCase):
	

	def test_high_card_vs_two_pair(self):
		hand1 = ['8C', 'TS', 'KC', '9H', '4S'] 
		hand2 = ['7D', '7S', '5D', '3S', '5C']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 2
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_four_of_a_kind_vs_full_house(self):
		hand1 = ['8C', '8S', 'KC', '8H', '8D'] 
		hand2 = ['AD', 'AS', 'KD', 'KS', 'AC']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 1
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

class Wheel(unittest.TestCase):
	
	WHEEL_STRAIGHT_FLUSH = ['2S', '3S', 'AS', '4S', '5S']
	WHEEL_STRAIGHT = ['2H', '3S', 'AC', '4S', '5D']


	def test_wheel_straight_vs_straight(self):
		"""wheel straight always loses to any other straight"""
		hand1 = self.WHEEL_STRAIGHT 
		hand2 = ['7D', '6S', '5D', '3S', '4C']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 2
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_wheel_straight_vs_two_pair(self):
		
		hand1 = self.WHEEL_STRAIGHT 
		hand2 = ['7D', '7S', '5D', '3S', '3C']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 1
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_wheel_straight_flush_vs_nut_flush(self):
		
		hand1 = self.WHEEL_STRAIGHT_FLUSH 
		hand2 = ['AD', 'KD', '8D', 'JD', '4D']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 1
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

	def test_wheel_straight_flush_vs_straight_flush(self):
		"""wheel straight flus always loses to any other straight flush"""
		hand1 = self.WHEEL_STRAIGHT_FLUSH 
		hand2 = ['6D', '5D', '4D', '2D', '3D']

		hand1_ranking = rank_hand(hand1)
		hand2_ranking = rank_hand(hand2)
		expected_result = 2
		self.assertEqual(compare_hands(hand1_ranking, hand2_ranking), expected_result)

if __name__ == '__main__':
    unittest.main()
