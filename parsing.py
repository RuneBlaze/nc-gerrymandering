from os.path import join, normpath, basename
import shapefile as sf
#FIXME: pandas is unnecessary, but using here for quick prototyping
def read_population(path):
    pop = {}
    with open(path) as fp:
        for line in fp:
            parsed = list(map(int, line.split("\t")[:2]))
            i, n = parsed
            pop[i] = n
    return pop

def read_adj_list(path):
    adj_list = {}
    with open(path) as fp:
        for line in fp:
            parsed = list(map(int, line.split("\t")))
            hd, tl = parsed[0], parsed[1:]
            adj_list[hd] = tl
    return adj_list

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