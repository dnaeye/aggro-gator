# Web scraper for Boomkat End-of-Year Top Releases
# Started 2020-12-28
# Updated 2020-12-28

# Import libraries
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url_2019 = "https://boomkat.com/charts/boomkat-end-of-year-charts-2019/940"
url_2020 = "https://boomkat.com/charts/boomkat-end-of-year-charts-2020/1234"

def get_page(year):
    if year == "2019":
        page = requests.get(url_2019)
    elif year == "2020":
        page = requests.get(url_2020)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

user_year = input("Enter year to get: ")

page = get_page(user_year)

results = page.find_all(class_='chart-item')

df = pd.DataFrame(columns=['rank', 'artist', 'album', 'genre', 'review'])
i = 1

for result in results:
    try:
        rank = i
        release = result.find('div', class_='chart-item-content-mobile show-for-small-only')
        artist = str(release.find(class_='release__artist').text.strip()).title()
        #if len(re.search(r'^.{2}\s', artist).group()) == 3:
        #    prefix = re.search(r'^.{2}\s', artist).group().upper()
        #    name = artist.split(" ")[1]
        #    artist = prefix + name
        #else:
        #    pass
        album = release.find(class_='release__title').text.strip()
        try:
            genre = release.find(class_='release__genre').text.strip()
        except:
            genre = "Unknown"
        try:
            review = result.find('div', class_='chart-item-review').text.strip()[0:500] \
                .replace("\r", "").replace("\n\n", " ")
            period = review.rfind('.')
            question = review.rfind('?')
            exclamation = review.rfind('!')
            ends = [period, question, exclamation]
            if max(ends) < 1:
                space = review.rfind(' ')
                max_end = space
            else:
                max_end = max(ends) + 1
            short_review = review[0:max_end]
        except:
            short_review = "No review available"

        df = df.append({'rank': rank, 'artist': artist, 'album': album, 'genre': genre, 'review': short_review}, ignore_index=True)
        print('Rank ' + str(i) + " : " + artist, "-", album, ";", genre, "; Review: ", short_review)
        i += 1

    except:
        print("Error getting chart item")

filename = "boomkat_" + user_year + ".csv"
df.to_csv(filename, index=False, encoding='utf-8-sig')