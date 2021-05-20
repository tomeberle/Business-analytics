import requests
import csv
import time
import datetime
from bs4 import BeautifulSoup
from Analysis import find_companies


def scrap_reddit(pagesToDo, thread):
    """ Scraps reddit, changing page and fetching post content 
    Input: pagesTodo (number of pages to scrape), thread (e.g. wallstreetbets)
    Returns: [[counter, date, _time, title, author, likes, comments], [...]]
    """
    # Using the old reddit as more simple
    url = "https://old.reddit.com/r/" + thread + "/"

    # Headers to mimic a browser visit
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Returns a requests.models.Response object
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Attribute to identify posts
    attrs = {'class': 'thing', 'data-domain': 'self.' + thread}

    counter = 1
    pageNb = 1
    output = []

    # Loop throuugh pages
    while (pageNb <= pagesToDo):
        # Loop through posts
        print('Scrapping Reddit page n°: ' + str(pageNb))
        for post in soup.find_all('div', attrs=attrs):
            # Identifying html items to scrape
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
                'div', attrs={'class': 'expando'}).text.strip()
            content = content.replace('\n', ' ')  # Removes breaklines
            content = " ".join(content.split())  # Cleaning unnecessary spaces

            # Writing post in CSV
            post_line = [counter, date, _time,
                         title, author, likes, comments, url, content]

            output.append(post_line)

            counter += 1

        # Next page
        next_button = soup.find("span", class_="next-button")
        next_page_link = next_button.find("a").attrs['href']
        time.sleep(2)
        page = requests.get(next_page_link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        pageNb += 1

    # Saving in CSV
    with open('output/reddit_output.csv', 'w', newline='') as f:
        head = csv.DictWriter(f, fieldnames=["counter", "date", "_time",
                                             "title", "author", "likes", "comments", "url", "content"])
        head.writeheader()
        writer = csv.writer(f)
        writer.writerows(output)

    # Returning output
    return output


# Fonction parameters
pagesToDo = 9
thread = "wallstreetbets"
content = scrap_reddit(pagesToDo, thread)
#content = find_companies(content)
