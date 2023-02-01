import random
import numpy as np
from collections import Counter
import pandas as pd
import itertools
import time

## add win or lose ###

colors = ['h', 'd', 's', 'c']      
deck = [(value, color) for value in list(range(2, 15)) for color in colors]

def deal_play_game(deck, num_player):

    #deck.remove(remove_cards[0])
    #deck.remove(remove_cards[1])

    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)

    rng = np.random.default_rng()
    
    ### 3 burn cards ####
    
    cards = rng.choice(deck, size=2*num_player + 8, replace=False)

    player_cards = cards[0:2*num_player]
    face_cards = cards[2*num_player:]
    
    pocket = [player_cards[0], player_cards[1]]

    flop = face_cards[1:4]
    turn = face_cards[5:6]
    river = face_cards[7:8]

    players = []

    for i in range(num_player-1):
        players.append([tuple(player_cards[i]), tuple(player_cards[i + num_player-1])])

    return pocket, flop, turn, river, players 

def get_result_game(c1,c2,c3,c4,c5,c6,c7):
    
#     j = 0
#     personal_cards_values = [hands[j][0][0], hands[j][1][0]]
#     personal_cards_suits = [hands[j][0][1], hands[j][1][1]]
    cards = [c1,c2,c3,c4,c5,c6,c7]
    #print(cards)
    values = []
    suits = []

    for i in range(len(cards)):

        values.append(cards[i][0])
        suits.append(cards[i][1])


    num_matching = dict(Counter(suits))
    pairs_matching = dict(Counter(values))
    #print(num_matching)
    #print(pairs_matching)

    lst_of_pairs = [key for key, val in pairs_matching.items() if val == 2]
    lst_of_triples = [key for key, val in pairs_matching.items() if val == 3]
    lst_of_quads = [key for key, val in pairs_matching.items() if val == 4]

    sorted_values = list(set(sorted(list(map(int, values)))))
    #print(sorted_values)
    #print(len(sorted_values))

    if all(elem in sorted_values for elem in [2,3,4,5,14]):

        low_ball_straight = True

    else:

        low_ball_straight = False
        
    #print(low_ball_straight)

    if (5 in num_matching.values()) or (6 in num_matching.values()) or (7 in num_matching.values()):

        flush_suit = [key for key, val in num_matching.items() if val >= 5][0]
        flush_cards = [values[i] for i in range(len(values)) if suits[i] == flush_suit]
        flush_indices = [i for i in range(len(suits)) if suits[i] == flush_suit]

        #flush_cards_values = [sorted_values[i] for i in range(len(suits)) if suits[i] == flush_suit]

        if len(flush_cards) == 5:
            is_flush = True
        else:
            flush_cards = flush_cards[0:5]
            is_flush = True

    else:
        is_flush = False

    if len(lst_of_triples) == 2:
        #lst_of_triples.remove(min(lst_of_triples))
        three_of_a_kind = True

    elif len(lst_of_triples) == 1:
        three_of_a_kind = True

    elif (len(lst_of_triples) == 1) & (len(lst_of_pairs) == 1):
        one_pair = True
        three_of_a_kind = True

    else:
        three_of_a_kind =  False

    if len(lst_of_pairs) == 3:
        #lst_of_pairs.remove(min(lst_of_pairs))
        one_pair = False
        two_pair = True

    elif len(lst_of_pairs) == 2:
        two_pair = True
        one_pair = False

    elif len(lst_of_pairs) == 1:
        one_pair = True
        two_pair = False

    else:
        two_pair = False
        one_pair = False
        
    if len(sorted_values) > 4:
        
        try:

            if ((sorted_values[0] == sorted_values[1] - 1) & (sorted_values[1] == sorted_values[2] - 1) &
                (sorted_values[2] == sorted_values[3] - 1) & (sorted_values[3] == sorted_values[4] - 1)):

                is_straight = True
                straight_cards = [sorted_values[0], sorted_values[1], sorted_values[2], sorted_values[3], sorted_values[4]]
                #kickers = [sorted_values[5], sorted_values[6]]
                straight_indices = [i for i in range(len(sorted_values)) if (sorted_values[i] in straight_cards)]

            elif ((sorted_values[1] == sorted_values[2] - 1) & (sorted_values[2] == sorted_values[3] - 1) &
                (sorted_values[3] == sorted_values[4] - 1) & (sorted_values[4] == sorted_values[5] - 1)):

                is_straight = True
                straight_cards = [sorted_values[1], sorted_values[2], sorted_values[3], sorted_values[4], sorted_values[5]]
                #kickers = [sorted_values[0], sorted_values[6]]
                straight_indices = [i for i in range(len(sorted_values)) if (sorted_values[i] in straight_cards)]

            elif ((sorted_values[2] == sorted_values[3] - 1) & (sorted_values[3] == sorted_values[4] - 1) &
                (sorted_values[4] == sorted_values[5] - 1) & (sorted_values[5] == sorted_values[6] - 1)):

                is_straight = True
                straight_cards = [sorted_values[2], sorted_values[3], sorted_values[4], sorted_values[5], sorted_values[6]]
                #kickers = [sorted_values[0], sorted_values[1]]
                straight_indices = [i for i in range(len(sorted_values)) if (sorted_values[i] in straight_cards)]

            else:
                is_straight = False
                
        except:
            is_straight = False

    else:

        is_straight = False
    #print(is_straight,is_flush)
    
    if (is_straight) & (is_flush):
        if straight_indices == flush_indices:

            is_straight_flush = True
        else:
            is_straight_flush = False

    else:

        is_straight_flush = False


    if (max(sorted_values) == 14) & (is_straight_flush):

        hand_value =  10
        #pocket_cards = player_cards
        #self.best_five = straight_cards
        #self.kickers = []
        hand_name = "Royal Flush"

    elif ((is_straight) & (is_flush))|((low_ball_straight) & (is_flush)):

        hand_value =  9
    #     best_five = straight_cards
    #     self.pocket_cards = player_cards
    #     self.kickers = []
        hand_name = "Straight Flush"

    elif 4 in pairs_matching.values():

        hand_value =  8
        #self.pocket_cards = player_cards
        #self.best_five = lst_of_quads
        #self.kickers = kickers
        hand_name = "Four of a Kind"

    #     possible_kickers = list(set(lst_of_quads) - set(player_cards_values))

    #     if len(possible_kickers)>0:
    #         self.kickers = possible_kickers
    #     else:
    #         self.kickers = max(community_cards_values)


    elif (three_of_a_kind) & (one_pair):

        hand_value =  7
    #     self.pocket_cards = player_cards
    #     self.best_five = [lst_of_triples[0], lst_of_pairs[0]]
    #     self.kickers = []
        hand_name = "Full House"

    elif is_flush:

        hand_value =  6
    #     self.pocket_cards = player_cards
    #     self.best_five = flush_cards_values
    #     self.kickers = []
        hand_name = "Flush"

    elif (is_straight)|(low_ball_straight):

        hand_value =  5
    #     self.pocket_cards = player_cards
    #     self.best_five = straight_cards
    #     self.kickers = []
        hand_name = "Straight"

    elif (three_of_a_kind):

        hand_value =  4
    #     self.pocket_cards = player_cards
    #     self.best_five = lst_of_triples
        #self.kickers = kickers
        hand_name = "Three of a Kind"
    #     possible_kickers = [x for x in player_cards_values if x not in lst_of_triples]

    #     if len(possible_kickers)>0:
    #         self.kickers = possible_kickers
    #     else:
    #         self.kickers = []

    elif two_pair:

        hand_value =  3
    #     self.pocket_cards = player_cards
    #     self.best_five = lst_of_pairs 
        #self.kickers = kickers
        hand_name = "Two Pair"
        #possible_kickers = [x for x in player_cards_values if x not in lst_of_pairs]
        #possible_kickers = list(set(lst_of_pairs) - set(player_cards_values))

    #     if len(possible_kickers)>0:
    #         self.kickers = possible_kickers
    #     else:
    #         self.kickers = []

    elif (one_pair):

        hand_value =  2
    #     self.pocket_cards = player_cards
    #     self.best_five = lst_of_pairs
    #     #self.kickers = kickers
        hand_name = "Pair"

    #     possible_kickers = [x for x in player_cards_values if x not in lst_of_pairs]

    #     if len(possible_kickers)>0:
    #         self.kickers = sorted(possible_kickers)
    #     else:
    #         self.kickers = []

    else:

        hand_value =  1
    #     self.pocket_cards = player_cards
    #     self.best_five = max(sorted_values)
        #self.kickers = kickers
        hand_name = "High Card"
        #possible_kickers = [x for x in player_cards_values if x != max(sorted_values)]

    #     if len(possible_kickers)>0:
    #         self.kickers = so
    
#     if three_of_a_kind:
#         print(cards)
        
#     if 4 in pairs_matching.values():
#         print(cards)

    return hand_value, hand_name




def print_game(num_player):
    pocket, flop, turn, river, players = deal_play_game(deck, num_player)
    print("Player 1 Cards")
    print(''.join(map(str,pocket[0])),''.join(map(str,pocket[1])))
    time.sleep(3)
    print('')
    print('Flop')
    print(''.join(map(str,flop[0])),''.join(map(str,flop[1])), ''.join(map(str,flop[2])))
    time.sleep(1)
    print('Turn')
    print(''.join(map(str,turn[0])))
    time.sleep(1)
    print('River')
    print(''.join(map(str,river[0])))
    results = get_result_game(pocket[0],pocket[1],flop[0],flop[1],flop[2],turn[0],river[0])
    print(results)
    time.sleep(2)
    print('')
    print("Opponent Hands:")
    for i in range(len(players)):
        print(''.join(map(str,players[i][0])),''.join(map(str,players[i][1])))

    return "Game End"


if __name__ == '__main__':
    num_player = 6
    print_game(num_player)
