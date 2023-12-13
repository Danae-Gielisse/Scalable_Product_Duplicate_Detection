import statistics
from performance import *
from data_preparation import *
from functions import *
from clustering import *
import pickle

# get the test dataframes
with open('test_df_list.pkl', 'rb') as file:
    test_df_list = pickle.load(file)

def test(test_df, b, t):
    print("Start testing")
    # produce lists of the columns in the test df
    titles_list = test_df['Title'].tolist()
    products_list_test_index = test_df["product_index_train"].tolist()
    model_id_list = test_df["ModelID"].tolist()
    # pre-process titles
    titles_list_processed = pre_process(titles_list)
    # extract model words
    model_words = extract_model_words(titles_list_processed)
    # obtain binary matrix (binary vector for each of the products)
    products_title_dict = extract_titles(products_list_test_index, titles_list_processed)
    binary_matrix = obtain_binary_matrix(model_words, products_title_dict, products_list_test_index)
    # apply minhashing to obtain the signature matrix
    signature_matrix = minhashing(binary_matrix)
    # determine the true duplicates
    true_duplicates = find_true_duplicates(model_id_list)
    # create dataframe to store the results for LSH
    results_LSH = pd.DataFrame(index=['pair_quality', 'pair_completeness', 'F1_star', 'Fraction_of_comparisons'])
    # create webshop list
    webshop_list, webshop_list_number = obtain_webshop_labels(test_df)
    # obtain candidates from LSH
    candidates_LSH, threshold_LSH = locality_sensitive_hashing(signature_matrix, b)
    # obtain pair quality, pair completeness, f1 star and fraction of comparisons and store the values
    pq = pair_quality(candidates_LSH, true_duplicates)
    pc = pair_completeness(candidates_LSH, true_duplicates)
    f1star = F1_star(pq, pc)
    fraction_of_c = fraction_of_comparisons(candidates_LSH, products_list_test_index)
    results_LSH.loc["pair_quality", b] = pq
    results_LSH.loc["pair_completeness", b] = pc
    results_LSH.loc["F1_star", b] = f1star
    results_LSH.loc["Fraction_of_comparisons", b] = fraction_of_c
    # determine to which cluster each product belongs to
    cluster = clustering(np.transpose(signature_matrix), t)
    # obtain the predicted duplicates
    duplicates = []
    for candidate_pair in candidates_LSH:
        product1, product2 = candidate_pair
        if webshop_list_number[product1] != webshop_list_number[product2] and cluster[product1] == cluster[product2]:
            duplicates.append(candidate_pair)
    TP, FP, TN, FN = evaluate_duplicates_with_product_count(true_duplicates, duplicates, len(products_list_test_index))
    F1 = F1_score(TP, FN, FP)

    return results_LSH, F1

F1_values = []
results_LSH_list = []
for test_df in test_df_list:
    results_LSH, F1 = test(test_df, 55, 0.27)
    F1_values.append(F1)
    results_LSH_list.append(results_LSH)

mean_F1 = statistics.mean(F1_values)
print("The mean of the test F1 score is: " + str(mean_F1))

