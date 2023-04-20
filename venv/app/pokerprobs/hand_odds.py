import random
import numpy as np
from collections import Counter
import pandas as pd
import itertools
import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

colors = ['h', 'd', 's', 'c']      
deck = [(value, color) for value in list(range(2, 15)) for color in colors]

### add win % ###

def get_max_tuples(tuples_list, index):
    max_val = max(t[index] for t in tuples_list)
    return [t for t in tuples_list if t[index] == max_val]

def get_result_hand(c1,c2,c3,c4,c5,c6,c7):
    
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

def deal(deck, num_player,num_players_in_hand, remove_cards):

    deck.remove(remove_cards[0])
    deck.remove(remove_cards[1])

    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)
    random.shuffle(deck)

    rng = np.random.default_rng()
    
    cards = rng.choice(deck, size=2*(num_player-1) + 8, replace=False)

    player_cards = cards[0:2*(num_player-1)]
    face_cards = cards[2*(num_player-1):]
    
    #pocket = [player_cards[0], player_cards[1]]

    flop = face_cards[1:4]
    turn = face_cards[5:6]
    river = face_cards[7:8]

    players = []

    for i in range(num_player-1):
        players.append([player_cards[i], player_cards[i + (num_player-1)]])


    player_data = {
        "index":[],
        "deltas":[],
        "is_suited":[],
        "total":[],
        "is_pocket":[]
    }
    #print(players)
    
    for j in range(len(players)):
        player_data["index"].append(j)
        player_data["deltas"].append(abs(int(players[j][0][0]) - int(players[j][1][0])))
        player_data["is_suited"].append(players[j][0][1] == players[j][1][1])
        player_data["total"].append(int(players[j][0][0]) + int(players[j][1][0]))
        player_data["is_pocket"].append(players[j][0][0] == players[j][1][0])
        
    #print(player_data)
    
    player_df = pd.DataFrame(player_data)
    player_df["is_pocket"] = player_df["is_pocket"].astype(int)
    player_df["is_suited"] = player_df["is_suited"].astype(int)
    player_df['pts'] = (14 - player_df['deltas']) + (player_df['total']/5) + 5*player_df['is_pocket'] + 3*player_df['is_suited']
    player_df = player_df.sort_values('pts', ascending = False)
    
    player_list = player_df['index'].to_list()
    new_players = []
    for i in range(num_players_in_hand):
        new_players.append(players[player_list[i]])

    return flop, turn, river, new_players


def get_hand_odds(num_player,num_players_in_hand, hand, num_sims = 2000):

    card1 = hand[0]
    card2 = hand[1]

    if len(card1) > 2:
        card1 = (int(card1[0:2]), card1[-1])
    else:
        card1 = (int(card1[0]), card1[1])

    if len(card2) > 2:
        card2 = (int(card2[0:2]), card2[-1])
    else:
        card2 = (int(card2[0]), card2[1])

    remove_cards = [card1, card2]

    #results_dict = {}
    results_list = []
    
    result_hand = []
    
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

        flop, turn, river, players = deal(deck, num_player,num_players_in_hand, remove_cards)
        
        cards = [flop, turn, river]
        cards2 = [list(cards[0][0]), list(cards[0][1]), list(cards[0][2]), list(cards[1][0]), list(cards[2][0])]
    
        for element in cards2:
            element[0]=int(element[0])

        results_player = get_result_hand(list(remove_cards[0]), list(remove_cards[1]),cards2[0], cards2[1],cards2[2],cards2[3],cards2[4])
        #results_list.append(results_player)
        result_hand.append(results_player[1])
        
        results_dict = []
        #print(players)
        new_players = []
        
        players = [list(i) for i in players]
        
        for i in players:
            if int(i[0][0]) > int(i[1][0]):
                new_players.append(i)
            else:
                temp = [(i[1][0], i[1][1]), (i[0][0], i[0][1])]
                new_players.append(temp)

        players2 = sorted(new_players, key=lambda element: (int(element[0][0]), int(element[1][0])), reverse=True)

        players2_no_fold = players2[0:num_players_in_hand]

        op_hands = players2_no_fold
        for j in range(len(op_hands)):
            results = get_result_hand(op_hands[j][0],op_hands[j][1],flop[0],flop[1],flop[2],turn[0],river[0])
            #print(''.join(map(str,players[i][0])),''.join(map(str,players[i][1])) + ' |', end=' ')
            results_dict.append(results)
            

        opp = get_max_tuples(results_dict, 0)
        #print(len(opp))
        #print(opp)
        
        if len(opp) > 1:
            opp = get_max_tuples(opp, 2)
            
            if len(opp) > 1:
                opp = get_max_tuples(opp, 3)
            
        
        if opp[0][0] > results_player[0]:
            results_list.append(0)
            results_win_op[opp[0][1]].append(results_player[1])
        
        elif opp[0][0] == results_player[0]:
            #print(opp)
            #print(results_player)
            if int(opp[0][2]) > results_player[2]:
                results_list.append(0)
                results_win_op[opp[0][1]].append(results_player[1])
            elif opp[0][2] == results_player[2]:
                if int(opp[0][3]) > results_player[3]:
                    results_list.append(0)
                    results_win_op[opp[0][1]].append(results_player[1])
                elif opp[0][3] == results_player[3]:
                    results_list.append(1)
                else:
                    results_list.append(1)
                    results_win_op[results_player[1]].append(opp[0][1])       
            else:
                results_list.append(1)
                results_win_op[results_player[1]].append(opp[0][1])
        else:
            results_list.append(1)
            results_win_op[results_player[1]].append(opp[0][1])

            
    d = dict(Counter(result_hand))
    k={i:100*(j/num_sims) for i,j in d.items()}
    df = pd.DataFrame(k, index = [0]).T.reset_index()
    df.columns = ['Hand', 'Probability']
    df = df.sort_values('Probability', ascending = False)
    df = df.reset_index(drop = True)
    
    result_df = pd.DataFrame()
    result_df2 = pd.DataFrame()
    
    for k,v in results_win_op.items():
        try:
            d3 = dict(Counter(v))
            k3={i:100*(j/len(v)) for i,j in d3.items()}
            df3 = pd.DataFrame(k3, index = [0]).T.reset_index()
            df3.columns = ['Lose to', '% Lose']
            df3['Player Hand'] = k
            df3 = df3.sort_values('% Lose', ascending = False)
            #df3 = df3.reset_index(drop = True)
            result_df = pd.concat([result_df, df3], axis = 0)
        except: 
            print(k)
            
    df2 = df.merge(result_df, left_on = ['Hand'], right_on = ['Player Hand'])
    df2['adjusted_prob2'] = (df2['Probability']/100)*df2['% Lose']/100
    
    response = df2.groupby('Hand')['adjusted_prob2'].sum().round(3).to_dict()

    win_pct = sum(results_list)/len(results_list)
    
    return win_pct, response
# if __name__ == '__main__':
#     #print(5)
#     num_player = 6
#     results = get_hand_odds(num_player, ['2h','2c'], num_sims = 100)
#     print(results)