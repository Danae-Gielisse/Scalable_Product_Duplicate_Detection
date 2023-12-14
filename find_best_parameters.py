import pandas as pd

less_cleaning = False
cleaning_string = ''
if less_cleaning:
    cleaning_string = '_less_cleaning'

bootstrap_list = []
for i in range(20):
    bootstrap = pd.read_excel('results_F1_bootstrap_' + str(i) + cleaning_string + '.xlsx', index_col=0)
    bootstrap_list.append(bootstrap)


mean_F1 = pd.concat(bootstrap_list).groupby(level=0).mean()
max_location = mean_F1.stack().idxmax()
max_t = max_location[0]
max_b = max_location[1]
max_value = mean_F1.values.max()

print("The best threshold is: " + str(max_t))
print("The best b is: " + str(max_b))
print("The max F1_value is: " + str(max_value))

row_with_best_threshold = mean_F1.loc[max_t]
row_with_best_threshold.to_excel('row_with_best_threshold' + cleaning_string + '.xlsx', index_label='F1_score')