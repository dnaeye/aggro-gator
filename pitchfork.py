# Web scraper for Pitchfork End-of-Year Top Releases
# Started 2020-12-28

# Import libraries
import requests
from bs4 import BeautifulSoup
import re

base_url = "https://pitchfork.com/features/lists-and-guides/best-albums-"

def get_page(year):
    url = base_url + str(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

user_year = input("Enter year to get: ")

page = get_page(user_year)

titles = page.find_all('h2')

for title in titles:
    item = title.text.split(":")
    artist = item[0].strip()
    album = item[1].strip()

    print(artist)
    print(album + "\n")

paragraphs = page.find_all('p')

for paragraph in paragraphs:
    text = paragraph.text
    words = text.split(" ")
    paragraph_len = len(words)

    period = text.rfind('.')
    question = text.rfind('?')
    exclamation = text.rfind('!')
    ends = [period, question, exclamation]
    max_end = max(ends)

    if paragraph_len > 10 and max_end > 0:
        print(text)