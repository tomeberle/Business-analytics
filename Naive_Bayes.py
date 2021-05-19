import random
import nltk
import pandas as pd


def train_nb_classifier(df):
    """ This will train the classifier using the word sentiment feature set"""
    featureset = gen_featureset(df)

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
    print("Starting accuracy test...")
    b = nltk.classify.accuracy(classifier, training_set)
    print(b)
    acc = nltk.classify.accuracy(classifier, test_set)
    print("The accuracy of the model:", acc)

    return classifier


def gen_featureset(df):
    """ This function creates a feature set from the given dataframe"""
    featureset = list()
    for i in range(len(df)):
        feature_label = list()
        # Datetime,Text,Symbol,Sentiment,Movement
        # print(df.loc[i, "Symbol"], df.loc[i, "Sentiment"], df.loc[i, "Movement"], df.loc[i, "Datetime"], df.loc[i, "Text"])
        feature = {'sentiment': df.loc[i,
                                       "Sentiment"], 'datetime': df.loc[i, "Datetime"]}
        feature_label.append(feature)
        feature_label.append(df.loc[i, "Movement"])

        featureset.append(feature_label)
    return featureset
    for index in df.index:
        # feature_label is a list consisting of a case feature and its label
        print(df[index])
        feature_label = list()
        feature = name_feature(row[0])
        feature_label.append(feature)

        feature_label.append(row[1])

        featureset.append(feature_label)
    return featureset


df = pd.read_csv("output/twitter_sentiment_ceos.csv")
nb_classifier = train_nb_classifier(df)
