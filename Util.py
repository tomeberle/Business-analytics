import re
import csv


def treat_companies(filename):
    """ Cleans the CSV file with company names for better recognition in other functions.
    Example: Credit Suisse AG -> credit suisse
    """
    with open('assets/' + filename + '.csv', newline='') as f:
        reader = csv.reader(f)
        nasdaq = list(reader)

    output = []

    bad_words = ['inc', 'ag', 'inc.', 'sa', 'corp',
                 'corporation', 'holding', 'plc', 'ltd', '.', ',']

    for company in nasdaq:
        symbol = company[0]
        name = [word for word in company[1].split() if word.lower()
                not in bad_words]
        name = ' '.join(name).lower()

        if name == '':
            name = full_name
        full_name = company[1]
        name_and_type = company[2]

        post_line = [symbol, name, full_name, name_and_type]

        output.append(post_line)

    # Saving in CSV
    with open('assets/' + filename + '_clean.csv', 'w', newline='') as f:
        head = csv.DictWriter(f, fieldnames=["symbol", "name", "full_name",
                                             "name_and_type"])
        head.writeheader()
        writer = csv.writer(f)
        writer.writerows(output)


treat_companies('nasdaq-listed')
