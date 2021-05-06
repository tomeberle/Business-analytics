from cleanco import prepare_terms, basename
import csv


content = []


def load_csv(filename, subfolder):
    with open(subfolder + '/' + filename + '.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def find_companies(content):
    """ Identifies stock market companies in scrapped content. 
    Input: [[counter, date, _time, title, author, likes, comments], [...]]
    Output: identical list with new 'company' column. 
    """
    nasdaq = load_csv(filename='nasdaq-listed', subfolder='assets')

    for company in nasdaq:
        print(company[1])
        terms = prepare_terms()
        company[1] = basename(
            company[1], terms, prefix=False, middle=False, suffix=True).lower()
        print(company[1])
        # TODO: for loop to check if company is in: title, content, etc.
        # TODO: create new column with tickers


content = load_csv(filename='reddit_output', subfolder='output')
find_companies(content)
