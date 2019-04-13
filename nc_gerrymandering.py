from pgraph import PGraph 
from drawing import draw_all_faces, draw_subset_faces, draw_graph
from parsing import read_shapes

if __name__ == '__main__':    
    PRECINCT_NAME = 'Cumberland'
    PRECINCT_FOLDER = '%sPrecinct' % PRECINCT_NAME
    
    DATA_PATH = 'NCElectionData/ClusterData/ExtractedData/' + PRECINCT_FOLDER
    SHAPE_PATH = 'NCElectionData/ClusterData/ShapeFiles/' + PRECINCT_FOLDER + '/' + PRECINCT_FOLDER
    ELECTION_PATH = 'NCElectionData/ElectionData/results_pct_20121106.txt'
    
    faces = read_shapes(SHAPE_PATH)
    
    G = PGraph.from_data(PRECINCT_NAME, PRECINCT_FOLDER, DATA_PATH, SHAPE_PATH, ELECTION_PATH)
    draw_all_faces(G)
    draw_graph(G)
    draw_subset_faces(G, [0, 38, 2], circumcircle = True, convex_hull = True)
    