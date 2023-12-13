import pandas as pd

bootstrap_list = []
for i in range(20):
    bootstrap = pd.read_excel('results_F1_bootstrap_' + str(i) + '.xlsx', index_col=0)
    bootstrap_list.append(bootstrap)


mean_F1 = pd.concat(bootstrap_list).groupby(level=0).mean()
max_location = mean_F1.stack().idxmax()
max_t = max_location[0]
max_b = max_location[1]
max_value = mean_F1.values.max()

print("The best threshold is: " + str(max_t))
print("The best b is: " + str(max_b))
print("The max F1_value is: " + str(max_value))