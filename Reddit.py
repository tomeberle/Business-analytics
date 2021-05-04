import requests
import csv
import time
from bs4 import BeautifulSoup


def scrap_reddit(pagesToDo, thread):
    """ Scraping of reddit, changing page and fetching post content 
    Data: counter, date, _time, title, author, likes, comments """
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

    # Loop throuugh pages
    while (pageNb <= pagesToDo):
        # Loop through posts
        print('Page n°: ' + str(pageNb))
        for post in soup.find_all('div', attrs=attrs):
            title = post.find('p', class_="title").text
            author = post.find('a', class_='author').text
            date = post.find('time')['datetime'][:10]
            _time = post.find('time')['datetime'][11:19]

            comments = post.find('a', class_='comments').text.split()[0]
            if comments == "comment":
                comments = 0

            likes = post.find("div", attrs={"class": "score likes"}).text
            if likes == "•":
                likes = "None"

            # Scrapping each post's content
            url = post.find('a', attrs={'data-event-action': "title"})['href']
            page = requests.get(
                "https://old.reddit.com" + url, headers=headers)
            post_soup = BeautifulSoup(page.text, 'html.parser')
            content = post_soup.find(
                'div', attrs={'class': 'expando'}).text
            print(content)

            post_line = [counter, date, _time,
                         title, author, likes, comments, url]
            print(post_line)
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
pagesToDo = 2
thread = "wallstreetbets"
scrap_reddit(pagesToDo, thread)
