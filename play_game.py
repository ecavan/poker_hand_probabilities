import random
import numpy as np
from collections import Counter
import pandas as pd
import itertools
import time

### requires user to specify num_players ####

## add win or lose ###

colors = ['h', 'd', 's', 'c']      
deck = [(value, color) for value in list(range(2, 15)) for color in colors]

def deal_play_game(deck, num_player):

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
    
    cards = [c1,c2,c3,c4,c5,c6,c7]
    hand_cards = [c1,c2]
    #print(cards)
    values = []
    suits = []

    for i in range(len(cards)):

        values.append(cards[i][0])
        suits.append(cards[i][1])


    num_matching = dict(Counter(suits))
    pairs_matching = dict(Counter(values))

    lst_of_pairs = [key for key, val in pairs_matching.items() if val == 2]
    lst_of_triples = [key for key, val in pairs_matching.items() if val == 3]
    lst_of_quads = [key for key, val in pairs_matching.items() if val == 4]

    sorted_values = list(set(sorted(list(map(int, values)))))
    
    if all(elem in sorted_values for elem in [2,3,4,5,14]):

        low_ball_straight = True

    else:

        low_ball_straight = False

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
                straight_cards = [0]
                
        except:
            is_straight = False
            straight_cards = [0]

    else:

        is_straight = False
        straight_cards = [0]
    #print(is_straight,is_flush)
    #print(is_flush)
    
    if (is_straight) & (is_flush):
        if straight_indices == flush_indices:

            is_straight_flush = True
        else:
            is_straight_flush = False

    else:

        is_straight_flush = False

    if (max(straight_cards) == 14) & ((is_straight) & (is_flush)):

        hand_value =  10
        hand_name = "Royal Flush"
        high_card = 14
        kicker = []

    elif ((is_straight) & (is_flush))|((low_ball_straight) & (is_flush)):

        hand_value =  9
        
        if low_ball_straight:
            high_card = 5
        else:
            high_card = max(straight_cards)

        kicker = []
        hand_name = "Straight Flush"

    elif 4 in pairs_matching.values():

        hand_value =  8
        high_card = lst_of_quads[0]
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        try:
            kicker = max([i for i in hand_card_values if i != high_card])
        except:
            kicker = []
        hand_name = "Four of a Kind"

    elif (three_of_a_kind) & (len(lst_of_pairs)>0):
        
        ### additional logic for when high card is a list ####

        hand_value =  7
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        
        high_card = [max(lst_of_triples),max(lst_of_pairs)]
        kicker = []
        hand_name = "Full House"

    elif is_flush:

        hand_value =  6
        kicker = []
        high_card = max(flush_cards)
        hand_name = "Flush"

    elif (is_straight)|(low_ball_straight):

        hand_value =  5
        
        if low_ball_straight:
            high_card = 5
        else:
            high_card = max(straight_cards)
            
        kicker = []
        hand_name = "Straight"

    elif (three_of_a_kind):

        hand_value =  4
        high_card = max(lst_of_triples)
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        kicker = [i for i in hand_card_values if i != high_card]

        hand_name = "Three of a Kind"

    elif two_pair:

        hand_value =  3
        high_pair = max(lst_of_pairs)
        second_high_par = max([i for i in lst_of_pairs if  i!=high_pair])
        high_card = [high_pair,second_high_par]
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        kicker = [i for i in hand_card_values if i not in high_card]
        hand_name = "Two Pair"

    elif (one_pair):

        hand_value =  2
        hand_name = "Pair"
        
        high_pair = max(lst_of_pairs)
        #second_high_par = max([i for i in lst_of_pairs if  i!=high_pair])
        high_card = high_pair
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        kicker = [i for i in hand_card_values if i != high_card]
        
    else:

        hand_value =  1
        hand_name = "High Card"
        
        high_card = max(values)
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        kicker = [i for i in hand_card_values if i != high_card]

    return hand_value, hand_name, high_card, kicker



def print_game(num_player):
    pocket, flop, turn, river, players = deal_play_game(deck, num_player)
    #print("Player 1 Cards")
    print('')
    print(''.join(map(str,pocket[0])),''.join(map(str,pocket[1])))
    time.sleep(1)
    print('')
    print('Community Cards')
    print(''.join(map(str,flop[0])),''.join(map(str,flop[1])), ''.join(map(str,flop[2])), ''.join(map(str,turn[0])), ''.join(map(str,river[0])))

    results_player = get_result_game(pocket[0],pocket[1],flop[0],flop[1],flop[2],turn[0],river[0])
    #print('')
    #print(results[1] + ' ' + str(results[2]))
    time.sleep(1)
    results_dict = []
    print('')
    print("Opponent Hands:")
    for i in range(len(players)):
        results = get_result_game(players[i][0],players[i][1],flop[0],flop[1],flop[2],turn[0],river[0])
        print(''.join(map(str,players[i][0])),''.join(map(str,players[i][1])) + ' |', end=' ')
        results_dict.append(results)
        #print(results[1] + ' ' + str(results[2]))
    #results_dict.append(results_player)

    # for i in range(len(players)):
    #     if results_dict[-1][0] >
    opp = max(results_dict,key=lambda item:item[0])

    #print(results_dict)
    print('')
    print('')
    print('Hand Results')
    print(f"You had {results_player[1]} vs Top Opponent {opp[1]}")
    print('')
    #### logic to output win/lose, your hand vs top opponent ###
    # if results_player[0] < opp[0]:
    #     print('Lose')
    # elif results_player[0] > opp[0]:
    #     print("Win")
    # else:
    #     try:
    #         if int(results_player[2]) > int(opp[2]):
    #             print('Win')
    #         elif int(results_player[2]) < int(opp[2]):
    #             print('Lose')
    #         else:
    #             if int(results_player[3][0]) > int(opp[3][0]):
    #                 print("Win")
    #             elif int(results_player[3][0]) < int(opp[3][0]):
    #                 print('Lose')
    #             else:
    #                 print("Split")
    #     except:
    #         print('Split')




    return "End of Hand"


if __name__ == '__main__':
    num_player = 6
    print_game(num_player)
