import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.pyplot import figure
import datetime


mpl.rcParams['figure.figsize'] = (12,8)
df = pd.read_csv(r'C:\Users\tatqn\Desktop\test\Portfolio Projects\archive\movies.csv')
#pdtabulate=lambda df:tabulate(df,headers='keys', tablefmt='psql')
pd.options.mode.chained_assignment = None
mpl.rcParams['axes.formatter.useoffset'] = False


with pd.option_context("display.max_colwidth", None, "display.width", None):

    for col in df.columns:
        pct_missing = np.mean(df[col].isnull())
        print('{} - {}%'.format(col, pct_missing))
        #print(col, ' - ', pct_missing, '%')

    df['released'] = df['released'].astype(pd.StringDtype())
    df['release_year'] = df['released'].str.split(',').str[1].str.extract(r"(\d{4})")
    company_duplicates = df['company'].drop_duplicates().sort_values(ascending=False)
    df2=df.dropna(subset=['budget','gross'])
    df2['budget'] = df2['budget'].apply('int64')
    df2['gross'] = df2['gross'].apply('int64')
    gross_ascending = df2.sort_values(by=['gross'], inplace=False, ascending=False)
    print(gross_ascending.head(50))
    #df = df.dropna(how='all')
    plt.scatter(x=df2['budget'], y=df2['gross'])
    plt.title('Budget vs Gross Earnings')
    plt.xlabel('Gross Earnings')
    plt.ylabel('Budget for film')
    sns.regplot(x='budget', y='gross', data=df2, scatter_kws={"color":"red"}, line_kws={"color":"blue"})
    plt.show()
    correlation_matrix = df2.corr(numeric_only=True)
    sns.heatmap(correlation_matrix, annot=True)
    plt.title('Correlation Matrix for Numeric Features')
    plt.xlabel('Movie Features')
    plt.ylabel('Movie Features')
    plt.show()

    df_numerized = df2
    for col_name in df_numerized.columns:
        if(df_numerized[col_name].dtype == 'object'):
            df_numerized[col_name] = df_numerized[col_name].astype('category')
            df_numerized[col_name] = df_numerized[col_name].cat.codes

    print(df_numerized)
    correlation_matrix = df_numerized.corr(method='pearson', numeric_only=True)
    sns.heatmap(correlation_matrix, annot=True)
    plt.title('Correlation Matrix for Numeric Features')
    plt.xlabel('Movie Features')
    plt.ylabel('Movie Features')
    plt.show()

    correlation_mat = df_numerized.corr(numeric_only=True)
    corr_pairs = correlation_mat.unstack()
    sorted_pairs = corr_pairs.sort_values()
    high_corr = sorted_pairs[(sorted_pairs) > 0.5]
    print(high_corr)
