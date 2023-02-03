import random
import numpy as np
from collections import Counter
import pandas as pd
import itertools
import time

### doesn't require user to specify num_players ####

colors = ['h', 'd', 's', 'c']      
deck = [(value, color) for value in list(range(2, 15)) for color in colors]

def get_community_cards(deck):

    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)

    rng = np.random.default_rng()
    
    ### 3 burn cards ####
    
    cards = rng.choice(deck, size=8, replace=False)

    print('')
    print('Burn Cards')
    print(''.join(map(str,cards[0])), ''.join(map(str,cards[4])), ''.join(map(str,cards[6])))

    flop = cards[1:4]
    turn = cards[5:6]
    river = cards[7:8]
    
    cards2 = [list(flop[0]), list(flop[1]), list(flop[2]),list(turn[0]), list(river[0])]
    
    for element in cards2:
        element[0]=int(element[0])
    
    return cards2


def get_result_nuts(c1,c2,c3,c4,c5,c6,c7):
    
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
            straight_cards = [0]

    else:

        is_straight_flush = False
        straight_cards = [0]

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

def get_nuts(deck):

    face_cards = get_community_cards(deck)
    print('')
    print('Community Cards')
    print(''.join(map(str,face_cards[0])),''.join(map(str,face_cards[1])),''.join(map(str,face_cards[2])),''.join(map(str,face_cards[3])),''.join(map(str,face_cards[4])) )
    #print(face_cards)
    print('')
    #print('')

    for i in face_cards:
        deck.remove(tuple(i))

    all_hand_combs = list(itertools.combinations(deck, 2))

    hand_results = {"Cards":[], "Hand Name":[], "Hand Value":[], "High Card":[], "Kicker":[]}

    for i in range(len(all_hand_combs)):
        
        results = get_result_nuts(list(all_hand_combs[i][0]), list(all_hand_combs[i][1]),face_cards[0], face_cards[1],face_cards[2],face_cards[3],face_cards[4])
        #results_list.append(results[1])

        to_append = ''.join(map(str,all_hand_combs[i][0]))  + ' ' + ''.join(map(str,all_hand_combs[i][1]))
        
        hand_results["Cards"].append(to_append)
        hand_results["Hand Name"].append(results[1])
        hand_results["Hand Value"].append(results[0])
        hand_results["High Card"].append(results[2])
        hand_results["Kicker"].append(results[3])


    hand_df = pd.DataFrame(hand_results)
    hand_df["Frequency %"] = 100*hand_df.groupby("Hand Name")["Cards"].transform('nunique')/1081
    
    try:
    
        hand_df = pd.concat([hand_df, hand_df["High Card"].apply(pd.Series)], axis=1)

        hand_df.columns = ['Best Hand', 'Hand Name', 'Hand Value', 'drop', 'Kicker',
        'Frequency %', 'High Card1', "High Card2"]

        hand_df = hand_df.drop('drop', axis=1)

        hand_df['High Card2'] = hand_df['High Card2'].fillna(hand_df['High Card1'])

        hand_df = hand_df.sort_values(["Hand Value", 'High Card1', 'High Card2'], ascending = [False, False, False])
        hand_df = hand_df.drop_duplicates('Hand Name')

        hand_df = hand_df[['Best Hand', 'Hand Name', 'Hand Value','Frequency %']].reset_index(drop=True)
        hand_df.index = hand_df.index+1
        print(hand_df)
        print('')

    except:
        print('')
        print(hand_df)
    return hand_df

if __name__ == '__main__':
    #num_player = 6
    get_nuts(deck)