#!/usr/bin/env python
# coding: utf-8

# # Supervised Learning
# ## Machine learning (ML)
#
# The sentiment analysis program we wrote earlier adopts a non-machine learning algorithm.
# That is, it tries to define what words have good and bad sentiments and
# assumes all the necessary words of good and bad sentiments exist in the word_sentiment.csv file.
#
#
# Machine Learning (ML) is a class of algorithms, which are data-driven, i.e. unlike "normal" algorithms, it is the data that "tells" what the "good answer" is. A machine learning algorithm would not have such coded definition of what a good and bad sentiment is, but would "learn-by-examples". That is, you will show several sentences which have been labeled as good sentiment and bad sentiment and a good ML algorithm will eventually learn and be able to predict whether or not an unseen sentence has a good or bad sentiment. This particular example of sentiment analysis is "supervised", which means that your example words must be labeled, or explicitly say which sentences are good and which are bad.
#
# On the other hand, in the case of unsupervised learning, the sentence examples are not labeled. Of course, in such a case the algorithm itself cannot "invent" what a good sentiment is, but it can try to cluster the data into different groups, e.g. it can figure out that sentences that have certain  words are different from those hat have others (eg. it might cluster sentecences around words like mother,childeren etc. and find that cluster to be different from another group of sentences that contain words like politician).
# There are "intermediate" forms of supervision, i.e. semi-supervised and active learning. Technically, these are supervised methods in which there is some "smart" way to avoid a large number of labeled examples.
#
# - In active learning, the algorithm itself decides which thing you should label (e.g. it can be pretty sure about a sentence that has the word fantastic, but it might ask you to confirm if the sentence may have a negative like “not”).
# - In semi-supervised learning, there are two different algorithms, which start with the labeled examples, and then "tell" each other the way they think about some large number of unlabeled data. From this "discussion" they learn.
#
#
# #### Figure : Supervised learning approach
#
#
# <center>
#     <img src="ML_supervised.gif"  width="500" title="Supervised learning">
# </center>
#
# Ref 1:
# https://www.youtube.com/watch?v=nKW8Ndu7Mjw&t=382s
#
# Ref 2:
# https://www.nltk.org/book/ch06.html

# ### Excercise:
#
# In this excercise we try to improve the *word_sentiment.csv* file. We build a classifier model to predict the sentiment of an unseen word, using the the dictionary (corpus) of sentiments available in the word_sentiment.csv file.

# ### Training the ML algorithm
#
# #### Module : NLTK (Natural Language Tool Kit)
# NLTK module is built for working with language data.  NLTK supports classification, tokenization, stemming, tagging, parsing, and semantic reasoning functionalities. We will use the NLTK module and employ the naive Bayes method to classify words as being either positive or negative sentiment. You can also use other modules specifically meant for ML eg. sklearn module.
#
# THe nltk module already is installed in your lab PC. But it may not be included in your laptop. In case it is not you need to
#
# *pip install --user nltk*
#
# To check if it is insatlled just run
#
# *import nltk*

# In[ ]:


# pip install --user nltk


# ### Step 1.1: Feature extraction
# Define what features of a word that you want to use in order to classify the data set.
# We will first select only one feature: the first letter of the word.

# #### Feature Extractor

# In[ ]:

import random
import nltk
import csv


def word_sentiment_feature(word):
    """ Given a word, it returns a dictonary of the first letter of the word"""
    first_l = word[0]
    # features is of the dictionary type having only one feature
    features = {"first letter": first_l}
    return features


input_word = input("Enter a word: ").lower()
feature = word_sentiment_feature(input_word)
print(feature)


# #### Step 2: Create the feature vector/set
# We will use the corpus of sentiments from the word_sentiment.csv file to create a feature dataset which we will use to train and test the ML model.

# In[ ]:


def word_sentiment_feature(word):
    """ Given a word, it returns a dictonary of the first letter of the word"""
    first_l = word[0]
    # features is of the dictionary type having only one feature
    features = {"first letter": first_l}
    return features


def gen_featureset(sentiment_csv):
    """ This function creates a feature set for the word_sentiment.csv file"""
    featureset = list()

    with open(sentiment_csv, 'rt', encoding='utf-8') as csvobj:
        ws_data = csv.reader(csvobj)
        for row in ws_data:
            # feature_label is a list consisting of a case feature and its label
            feature_label = list()
            feature = word_sentiment_feature(row[0])
            feature_label.append(feature)

            # label: 'positive', 'neutral', 'negative'
            if int(row[1]) > 0:
                sentiment = 'positive'
            elif int(row[1]) < 0:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            feature_label.append(sentiment)

            print(feature_label)
            featureset.append(feature_label)
    return featureset


# SENTIMENT_CSV = "/Users/lix/Dropbox (HEC PARIS-)/Course and Research Sharing/Business Analytics Using Python at HEC/02 Python Basics/Sentiments/word_sentiment.csv"
SENTIMENT_CSV = "/Users/tomeberle/Downloads/word_sentiment.csv"

featureset = gen_featureset(SENTIMENT_CSV)
print(len(featureset))


# #### Step 3: Train the model on the training data set
# ##### Split the sample to training and testing data set
#
# We will split the feature data set into training and test data sets. The training set is used to train our ML model and then the testing set can be used to check how good the model is. It is normal to use 20% of the data set for testing purposes. In our case we will retain 1500 words for training and the rest for testing.
#
# ##### Use ML method (Naive Bayes) to create the classifier model
#
# The NLTK module gives us several ML methods to create a classifier model using our training set and based on our selected features.

# In[ ]:


def word_sentiment_feature(word):
    """ Given a word, it returns a dictonary of the first letter of the word"""
    first_l = word[0]
    # features is of the dictionary type having only one feature
    features = {"first letter": first_l}
    return features


def gen_featureset(sentiment_csv):
    """ This function creates a feature set for the word_sentiment.csv file"""
    featureset = list()
    with open(sentiment_csv, 'rt', encoding='utf-8') as csvobj:
        ws_data = csv.reader(csvobj)
        for row in ws_data:
            # feature_label is a list consisting of a case feature and its label
            feature_label = list()
            feature = word_sentiment_feature(row[0])
            feature_label.append(feature)
            # label: 'positive', 'neutral', 'negative'
            if int(row[1]) > 0:
                sentiment = 'positive'
            elif int(row[1]) < 0:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            feature_label.append(sentiment)

            featureset.append(feature_label)
    return featureset


def train_nb_classifier(sentiment_csv):
    """ This will train the classifier using the word sentiment feature set"""
    featureset = gen_featureset(sentiment_csv)
    # note that the whole feature set is used as the training set
    classifier = nltk.NaiveBayesClassifier.train(featureset)
    return classifier


nb_classifier = train_nb_classifier(SENTIMENT_CSV)
print('Naive Bayes Classifier:', nb_classifier)

# print the classifier's labels
print('Labels:')
print(sorted(nb_classifier.labels()))

# see the 5 most informative features that the classifier finds most effective
nb_classifier.show_most_informative_features(5)


# #### Step 4: Using the classifier object created predict the sentiment of a given word
#
#

# In[ ]:


def word_sentiment_feature(word):
    """ Given a word, it returns a dictonary of the first letter of the word"""
    first_l = word[0]
    # features is of the dictionary type having only one feature
    features = {"first letter": first_l}
    return features


def gen_featureset(sentiment_csv):
    """ This function creates a feature set for the word_sentiment.csv file"""
    featureset = list()
    with open(sentiment_csv, 'rt', encoding='utf-8') as csvobj:
        ws_data = csv.reader(csvobj)
        for row in ws_data:
            # feature_label is a list consisting of a case feature and its label
            feature_label = list()
            feature = word_sentiment_feature(row[0])
            feature_label.append(feature)
            # label: 'positive', 'neutral', 'negative'
            if int(row[1]) > 0:
                sentiment = 'positive'
            elif int(row[1]) < 0:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            feature_label.append(sentiment)

            featureset.append(feature_label)
    return featureset


def train_nb_classifier(sentiment_csv):
    """ This will train the classifier using the word sentiment feature set"""
    featureset = gen_featureset(sentiment_csv)
    # note that the whole feature set is used as the training set
    classifier = nltk.NaiveBayesClassifier.train(featureset)
    return classifier


nb_classifier = train_nb_classifier(SENTIMENT_CSV)

i_word = input("Enter a word: ").lower()
wordfeatures = word_sentiment_feature(i_word)
print('feature of the word:', wordfeatures)

sentiment = nb_classifier.classify(wordfeatures)
print('Predicted sentiment:', sentiment)


# #### Step 5: Evaluating the model
#
# Find how good the model is in identifying the labels. Ensure that the test set is distinct from the training corpus. If we simply re-used the training set as the test set, then a model that simply memorized its input, without learning how to generalize to new examples, would receive misleadingly high scores. The function nltk.classify.accuracy() will calculate the accuracy of a classifier model on a given test set.
# - Reduce variance in outcome by clubbing it (i.e. change the range of sentiment from -5 to 5 .. to -1 and 1)

# In[ ]:


def word_sentiment_feature(word):
    """ Given a word, it returns a dictonary of the first letter of the word"""
    first_l = word[0]
    # features is of the dictionary type having only one feature
    features = {"first letter": first_l}
    return features


def gen_featureset(sentiment_csv):
    """ This function creates a feature set for the word_sentiment.csv file"""
    featureset = list()
    with open(sentiment_csv, 'rt', encoding='utf-8') as csvobj:
        ws_data = csv.reader(csvobj)
        for row in ws_data:
            # feature_label is a list consisting of a case feature and its label
            feature_label = list()
            feature = word_sentiment_feature(row[0])
            feature_label.append(feature)
            # label: 'positive', 'neutral', 'negative'
            if int(row[1]) > 0:
                sentiment = 'positive'
            elif int(row[1]) < 0:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            feature_label.append(sentiment)

            featureset.append(feature_label)
    return featureset


def train_nb_classifier(sentiment_csv):
    """ This will train the classifier using the word sentiment feature set"""
    featureset = gen_featureset(sentiment_csv)
    # shuffle the corpus to overcome the issue of alphebetic ordering of the word
    # so that the training set and test set share the same distribution
    random.shuffle(featureset)

    num_ts = int(len(featureset)*0.8)
    # the first 80% as training set, the latter 20% as test set
    training_set, test_set = featureset[:num_ts], featureset[num_ts:]
    # training_set = featureset[:num_ts]
    # test_set = featureset[num_ts:]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    classifier.show_most_informative_features(5)

    acc = nltk.classify.accuracy(classifier, test_set)
    print("The accuracy of the model:", acc)

    return classifier


nb_classifier = train_nb_classifier(SENTIMENT_CSV)

i_word = input("Enter a word: ").lower()
i_features = word_sentiment_feature(i_word)
sentiment = nb_classifier.classify(i_features)
print('Predicted sentiment:', sentiment)


"""
# #### How to improve the prediction acurracy?
# 
# Direction 1: "better" (more informative) features, and perhaps more features
# Direction 2: Better classifier
"""


"""
4 Supervised Learning: Predict word sentiment
    
    Exercise 11: Improvement - More features, including the first and last letter

"""


"""
4 Supervised Learning: Predict word sentiment
    
    Exercise 12: Improvement - More features, including the first two letters

"""


"""
4 Supervised Learning: Predict the gender of a name
    
    Exercise 13: Identify features and use the naive classifer to predict 

"""


# #### Note: Development testing and error analysis
#
# Using a seperate development test set, we can generate a list of the errors that the classifier makes when predicting the sentiment. We can then examine individual error cases where the model predicted the wrong label, and try to determine what additional pieces of information would allow it to make the right decision (or which existing pieces of information are tricking it into making the wrong decision). The feature set can then be adjusted accordingly.


def word_sentiment_feature(word):
    """ Given a word, it returns a dictonary of the first letter of the word"""
    first_l = word[0]
    # features is of the dictionary type having only one feature
    features = {"first letter": first_l}
    return features


def gen_featureset(SENTIMENT_CSV):
    """ This function creates a feature set for the word_sentiment.csv file"""
    with open(SENTIMENT_CSV, 'rt', encoding='utf-8') as csvobj:
        ws_data = csv.reader(csvobj)
        featureset = list()
        for row in ws_data:
            w_feature = list()
            feature = word_sentiment_feature(row[0])  # first letter
            # feature = word_sentiment_features2(row[0]) # first two letters
            w_feature.append(row[0])
            w_feature.append(feature)
            if int(row[1]) > 0:
                sentiment = 1
            elif int(row[1]) < 0:
                sentiment = -1
            else:
                sentiment = 0
            w_feature.append(sentiment)
            # w_feature: [word, feature, sentiment]
            featureset.append(w_feature)
        return featureset


def train_nb_classifier(sentiment_csv):
    """ This will train the classifier using the word sentiment feature set"""
    featureset = gen_featureset(sentiment_csv)
    # shuffle the corpus to overcome the issue of alphebetic ordering of the word
    # so that the training set and test set share the same distribution
    random.shuffle(featureset)

    num_dev = int(len(featureset)*0.8)
    # the first 80% as development set, the latter 20% as test set
    dev_set = featureset[:num_dev]
    test_set = featureset[num_dev:]
    # the first 80% as training set, the latter 20% as development test set
    num_ts = int(num_dev*0.8)
    # training_set = dev_set[:num_ts]
    # dev_test_set = dev_set[num_ts:]
    training_set = [(feature, sentiment)
                    for (word, feature, sentiment) in dev_set[:num_ts]]
    dev_test_set = [(feature, sentiment)
                    for (word, feature, sentiment) in dev_set[num_ts:]]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    classifier.show_most_informative_features(5)

    acc = nltk.classify.accuracy(classifier, dev_test_set)
    print("The accuracy of the model:", acc)

    """##########
    # error analysis
    ##############"""
    errors = []
    i = 0
    while i < len(dev_test_set):
        wordfeature = dev_test_set[i][0]
        sentiment = dev_test_set[i][1]
        predicted = nb_classifier.classify(wordfeature)
        if predicted != sentiment:
            word = dev_set[i+num_ts][0]
            errors.append((sentiment, predicted, word))
        i += 1
    for (sentiment, predicted, word) in sorted(errors):
        print('label={:<3} predicted={:<3} word={:<20}' .format(
            sentiment, predicted, word))

    return classifier


SENTIMENT_CSV = "/Users/lix/Dropbox (HEC PARIS-)/Course and Research Sharing/Business Analytics Using Python at HEC/02 Python Basics/Sentiments/word_sentiment.csv"
# SENTIMENT_CSV = "C:/Users/pmedappa/Dropbox/Tilburg/Course 2019-2020/DSS/Lab4/Sentiments/word_sentiment.csv"

nb_classifier = train_nb_classifier(SENTIMENT_CSV)


"""
4 Supervised Learning: Predict word sentiment

    Exercise 14: 
        
   Features that we have attempted:
       (1) first letter
       (2) first letter, last letter
       (3) first letter, second letter

Based on the development testing and error analysis,
    what else features can we use in order to improve the prediction? 

"""
