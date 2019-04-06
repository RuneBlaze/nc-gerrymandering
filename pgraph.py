from networkx import Graph
from os.path import join
import pandas as pd


#FIXME: pandas is unnecessary, but using here for quick prototyping
def read_neighbors(path):
    neighbors = pd.read_csv(path)
    for (i, r) in neighbors.iterrows():
        print(i ,r)

class PGraph(Graph):
    @staticmethod
    def from_data(path):
        join(path, "")