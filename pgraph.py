from math import pi, isclose
from networkx import Graph
import networkx as nx
from os.path import join, normpath, basename
import pandas as pd
import shapefile as sf
from parsing import read_population, read_shapes
from geometry import make_oriented, \
                     perimeter_area, \
                     convex_hull_perimeter_area, \
                     enclosing_circle_center_radius


def construct_graph(path):
    """reads the adjacency list and construct the base graph"""
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
    def from_data(data_path, shape_path, debug = False):
        precinct_name = basename(normpath(data_path))
        area_path = join(data_path, "%s_AREAS.txt" % precinct_name)
        neighbors_path = join(data_path, "%s_NEIGHBORS.txt" % precinct_name)
        pop_path = join(data_path, "%s_POPULATION.txt" % precinct_name)
        
        G = construct_graph(neighbors_path)
        pops = read_population(pop_path)
        shapes = read_shapes(shape_path)
        for k, v in pops.items():
            G.nodes[k]['population'] = v
        for index, points in shapes.items():
            oriented = make_oriented(points)
            G.nodes[index]['points'] = oriented
            
            perimeter, area = perimeter_area(points)
            G.nodes[index]['perimeter'] = perimeter
            G.nodes[index]['area'] = area
            
            ch_perimeter, ch_area = convex_hull_perimeter_area(points)
            G.nodes[index]['ch_perimeter'] = ch_perimeter
            G.nodes[index]['ch_area'] = ch_area
            
            center, radius = enclosing_circle_center_radius(points)
            G.nodes[index]['enclosing_circle_circumference'] = 2 * pi * radius
            G.nodes[index]['enclosing_circle_area'] = pi * radius * radius
            G.nodes[index]['enclosing_circle_center'] = center
            
            if debug:
                assert(len(oriented) == len(points))
                assert(isclose(perimeter_area(oriented)[0], perimeter_area(points)[0]))
                assert(isclose(perimeter_area(oriented)[1], perimeter_area(points)[1]))
                assert(isclose(enclosing_circle_center_radius(oriented)[0][0], enclosing_circle_center_radius(points)[0][0]))
                assert(isclose(enclosing_circle_center_radius(oriented)[0][1], enclosing_circle_center_radius(points)[0][1]))
                assert(isclose(enclosing_circle_center_radius(oriented)[1], enclosing_circle_center_radius(points)[1]))
        return G

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    precint_name = 'CumberlandPrecinct'
    
    data_path = 'NCElectionData/ClusterData/ExtractedData/' + precint_name
    shape_path = 'NCElectionData/ClusterData/ShapeFiles/' + precint_name + '/' + precint_name
    
    draw_shapefile(shape_path)
    
    G = PGraph.from_data(data_path, shape_path)
    print(G)
    
    nx.draw_spectral(G)
    plt.show()