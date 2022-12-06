import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Pandas settings
data = pd.read_csv(r'C:\Users\Mishi-PC\Desktop\Projects\Portfolio2\top 500 gross movies\top-500-movies.csv')
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
df = pd.DataFrame(data)

#Converting the data
df['year'] = df['year'].astype(pd.StringDtype())
df['opening_weekend'] = df['opening_weekend'].astype(pd.Int64Dtype())
df['year'] = df['year'].str.split('.').str[0].str.extract(r"(\d{4})")
df['genre'] = df['genre'].astype(pd.StringDtype())
print(df)

#Determening which genre has the highest average worldwide_gross
gross_by_genre = df.groupby(['genre'], as_index=False).mean(numeric_only=True)
print(gross_by_genre)
plt.bar(gross_by_genre['genre'], gross_by_genre['worldwide_gross'])
plt.show()

#Grouping the dataframe by genre in order to see how many movies in the list are from each genre
count_by_genre = df.groupby(['genre'], as_index=False).count()
count_by_genre['count_in_pct'] = (count_by_genre['title'] / count_by_genre['title'].sum()) * 100
print(count_by_genre)
y = np.array(count_by_genre['count_in_pct'])
label=list(df.columns.values)
myexplode = [0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
mycolors = ["Gold", "DarkSeaGreen", "Violet", "Crimson", "DimGrey", "Aqua", "SandyBrown", "Aquamarine", "Blue", "Coral"]
plt.pie(y, labels=count_by_genre['genre'], explode=myexplode, shadow=True, autopct='%1.1f%%', colors=mycolors)
plt.legend()
plt.show()
#The graphic shows that more than 80% of the movies in the top 500 are Action and Adventure

#Finding correlations between the different movie features
#Numerizing the values in order to analyze the data with a correlation matrix

df_numerized = df
for col_name in df_numerized.columns:
    if (df_numerized[col_name].dtype == 'object'):
        df_numerized[col_name] = df_numerized[col_name].astype('category')
        df_numerized[col_name] = df_numerized[col_name].cat.codes

correlation_matrix = df_numerized.corr(method='pearson', numeric_only=True)
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix for Numeric Features')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()

#Showing only the pairs with correlation index > 0.5
correlation_mat = df_numerized.corr(numeric_only=True)
corr_pairs = correlation_mat.unstack()
sorted_pairs = corr_pairs.sort_values()
high_corr = sorted_pairs[(sorted_pairs) > 0.5]
print(high_corr)

#Determining the correlation between Production Budget and Worldwide Gross
plt.scatter(x=df['production_cost'], y=df['worldwide_gross'])
plt.title('Budget vs Gross Earnings')
plt.xlabel('Gross Earnings')
plt.ylabel('Budget for film')
sns.regplot(x='production_cost', y='worldwide_gross', data=df, scatter_kws={"color": "green"}, line_kws={"color": "blue"})
plt.show()
#The Graph is showing positive correlation between the production cost and worldwide gross.


#Theaters column - maximum number of theaters showing the film at one time
#Determening if there is a high correlation between the production costs and the number of theaters showing the movie.
plt.scatter(x=df['theaters'], y=df['production_cost'])
plt.show()
# The graphic is showing that even movies with the lowest production costs are shown in as many theaters as movies with 3 times bigger production costs.

