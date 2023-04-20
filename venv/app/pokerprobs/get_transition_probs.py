import random
import numpy as np
from collections import Counter
import pandas as pd
import itertools
import warnings
warnings.filterwarnings("ignore")

colors = ['h', 'd', 's', 'c']      
deck = [(value, color) for value in list(range(2, 15)) for color in colors]

def get_result_probs(c1,c2,c3,c4,c5,c6 = 'Opt',c7 = 'Opt'):
    
    if (c6 == 'Opt')&(c7=='Opt'):
        cards = [c1,c2,c3,c4,c5]
        
    elif (c6!='Opt')&(c7=='Opt'):
        cards = [c1,c2,c3,c4,c5,c6]
        
    else:
        cards = [c1,c2,c3,c4,c5, c6, c7]
    
    
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
        flush_cards = [int(values[i]) for i in range(len(values)) if suits[i] == flush_suit]
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

    elif (len(lst_of_triples) == 1) & (len(lst_of_pairs) > 0):
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

#     if (max(straight_cards) == 14) & ((is_straight) & (is_flush)):

#         hand_value =  10
#         hand_name = "Royal Flush"
#         high_card = 14
#         high_card2 = 0
#         kicker = []

    if ((is_straight) & (is_flush))|((low_ball_straight) & (is_flush)):

        hand_value =  9
        
        if low_ball_straight:
            high_card = 5
            high_card2 = 15
            hand_name = "Straight Flush"
        else:
            high_card = max(straight_cards)
            high_card2 = sum(straight_cards)
            hand_name = "Straight Flush"

        kicker = []
        #hand_name = "Straight Flush"

    elif 4 in pairs_matching.values():

        hand_value =  8
        high_card = lst_of_quads[0]
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        #high_card2 = max([i for i in hand_card_values if i != high_card])
        try:
            kicker = max([i for i in hand_card_values if i != high_card])
            high_card2 = max([i for i in hand_card_values if i != high_card])
        except:
            high_card2 = max([i for i in hand_card_values])
            kicker = []
        hand_name = "Four of a Kind"

    elif (three_of_a_kind) & (len(lst_of_pairs)>0):
        
        ### additional logic for when high card is a list ####

        hand_value =  7
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        
        high_card = max(lst_of_triples) 
        high_card2 = max(lst_of_pairs) 
        kicker = []
        hand_name = "Full House"

    elif is_flush:

        hand_value =  6
        kicker = []
        #print(flush_cards)
        high_card = max(flush_cards)
        high_card2 = sum(flush_cards)
        hand_name = "Flush"

    elif (is_straight)|(low_ball_straight):

        hand_value =  5
        
        if low_ball_straight:
            high_card = 5
            high_card2 = 15
            hand_name = "Straight"
        else:
            high_card = max(straight_cards)
            high_card2 = sum(straight_cards)
            hand_name = "Straight"
            
        kicker = []
        #hand_name = "Straight"

    elif (three_of_a_kind):

        hand_value =  4
        high_card = max(lst_of_triples)
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        
        try:
            kicker = [i for i in hand_card_values if i != high_card]

            high_card2 = max([i for i in hand_card_values if i != high_card])
        except:
            #print("pair")
            #print(high_card, hand_card_values)
            high_card2 = max([i for i in hand_card_values])
            kicker = 0
            pass

        hand_name = "Three of a Kind"

    elif two_pair:

        hand_value =  3
        high_pair = max(lst_of_pairs)
        second_high_par = max([i for i in lst_of_pairs if  i!=high_pair])
        high_card = high_pair
        high_card2 = second_high_par
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        kicker = [i for i in hand_card_values if i != high_card]
        hand_name = "Two Pair"

    elif (one_pair):

        hand_value =  2
        hand_name = "Pair"
        
        high_pair = max(lst_of_pairs)
        
        #second_high_par = max([i for i in lst_of_pairs if  i!=high_pair])
        high_card = high_pair
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        try:
            kicker = [i for i in hand_card_values if i != high_card]

            high_card2 = max([i for i in hand_card_values if i != high_card])
        except:
            #print("pair")
            #print(high_card, hand_card_values)
            high_card2 = max([i for i in hand_card_values])
            kicker = 0
            pass
        
    else:

        hand_value =  1
        hand_name = "High Card"
        #print(values)
        high_card = max(values)
        hand_card_values = [hand_cards[0][0], hand_cards[1][0]]
        try:
            #print("High Card")
            kicker = [i for i in hand_card_values if i != high_card]

            high_card2 = max([i for i in hand_card_values if i != high_card])
        except:
            #print(high_card, hand_card_values)
            high_card2 = 0
            kicker = 0
            pass
        

    return hand_value, hand_name, high_card, high_card2, kicker, hand_cards



def deal_new(deck, num_player, remove_cards):

    deck.remove(remove_cards[0])
    deck.remove(remove_cards[1])

    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)

    rng = np.random.default_rng()
    
    cards = rng.choice(deck, size=2*(num_player-1) + 8, replace=False)
    community_cards = cards[2*(num_player-1):]
    
    flop = [community_cards[1], community_cards[2], community_cards[3]]
    turn = community_cards[5]
    river = community_cards[7]
    
    players = []

    for i in range(num_player-1):
        #print(i)
        players.append((cards[i], cards[i + (num_player-1)]))
        
    return players, flop, turn, river

def get_transition_probs(num_player, hand, num_sims = 1000):

    card1 = hand[0]
    card2 = hand[1]

    remove_cards = []
    
    for i in [card1, card2]:

        if len(i) > 2:
            temp = (int(i[0:2]), i[-1])
        else:
            temp = (int(i[0]), i[1])
            
        remove_cards.append(temp)

    results_list = []
    
    result_hand = {
        "flop":[],
        "turn":[],
        "river":[]
    }
    
    result_hand_opp = []
    
    results_win_op = {
        "High Card":[],
        "Pair":[],
        "Two Pair":[],
        "Three of a Kind":[],
        "Straight":[],
        "Straight (Lowball)":[],
        "Flush":[],
        "Full House":[],
        "Four of a Kind":[],
        "Straight Flush":[],
        "Straight Flush (Lowball)":[],
        "Royal Flush":[]
    }


    for i in range(num_sims):

        colors = ['h', 'd', 's', 'c']      
        deck = [(value, color) for value in list(range(2, 15)) for color in colors]

        players, flop, turn, river = deal_new(deck, num_player, remove_cards)
        
        cards = [flop, turn, river]
        #print(list(cards[0][0]), list(cards[0][1]), list(cards[0][2]), list(cards[1][0]), list(cards[2][0]))
        #cards2 = [list(cards[0][0]), list(cards[0][1]), list(cards[0][2]), list(cards[1][0]), list(cards[2][0])]
        
        cards2 = []
        
        for i in [flop[0], flop[1], flop[2], turn, river]:

            if len(i) > 2:
                temp = (int(i[0:2]), i[-1])
            else:
                temp = (int(i[0]), i[1])

            cards2.append(temp)
            
        #print(cards2)

        #results_player = get_result_nuts(list(remove_cards[0]), list(remove_cards[1]),cards2[0], cards2[1],cards2[2],cards2[3],cards2[4])
        
        results_player1 = get_result_probs(list(remove_cards[0]), list(remove_cards[1]),cards2[0], cards2[1],cards2[2],'Opt','Opt')
        #print(results_player)
        results_player2 = get_result_probs(list(remove_cards[0]), list(remove_cards[1]),cards2[0], cards2[1],cards2[2],cards2[3],'Opt')
        #print(results_player)
        results_player3 = get_result_probs(list(remove_cards[0]), list(remove_cards[1]),cards2[0], cards2[1],cards2[2],cards2[3],cards2[4])
        #print(results_player)
        #results_list.append(results_player)
        
        result_hand['flop'].append(results_player1[1])
        result_hand['turn'].append(results_player2[1])
        result_hand['river'].append(results_player3[1])

    temp = pd.DataFrame(result_hand)
    
    return temp


def get_transition_matrix(temp):
    
    transition_counts = temp.groupby(['flop', 'turn', 'river']).size().reset_index(name='count')

    # Compute the total counts for each starting state
    state_counts = temp.groupby(['flop']).size().reset_index(name='total_count')

    # Merge the transition and state counts together
    transition_probabilities = pd.merge(transition_counts, state_counts, on='flop')

    # Compute the transition probabilities
    transition_probabilities['probability'] = transition_probabilities['count'] / transition_probabilities['total_count']

    # View the transition probabilities
    transition_probabilities = transition_probabilities.drop_duplicates(['flop', 'river'])
    matrix = transition_probabilities.pivot(index='flop', columns='river', values='probability')

    # Fill any missing transition probabilities with zeros
    matrix = matrix.fillna(0)

    # Rename the rows and columns to match the state names
    matrix = matrix.rename_axis(None, axis=0).rename_axis(None, axis=1)
    
    max_state_len = max(len(state) for state in matrix.columns)
    padding = max_state_len -2  # Add four spaces to account for "-->" and "probability:"

    transition_probabilities_str = 'Transition probabilities:\n'
    
    counter = 0
    
    for i, row_state in enumerate(matrix.index):
        for j, col_state in enumerate(matrix.columns):
            prob = matrix.iloc[i, j]
            if (prob > 0.01)&(prob <1):
                padded_row_state = row_state.ljust(padding)
                padded_col_state = col_state.ljust(padding)
                transition_probabilities_str += f"{padded_row_state} ---> {padded_col_state} {prob:.2f}"
                #print(''
                counter += 1
                if counter == 3:
                    transition_probabilities_str += '\n'
                    counter = 0
                else:
                    transition_probabilities_str += '\n'
                    
    return transition_probabilities_str
