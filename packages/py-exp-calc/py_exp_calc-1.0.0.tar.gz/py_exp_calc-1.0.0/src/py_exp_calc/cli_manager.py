import argparse
import numpy as np
from py_exp_calc.exp_calc import *

def based_0(string): return int(string) - 1

def clusterize(args = None):
    if args == None: args = sys.argv[1:]
    parser = argparse.ArgumentParser(description="Get clusters")
    parser.add_argument("-i", "--input_file", dest="input",
        help="Path to input file")
    parser.add_argument("-x", "--x_dim", dest="x_dim",
        help="Item list file for x axis")
    parser.add_argument("-y", "--y_dim", dest="y_dim",
        help="Item list file for y axis")
    parser.add_argument("-n", "--n_clusters", dest="n_clusters",
        help="N clusters for cut tree algorithm")
    parser.add_argument("-o", "--output_file", dest="output",
        help="Path to input file")

    opts =  vars(parser.parse_args(args))
    main_clusterize(opts)

def main_clusterize(args):
    x_names = read_tabular_file(args['x_dim'], [0])
    x_names = [ x[0] for x in x_names ]
    y_names = read_tabular_file(args['y_dim'], [0])
    y_names = [ y[0] for y in y_names ]
    observation_matrix = np.loadtxt(args['input'])
    if len(observation_matrix.shape) == 1: # conver 1 Dimensional array to 2 Dimensional array
        observation_matrix = observation_matrix.reshape(observation_matrix.size, 1)
    clusters, cls_objects = get_hc_clusters(observation_matrix, identify_clusters='cut_tree', item_list = x_names, n_clusters= args['n_clusters'])
    write_dict(clusters, args['output'])

def read_tabular_file(input_file, cols):
    data = []
    with open(input_file) as f:
        for line in f:
            fields = line.rstrip().split("\t")
            data.append([fields[i] for i in cols])
    return data

def write_dict(dict, file):
    with open(file, 'w') as f:
        for k, values in dict.items():
            f.write(f"{k}\t{','.join(values)}\n")