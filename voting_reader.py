import pandas as pd
from typing import Dict, List, NamedTuple
from collections import defaultdict
from enum import Enum
import shapefile as sf

class Contest(Enum):
    straight = 0
    house = 1

class Party(Enum):
    dem = 0
    rep = 1

class Voting(NamedTuple):
    contest : Contest
    party : Party
    votes : int


def extract_row_data(r) -> (str, Party, int):
    k = r['precinct'].split('_')[0]
    party = Party.dem if r['party'] == 'DEM' else Party.rep
    votes = r['total votes']
    return (k, party, votes)

def read_votes(path : str, county : str) -> Dict[str, List[Voting]]:
    df_ = pd.read_csv(path)
    #(df_.county == county.upper()) & (df_.county == county.upper()) & 
    # straight_votes = df_[(df_.contest.str.contains('STRAIGHT'))]
    house_votes = df_[(df_.contest.str.contains('HOUSE'))]
    res = defaultdict(list)
    # for _, r in straight_votes.iterrows():
    #     k, pt, votes = extract_row_data(r)
    #     res[k].append(Voting(Contest.straight, pt, votes))
    for _, r in house_votes.iterrows():
        k, pt, votes = extract_row_data(r)
        res[k].append(Voting(Contest.house, pt, votes))
    return dict(res)

def read_precinct_prefixes(path : str) -> List[str]:
    shapefile = sf.Reader(path)
    prefixes = [r[2] for r in shapefile.records()]
    return prefixes


from math import sqrt, erf
def phi(x):
    #'Cumulative distribution function for the standard normal distribution'
    return (1.0 + erf(x / sqrt(2.0))) / 2.0

def dem_prob(dem : int, rep : int, n : int = 0) -> float:
    n = n or (dem + rep)
    p = dem / (dem + rep)
    avg = p * n
    var = n * p * (1 - p)
    # print(avg, var)
    winning = (dem + rep) / 2
    # print((winning - avg) / var)
    return 1 - phi((winning - avg) / sqrt(var))