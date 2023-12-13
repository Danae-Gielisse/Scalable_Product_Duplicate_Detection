import pandas as pd
import matplotlib.pyplot as plt

LSH_df_list = []
for i in range(20):
    LSH_df = pd.read_excel('results_LSH_bootstrap_' + str(i) + '.xlsx', index_col=0)
    LSH_df_list.append(LSH_df)


mean_LSH = pd.concat(LSH_df_list).groupby(level=0).mean()
plot_list_y = ["pair_quality", "pair_completeness", "F1_star"]

def plot_vs_fraction(row):
    y = mean_LSH.loc[row]
    x = mean_LSH.loc["Fraction_of_comparisons"]
    plt.scatter(x, y, color='red')

    plt.plot(x, y, marker='o', linestyle='-', color='red')
    plt.xlabel('fraction of comparisons')
    if row == 'pair_quality':
        plt.ylabel('pair quality')
    elif row == 'pair_completeness':
        plt.ylabel('pair completeness')
    else:
        plt.ylabel('f1 star')

    plt.title('')
    plt.show()


    plt.savefig(row + '.png')

for e in plot_list_y:
   plot_vs_fraction(e)
