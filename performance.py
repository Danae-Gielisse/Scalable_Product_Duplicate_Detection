import numpy as np

def jaccard_similarity(vector1, vector2):
    intersection = sum(el1 and el2 for el1, el2 in zip(vector1, vector2))
    union = intersection + sum(el1 and not el2 or not el1 and el2 for el1, el2 in zip(vector1, vector2))
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

def predict_duplicates(candidate_pairs, threshold, binary_matrix):
        similar_jaccard = set()
        similar_cosine = set()
        for candidate in candidate_pairs:
            candidate_product_1 = int(candidate[0])
            candidate_product_2 = int(candidate[1])
            c1 = (binary_matrix[:, candidate_product_1])
            c2 = (binary_matrix[:, candidate_product_2])
            jaccard = jaccard_similarity(c1, c2)
            cosine = cosine_similarity(c1, c2)
            if jaccard >= threshold:
                similar_jaccard.add(tuple(sorted((candidate_product_1, candidate_product_2))))
            if cosine >= threshold:
                similar_cosine.add(tuple(sorted((candidate_product_1, candidate_product_2))))
        return similar_jaccard, similar_cosine


def pair_quality(candidates, true_duplicates):
    number_of_duplicates_found = number_of_duplicates_found_LSH(candidates, true_duplicates)
    number_of_comparisons = len(candidates)
    return number_of_duplicates_found / number_of_comparisons


def pair_completeness(candidates, true_duplicates):
    number_of_duplicates_found = number_of_duplicates_found_LSH(candidates, true_duplicates)
    total_number_of_duplicates = len(true_duplicates)
    return number_of_duplicates_found / total_number_of_duplicates


def F1_star(pair_quality, pair_completeness):
    return (2 * pair_quality * pair_completeness) / (pair_quality + pair_completeness)


def F1_score(TP, FN, FP):
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    return (2 * precision * recall) / (precision + recall)


def fraction_of_comparisons(candidates, products_list):
    number_of_comparisons = len(candidates)
    number_of_products = len(products_list)
    total_com = (number_of_products * (number_of_products - 1))/2
    return number_of_comparisons / total_com

def number_of_duplicates_found_LSH(candidates, true_duplicates):
    common_tuples = set(candidates).intersection(set(true_duplicates))
    return len(common_tuples)

def evaluate_duplicates_with_product_count(true_duplicates, predicted_duplicates, total_products):
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    true_duplicates_set = set(true_duplicates)
    predicted_duplicates_set = set(predicted_duplicates)

    total_combinations = total_products * (total_products - 1) // 2

    for pair in predicted_duplicates_set:
        if pair in true_duplicates_set:
            true_positives += 1
        else:
            false_positives += 1

    for pair in true_duplicates_set:
        if pair not in predicted_duplicates_set:
            false_negatives += 1

    total_non_duplicates = total_combinations - len(true_duplicates)

    true_negatives = total_non_duplicates - false_positives - false_negatives - true_positives

    return true_positives, false_positives, true_negatives, false_negatives

def evaluate_found_duplicates(duplicates_matrix, true_duplicate_matrix):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    number_of_products = len(duplicates_matrix)
    for i in range(number_of_products):
        for j in range(i, number_of_products):
            if i != j:
                if duplicates_matrix[i][j] == 1 and true_duplicate_matrix[i][j] == 1:
                    TP += 1
                elif duplicates_matrix[i][j] == 1 and true_duplicate_matrix[i][j] == 0:
                    FP += 1
                elif duplicates_matrix[i][j] == 0 and true_duplicate_matrix[i][j] == 1:
                    FN += 1
                else:
                    TN += 1

    return TP, FP, TN, FN


