from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform

def obtain_webshop_labels(train_df):
    webshop_list = []
    webshop_list_number = []
    for shop_name in train_df["Shop"]:
        if (shop_name == 'amazon.com'):
            webshop_list.append('amazon')
            webshop_list_number.append(1)
        elif (shop_name == 'bestbuy.com'):
            webshop_list.append('bestbuy')
            webshop_list_number.append(2)
        elif (shop_name == 'newegg.com'):
            webshop_list.append('newegg')
            webshop_list_number.append(3)
        else:
            webshop_list.append('thenerds')
            webshop_list_number.append(4)
    return webshop_list, webshop_list_number

def clustering(signature_matrix, threshold):
    # Compute pairwise distances between items
    distance_matrix= pdist(signature_matrix, metric='jaccard')

    # Perform hierarchical clustering
    Z = linkage(distance_matrix, method='ward')

    # Obtain the cluster for each product
    clusters = fcluster(Z, threshold, criterion='distance')

    return clusters