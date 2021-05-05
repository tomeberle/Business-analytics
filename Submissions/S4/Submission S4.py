import random
import nltk
import csv

SENTIMENT_CSV = "/Users/tomeberle/Downloads/word_sentiment.csv"

""" 
4 Supervised Learning: Predict word sentiment 
     
    Exercise 11: Improvement - More features, including the first and last letter

"""
#  Adding first letters and last letters.
## Result: 65% accuracy


def word_sentiment_feature(word):
    """ Given a word, it returns a dictonary of the first letter of the word"""
    first_l = word[0]
    last_l = word[-1]
    # features is of the dictionary type having only one feature
    features = {"first letter": first_l, "last letter": last_l}
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
    classifier.show_most_informative_features(20)

    acc = nltk.classify.accuracy(classifier, test_set)
    print("The accuracy of the model:", acc)

    return classifier


nb_classifier = train_nb_classifier(SENTIMENT_CSV)

i_word = input("Enter a word: ").lower()
wordfeatures = word_sentiment_feature(i_word)
print('feature of the word:', wordfeatures)

sentiment = nb_classifier.classify(wordfeatures)
print('Predicted sentiment:', sentiment)


""" 
4 Supervised Learning: Predict word sentiment 
     
    Exercise 12: Improvement - More features, including the first two letters
"""
#  Adding first two letters, vowels and consonants to the model.
## Result: 65% accuracy


def count_vowels(word):
    vowels = 0
    consonants = 0

    for i in word:
        if(i == 'a' or i == 'e' or i == 'i' or i == 'o' or i == 'u'):
            vowels = vowels + 1
        else:
            consonants = consonants + 1
    return vowels, consonants


def word_sentiment_feature(word):
    """ Given a word, it returns a dictonary of the first letter of the word"""
    first_l = word[:2]
    last_l = word[-1]
    vowels = count_vowels(word)[0]
    consonants = count_vowels(word)[1]
    # features is of the dictionary type having only one feature
    features = {"first two letter": first_l, "last letter": last_l,
                "vowels": vowels, "consonants": consonants}
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
    classifier.show_most_informative_features(20)

    acc = nltk.classify.accuracy(classifier, test_set)
    print("The accuracy of the model:", acc)

    return classifier


nb_classifier = train_nb_classifier(SENTIMENT_CSV)

i_word = input("Enter a word: ").lower()
wordfeatures = word_sentiment_feature(i_word)
print('feature of the word:', wordfeatures)

sentiment = nb_classifier.classify(wordfeatures)
print('Predicted sentiment:', sentiment)


""" 
4 Supervised Learning: Predict the gender of a name 
     
    Exercise 13 (optional): Identify features and use the naive classifer to predict 
"""
#  Features: first and last letter of the name
#  Precision: 80%


NAME_CSV = "/gender.csv"


def name_feature(word):
    """ Given a name, it returns a dictonary of the first and last letter of the name"""
    first_l = word[0]
    last_l = word[-1]
    # features is of the dictionary type having only one feature
    features = {"first letter": first_l, "last letter": last_l}
    return features


def gen_featureset(name_csv):
    """ This function creates a feature set for the gender.csv file"""
    featureset = list()
    with open(name_csv, 'rt', encoding='utf-8') as csvobj:
        ws_data = csv.reader(csvobj)
        for row in ws_data:
            # feature_label is a list consisting of a case feature and its label
            feature_label = list()
            feature = name_feature(row[0])
            feature_label.append(feature)

            feature_label.append(row[1])

            featureset.append(feature_label)
    return featureset


def train_nb_classifier(name_csv):
    """ This will train the classifier using the word sentiment feature set"""
    featureset = gen_featureset(name_csv)
    print(featureset)
    # shuffle the corpus to overcome the issue of alphebetic ordering of the word
    # so that the training set and test set share the same distribution
    random.shuffle(featureset)

    num_ts = int(len(featureset)*0.8)
    # the first 80% as training set, the latter 20% as test set
    training_set, test_set = featureset[:num_ts], featureset[num_ts:]
    # training_set = featureset[:num_ts]
    # test_set = featureset[num_ts:]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    classifier.show_most_informative_features(20)

    acc = nltk.classify.accuracy(classifier, test_set)
    print("The accuracy of the model:", acc)

    return classifier


nb_classifier = train_nb_classifier(NAME_CSV)

i_word = input("Enter a name: ").lower()
wordfeatures = name_feature(i_word)
print('feature of the name:', wordfeatures)

sentiment = nb_classifier.classify(wordfeatures)
print('Predicted sentiment:', sentiment)
