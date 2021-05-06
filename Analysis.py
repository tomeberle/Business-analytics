from cleanco import prepare_terms, basename
import csv


content = []


def load_csv(filename, subfolder):
    """ Loads CSV easily
    Input: filename, subfolder. E.g. assets/nasdaq.csv -->  filename='assets', subfolder='nasdaq.csv' 
    Output: data
    """
    with open(subfolder + '/' + filename + '.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def find_companies(content):
    """ Identifies stock market companies in scrapped content. 
    Input: [[counter, date, _time, title, author, likes, comments], [...]]
    Output: identical list with new 'company' column. 
    """
    nasdaq = load_csv(filename='nasdaq-listed_clean', subfolder='assets')
    test_string = "This text is about a company called credit suisse company and , of couse, is it working"

    # TODO: for loop to check if company is in: title, content, etc.
    for company in nasdaq:
        match_name = test_string.find(company[1])
        if match_name != -1:
            print('Found company: ' + str(company))

        match_symbol = test_string.find(company[0])
        if match_symbol != -1:
            print('Found company: ' + str(company))

    # TODO: create new column with tickers


content = load_csv(filename='reddit_output', subfolder='output')
find_companies(content)
