## Imports

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Union, Any
from tqdm import tqdm, trange
from itertools import product
from functools import lru_cache

## Constants

DATA_DIR = "data"
CACHE_SIZE = None
NUM_DAYS = 68

def get_full_data() -> pd.DataFrame:
    """
    Gets full experiment data as DataFrame. Sorted first by subject #, then by day.
    Data includes: stored, sold, price
    """

    # Read .csv files
    daily_prices_raw = pd.read_csv(f'{DATA_DIR}/prices.csv')
    stored_raw = pd.read_csv(f'{DATA_DIR}/stored.csv')
    sold_raw = pd.read_csv(f'{DATA_DIR}/sold.csv')

    # These 3 dataframes are structured the same when imported. This code changes the dataframe to a multilevel index dataframe, so that the first-level index is the participant, and the second-level index is the day

    stored = stored_raw.stack()
    stored = pd.DataFrame(stored)
    stored.rename(columns={0:'stored'}, inplace=True)
    #print(stored)

    sold = sold_raw.stack()
    sold = pd.DataFrame(sold)
    sold.rename(columns={0:'sold'}, inplace=True)
    #print(sold)

    daily_prices = daily_prices_raw.stack()
    daily_prices = pd.DataFrame(daily_prices)
    daily_prices.rename(columns={0:'price'}, inplace=True)
    #print(prices)

    ##########

    # This joins the dataframes restructured above into a dataframe called 'participants'
    participants = stored.join(sold, how="outer")
    participants = participants.join(daily_prices, how="outer")

    participants = participants.rename_axis(index=('participant','day')) #renames index levels

    return participants

def std_dev(error: float, n: int) -> float:
    # TODO: Implement this
    raise NotImplementedError

def get_valid_param_ranges(precision: float = 0.001) -> Dict[str, List[float]]:
    """Returns a list of all the valid values for each parameter, given the precision.
    Note that all params ranges are returned, even if the parameter is not free.
    Inputs:
        precision: the amount to increment each value when iterating through all possible values."""
    valid_parameter_ranges: Dict[str, List[float]] = {
        "a": list(np.arange(0, 1 + precision, precision)),
        "b": list(np.arange(0, 1 + precision, precision)),
        "g": list(np.arange(0, 1 + precision, precision)),
        "l": list(np.arange(1, 3.5 + precision, precision)),
        "tw": list(np.arange(0, NUM_DAYS, 1))
    }
    return valid_parameter_ranges

# Get probabilities of each price
prices_probabilities: pd.DataFrame = pd.read_csv(f'{DATA_DIR}/prices_probabilities.csv')

@lru_cache(maxsize=CACHE_SIZE)
def p(price: int) -> float:
    """Gets the probability of a given price occuring.
    NOTE: This uses the normalized integer price, i.e. $1.5 -> 15
    Inputs:
        price: price as an int"""
    return prices_probabilities.loc[price - 1]["probability"]

if __name__ == '__main__':

    # Check that the function works
    print(get_full_data().index[-1][0])
    print(len(get_full_data()))
