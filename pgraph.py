from math import pi, isclose
from networkx import Graph
import networkx as nx
from os.path import join
from parsing import read_population, \
                    read_shapes, \
                    read_adj_list, \
                    read_border_lengths
from geometry import make_oriented, \
                     perimeter_area, \
                     convex_hull_perimeter_area, \
                     enclosing_circle_center_radius
from voting_reader import Contest, Party, Voting, read_votes, read_precinct_prefixes

def construct_graph(path, weights = []):
    """reads the adjacency list and construct the base graph"""
    G = Graph()
    adj_list = read_adj_list(path)
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
            G.add_edge(n, v, weight = weights[n][v])
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
    def from_data(precinct_name, precinct_folder, data_path, shape_path, election_path, debug = False):
        area_path = join(data_path, "%s_AREAS.txt" % precinct_folder)
        neighbors_path = join(data_path, "%s_NEIGHBORS.txt" % precinct_folder)
        pop_path = join(data_path, "%s_POPULATION.txt" % precinct_folder)
        border_path = join(data_path, "%s_BORDERLENGTHS.txt" % precinct_folder)
        
        shapes = read_shapes(shape_path)
        num_precincts = len(shapes)
        border_perimeters = read_border_lengths(num_precincts, border_path)
        G = construct_graph(neighbors_path, border_perimeters)
        pops = read_population(pop_path)
        
        for k, v in pops.items():
            G.nodes[k]['population'] = v
        voting_data = read_votes(election_path, precinct_name)
        voting_prefixes = read_precinct_prefixes(shape_path)
        for index in G.nodes:
            G.nodes[index]['voting'] = voting_data[voting_prefixes[index]]
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
    
    PRECINCT_NAME = 'Cumberland'
    PRECINCT_FOLDER = '%sPrecinct' % PRECINCT_PREFIX
    
    DATA_PATH = 'NCElectionData/ClusterData/ExtractedData/' + PRECINCT_FOLDER
    SHAPE_PATH = 'NCElectionData/ClusterData/ShapeFiles/' + PRECINCT_FOLDER + '/' + PRECINCT_FOLDER
    ELECTION_PATH = 'NCElectionData/ElectionData/results_pct_20121106.txt'
    
    draw_shapefile(SHAPE_PATH)
    
    G = PGraph.from_data(PRECINCT_NAME, PRECINCT_FOLDER, DATA_PATH, SHAPE_PATH, ELECTION_PATH)
    print(G)
    
    nx.draw_spectral(G)
    plt.show()