# Python Poker Tools

[![Screen-Shot-2023-02-03-at-4-19-47-PM.png -thumbnail](https://i.postimg.cc/qBCxmFxx/Screen-Shot-2023-02-03-at-4-19-47-PM.png)](https://postimg.cc/0rPSjc3z)

Image from https://www.888poker.com/magazine/how-to-play-poker/hands.

To install:
```
pip install pokerprobs
```
(or download the repo, cd into it and run pip install -e .; if not try the same with pip3)

The cards are input and output as, for example, 12h,9d,3c; where h,d,c,s represent the suits hearts, diamonds, clubs and spades and 11,12,13,14 represent the jack, queen, king and ace respectively. There are three modules. After installing you can run:

```

>>> import pokerprobs 
>>> pokerprobs.print_game(num_players)
```

This outputs a mock hand against specified number of players. It doesn't encoporate betting, but you can think about what you would have done given the flop, turn, ect. The output for a 6 player hand I ran for ex:

```
8c 11c

Community Cards
10s 12d 14c 7h 6d

Opponent Hands:
8c 3c | 11c 5s | 12h 5c | 9d 3s | 2c 7c | 

Hand Results
You had High Card vs Top Opponent Pair
```
You can also run:
```
>>> import pokerprobs 
>>> pokerprobs.get_nuts()
```
example output:
```
Burn Cards
5s 11c 14h

Community Cards
14s 14c 2h 9h 13h

  Best Hand        Hand Name  Hand Value  Frequency %
1   14h 14d   Four of a Kind           8     0.092507
2   13s 14h       Full House           7     2.497687
3    6h 14h            Flush           6     4.162812
4   10s 14h  Three of a Kind           4     5.827937
5    9c 13s         Two Pair           3    37.465310
6   10s 11d             Pair           2    49.953747
```
This function returns a (right now random) set of community cards, and iterates through all combinations of starting hands to give you the best 5-card results and the probability that they will occur. 

Finally, 
```
>>> import pokerprobs 
>>> pokerprobs.get_hand_odds(num_players, num_sims)
```
This function asks you for a starting hand (2 cards) and outputs the probability of each 5-card result using monte carlo simulations. The default number of sims is 10k (you can run the function as  pokerprobs.get_hand_odds(num_players)); but in my experience you may want to set num_sims to be between 100k-300k for the best result for the rarer hand combinations. For example, here I've input the Doyle Brunson special:
```
First Card: 10s
Second Card: 2c

              Hand  Probability
0   Four of a Kind         0.13
1   Straight Flush         0.13
2            Flush         1.84
3       Full House         2.01
4         Straight         3.25
5  Three of a Kind         4.28
6        High Card        20.26
7         Two Pair        22.00
8             Pair        46.10
```

As an aside, this example compares the returned probabilities when playing with pocket kings

```
>>> pokerprobs.get_hand_odds(6)
First Card: 13c
Second Card: 13d

              Hand  Probability
0   Straight Flush         0.04
1   Four of a Kind         0.76
2         Straight         1.03
3            Flush         1.83
4       Full House         8.30
5  Three of a Kind        11.93
6             Pair        36.17
7         Two Pair        39.94

>>> pokerprobs.get_hand_odds(6,500000)
First Card: 13c
Second Card: 13d

              Hand  Probability
0      Royal Flush       0.0008
1   Straight Flush       0.0370
2   Four of a Kind       0.8388
3         Straight       1.2202
4            Flush       1.9514
5       Full House       8.3452
6  Three of a Kind      11.9694
7             Pair      36.0032
8         Two Pair      39.6340
```

There is an obvious trade off in the time it takes for the function to execute.

If you would like to specify your own community cards (ortherwise it will default to random):
 
```
>>> import pokerprobs
>>> pokerprobs.get_nuts(False)
Community Cards (Spaced): 12s 10h 5d 6c 5s
  Best Hand        Hand Name  Hand Value  Frequency %
1     5h 5c   Four of a Kind           8     0.092507
2   12h 12d       Full House           7     2.497687
3     2h 5h  Three of a Kind           4     6.660500
4   14h 14d         Two Pair           3    37.465310
5     2h 3h             Pair           2    53.283996
```
As I get more time I'd like to expand the functionality to the get_nuts (just as a disclaimer record, the "Nuts" is the best hand in poker) and get_hand_odds functions to allow for simulations after flop, turn, river.


Feel free to email me @ eli_cavan@live.ca or DM on twitter @cavan_elijah for comments/requests. 
