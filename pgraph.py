from networkx import Graph
import networkx as nx
from os.path import join, normpath, basename
import pandas as pd
import sys

#FIXME: pandas is unnecessary, but using here for quick prototyping

# returns an adjacency list, 
def read_neighbors(path):
    # return nx.read_adjlist(path)
    G = Graph()
    adj_list = {}
    with open(path) as fp:
        for line in fp:
            parsed = list(map(int, line.split("\t")))
            hd, tl = parsed[0], parsed[1:]
            adj_list[hd] = tl
    G.add_nodes_from(set(adj_list.keys()) - set([-1]))
    for n in G.nodes:
        G.nodes[n]['boundary'] = False
    for n, adj in adj_list.items():
        if n == -1:
            continue
        for v in adj:
            if v == -1:
                G.nodes[n]['boundary'] = True
                continue
            G.add_edge(n, v)
    return G

def read_population(path):
    pop = {}
    with open(path) as fp:
        for line in fp:
            parsed = list(map(int, line.split("\t")[:2]))
            i, n = parsed
            pop[i] = n
    return pop

class PGraph(Graph):
    @staticmethod
    def from_data(cluster_path):
        precinct_name = basename(normpath(cluster_path))
        area_path = join(cluster_path, "%s_AREAS.txt" % precinct_name)
        neighbors_path = join(cluster_path, "%s_NEIGHBORS.txt" % precinct_name)
        pop_path = join(cluster_path, "%s_POPULATION.txt" % precinct_name)
        G = read_neighbors(neighbors_path)
        pops = read_population(pop_path)
        for k, v in pops.items():
            G.nodes[k]['population'] = v
        return G

if __name__ == '__main__':
    precint_name = 'CumberlandPrecinct'
    
    cluster_path = 'NCElectionData/ClusterData/ExtractedData/' + precint_name
    
    G = PGraph.from_data(cluster_path)
    print(G)
    
    import matplotlib.pyplot as plt
    nx.draw_spectral(G)
    # nx.draw_networkx_labels(G)
    plt.show()