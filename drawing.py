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
        ax.plot(x, y, color = 'black')
    plt.show()
    
def draw_subset(ax,
                pgraph,  
                subset, 
                draw_convex_hull = False, 
                draw_circumcircle = False,
                subset_fill_color = 'blue',
                circumcircle_color = 'purple',
                convex_hull_color = 'green'):
    """ 
    Draws the given precinct graph and fills in subset of precincts provided
    
    Parameters:
    subset -- iterable of indices that indicate the subset of precincts chosen
    draw_convex_hull -- boolean that indicates if the convex hull of the chosen precincts will be drawn
    draw_circumcircle -- boolean that indicates if the circumcircle of the chosen precincts will be drawn
    """
    for index in pgraph:
        face = pgraph.nodes[index]['points']
        polygon = face + [face[0]]
        x, y = zip(*polygon)
        ax.plot(x, y, color = 'black')
        if index in subset:
            ax.fill(x, y, color = subset_fill_color)
    if draw_circumcircle:
        center, radius = PGraph.calculate_subset_circumcircle(pgraph, subset)
        circle = mpatches.Circle(center, radius, linewidth = 3.0, fill = False, color = circumcircle_color)
        ax.add_artist(circle)
    if draw_convex_hull:
        hull = PGraph.calculate_subset_convex_hull(pgraph, subset)
        hull = hull + [hull[0]]
        x, y = zip(*hull)
        ax.plot(x, y, color = convex_hull_color, linewidth = 3.0)
        
def draw_some_faces(pgraph, 
                      subset,
                      draw_convex_hull = False,
                      draw_circumcircle = False,
                      subset_fill_color = 'cyan',
                      circumcircle_color = 'purple',
                      convex_hull_color = 'blue',
                      figsize = (8, 8)):
    fig, ax = plt.subplots(figsize = figsize)
    draw_subset(ax, pgraph, subset, draw_convex_hull, draw_circumcircle, subset_fill_color, circumcircle_color, convex_hull_color)
    plt.show()
    
def draw_partition(pgraph, subset, figsize = (8, 8)):
    all_nodes = set(range(len(pgraph)))
    complement = all_nodes - subset
    fig, ax = plt.subplots(figsize = figsize)
    draw_subset(ax,
                pgraph, 
                subset,
                draw_convex_hull = True, 
                draw_circumcircle = True,
                subset_fill_color = 'cyan',
                circumcircle_color = 'purple',
                convex_hull_color = 'blue')
    draw_subset(ax,
                pgraph, 
                complement,
                draw_convex_hull = True, 
                draw_circumcircle = True,
                subset_fill_color = 'pink',
                circumcircle_color = 'orange',
                convex_hull_color = 'red')
    plt.show()