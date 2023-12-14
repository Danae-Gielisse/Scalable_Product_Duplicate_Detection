import random
from bootstrap import *
from performance import *
from data_preparation import *
from functions import *
import pickle
from clustering import *

# load the json data
data = load_json('Data/TVs-all-merged.json')

# set dictionairy to dataframe
dataframe = dictionary_to_dataframe(data)

# get the dataframe without the features
data_without_features = dataframe.iloc[:, :5]
data_without_features['product_index'] = data_without_features.index

def train_new(train_df):
    print("Start training")
    # produce lists of the columns in the train df
    titles_list = train_df['Title'].tolist()
    products_list_train_index = train_df["product_index_train"].tolist()
    model_id_list = train_df["ModelID"].tolist()
    # pre-process titles
    titles_list_processed = pre_process(titles_list)
    # extract model words
    model_words = extract_model_words(titles_list_processed)
    # obtain binary matrix (binary vector for each of the products)
    products_title_dict = extract_titles(products_list_train_index, titles_list_processed)
    binary_matrix = obtain_binary_matrix(model_words, products_title_dict, products_list_train_index)
    # apply minhashing to obtain the signature matrix
    signature_matrix = minhashing(binary_matrix)
    # determine the true duplicates
    true_duplicates = find_true_duplicates(model_id_list)
    # determine b and threshold values
    b_values = [1, 3, 5, 10, 15, 30, 40, 45, 50, 55, 60, 70, 80, 90, 100, 125, 150, 160, 170, 180, 190,  200, 250, 300]
    threshold_values = [0.1, 0.2, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1, 1.1, 1.3]
    # create dataframe to store the results for F1 and LSH
    results_F1 = pd.DataFrame(index=threshold_values, columns=b_values)
    results_LSH = pd.DataFrame(index=['pair_quality', 'pair_completeness', 'F1_star', 'Fraction_of_comparisons'])
    # create webshop list
    webshop_list, webshop_list_number = obtain_webshop_labels(train_df)
    for b in range(0, len(b_values)):
        # obtain candidates from LSH
        candidates_LSH, t = locality_sensitive_hashing(signature_matrix, b_values[b])
        # obtain pair quality, pair completeness, f1 star and fraction of comparisons and store the values
        pq = pair_quality(candidates_LSH, true_duplicates)
        pc = pair_completeness(candidates_LSH, true_duplicates)
        f1star = F1_star(pq, pc)
        fraction_of_c = fraction_of_comparisons(candidates_LSH, products_list_train_index)
        results_LSH.loc["pair_quality", b_values[b]] = pq
        results_LSH.loc["pair_completeness", b_values[b]] = pc
        results_LSH.loc["F1_star", b_values[b]] = f1star
        results_LSH.loc["Fraction_of_comparisons", b_values[b]] = fraction_of_c
        for threshold in threshold_values:
            # determine to which cluster each product belongs to
            cluster = clustering(np.transpose(signature_matrix), threshold)
            # obtain the predicted duplicates
            duplicates = []
            for candidate_pair in candidates_LSH:
                product1, product2 = candidate_pair
                if webshop_list_number[product1] != webshop_list_number[product2] and cluster[product1] == cluster[product2]:
                    duplicates.append(candidate_pair)
            # calculate F1 score and store in dataframe
            TP, FP, TN, FN = evaluate_duplicates_with_product_count(true_duplicates, duplicates, len(products_list_train_index))
            F1 = F1_score(TP, FN, FP)
            results_F1.loc[threshold, b_values[b]] = F1
    return results_LSH, results_F1

def train_multiple_times(number_of_bootstraps, seed):
    random.seed(seed)
    random_seeds = [random.randint(1, 1000) for _ in range(number_of_bootstraps)]
    for i in range(0, number_of_bootstraps):
        string_bootstrap = '_bootstrap_' + str(i)
        test_df_list = []
        train_df, test_df = obtain_train_test_df(data_without_features, random_seeds[i])

        # Save test_df for testing
        test_df_list.append(test_df)

        results_LSH, results_F1 = train_new(train_df)
        results_LSH.to_excel('results_LSH' + string_bootstrap + '.xlsx', index=True)
        results_F1.to_excel('results_F1' + string_bootstrap + '.xlsx', index=True)

    return test_df_list

# train multiple times
test_df_list = train_multiple_times(20, 39)

# store the test dataframes for testing
with open('test_df_list.pkl', 'wb') as file:
    pickle.dump(test_df_list, file)

