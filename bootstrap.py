import numpy as np

def obtain_train_test_df(df, seed_value):
    np.random.seed(seed_value)

    train_data = df.sample(n=1000)
    train_indices = train_data.index
    test_data = df.drop(train_indices)

    train_data.reset_index(drop=True, inplace=True)
    test_data.reset_index(drop=True, inplace=True)
    train_data['product_index_train'] = train_data.index
    test_data['product_index_train'] = test_data.index

    return train_data, test_data
