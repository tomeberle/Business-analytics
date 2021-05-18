import pandas as pd
from scipy.stats import chi2_contingency

tweets_df1 = pd.read_csv("C:/Users/patri/Desktop/HEC/5th Bimester/Business Analytics/twitter_sentiment_companies.csv", parse_dates=["Date"])
    
tweets_df1.loc[(tweets_df1.Sentiment > 0),'Sentiment']= 1
tweets_df1.loc[(tweets_df1.Sentiment < 0),'Sentiment']= -1
tweets_df1['Sentiment'] = tweets_df1['Sentiment'].replace([0, 1, -1],['neutral','positive','negative'])

tweets_df1['Movement'] = tweets_df1['Movement'].replace([0, 1, -1],['no_move','up','down'])

# Contingency Table
contingency = pd.crosstab(tweets_df1['Sentiment'], tweets_df1['Movement'])

# Chi-Squared Test
chi2, p, dof, expected = chi2_contingency(contingency)
chi2, p

# G-Test or log-likelihood ratio
g, p, dof, expcted = chi2_contingency(contingency, lambda_="log-likelihood")
g, p
