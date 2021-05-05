'''
    Exercise 6: Scrap more information about TripAdvisor reviews

       url = "https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html"

   Please write a code that prints out 
           review content, 
           numeric rating, 
           title,
           date,
           reviewer's username 
   of ALL the 10 reviews on the FIRST page of a particular restaurant
   '''

#this is Patrick's comment

import csv
import requests
from bs4 import BeautifulSoup


def scrapecontent(url):
    scrape_response = requests.get(url)
    print(scrape_response.status_code)

    if scrape_response.status_code == 200:
        soup = BeautifulSoup(scrape_response.text)
        return soup
    else:
        print('Error accessing url: ', scrape_response.status_code)
        return None


def main():
    scrape_url = 'https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html'
    ret_soup = scrapecontent(scrape_url)
    # print(ret_soup.find_all("div", class_="prw_rup prw_reviews_review_resp"))
    if ret_soup:
        count = 1
        for rev_data in ret_soup.find_all("div", class_="prw_rup prw_reviews_review_resp"):
            print(rev_data)
            print('review number: ', count)

            title = rev_data.find('span', class_='noQuotes')
            print('title: ', title.text)

            review = rev_data.find('p', class_='partial_entry')
            print('review content: ', review.text)

            rating = rev_data.find('span', class_='ui_bubble_rating')
            print('numeric rating: ', int(int(rating['class'][1][7:])/10))

            date = rev_data.find('span', class_='ratingDate')
            print('date: ', date['title'])

            username = rev_data.find('div', class_='info_text pointer_cursor')
            print("reviewer's username: ", username.text)

            count += 1
            print('\n')


main()


'''
    Excercise 7: Predict the sentiment (positive, negative, neutral) of review text

    url = "https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html"

    for ALL the 10 reviews on the FIRST page of a particular restaurant:

# Using the corpus of word sentiment in the word_sentiment.csv file, 
# calculate the sentiment of review texts.*
If the sentiment score is positive, the sentiment is positive;
if the sentiment score is negative, the sentiment is negative;
if the sentiment score is zero, the sentiment is neutral.
'''


SENTIMENT_CSV = "/content/word_sentiment.csv"
NEGATIVE_WORDS = ["not", "don't", "doesn't"]


def word_sentiment(word):
    with open(SENTIMENT_CSV, 'rt', encoding='utf-8') as senti_data:
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
        previous_index = words_list.index(word) - 1
        if words_list[previous_index] in NEGATIVE_WORDS:
            sentiment = sentiment + -1 * int(word_sentiment(word))
        else:
            sentiment = sentiment + int(word_sentiment(word))
    return sentiment


scrape_url = "https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html"
response = requests.get(scrape_url)
print(response.status_code)


def review_sentiment():
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        count = 1
        print("These are the sentiments of each review: ")
        for review in soup.find_all('p', class_='partial_entry'):
            pure_review = review.text.lower()
            review_sentiment = sentiment(pure_review)
            if review_sentiment > 0:
                print("The sentiment of review ", count, "is positive")
            elif review_sentiment == 0:
                print("The sentiment of review ", count, "is neutral")
            else:
                print("The sentiment of review ", count, "is negative")
            count += 1


review_sentiment()


'''
Excercise 8: Predict the sentiment (positive, negative, neutral) of review text
        and compare with the ground true (the actual review rating)

    url = "https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html"

    for ALL the 10 reviews on the FIRST page of a particular restaurant:
        
Using the corpus of word sentiment in the word_sentiment.csv file, 
calculate the sentiment of review texts as the predicted sentiment:
If the sentiment score is positive, the sentiment is positive;
if the sentiment score is negative, the sentiment is negative;
if the sentiment score is zero, the sentiment is neutral.

Scrap the review rating of the reviews, and get the ground truth
if the rating is greater than 3, the sentiment is positive;
if the rating is less than 3, the sentiment is negative;
if the rating is equal to 3, the sentiment is neutral.

Question: Compute the prediction accuracy (hit rate) for the 10 reviews, i.e.,
    how many times the predictions are correct??
'''


SENTIMENT_CSV = "/content/word_sentiment.csv"
NEGATIVE_WORDS = ["not", "don't", "doesn't"]


def word_sentiment(word):
    """This function uses the word_sentiment.csv file to find the sentiment of the word 
    entered"""
    with open(SENTIMENT_CSV, 'rt', encoding='utf-8') as senti_data:
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
        previous_index = words_list.index(word) - 1
        if words_list[previous_index] in NEGATIVE_WORDS:
            sentiment = sentiment + -1 * int(word_sentiment(word))
        else:
            sentiment = sentiment + int(word_sentiment(word))
    return sentiment


scrape_url = "https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html"
response = requests.get(scrape_url)
print(response.status_code)


def accuracy():
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        review_list = []
        for review in soup.find_all('p', class_='partial_entry'):
            pure_review = review.text.lower()
            review_sentiment = sentiment(pure_review)
            if review_sentiment > 0:
                review_list.append('positive')
            elif review_sentiment == 0:
                review_list.append('neutral')
            else:
                review_list.append('negative')

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        rating_list = []
        for review in soup.find_all('div', class_='ui_column is-9'):
            for rating in review.find_all('span', class_='ui_bubble_rating'):
                actual_rating = int(int(rating['class'][1][7:])/10)
                if actual_rating > 3:
                    rating_list.append('positive')
                elif actual_rating == 3:
                    rating_list.append('neutral')
                else:
                    rating_list.append('negative')

    matches = len([i for i, j in zip(rating_list, review_list) if i == j])
    accuracy = matches / len(rating_list)
    print('The prediction accuracy is', accuracy)


accuracy()
