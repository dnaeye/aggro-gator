# Web scraper for Pitchfork End-of-Year Top Releases
# Started 2020-12-28
# Updated 2021-01-03

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unidecode
import os

# Base URL for Pitchfork Best Albums webpages
base_url = "https://pitchfork.com/features/lists-and-guides/best-albums-"

# Scrape Pitchfork webpage
def get_page(year):
    url = base_url + str(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

# Get user-desired year
user_year = input("Enter year to get: ")

# Get Pitchfork webpage for user year
page = get_page(user_year)

# Initialize empty dataframe to store parsed data
df = pd.DataFrame(columns=['rank', 'artist', 'album', 'review_url'])
i = 50

# Get artist and album titles from webpage
titles = page.find_all('h2')

# Parse artist and album titles and create Pitchfork review URL
for title in titles:
    rank = i
    item = title.text.split(":")
    artist = item[0].strip()
    album = item[1].strip()

    artist_url = re.sub(r"[^\w\s\-]*", "", re.sub("\s", "-", artist.lower().replace(" / ", " ")))
    artist_url = unidecode.unidecode(artist_url)
    album_url = re.sub(r"[^\w\s\-]*", "", re.sub("\s", "-", album.lower().replace(" / ", " ")))
    album_url = unidecode.unidecode(album_url)
    review_url = "https://pitchfork.com/reviews/albums/" + artist_url + "-" + album_url + "/"
    r = requests.get(review_url)
    if r.status_code != 200:
        review_url = 'Not available'
    else:
        pass

    print('Rank ' + str(i), ":", artist, "-", album)
    df = df.append({'rank': i, 'artist': artist, 'album': album, 'review_url': review_url}, ignore_index=True)
    i -= 1

# Initialize empty list to store album reviews
tl = []

# Get album review content from webpage
paragraphs = page.find_all('p')

# Parse album reviews
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
        #print(short_review + "\n")
        tl.append(short_review)
    else:
        pass

# Convert reviews list to series
tf = pd.Series(tl)

# Need to manually exclude webpage intro and end paragraphs and additional para from reviews longer than 1 para
if user_year == '2020':
    rf = tf[3:-1]
    rf = rf.drop([8, 27, 50], axis=0)
    rf = rf.reset_index(drop=True)
elif user_year == '2019':
    rf = tf[4:-4]
    xword = ['Notably, uknowhatimsayin¿', 'Designer is', 'These echoes', 'On "Hollywood,"',
             'Like the', 'The record', 'Seasoned experts', 'Surveying a', 'Giannascoli’s tendency',
             'The songs', 'Take “Writing,”', 'But it’s', 'For all']
    rf = rf[~rf.apply(lambda x: x.split()[0] + " " + x.split()[1]).isin(xword)]

# Add review column to dataframe with reviews series
df['review'] = rf.reset_index(drop=True)

# Sort albums from #1 to #50 instead of Pitchfork's default #50 to #1
df = df.sort_values('rank', ascending=True)

# Output data to file
filename = "pitchfork_" + user_year + ".csv"
if not os.path.exists('data'):
    os.makedirs('data')
df.to_csv("data/" + filename, index=False, encoding='utf-8-sig')