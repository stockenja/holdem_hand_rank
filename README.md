# holdem_hand_rank

This is project aims to rank each starting hand's strength in Texas Hold'em. We define the hank rank based on the probability of winning assuming all players are playing (i.e. no hand range).

## Setup

Set up virtualenv for Python 3:

```
python3.7 -m venv hhr_env
```

Start virtualenv:

```
source hhr_env/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

## Running the code

If you have not start virtualenv, start it:

```
source hhr_env/bin/activate
```


Next, simply run:

```
python rank_holdem_hands.py
```


## About the calculation of winning odds
The odds of winning for each hand is calculated using Edge.poker's [poker odds calculator](https://app.edge.poker) engine. Due to proprietary nature of the engine, we cannot release the source code that calculates the probability. However, from a pseudo code perspective, it looks something like this:

```
winning_odds = Engine.estimateOdds(hand, numOfPlayers, numOfSimulations)
```

You might noticed that existence of `numOfSimulations` variable. This is required because the engine is based on Monte Carlo simulation. The number simulation done for each hand is 10,000 currently.

The computed winning probability is stored in `handWinRate_6p.csv` and `handWinRate_9p.csv` (under the `data` folder) for the 6 players and 9 players game respectively.

If you have more questions about calculating the winning odds, you can visit the following page:

<https://app.edge.poker/faqs>


## Hand Strength Ranking

With the given winning odds, the algorithm to calculate the rank is roughly as follow:

1. Transform hands into one of the following categories: (i) pairs, (ii) same suit and (iii) off-suit.
2. Add the transformed hand into a dictionary as a key and append the probability into a list
3. Repeat steps 1 to 2 for all hands
4. Go through each keys in the dictionary and calculate the average probability
5. Finally, transform dictionary into tuple and sort it based on the probability of winning in reverse order.

The results can be found in the folder `results\`.


# Notes

In the result file `hand_rank.csv`, all ranks are sorted based on the 6 players table's winning odds. You may noticed that, if the ranks were sorted by 9 players winning odds, the sorting order would be slightly different. This is due to 2 reasons:

1. Insufficient number of simulations for the 9 player table
2. Winning odds of hands are very close to each other in the 9 player table

A future work would be to increase the number of simulation to get less volatile results. Nonetheless, the results here is good estimate of the starting hand ranking.
