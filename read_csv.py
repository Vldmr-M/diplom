import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv("experiment1.csv",sep='\t')

ax = sns.histplot(df["hillclimb"],multiple="dodge",bins = [0,50,170])
ax.set(
    xlabel="отклонение",
    ylabel="количество задач")
ax.set_xticks(range(0,170,10))
ax.set_title("Отклонение решений от потимума")
# print(df["ega"].mean())
# print(df["modif_ega"].mean())
plt.show()