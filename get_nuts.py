import random
import numpy as np
from collections import Counter
import pandas as pd
import itertools
import time

## add win or lose ###

colors = ['h', 'd', 's', 'c']      
deck = [(value, color) for value in list(range(2, 15)) for color in colors]

