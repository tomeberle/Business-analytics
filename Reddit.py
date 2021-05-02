import requests
import csv
import time
from bs4 import BeautifulSoup


def scrap_reddit(pagesToDo, thread):
    # Using the old reddit as more simple
    url = "https://old.reddit.com/r/" + thread + "/"

    # Headers to mimic a browser visit
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Returns a requests.models.Response object
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    attrs = {'class': 'thing', 'data-domain': 'self.' + thread}

    counter = 1
    pageNb = 1
    while (pageNb <= pagesToDo):
        # Loop through posts
        print('Page n°: ' + str(pageNb))
        for post in soup.find_all('div', attrs=attrs):
            title = post.find('p', class_="title").text
            author = post.find('a', class_='author').text

            comments = post.find('a', class_='comments').text.split()[0]
            if comments == "comment":
                comments = 0

            likes = post.find("div", attrs={"class": "score likes"}).text
            if likes == "•":
                likes = "None"

            print('Scrapping n' + str(counter) + ': ' + title)

            post_line = [counter, title, author, likes, comments]

            # Writing post in CSV
            # TODO: Add columns
            # TODO: Read csv file to compare
            with open('reddit_output.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(post_line)

            counter += 1

        # Next page
        next_button = soup.find("span", class_="next-button")
        next_page_link = next_button.find("a").attrs['href']
        time.sleep(2)
        page = requests.get(next_page_link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        pageNb += 1


# Fonction parameters
pagesToDo = 3
thread = "wallstreetbets"
scrap_reddit(pagesToDo, thread)
