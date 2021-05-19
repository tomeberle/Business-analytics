import pandas as pd
from scipy.stats import chi2_contingency

def run_chisquared_company(tweets_df1):
    tweets_df1 = pd.read_csv("output/twitter_sentiment_companies.csv")
    tweets_df1.dropna(subset=["Movement"], inplace=True)

    tweets_df1.loc[(tweets_df1.Sentiment > 0),'Sentiment']= 1
    tweets_df1.loc[(tweets_df1.Sentiment < 0),'Sentiment']= -1
    tweets_df1['Sentiment'] = tweets_df1['Sentiment'].replace([0, 1, -1],['neutral','positive','negative'])

    tweets_df1['Movement'] = tweets_df1['Movement'].astype(int)
    tweets_df1['Movement'] = tweets_df1['Movement'].replace([0, 1, -1],['no_move','up','down'])
    print(tweets_df1)

    # Contingency Table
    contingency = pd.crosstab(tweets_df1['Sentiment'], tweets_df1['Movement'])

    # Chi-Squared Test
    chi2, p, dof, expected = chi2_contingency(contingency)
    return chi2, p


def run_gtest_company(tweets_df1):
    tweets_df1 = pd.read_csv("output/twitter_sentiment_companies.csv")
    tweets_df1.dropna(subset=["Movement"], inplace=True)
    
    tweets_df1.loc[(tweets_df1.Sentiment > 0),'Sentiment']= 1
    tweets_df1.loc[(tweets_df1.Sentiment < 0),'Sentiment']= -1
    tweets_df1['Sentiment'] = tweets_df1['Sentiment'].replace([0, 1, -1],['neutral','positive','negative'])

    tweets_df1['Movement'] = tweets_df1['Movement'].astype(int)
    tweets_df1['Movement'] = tweets_df1['Movement'].replace([0, 1, -1],['no_move','up','down'])

    # Contingency Table
    contingency = pd.crosstab(tweets_df1['Sentiment'], tweets_df1['Movement'])

    # G-Test or log-likelihood ratio
    g, p, dof, expcted = chi2_contingency(contingency, lambda_="log-likelihood")
    return g, p


def run_chisquared_ceo(tweets_df1):
    tweets_df1 = pd.read_csv("output/twitter_sentiment_ceos.csv")
    tweets_df1.dropna(subset=["Movement"], inplace=True)
    
    tweets_df1.loc[(tweets_df1.Sentiment > 0),'Sentiment']= 1
    tweets_df1.loc[(tweets_df1.Sentiment < 0),'Sentiment']= -1
    tweets_df1['Sentiment'] = tweets_df1['Sentiment'].replace([0, 1, -1],['neutral','positive','negative'])
    
    tweets_df1['Movement'] = tweets_df1['Movement'].astype(int)
    tweets_df1['Movement'] = tweets_df1['Movement'].replace([0, 1, -1],['no_move','up','down'])

    # Contingency Table
    contingency = pd.crosstab(tweets_df1['Sentiment'], tweets_df1['Movement'])

    # Chi-Squared Test
    chi2, p, dof, expected = chi2_contingency(contingency)
    return chi2, p


def run_gtest_ceo(tweets_df1):
    tweets_df1 = pd.read_csv("output/twitter_sentiment_companies.csv")
    tweets_df1.dropna(subset=["Movement"], inplace=True)
    
    tweets_df1.loc[(tweets_df1.Sentiment > 0),'Sentiment']= 1
    tweets_df1.loc[(tweets_df1.Sentiment < 0),'Sentiment']= -1
    tweets_df1['Sentiment'] = tweets_df1['Sentiment'].replace([0, 1, -1],['neutral','positive','negative'])

    tweets_df1['Movement'] = tweets_df1['Movement'].astype(int)
    tweets_df1['Movement'] = tweets_df1['Movement'].replace([0, 1, -1],['no_move','up','down'])

    # Contingency Table
    contingency = pd.crosstab(tweets_df1['Sentiment'], tweets_df1['Movement'])

    # G-Test or log-likelihood ratio
    g, p, dof, expcted = chi2_contingency(contingency, lambda_="log-likelihood")
    return g, p