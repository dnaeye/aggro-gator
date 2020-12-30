# Web scraper for Pitchfork End-of-Year Top Releases
# Started 2020-12-28
# Updated 2020-12-28

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://pitchfork.com/features/lists-and-guides/best-albums-"

def get_page(year):
    url = base_url + str(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

user_year = input("Enter year to get: ")

page = get_page(user_year)

df = pd.DataFrame(columns=['rank', 'artist', 'album'])
i = 50
titles = page.find_all('h2')

for title in titles:
    rank = i
    item = title.text.split(":")
    artist = item[0].strip()
    album = item[1].strip()

    print('Rank ' + str(i), ":", artist, "-", album)
    df = df.append({'rank': i, 'artist': artist, 'album': album}, ignore_index=True)
    i -= 1

tl = []

paragraphs = page.find_all('p')

for paragraph in paragraphs:
    text = paragraph.text[0:500]
    words = text.split(" ")
    paragraph_len = len(words)

    period = text.rfind('.')
    question = text.rfind('?')
    exclamation = text.rfind('!')
    ends = [period, question, exclamation]
    max_end = max(ends) + 1

    if paragraph_len > 10 and max_end > 1:
        short_review = text[0:max_end]
        print(short_review + "\n")
        tl.append(short_review)
    else:
        pass

tf = pd.Series(tl)

# Need to manually exclude webpage intro and end paragraphs and additional para from reviews longer than 1 para
if user_year == '2020':
    rf = tf[3:-1]
    rf = rf.drop([8, 27, 50], axis=0)
    rf = rf.reset_index(drop=True)

df['review'] = rf
df = df.sort_values('rank', ascending=True)

filename = "pitchfork_" + user_year + ".csv"
df.to_csv(filename, index=False, encoding='utf-8-sig')