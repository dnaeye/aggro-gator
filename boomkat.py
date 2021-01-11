# Web scraper for Boomkat End-of-Year Top Releases
# Started 2020-12-28
# Updated 2021-01-03

# Import libraries
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import unidecode

# URLs for Boomkat End of Year Charts
url_2015 = "https://boomkat.com/charts/2015/122"
url_2016 = "https://boomkat.com/charts/2016/306"
url_2017 = "https://boomkat.com/charts/2017/558"
url_2018 = "https://boomkat.com/charts/boomkat-end-of-year-charts-2018/677"
url_2019 = "https://boomkat.com/charts/boomkat-end-of-year-charts-2019/940"
url_2020 = "https://boomkat.com/charts/boomkat-end-of-year-charts-2020/1234"

# Scrape Boomkat webpage
def get_page(year):
    page_url = eval("url_" + user_year)
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

# Get user-desired year
user_year = input("Enter year to get: ")

# Get Boomkat webpage for user year
page = get_page(user_year)

# Get album content from webpage
results = page.find_all(class_='chart-item')

# Initialize empty dataframe to store parsed data
df = pd.DataFrame(columns=['rank', 'artist', 'album', 'genre', 'review_url', 'review'])
i = 1

# Parse artist, album, genre, review data
for result in results:
    try:
        rank = i
        release = result.find('div', class_='chart-item-content-mobile show-for-small-only')
        artist = str(release.find(class_='release__artist').text.strip()).title()
        album = release.find(class_='release__title').text.strip()

        # Create Boomkat review URL
        try:
            review_url = "https://boomkat.com" + \
                         result.find('div', class_='chart-item-link chart-item-link--fulldetails')\
                             .find('a', href=True)['href']
        except:
            review_url = "https://boomkat.com"

        # Get album images
        # try:
        #     image = str(result.find(class_='chart-item-image').find('img'))
        #     image_url = re.findall(r'src="(.*)"\s', image)[0]
        #     image_ext = os.path.splitext(image_url)[1]
        #     filename = artist + " - " + album + image_ext
        #
        #     image_r = requests.get(image_url, stream=True)
        #     if image_r.status_code == 200:
        #         image_r.raw.decode_content = True
        #         if not os.path.exists('images'):
        #             os.makedirs('images')
        #         with open('images/' + filename, 'wb') as f:
        #             shutil.copyfileobj(image_r.raw, f)
        #         print('Successfully downloaded: ', filename)
        #     else:
        #         print('Image could not be retrieved.')
        # except:
        #     pass

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

        df = df.append({'rank': rank, 'artist': artist, 'album': album, 'genre': genre,
                        'review_url': review_url, 'review': short_review}, ignore_index=True)
        print('Rank ' + str(i) + " : " + artist, "-", album, ";", genre, "; review_url", review_url,
              "; Review: ", short_review)
        i += 1

    except:
        print("Error getting chart item")

# Output data to file
filename = "boomkat_" + user_year + ".csv"
if not os.path.exists('data'):
    os.makedirs('data')
df.to_csv("data/" + filename, index=False, encoding='utf-8-sig')