import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv("delta.csv",sep='\t')

sns.histplot(df, bins=10,multiple="dodge")
plt.show()