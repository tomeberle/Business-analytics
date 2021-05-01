import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data to
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:cnbc since:2019-05-01').get_items()):
    if i>500:
        break
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.username])
    
# Creating a dataframe from the tweets list above & cleaning
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
tweets_df1['Text'] = tweets_df1['Text'].str.lower()
tweets_df1['Text'] = tweets_df1['Text'].replace(r'[^a-z ]', '', regex=True).replace("'", '')
tweets_df1['Text'] = tweets_df1['Text'].apply(lambda x: ' '.join([y for y in x.split() if 'http' not in y]))

# Sentiment Analysis
import csv 

SENTIMENT_CSV = "C:/Users/patri/Desktop/HEC/5th Bimester/Business Analytics/Session 2/Part 2/word_sentiment.csv"
NEGATIVE_WORDS = ["not", "dont", "doesnt", "no", "arent", "isnt"]

def word_sentiment(word):
    with open(SENTIMENT_CSV, 'rt',encoding = 'utf-8') as senti_data:
        sentiment = csv.reader(senti_data)
        for data_row in sentiment:          
            if data_row[0] == word.lower():
                sentiment_val = data_row[1]                
                return sentiment_val
        return 0    
                
def sentiment(sentence):
    sentiment = 0 
    words_list = sentence.split()
    for word in words_list:
      previous_index = words_list.index(word) -1
      if words_list[previous_index] in NEGATIVE_WORDS: 
        sentiment = sentiment + -1 * int(word_sentiment(word))
      else: 
        sentiment = sentiment + int(word_sentiment(word))
    return sentiment   

tweets_df1['Sentiment'] = tweets_df1['Text'].apply(sentiment)


# Export as CSV
tweets_df1.to_csv (r'C:\Users\patri\Desktop\HEC\5th Bimester\Business Analytics\cnbc.csv', encoding='utf-8-sig')


#time seems not to be correct: two hours behind Paris time
