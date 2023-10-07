import numpy, os
import pytest

from py_exp_calc.exp_calc import *

__author__ = "seoanezonjic"
__copyright__ = "seoanezonjic"
__license__ = "MIT"

####################################
#DATA
####################################

@pytest.fixture
def first_list():
    return [1,2,3,4,5]

@pytest.fixture
def second_list():
    return [3,4,5,6,7]

@pytest.fixture
def matrix():
    return np.array([[3,  2,  1,   4], 
                     [5,  3,  7,   8], 
                     [9,  10, 3, 12],
                     [13, 14, 15, 3]])

@pytest.fixture
def net():
    return np.array([[0, 1, 1, 0, 0],
                     [1, 0, 1, 0, 1],
                     [1, 1, 0, 1, 0],
                     [0, 0, 1, 0, 1],
                     [0, 1, 0, 1, 0]])

@pytest.fixture
def rectangular_matrix():
    return np.array([[1,  1,  0], 
                     [0,  0,  1], 
                     [0,  0,  1],
                     [1,  1,  0],
                     [1,  1,  1]])

@pytest.fixture
def rowIds():
    return ['P1', 'P2', 'P3', 'P4', 'P5']

@pytest.fixture
def colIds():
    return ['D1', 'D2', 'D3']



####################################
# LIST OPERATIONS
####################################

# One List operation
####################################

def test_get_stats_from_list():
    sample = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    
    expected = [['Elements', '10'], ['Elements Non Zero', '8'], ['Non Zero Density', '0.8'], ['Max', '4'],
                ['Min', '0'], ['Average', '2.0'], ['Variance', '2.0'], ['Standard Deviation', '1.4142135623730951'],
                ['Q1', '1.0'], ['Median', '2.0'], ['Q3', '3.0'], ['Min Non Zero', '1'], ['Average Non Zero', '2.5'],
                ['Variance Non Zero', '1.25'], ['Standard Deviation Non Zero', '1.118033988749895'], ['Q1 Non Zero', '1.75'],
                ['Median Non Zero', '2.5'], ['Q3 Non Zero', '3.25']]
    
    returned = list(get_stats_from_list(sample))
    assert expected == returned

# List x List operation
####################################

def test_intersection(first_list, second_list):
    assert intersection(first_list, second_list) == [3,4,5]

def test_union(first_list, second_list):
    assert union(first_list, second_list) == [1,2,3,4,5,6,7]
    
def test_diff(first_list, second_list):
    assert diff(first_list, second_list) == [1,2]
    assert diff(second_list, first_list) == [6,7]

####################################
# DIC OPERATIONS
####################################

# Values - operation
####################################

## Get
######

def test_dig():
    nested_dict = {5 : { 7: 'a'}}
    assert dig(nested_dict, 5, 7) == 'a'
    assert dig(nested_dict, 5, 2) == None


def test_get_hash_values_idx():
    input_hash = {"P1": ["D4", "D5", "D3"], "P2": ["D3"], "P3": ["D5", "D8"]}
    expected = {"D4": 0, "D5": 1, "D3": 2, "D8": 3}
    returned = get_hash_values_idx(input_hash)
    assert expected == returned

# Insert
########

def test_add_record():
    dict_test = {}
    add_record(dict_test, "D1", "P1")
    assert dict_test == {"D1": ["P1"]}    
    add_record(dict_test, "D1", "P2", uniq=True)
    assert dict_test == {"D1": ["P1", "P2"]}    
    add_record(dict_test, "D1", "P2", uniq=True)
    assert dict_test == {"D1": ["P1", "P2"]}    
    add_record(dict_test, "D1", "P2")
    assert dict_test == {"D1": ["P1", "P2", "P2"]}   
    add_record(dict_test, "D2", "P3", uniq=True)
    assert dict_test == {"D1": ["P1", "P2", "P2"], "D2": ["P3"]}

def test_add_nested_record():
    input_hash = {}
    add_nested_record(input_hash, "D1", "P1", 3)
    assert input_hash == {"D1": {"P1": 3}}
    add_nested_record(input_hash, "D1", "P2", 5)
    assert input_hash == {"D1": {"P1": 3, "P2": 5}}
    add_nested_record(input_hash, "D2", "P5", 9)
    assert input_hash == {"D1": {"P1": 3, "P2": 5}, "D2": {"P5": 9}}

# Keys - operation
####################################

def test_transform_keys():
    input_hash = {"A": 1, "B": 2, "C": 3}
    duplicate_string = lambda x: x + x
    
    expected = {"AA": 1, "BB": 2, "CC": 3}
    returned = transform_keys(input_hash, duplicate_string)
    assert expected == returned

def test_invert_nested_hash():
    initial_hash = {"D1": {"P1": 3, "P2": 4}, "D2": {"P3": 5}, "D3": {"P1": 9}}
    inverted_hash = {"P1": {"D1": 3, "D3": 9}, "P2": {"D1": 4}, "P3": {"D2": 5}}
    returned_inverted_hash = invert_nested_hash(initial_hash)
    assert inverted_hash == returned_inverted_hash

def test_remove_nested_entries():
    initial_hash = {"D1": {"P1": 3, "P2": 8}, "D2": {"P3": 2}, "D3": {"P1": 9}}
    filter_func = lambda k, v: v > 5

    expected = {"D1": {"P2": 8}, "D3": {"P1": 9}}
    
    remove_nested_entries(initial_hash, filter_func)
    assert expected == initial_hash

####################################
# ARRAY (Matrix) OPERATIONS
####################################

# I/O operations
####################################

def test_save_and_load():
    matrix = np.array([[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 1]])
    x_axis_names = ['S1', 'S2', 'S3', 'S4']
    y_axis_names = ['S1', 'S2', 'S3', 'S4']
    
    save(matrix, 'test_matrix.npy', x_axis_names, 'test_x_axis.txt', y_axis_names, 'test_y_axis.txt')
    loaded_matrix, loaded_x_axis, loaded_y_axis = load('test_matrix.npy', 'test_x_axis.txt', 'test_y_axis.txt')
    
    assert (matrix == loaded_matrix).all()
    assert x_axis_names == loaded_x_axis
    assert y_axis_names == loaded_y_axis

    save(matrix, 'test_matrix.npy')
    loaded_matrix, loaded_x_axis, loaded_y_axis = load('test_matrix.npy')
    assert (matrix == loaded_matrix).all()
    assert None == loaded_x_axis
    assert None == loaded_y_axis

    #Deleting files
    os.remove('test_matrix.npy')
    os.remove('test_x_axis.txt')
    os.remove('test_y_axis.txt')

# Normalization
####################################

def test_normalize_matrix(matrix):
    expected_min_max = (matrix - 1) / 14.0 #min = 1, max = 15 in the input matrix
    returned_min_max = normalize_matrix(matrix, "min_max")
    assert (expected_min_max == returned_min_max).all()

    expected_cosine = matrix / 3.0 #all the values in the input matrix diagonal are 3, so square root of denominator (matrix[i, i] * matrix[j,j]) is always 3
    returned_cosine = normalize_matrix(matrix, "cosine")
    assert (expected_cosine == returned_cosine).all()

    expected_row_col = np.array([[0.3       , 0.13187609, 0.05423261, 0.18856181],
                                [0.32969024, 0.13043478, 0.25031949, 0.24866795],
                                [0.48809353, 0.35759927, 0.08823529, 0.306786  ],
                                [0.61282588, 0.43516891, 0.38348249, 0.06666667]])
    returned_row_col = normalize_matrix(matrix, "rows_cols")
    assert np.isclose(expected_row_col, returned_row_col).all()


def test_min_max_normalization_matrix(matrix):
    expected_min_max = (matrix - 1) / 14.0 #min = 1, max = 15 in the input matrix
    returned_min_max = min_max_normalization_matrix(matrix)
    assert (expected_min_max == returned_min_max).all()

def test_cosine_normalization_matrix(matrix):
    expected_cosine = matrix / 3.0 #all the values in the input matrix diagonal are 3, so square root of denominator (matrix[i, i] * matrix[j,j]) is always 3
    returned = cosine_normalization(matrix)
    assert (expected_cosine == returned).all()

def test_rows_cols_normalization_matrix(matrix):
    expected_row_col = np.array([[0.3       , 0.13187609, 0.05423261, 0.18856181],
                                [0.32969024, 0.13043478, 0.25031949, 0.24866795],
                                [0.48809353, 0.35759927, 0.08823529, 0.306786  ],
                                [0.61282588, 0.43516891, 0.38348249, 0.06666667]])
    returned_row_col = row_col_normalization(matrix)
    assert np.isclose(expected_row_col, returned_row_col).all()

# Sim <-> Dis conversion
####################################

def test_coords2sim(net):
    dotProduct_expected =  [[2, 1, 1, 1, 1],
                            [1, 3, 1, 2, 0],
                            [1, 1, 3, 0, 2],
                            [1, 2, 0, 2, 0],
                            [1, 0, 2, 0, 2]]
    dotProduct_returned = coords2sim(net)

    normalizedScaling_expected =   [[1.        , 0.22540333, 0.22540333, 0.36754447, 0.36754447],
                                    [0.22540333, 1.        , 0.10557281, 0.5527864 , 0.        ],
                                    [0.22540333, 0.10557281, 1.        , 0.        , 0.5527864 ],
                                    [0.36754447, 0.5527864 , 0.        , 1.        , 0.10557281],
                                    [0.36754447, 0.        , 0.5527864 , 0.10557281, 1.        ]]
    normalizedScaling_returned = coords2sim(net, "normalizedScaling")
    
    euclidean_expected =   [[1.        , 0.3660254 , 0.3660254 , 0.41421356, 0.41421356],
                            [0.3660254 , 1.        , 0.33333333, 0.5       , 0.30901699],
                            [0.3660254 , 0.33333333, 1.        , 0.30901699, 0.5       ],
                            [0.41421356, 0.5       , 0.30901699, 1.        , 0.33333333],
                            [0.41421356, 0.30901699, 0.5       , 0.33333333, 1.        ]]
    euclidean_returned = coords2sim(net, "euclidean")

    assert (dotProduct_expected == dotProduct_returned).all()
    assert np.isclose(normalizedScaling_expected, normalizedScaling_returned).all()
    assert np.isclose(euclidean_expected, euclidean_returned).all()

def test_coords2dis(net):
    expected = [[0.         ,1.73205081, 1.73205081, 1.41421356, 1.41421356],
                [1.73205081 ,0.        , 2.        , 1.        , 2.23606798],
                [1.73205081 ,2.        , 0.        , 2.23606798, 1.        ],
                [1.41421356 ,1.        , 2.23606798, 0.        , 2.        ],
                [1.41421356 ,2.23606798, 1.        , 2.        , 0.        ]]
    returned = coords2dis(net)
    assert np.isclose(expected, returned).all()

# Stats
####################################

def test_get_corr(): #Leave for now
    pass

def test_pearsonr(): #Leave for now
    pass

def test_get_stats_from_matrix(net):
    expected = [['Matrix - Dimensions', '5x5'], ['Matrix - Elements', '25'], ['Matrix - Elements Non Zero', '12'], ['Matrix - Non Zero Density', '0.48'], ['Weigth - Max', '1'], ['Weigth - Min', '0'], ['Weigth - Average', '0.48'], ['Weigth - Variance', '0.24960000000000016'], ['Weigth - Standard Deviation', '0.499599839871872'], ['Weigth - Q1', '0.0'], ['Weigth - Median', '0.0'], ['Weigth - Q3', '1.0'], ['Weigth - Min Non Zero', '1'], ['Weigth - Average Non Zero', '1.0'], ['Weigth - Variance Non Zero', '0.0'], ['Weigth - Standard Deviation Non Zero', '0.0'], ['Weigth - Q1 Non Zero', '1.0'], ['Weigth - Median Non Zero', '1.0'], ['Weigth - Q3 Non Zero', '1.0'], ['Node - Elements', '5'], ['Node - Elements Non Zero', '5'], ['Node - Non Zero Density', '1.0'], ['Edges - Max', '3'], ['Edges - Min', '2'], ['Edges - Average', '2.4'], ['Edges - Variance', '0.24'], ['Edges - Standard Deviation', '0.4898979485566356'], ['Edges - Q1', '2.0'], ['Edges - Median', '2.0'], ['Edges - Q3', '3.0'], ['Edges - Min Non Zero', '2'], ['Edges - Average Non Zero', '2.4'], ['Edges - Variance Non Zero', '0.24'], ['Edges - Standard Deviation Non Zero', '0.4898979485566356'], ['Edges - Q1 Non Zero', '2.0'], ['Edges - Median Non Zero', '2.0'], ['Edges - Q3 Non Zero', '3.0']]
    returned = list(get_stats_from_matrix(net))
    assert expected == returned

def test_get_primary_stats():
    listt = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    listt = np.array(listt).reshape((1,len(listt)))

    matrix = np.array([[0, 0, 0, 0],[ 1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]])

    expected = {'count': 16, 'countNonZero': 12, 'sum': 24, 'max': 3, 'min': 0, 'minNonZero': 1, 'q1': 0.75, 'median': 1.5, 'q3': 2.25, 'q1NonZero': 1.0, 'medianNonZero': 2.0, 'q3NonZero': 3.0, 'average': 1.5, 'averageNonZero': 2.0, 'sumDevs': 20.0, 'sumDevsNonZero': 8.0, 'variance': 1.25, 'varianceNonZero': 0.6666666666666666, 'standardDeviation': 1.118033988749895, 'standardDeviationNonZero': 0.816496580927726}
    stats_list = get_primary_stats(listt)
    stats_matrix = get_primary_stats(matrix)
    assert expected == stats_list
    assert expected == stats_matrix

def test_get_connection_number(net):
    expected = np.array([2,3,3,2,2])
    returned = get_connection_number(net) 
    assert (expected == returned).all()

def test_get_quartiles():
    numbers = [1,2,3,4,5,6,7,8,9,10]
    expected = {'median': 5.5, 'q1': 3.25, 'q3': 7.75}
    returned = get_quartiles(numbers, None)
    assert expected == returned

def test_get_composed_stats(): #Tested in test_get_primary_stats
    pass

# Filtering
####################################

def test_binarize_mat():
    input_matrix = np.array([[3, 0, 0, 0],[0, 0, 7, 8],[0, 10, 0, 12],[0, 14, 15, 0]])
    expected_matrix = np.array([[1, 0, 0, 0],[0, 0, 1, 1],[0, 1, 0, 1],[0, 1, 1, 0]])
    returned_matrix = binarize_mat(input_matrix)
    assert (expected_matrix == returned_matrix).all()

def test_filter_cutoff_mat(matrix):
    expected_cutoff_5 = np.array([[0, 0, 0, 0],[5, 0, 7, 8],[9, 10, 0, 12],[13, 14, 15, 0]])
    expected_cutoff_14 = np.array([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 14, 15, 0]])
    expected_cutoff_20 = np.array([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]])
    
    returned_cutoff_5 = filter_cutoff_mat(matrix, 5)
    returned_cutoff_14 = filter_cutoff_mat(matrix, 14)
    returned_cutoff_20 = filter_cutoff_mat(matrix, 20)

    assert (expected_cutoff_5 == returned_cutoff_5).all()
    assert (expected_cutoff_14 == returned_cutoff_14).all()
    assert (expected_cutoff_20 == returned_cutoff_20).all()

def test_percentile_filter(matrix):
    expected_50 = np.array([[3, 0, 0, 0],[0, 0, 7, 8],[0, 10, 0, 12],[0, 14, 15, 0]])
    returned_50 = percentile_filter(matrix, 50)
    assert (expected_50 == returned_50).all()

def test_remove_zero_lines():
    input_matrix = np.array([[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 12],
                             [0, 0, 15, 0]])
    colnames = ['S1', 'S2', 'S3', 'S4']
    rownames = ['P1', 'P2', 'P3', 'P4']
    
    expected_matrix = np.array([[0, 12], [15, 0]])
    expected_colnames = ['S3', 'S4']
    expected_rownames = ['P3', 'P4']

    returned_matrix, returned_colnames, returned_rownames = remove_zero_lines(input_matrix, colnames, rownames)
    assert (expected_matrix == returned_matrix).all()
    assert expected_colnames == returned_colnames
    assert expected_rownames == returned_rownames

# Clustering
####################################

def test_get_hc_clusters():
    matrix = np.array([[3, 5, 0, 0, 0, 0], [4, 6, 0, 0, 0, 0], [0, 0, 0, 0, 1, 2], [0, 0, 0, 0, 3, 2]])
    expected = np.array([[0,0,0,0],[1,0,0,0],[2,1,1,0],[3,2,1,0]])
    result = get_hc_clusters(matrix)
    assert (expected == result).all()

def test_get_cls_max_avg():
    pass

def test_get_avg_value4tree_cut():
    pass

def test_get_member_list():
    pass

def test_add_cluster_members():
    pass

def test_get_cluster_avg_value():
    pass

def test_tag_items_in_clusters():
    clusters = np.array([[0,0,0,0],[1,0,0,0],[2,1,1,0],[3,2,1,0]])
    names = ['C1', 'C2', 'C3', 'C4']

    expected = {0: ['C1'], 1: ['C2'], 2: ['C3'], 3: ['C4']}
    returned = tag_items_in_clusters(clusters, names)
    assert expected == returned

####################################
# Explicit conversions
####################################

# General conversor #

def test_transform2obj():
    matrix_format = np.array(  [[0, 1, 1, 0],
                                [1, 0, 0, 1],
                                [1, 0, 0, 1],
                                [0, 1, 1, 0]])
    pairs_format = [['S1', 'S2', 1], ['S1', 'S3', 1], ['S2', 'S4', 1], ['S3', 'S4', 1]]
    nested_pairs_format = {'S1': {'S2': 1, 'S3': 1}, 'S2': {'S4': 1}, 'S3': {'S4': 1}}

    returned, rowIds, colIds = transform2obj(pairs_format, inFormat="pair", outFormat="matrix")
    assert (matrix_format == returned).all()
    assert rowIds == ['S1', 'S2', 'S3', 'S4']
    assert colIds == ['S1', 'S2', 'S3', 'S4']

    returned, rowIds, colIds = transform2obj(nested_pairs_format, inFormat="nested_pairs", outFormat="matrix")
    assert (matrix_format == returned).all()
    assert rowIds == ['S1', 'S2', 'S3', 'S4']
    assert colIds == ['S1', 'S2', 'S3', 'S4']

    returned, rowIds, colIds = transform2obj(nested_pairs_format, inFormat="nested_pairs", outFormat="pair")
    assert pairs_format == returned


    expected_pairs = [['S1', 'S1', 0], ['S1', 'S2', 1], ['S1', 'S3', 1], ['S1', 'S4', 0], 
                      ['S2', 'S1', 1], ['S2', 'S2', 0], ['S2', 'S3', 0], ['S2', 'S4', 1], 
                      ['S3', 'S1', 1], ['S3', 'S2', 0], ['S3', 'S3', 0], ['S3', 'S4', 1], 
                      ['S4', 'S1', 0], ['S4', 'S2', 1], ['S4', 'S3', 1], ['S4', 'S4', 0]]
    returned, rowIds, colIds = transform2obj(matrix_format, inFormat="matrix", outFormat="pair", 
                                             colIds=['S1', 'S2', 'S3', 'S4'], rowIds=['S1', 'S2', 'S3', 'S4'])

    assert expected_pairs == returned
    assert rowIds == ['S1', 'S2', 'S3', 'S4']
    assert colIds == ['S1', 'S2', 'S3', 'S4']
    

# Dic -> Matrix(array)
####################################

def test_to_bmatrix():
    bhash_squared = {'S1' : ['S3'], 'S2' : ['S3', 'S4'], 'S3' : ['S1'], 'S4' : ['S2', 'S3']}
    result_bmatrix_squared_to_hash = np.array([[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 1]])
    test_bmatrix_squared, y_names, x_names = to_bmatrix(bhash_squared)
    assert (result_bmatrix_squared_to_hash == test_bmatrix_squared).all()
    assert y_names == ['S1', 'S2', 'S3', 'S4']
    assert x_names == ['S3', 'S4', 'S1', 'S2']

def test_to_wmatrix_squared():
    #Not symmetric case scenario
    whash_squared = {'S1' : {'S3': 3}, 'S2' : {'S3': 2, 'S4': 5}, 'S3' : {'S4': 4}} 
    result_whash_squared_to_hash = np.array([[0, 3, 0, 0], 
                                             [0, 0, 0, 4], 
                                             [0, 2, 0, 5], 
                                             [0, 0, 0, 0]])
    
    test_whash_squared, names = to_wmatrix(whash_squared, squared=True, symm=False)
    print(test_whash_squared)
    assert (result_whash_squared_to_hash == test_whash_squared).all()
    assert names == ['S1', 'S3', 'S2', 'S4']

    #Symmetric case scenario
    result_whash_squared_to_hash_symmetric = np.array([[0, 3, 0, 0], 
                                                       [3, 0, 2, 4], 
                                                       [0, 2, 0, 5], 
                                                       [0, 4, 5, 0]])
    test_whash_squared_symmetric, names = to_wmatrix(whash_squared, squared=True, symm=True)
    print(test_whash_squared_symmetric)
    assert (result_whash_squared_to_hash_symmetric == test_whash_squared_symmetric).all()
    assert names == ['S1', 'S3', 'S2', 'S4']
        

def test_to_wmatrix_rectangular():
    #Not symmetric case scenario
    whash_rectangular = {'S1' : {'P3': 3}, 'S2' : {'P3': 2, 'P4': 5}, 'S3' : {'P1': 7, 'P2': 1}}
    result_whash_rectangular_to_hash = np.array([[3, 0, 0, 0], [2, 5, 0, 0], [0, 0, 7, 1]])
    test_whash_rectangular, y_names, x_names = to_wmatrix(whash_rectangular, squared=False, symm=False)
    
    assert (result_whash_rectangular_to_hash == test_whash_rectangular).all()
    assert y_names == ["S1", "S2", "S3"]
    assert x_names == ["P3", "P4", "P1", "P2"]


# Dic -> List
####################################

def test_nested_pairs2pairs():
    nested_pairs = {"A": {"B": 1, "C": 2}, "B": {"C": 3, "D":4}, "C":{"D": 5}}
    
    expected = [["A", "B", 1], ["A", "C", 2], ["B", "C", 3], ["B", "D", 4], ["C", "D", 5]]
    returned = nested_pairs2pairs(nested_pairs)
    assert expected == returned

# List -> Matrix(Array)
####################################

def test_pairs2matrix():
    expected_matrix_format = np.array(  [[0, 1, 1, 0],
                                        [1, 0, 0, 1],
                                        [1, 0, 0, 1],
                                        [0, 1, 1, 0]])
    
    pairs_format = [['S1', 'S2', 1], ['S1', 'S3', 1], ['S2', 'S4', 1], ['S3', 'S4', 1]]
    returned_matrix, rowIds, colIds = pairs2matrix(pairs_format)

    assert ( returned_matrix == expected_matrix_format).all()
    assert rowIds == ['S1', 'S2', 'S3', 'S4']
    assert colIds == ['S1', 'S2', 'S3', 'S4']

def test_update_index(): #TODO: not quite sure if this is how the code is actually working, but this function is also being tested in higher order functions
    index = {"A": 2, "B":3}
    assert update_index(index, "A", 2) == 2
    assert update_index(index, "B", 3) == 3
    assert update_index(index, "C", 0) == 1


# Matrix(Array) -> List
####################################

def test_matrix2pairs(net, rectangular_matrix, rowIds, colIds):
    expected_rectangular_pairs = [['P1', 'D1', 1], ['P1', 'D2', 1], ['P1', 'D3', 0], 
                                  ['P2', 'D1', 0], ['P2', 'D2', 0], ['P2', 'D3', 1], 
                                  ['P3', 'D1', 0], ['P3', 'D2', 0], ['P3', 'D3', 1], 
                                  ['P4', 'D1', 1], ['P4', 'D2', 1], ['P4', 'D3', 0], 
                                  ['P5', 'D1', 1], ['P5', 'D2', 1], ['P5', 'D3', 1]]
    returned_rectangular_pairs = matrix2pairs(rectangular_matrix, rowIds, colIds)
    assert expected_rectangular_pairs == returned_rectangular_pairs

    expected_symm_pairs = [['P1', 'P1', 0], ['P1', 'P2', 1], ['P1', 'P3', 1], ['P1', 'P4', 0], ['P1', 'P5', 0], 
                                            ['P2', 'P2', 0], ['P2', 'P3', 1], ['P2', 'P4', 0], ['P2', 'P5', 1], 
                                                             ['P3', 'P3', 0], ['P3', 'P4', 1], ['P3', 'P5', 0], 
                                                                              ['P4', 'P4', 0], ['P4', 'P5', 1], 
                                                                                               ['P5', 'P5', 0]]
    returned_squared_symmetric_pairs = matrix2pairs(net, rowIds, rowIds, symm=True)
    assert expected_symm_pairs == returned_squared_symmetric_pairs

def test_matrixes2pairs(net, rectangular_matrix, rowIds, colIds):
    doubled_rectangular = rectangular_matrix * 2
    doubled_symmetric = net * 2

    expected_rectangular_pairs = [['P1', 'D1', 1, 2], ['P1', 'D2', 1, 2], ['P1', 'D3', 0, 0], 
                                  ['P2', 'D1', 0, 0], ['P2', 'D2', 0, 0], ['P2', 'D3', 1, 2], 
                                  ['P3', 'D1', 0, 0], ['P3', 'D2', 0, 0], ['P3', 'D3', 1, 2], 
                                  ['P4', 'D1', 1, 2], ['P4', 'D2', 1, 2], ['P4', 'D3', 0, 0], 
                                  ['P5', 'D1', 1, 2], ['P5', 'D2', 1, 2], ['P5', 'D3', 1, 2]]
    returned_rectangular_pairs = matrixes2pairs([rectangular_matrix, doubled_rectangular], rowIds, colIds)
    assert expected_rectangular_pairs == returned_rectangular_pairs


    expected_symm_pairs = [['P1', 'P1', 0, 0], ['P1', 'P2', 1, 2], ['P1', 'P3', 1, 2], ['P1', 'P4', 0, 0], ['P1', 'P5', 0, 0], 
                                               ['P2', 'P2', 0, 0], ['P2', 'P3', 1, 2], ['P2', 'P4', 0, 0], ['P2', 'P5', 1, 2], 
                                                                   ['P3', 'P3', 0, 0], ['P3', 'P4', 1, 2], ['P3', 'P5', 0, 0], 
                                                                                       ['P4', 'P4', 0, 0], ['P4', 'P5', 1, 2], 
                                                                                                           ['P5', 'P5', 0, 0]]
    returned_symmetric_pairs = matrixes2pairs([net, doubled_symmetric], rowIds, rowIds, symm=True)
    assert expected_symm_pairs == returned_symmetric_pairs
    

def test_matrix2relations():
    rectangular_matrix = np.array([[-0.1, -3.0,  2.0],
                                   [ 1.0, -4.0, -1.0]])
    rowIds = ['P1', 'P2']
    colIds = ['D1', 'D2', 'D3']
    expected_relations = [["P1", "D3", 2], ["P2", "D1", 1]]
    
    returned_rectangular_pairs = matrix2relations(rectangular_matrix, rowIds, colIds)
    assert expected_relations == returned_rectangular_pairs

    symm_matrix = np.array([[-1.0,  1.0, -1.0],
                            [ 1.0, -1.0,  1.0],
                            [-1.0,  1.0, -1.0]])

    expected_symm_pairs = [["D1", "D2", 1], ["D2", "D3", 1]]
    returned_squared_symmetric_pairs = matrix2relations(symm_matrix, colIds, colIds, symm=True)
    assert expected_symm_pairs == returned_squared_symmetric_pairs