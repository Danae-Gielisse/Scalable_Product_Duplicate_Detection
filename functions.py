import re
import collections
from itertools import combinations
import numpy as np

def extract_model_words(string_list):
    model_words = []

    # Regex-pattern for model words
    regex = r'([a-zA-Z0-9]*(([0-9]+[^0-9, ]+)|([^0-9, ]+[0-9]+))[a-zA-Z0-9]*)'

    for string in string_list:
        matches = re.findall(regex, string)
        for match in matches:
            word = match[0]
            if word not in model_words:
                model_words.append(word)

    return model_words


def obtain_binary_matrix(model_words, products_title_dict, products_list):
    binary_matrix = np.full((len(model_words), len(products_list)), np.nan, dtype=int)

    for product_index in products_list:
        product_title = products_title_dict[product_index]
        binary_vector = np.full((len(model_words), 1), np.nan)

        for mw_idx, mw in enumerate(model_words):
            if mw in product_title:
                binary_vector[mw_idx][0] = 1
            else:
                binary_vector[mw_idx][0] = 0

        binary_matrix[:, product_index] = np.squeeze(binary_vector)

    return binary_matrix

def hash_function(a, b, x, prime):
    return (a + b * x) % prime

def minhashing(binary_matrix):
    # set signature matrix to 50% of the size of the binary matrix
    number_of_rows, number_of_products = binary_matrix.shape
    n = int(number_of_rows / 2)
    signature_matrix = np.full((n, number_of_products), np.inf, dtype=int)

    # Generate random integers a and b
    np.random.seed(39)
    a_b_matrix = np.random.randint(1, 1000, size=(n, 2))

    # Create arrary of hash_values
    prime = 683
    for row_index in range(number_of_rows):
        for i in range(n):
            a, b = a_b_matrix[i]
            hash_value = hash_function(a, b, row_index+1, prime)
            for product_index in range(number_of_products):
                if binary_matrix[row_index][product_index] == 1:
                    if signature_matrix[i][product_index] > hash_value:
                        signature_matrix[i][product_index] = hash_value

    return signature_matrix


def jaccard_similarity(array1, array2):
    set1 = set(array1)
    set2 = set(array2)

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    jaccard_similarity = intersection / union if union != 0 else 0
    return jaccard_similarity


def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    if norm_a != 0 and norm_b != 0:
        similarity = dot_product / (norm_a * norm_b)
        return similarity
    else:
        return 0.0


def locality_sensitive_hashing(signature_matrix, b):
    n, number_of_products = signature_matrix.shape
    r = int(n / b)
    threshold = (1 / b) ** (1 / r)
    print('Treshold: ' + str(threshold))
    hash_buckets = collections.defaultdict(set)
    bands = np.array_split(signature_matrix, b, axis=0)
    for i, band in enumerate(bands):
        for j in range(number_of_products):
            band_id = tuple(list(band[:, j]) + [str(i)])
            hash_buckets[band_id].add(j)
    candidate_pairs = set()
    for bucket in hash_buckets.values():
        if len(bucket) >= 2:
            for pair in combinations(bucket, 2):
                candidate_pairs.add(tuple(sorted(pair)))
    sorted_candidate_pairs = sorted(candidate_pairs)

    return sorted_candidate_pairs, threshold


def find_true_duplicates(model_id_list):
    # Create a dictionary to store the indexes of products with the same model_id
    model_id_indexes = {}
    result = []

    # Iterate through the lists and store the indexes in the dictionary
    for index, model_id in enumerate(model_id_list):
        if model_id in model_id_indexes:
            model_id_indexes[model_id].append(index)
        else:
            model_id_indexes[model_id] = [index]

    # Find model_ids with more than one index and add the combinations to the results list
    for model_id, indexes in model_id_indexes.items():
        if len(indexes) > 1:
            for i in range(len(indexes) - 1):
                for j in range(i + 1, len(indexes)):
                    result.append((indexes[i], indexes[j]))

    return result

def create_duplicate_matrix(number_of_products, tuple_list):
    matrix = [[0 for _ in range(number_of_products)] for _ in range(number_of_products)]

    for pair in tuple_list:
        i, j = pair
        if i < j:
            matrix[i][j] = 1
    return matrix
