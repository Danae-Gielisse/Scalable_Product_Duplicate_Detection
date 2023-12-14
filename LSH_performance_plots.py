import pandas as pd
import matplotlib.pyplot as plt


F1_score = pd.read_excel('row_with_best_threshold.xlsx', index_col=0).values
F1_score_less_cleaning = pd.read_excel('row_with_best_threshold_less_cleaning.xlsx', index_col=0).values

F1_score_df = pd.DataFrame(F1_score.reshape(1, -1))
F1_score_df_less_cleaning = pd.DataFrame(F1_score_less_cleaning.reshape(1, -1))

LSH_df_list = []
for i in range(20):
    LSH_df = pd.read_excel('results_LSH_bootstrap_' + str(i) + '.xlsx', index_col=0)
    LSH_df_list.append(LSH_df)

LSH_df_list_less_cleaning = []
for i in range(20):
    LSH_df_less_cleaning = pd.read_excel('results_LSH_bootstrap_' + str(i) + '_less_cleaning.xlsx', index_col=0)
    LSH_df_list_less_cleaning.append(LSH_df_less_cleaning)

F1_score_df.columns = LSH_df_list[0].columns
F1_score_less_cleaning_df = LSH_df_list_less_cleaning[0].columns
F1_score_df.index = ['F1_score']
F1_score_df_less_cleaning.index  = ['F1_score']

mean_LSH = pd.concat(LSH_df_list).groupby(level=0).mean()
mean_LSH_less_cleaning = pd.concat(LSH_df_list_less_cleaning).groupby(level=0).mean()
LSH = pd.concat([mean_LSH, F1_score_df])
LSH_less_cleaning = pd.concat([mean_LSH_less_cleaning, F1_score_df_less_cleaning])

plot_list_y = ["pair_quality", "pair_completeness", "F1_star", "F1_score"]

def plot_vs_fraction(row):
    y = LSH.loc[row]
    x = LSH.loc["Fraction_of_comparisons"]
    y_less_cleaning = LSH_less_cleaning.loc[row]
    x_less_cleaning = LSH_less_cleaning.loc["Fraction_of_comparisons"]
    plt.scatter(x, y, color='red')
    plt.scatter(x_less_cleaning, y_less_cleaning, color='blue')
    plt.plot(x, y, marker='o', linestyle='-', color='red', label='more data cleaning')
    plt.plot(x_less_cleaning, y_less_cleaning, marker='o', linestyle='-', color='blue', label='less data cleaning')
    plt.xlabel('fraction of comparisons')
    if row == 'pair_quality':
        plt.ylabel('pair quality')
        plt.legend(loc='upper right')
    elif row == 'pair_completeness':
        plt.ylabel('pair completeness')
        plt.legend(loc='lower right')
    elif row == 'F1_score':
        plt.ylabel('F1 score')
        plt.legend(loc='lower right')
    else:
        plt.ylabel('f1 star')
        plt.legend(loc='lower right')


    plt.show()


    plt.savefig(row + '.png')

for e in plot_list_y:
   plot_vs_fraction(e)
