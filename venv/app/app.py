from shiny import App,  reactive, render, ui
import pokerprobs
from collections import Counter
import pandas as pd
import itertools
import random
import numpy as np
import json

#### get transition probabilities #############

colors = ['h', 'd', 's', 'c']      
deck = [(value, color) for value in list(range(2, 15)) for color in colors]
deck_choices = [''.join(map(str, deck[i])) for i in range(len(deck))]

def get_range(deck, suited_option = "Ignore", pocket_pair_option = "Ignore", face_card_option = "Ignore", gap_option = "Ignore"):
    
    all_hand_combs = list(itertools.combinations(deck, 2))
    filtered_data = all_hand_combs
    
    if suited_option != "Ignore":
        if suited_option == "Suited":
            filtered_data = [i for i in filtered_data if i[0][1] == i[1][1]] 
        elif suited_option == "UnSuited":
            filtered_data = [i for i in filtered_data if i[0][1] != i[1][1]] 

    if face_card_option != "Ignore":
        if face_card_option == "0":
            filtered_data = [i for i in filtered_data if int(i[0][0]) < 10]  
        elif face_card_option == "1":
            if suited_option == "UnSuited":
                filtered_data = [(i, j) for i in [i for i in deck if int(i[0]) < 10] for j in [i for i in deck if int(i[0]) >= 10]]
            elif suited_option == "Suited":
                filtered_data = [(i, j) for i in [i for i in deck if int(i[0]) < 10] for j in [i for i in deck if int(i[0]) >= 10]]
                filtered_data = [i for i in filtered_data if i[0][1] == i[1][1]]
            else:
                filtered_data = [(i, j) for i in [i for i in deck if int(i[0]) < 10] for j in [i for i in deck if int(i[0]) >= 10]]   
        else:
            filtered_data = [i for i in filtered_data if int(i[0][0]) >= 10] 
            
    if pocket_pair_option != "Ignore":
        if pocket_pair_option == "Yes":
            if (gap_option == "Ignore"):
                #print('here')
                filtered_data = [i for i in filtered_data if int(i[0][0]) == int(i[1][0])]
            elif (gap_option == "0"):
                filtered_data = [i for i in filtered_data if i[0][0] == i[1][0]]
            else:
                pass
        else:
            pass 
        
    if gap_option != "Ignore":
        if gap_option == '0':
            pass
        elif gap_option == '1 - Gap':
            filtered_data = [i for i in filtered_data if abs(i[0][0] - i[1][0]) == 1]
        elif gap_option == '2 - Gap':
            filtered_data = [i for i in filtered_data if abs(i[0][0] - i[1][0]) == 2]
        elif gap_option == '3 - Gap':
            filtered_data = [i for i in filtered_data if abs(i[0][0] - i[1][0]) == 3]
        else:
            filtered_data = [i for i in filtered_data if abs(i[0][0] - i[1][0]) > 3]
    if len(filtered_data) < 1:
        filtered_data = list(itertools.combinations(deck, 2))
        
    return filtered_data

def get_random_choice(range_):
    rnd_indices = np.random.choice(len(range_), size=1)[0]
    try:
        hand = range_[rnd_indices]
    except:
        hand = range_[0]
    return hand

def clean_card(hand):
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
    return remove_cards

#### df flops ##

#df_flops = pd.read_csv('flop_ranges.csv')

def get_df_flop(remove_cards):
    suits = ["s", "c", "d", "h"]
    numbers = list(range(2, 15))
    cards = [(num, suit) for num in numbers for suit in suits]

    for x in remove_cards:
        cards.remove(x)

    hand_combos = list(itertools.combinations(cards, 3))

    hand_dict = {}

    for i in hand_combos:
        lst = list(i)
        nums = [x[0] for x in lst]
        suits = [x[1] for x in lst]
        face = [i for i in nums if i > 9]
        num_face = len(face)
        d1 = abs(nums[0] - nums[1])
        d2 = abs(nums[0] - nums[2])
        d3 = abs(nums[1]-nums[2])
        sums = sum(nums)
        nflush = Counter(suits).most_common(1)[0][1]
        is_pared = Counter(nums).most_common(1)[0][1]
        
        temp = [d1,d2,d3,num_face,sums,nflush, is_pared]
        
        hand_dict[i] = temp

    df_flops = pd.DataFrame(hand_dict).T#.reset_index()
    df_flops.columns = [ 'd1', 'd2','d3','num_face','sum', 'nflush','is_pair']

    df_flops['dtot1'] = df_flops['d1'] + df_flops['d2'] + df_flops['d3'] 
    df_flops['dtot2'] = df_flops['d2'] + df_flops['d3'] 

    return df_flops


def get_flop(df_flops, numflush, num_pairs, numface, ngap):
    if numflush != "Ignore":
        if numflush == '2':
            temp = df_flops[df_flops.nflush == 2]
        elif numflush == '0':
            temp = df_flops[df_flops.nflush == 0]
        else:
            temp = df_flops[df_flops.nflush == 3]
    else:
        temp = df_flops

    if num_pairs != "Ignore":
        if num_pairs == 'No':
            temp = temp[temp.is_pair == 1]
        elif num_pairs == 'Yes':
            temp = temp[temp.is_pair == 2]
        else:
            temp = temp[temp.is_pair == 3]

    if numface != "Ignore":
        if numface == "0":
            temp = temp[temp.num_face == 0]
        elif numface == "1":
            temp = temp[temp.num_face == 1]
        elif numface == "2":
            temp = temp[temp.num_face == 2]
        else:
            temp = temp[temp.num_face == 3]

    #"GutShot", "Open Ended"
    if ngap != 'Ignore':
        if ngap ==  "Open Ended":
            temp = temp[(temp.dtot1 < 5)]
        elif ngap ==  "GutShot":
            temp = temp[(temp.dtot1 > 4)&(temp.dtot1 < 10)]

    flops = temp.index.tolist()
    #print(temp.columns)

    rng = np.random.default_rng()

    return rng.choice(flops, 1)[0] 
    
app_ui = ui.page_fluid(
    ui.navset_tab_card(
        ui.nav("Equity Range Calculator", 
            ui.row(
                ui.column(
                    3,
            ui.input_slider("num_players", "Seats at the Table (inclusive)", value=6, min=2, max=11)
                ),
                ui.column(
                    3,
            ui.input_slider("num_players_hands", "Players in Hand (exclusive)", value=3, min=1, max=10),
            )
            ),
            ui.row(
                ui.column(
                    2,
            ui.input_checkbox("show", "Do Not Uncheck", True)
                ),
                ui.column(
                    2,
            ui.panel_conditional(
        "input.show", ui.input_radio_buttons("radio", "Suited? ", ["Select Range", "Select Hand", "Random"])
            )
                )
            ),
        ui.row(
            ui.column(
            2,
            ui.panel_conditional(
        "input.radio === 'Select Range'",
        ui.input_selectize("radio_suit", "Choose ", ["Ignore","Suited", "UnSuited"]),
            )
            ),
        ui.column(
            2,
            ui.panel_conditional(
        "input.radio === 'Select Range'",
        ui.input_selectize("radio_face", "Face Cards ", ["Ignore","1", "2", "0"]),
            )
        ),
                ui.column(
            2,
            ui.panel_conditional(
                "input.radio === 'Select Range'",
                ui.input_selectize("radio_pocket", "Pocket Pair? ", ["Ignore","No", "Yes"]),
                    ),
                ),
                ui.column(
            2,
            ui.panel_conditional(
                "input.radio === 'Select Range'",
                ui.input_selectize("radio_gap", "Straight Potential? ", ["Ignore","0", "1 - Gap", "2 - Gap", "3 - Gap", '> 3 - Gap'], multiple = False),
                    )
                )
            ),
            ui.panel_conditional("input.radio === 'Select Hand'", 
                    ui.input_selectize("hand_input", "(2) Hole Cards", deck_choices, multiple = True),
                                ),
        "* Note: Ranges default to random. Suited & Pocket pair is invalid. 1 Face card and pocket pair is invalid, ect. *",
                    ui.tags.br(),
                    ui.tags.br(),
                    ui.input_action_button("btn", "Click me"),
                    ui.tags.br(),
                    ui.tags.br(),
                    #ui.output_text("txt"),
                    ui.output_text_verbatim("txt", placeholder=True),
            ui.row(
                ui.column(
                    2,
            ui.input_checkbox("show2", "Do Not Uncheck", True)
                ),
                ui.column(
                    2,
            ui.panel_conditional(
        "input.show2", ui.input_radio_buttons("radio2", "Choose ", ["Select Range", "Choose Flop", "Random"])
            )
                )
            ),
        ui.row(
            ui.column(
            2,
            ui.panel_conditional(
        "input.radio2 === 'Select Range'",
        ui.input_selectize("radio_suit2", "N-Flush ", ["Ignore","0","2", "3"]),
            )
            ),
        ui.column(
            2,
            ui.panel_conditional(
        "input.radio2 === 'Select Range'",
        ui.input_selectize("radio_face2", "Face Cards ", ["Ignore","0", "1", "2", "3"]),
            )
        ),
                ui.column(
            2,
            ui.panel_conditional(
                "input.radio2 === 'Select Range'",
                ui.input_selectize("radio_pocket2", "Is Board Paired? ", ["Ignore","No", "Yes", "Trips"]),
                    ),
                ),
                ui.column(
            2,
            ui.panel_conditional(
                "input.radio2 === 'Select Range'",
                ui.input_selectize("radio_gap2", "Straight Potential? ", ["Ignore", "GutShot", "Open Ended"], multiple = False),
                    )
                )
            ),
            ui.panel_conditional("input.radio2 === 'Choose Flop'", 
                    ui.input_selectize("hand_input2", "(3) Flop Cards", deck_choices, multiple = True),
                                ),
                    "* Note: Invalid ranges are: Board paired + 3-flush.  *",
                    ui.tags.br(),
                    ui.tags.br(),
                    ui.input_action_button("btn2", "Click me"),
                    ui.tags.br(),
                    ui.tags.br(),
                    #ui.output_text("txt"),
                    ui.output_text_verbatim("txt2",placeholder=True)
                    ),
                    ui.nav("Transition Probabilities",
                    
                    ui.row(
                ui.column(
                    3,
            ui.input_slider("num_players3", "Seats at the Table (inclusive)", value=6, min=2, max=11)
                ),
                ui.column(
                    3,
            " "
            )
            ),
            ui.row(
                ui.column(
                    2,
            ui.input_checkbox("show3", "Do Not Uncheck", True)
                ),
                ui.column(
                    2,
            ui.panel_conditional(
        "input.show3", ui.input_radio_buttons("radio3", "Suited? ", ["Select Range", "Select Hand", "Random"])
            )
                )
            ),
        ui.row(
            ui.column(
            2,
            ui.panel_conditional(
        "input.radio3 === 'Select Range'",
        ui.input_selectize("radio_suit3", "Choose ", ["Ignore","Suited", "UnSuited"]),
            )
            ),
        ui.column(
            2,
            ui.panel_conditional(
        "input.radio3 === 'Select Range'",
        ui.input_selectize("radio_face3", "Face Cards ", ["Ignore","1", "2", "0"]),
            )
        ),
                ui.column(
            2,
            ui.panel_conditional(
                "input.radio3 === 'Select Range'",
                ui.input_selectize("radio_pocket3", "Pocket Pair? ", ["Ignore","No", "Yes"]),
                    ),
                ),
                ui.column(
            2,
            ui.panel_conditional(
                "input.radio3 === 'Select Range'",
                ui.input_selectize("radio_gap3", "Straight Potential? ", ["Ignore","0", "1 - Gap", "2 - Gap", "3 - Gap", '> 3 - Gap'], multiple = False),
                    )
                )
            ),
            ui.panel_conditional("input.radio3 === 'Select Hand'", 
                    ui.input_selectize("hand_input3", "(2) Hole Cards", deck_choices, multiple = True),
                                ),
        "* Note: Ranges default to random. Suited & Pocket pair is invalid. 1 Face card and pocket pair is invalid, ect. *",
                    ui.tags.br(),
                    ui.tags.br(),
                    ui.input_action_button("btn3", "Click me"),
                    ui.tags.br(),
                    ui.tags.br(),
                    #ui.output_text("txt"),
                    ui.output_text_verbatim("txt3", placeholder=True)
                    
                    ),
    # "The value of the slider when the button was last clicked:",
    # ui.tags.br(),,
        ui.nav("The Implied Odds Game", 
            "Under Construction",
            ui.tags.br(),
            ui.tags.br(),
            ui.input_action_button("btn4", "Click me"),
            "A Random poker hand: ",
            ui.tags.br(),
            ui.tags.br(),
            ui.output_text_verbatim("txt4", placeholder=True)
        )
    )
)


def server(input, output, session):

    # The @reactive.event() causes the function to run only when input.btn is
    # invalidated.
    @reactive.Effect
    @reactive.event(input.btn)
    def _():
        print(f"You clicked the button!")

    @reactive.Effect
    @reactive.event(input.btn2)
    def _():
        print(f"You clicked the button!2")

    @reactive.Effect
    @reactive.event(input.btn3)
    def _():
        print(f"You clicked the button!3")
        #print(pokerprobs.print_game(6))
        # You can do other things here, like write data to disk.

    # This output updates only when input.btn is invalidated.
    @output
    @render.text
    @reactive.event(input.btn)
    def txt():
        if input.radio() == "Select Hand":
            data, win_pct = pokerprobs.get_hand_odds(input.num_players(),input.num_players_hands(), input.hand_input())
            #response = "Winning Percentage: " + str(win_pct) + str(data)
            string_ = data, win_pct

            string_to_print = f"\n A sample hand is {input.hand_input()} \n Your overall equity is {data} \n \n Preflop Equity breakdown: \n "

            dumps = json.dumps(win_pct, indent = 2, separators=(',', ': '))
            response = string_to_print + dumps
            #print(response)
        elif input.radio() == "Random":
            play_cards = get_range(deck, suited_option = "Ignore", pocket_pair_option = "Ignore", face_card_option = "Ignore", gap_option = "Ignore")
            unclean_hand = get_random_choice(play_cards)
            hand = clean_card(unclean_hand)
            nice_hand = f"{hand[0][0]}{hand[0][1]},{hand[1][0]}{hand[1][1]}"
            #print(unclean_hand, hand)
            data, win_pct = pokerprobs.get_hand_odds(input.num_players(),input.num_players_hands(), hand)
            string_to_print = f"\n A sample hand is {nice_hand} \n Your overall equity is {data} \n \n Preflop Equity breakdown: \n "

            dumps = json.dumps(win_pct, indent = 2, separators=(',', ': '))
            response = string_to_print + dumps
            #print(response)
        elif input.radio() == "Select Range":
            play_cards = get_range(deck, suited_option = input.radio_suit(), pocket_pair_option = input.radio_pocket(), face_card_option =input.radio_face(), gap_option = input.radio_gap())
            unclean_hand = get_random_choice(play_cards)
            hand = clean_card(unclean_hand)
            nice_hand = f"{hand[0][0]}{hand[0][1]},{hand[1][0]}{hand[1][1]}"
            data, win_pct = pokerprobs.get_hand_odds(input.num_players(),input.num_players_hands(), hand)
            string_to_print = f"\n A sample hand is {nice_hand} \n Your overall equity is {data} \n \n Preflop Equity breakdown: \n "

            dumps = json.dumps(win_pct, indent = 2, separators=(',', ': '))
            response = string_to_print + dumps
        else:
            pass

        return response

    @output
    @render.text
    @reactive.event(input.btn2)
    def txt2():

        if (input.radio2() == "Random"):
            play_cards = get_range(deck, suited_option = "Ignore", pocket_pair_option = "Ignore", face_card_option = "Ignore", gap_option = "Ignore") 
            unclean_hand = get_random_choice(play_cards)
            hand = clean_card(unclean_hand)
            nice_hand = f"{hand[0][0]}{hand[0][1]},{hand[1][0]}{hand[1][1]}"
        elif (input.radio() == "Select Range"):
            play_cards = get_range(deck, suited_option = input.radio_suit(), pocket_pair_option = input.radio_pocket(), face_card_option =input.radio_face(), gap_option = input.radio_gap())
            unclean_hand = get_random_choice(play_cards)
            hand = clean_card(unclean_hand)
            nice_hand = f"{hand[0][0]}{hand[0][1]},{hand[1][0]}{hand[1][1]}"
        else:
            play_cards = input.hand_input()
            hand = clean_card(play_cards)
            nice_hand = hand

        #print(input.n())
        if (input.radio2() == "Choose Flop"):
            flop = input.hand_input2()
            nice_flop = flop
            data2, win_pct2 = pokerprobs.get_nuts(input.num_players(),input.num_players_hands(), hand,flop, num_sims = 1000)

            string_to_print2 = f"\n A sample hand is {nice_hand} \n A sample flop is {nice_flop} \n Your new equity is {data2} \n \n Flop Equity breakdown: \n "

            dumps2 = json.dumps(win_pct2, indent = 2, separators=(',', ': '))
            response2 = string_to_print2 + dumps2

        elif input.radio2() == "Random":
            df_flops = get_df_flop(hand)
            flop = get_flop(df_flops, "Ignore", "Ignore", "Ignore", "Ignore")

            nice_flop = f"{flop[0][0]}{flop[0][1]},{flop[1][0]}{flop[1][1]},{flop[2][0]}{flop[2][1]}"
            data2, win_pct2 = pokerprobs.get_nuts(input.num_players(),input.num_players_hands(), hand,flop, num_sims = 1000)

            string_to_print2 = f"\n A sample hand is {nice_hand} \n A sample flop is {nice_flop} \n Your new equity is {data2} \n \n Flop Equity breakdown: \n "

            dumps2 = json.dumps(win_pct2, indent = 2, separators=(',', ': '))
            response2 = string_to_print2 + dumps2

        elif input.radio2() == "Select Range":
            df_flops = get_df_flop(hand)
            flop = get_flop(df_flops, numflush = input.radio_suit2(), num_pairs= input.radio_pocket2(), numface=input.radio_face2(), ngap= input.radio_gap2())
            #flop2 = [eval(i) for i in flop]
            nice_flop = f"{flop[0][0]}{flop[0][1]},{flop[1][0]}{flop[1][1]},{flop[2][0]}{flop[2][1]}"

            data2, win_pct2 = pokerprobs.get_nuts(input.num_players(),input.num_players_hands(), hand,flop, num_sims = 1000)

            string_to_print2 = f"\n A sample hand is {nice_hand} \n A sample flop is {nice_flop} \n Your new equity is {data2} \n \n Flop Equity breakdown: \n "

            dumps2 = json.dumps(win_pct2, indent = 2, separators=(',', ': '))
            response2 = string_to_print2 + dumps2
            #response2 = flop,hand
        else:
            pass

        return response2

    @output
    @render.text
    @reactive.event(input.btn3)
    def txt3():
        #print(input.n())
        if input.radio3() == "Select Hand":
            data = pokerprobs.get_transition_probs(input.num_players3(), input.hand_input3())
            response3 = f"You had {input.hand_input3()} \n" + prob_str

        elif input.radio3() == "Random":
            play_cards3 = get_range(deck, suited_option = "Ignore", pocket_pair_option = "Ignore", face_card_option = "Ignore", gap_option = "Ignore")
            unclean_hand3 = get_random_choice(play_cards3)
            hand3 = clean_card(unclean_hand3)
            nice_hand3 = f"{hand3[0][0]}{hand3[0][1]},{hand3[1][0]}{hand3[1][1]}"

            data = pokerprobs.get_transition_probs(input.num_players3(), hand3)
            prob_str = pokerprobs.get_transition_matrix(data)
            response3 = f"You had {nice_hand3} \n" + prob_str

            #print(response)
        elif input.radio3() == "Select Range":
            play_cards3 = get_range(deck, suited_option = input.radio_suit3(), pocket_pair_option = input.radio_pocket3(), face_card_option =input.radio_face3(), gap_option = input.radio_gap3())
            unclean_hand3 = get_random_choice(play_cards3)
            hand3 = clean_card(unclean_hand3)
            nice_hand3 = f"{hand3[0][0]}{hand3[0][1]},{hand3[1][0]}{hand3[1][1]}"

            data = pokerprobs.get_transition_probs(input.num_players3(), hand3)
            prob_str = pokerprobs.get_transition_matrix(data)
            response3 = f"You had {nice_hand3} \n" + prob_str

        else:
            pass

        return response3

    @output
    @render.text
    @reactive.event(input.btn4)
    def txt4():
        #print(input.n())
        return "Not Ready Yet!"


app = App(app_ui, server)
