import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data to
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:JeffBezos since:2019-05-01').get_items()):
    if i>500:
        break
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.username])
    
# Creating a dataframe from the tweets list above 
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
tweets_df1['Text'] = tweets_df1['Text'].replace({'â€™':"'"})

tweets_df1.to_csv (r'C:\Users\patri\Desktop\HEC\5th Bimester\Business Analytics\jeff_bezos.csv', encoding='utf-8-sig')
