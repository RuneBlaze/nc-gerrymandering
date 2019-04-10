from networkx import Graph
import networkx as nx
from os.path import join, normpath, basename
import pandas as pd
import sys
import shapefile as sf

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

def read_shapes(path):
    """ 
    Parses point information from a shapefile
    
    Parameters:
    path -- the base filename of the shapefile or
            the complete filename of any of the shapefile component files.
    
    
    Returns a mapping from precinct indices to a list of points
    describing that precinct
    
    The points are in the same order they were stored
    in the input shapefile
    """
    shapes = {}
    shapefile = sf.Reader(path)
    for index, shape in enumerate(shapefile.shapes()):
        shapes[index] = shape.points
    return shapes

def draw_shapefile(path, figsize = (8, 8)):
    """ Draws the shapefile stored at the given path """
    faces = read_shapes(path)
    plt.figure(figsize = figsize)
    for face in faces.values():
        polygon = face + [face[0]]
        x, y = zip(*polygon)
        plt.plot(x, y)
    plt.show()

class PGraph(Graph):
    @staticmethod
    def from_data(data_path, shape_path):
        precinct_name = basename(normpath(data_path))
        area_path = join(data_path, "%s_AREAS.txt" % precinct_name)
        neighbors_path = join(data_path, "%s_NEIGHBORS.txt" % precinct_name)
        pop_path = join(data_path, "%s_POPULATION.txt" % precinct_name)
        G = read_neighbors(neighbors_path)
        pops = read_population(pop_path)
        shapes = read_shapes(shape_path)
        for k, v in pops.items():
            G.nodes[k]['population'] = v
        for index, points in shapes.items():
            G.nodes[index]['points'] = points
        return G

if __name__ == '__main__':
    precint_name = 'CumberlandPrecinct'
    
    data_path = 'NCElectionData/ClusterData/ExtractedData/' + precint_name
    shape_path = 'NCElectionData/ClusterData/ShapeFiles/' + precint_name + '/' + precint_name
    
    draw_shapefile(shape_path)
    
    G = PGraph.from_data(data_path, shape_path)
    print(G)
    
    import matplotlib.pyplot as plt
    nx.draw_spectral(G)
    # nx.draw_networkx_labels(G)
    plt.show()