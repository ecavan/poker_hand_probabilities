# Python Poker Tools

To install:
```
pip install pokerprobs
```
(or download the repo and run pip install -e .)

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
This function asks you for a starting hand (2 cards) and outputs the probability of each 5-card result using monte carlo simulations. The default number of sims is 10k (you can run the function as  pokerprobs.get_hand_odds(num_players) ); but in my experience you may want to set num_sims to be between 100k-300k for the best result for the rarer hand combinations. For example, here I've input the Doyle Brunson special:
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




