import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pgraph import PGraph
from networkx import draw_spectral

def draw_graph(pgraph):
    draw_spectral(pgraph)
    plt.show()
    

def draw_all_faces(pgraph, figsize = (8, 8)):
    """ Draws all faces of the precinct graph"""
    fig, ax = plt.subplots(figsize = figsize)
    for index in pgraph:
        face = pgraph.nodes[index]['points']
        polygon = face + [face[0]]
        x, y = zip(*polygon)
        ax.plot(x, y)
    plt.show()
    
def draw_subset_faces(pgraph,  
                     subset, 
                     convex_hull = False, 
                     circumcircle = False,
                     color = 'b',
                     figsize = (8, 8)):
    """ 
    Draws the shapefile stored at given path and fills in subset of precincts provided
    
    Parameters:
    subset -- iterable of indices that indicate the subset of precincts chosen
    draw_convex_hull -- boolean that indicates if the convex hull of the chosen precincts will be drawn
    draw_circumcircle -- boolean that indicates if the circumcircle of the chosen precincts will be drawn
    """
    fig, ax = plt.subplots(figsize = figsize)
    for index in pgraph:
        face = pgraph.nodes[index]['points']
        polygon = face + [face[0]]
        x, y = zip(*polygon)
        ax.plot(x, y)
        if index in subset:
            ax.fill(x, y, color = color)
    if circumcircle:
        center, radius = PGraph.calculate_subset_circumcircle(pgraph, subset)
        circle = mpatches.Circle(center, radius, linewidth = 2.0, fill = False)
        ax.add_artist(circle)
    plt.show()