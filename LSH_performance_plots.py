import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("results_LSH.xlsx", index_col=0)
plot_list_y = ["pair_quality", "pair_completeness", "F1_star"]

def plot_vs_fraction(row):
    y = df.loc[row]
    x = df.loc["Fraction_of_comparisons"]
    plt.scatter(x, y, color='red')

    plt.plot(x, y, marker='o', linestyle='-', color='red')
    plt.xlabel('Fraction_of_comparisons')
    plt.ylabel(row)

    plt.title('Scatter plot met gesmoothe lijn')
    plt.show()

    # Save the plot
    plt.savefig( row + '.png')

for e in plot_list_y:
   plot_vs_fraction(e)
