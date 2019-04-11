import matplotlib.pyplot as plt
from parsing import read_shapes 

def draw_shapefile(path, figsize = (8, 8)):
    """ Draws the shapefile stored at the given path """
    faces = read_shapes(path)
    plt.figure(figsize = figsize)
    for face in faces.values():
        polygon = face + [face[0]]
        x, y = zip(*polygon)
        plt.plot(x, y)
    plt.show()