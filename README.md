# Aggro-gator

Pitchfork has risen to become one of the most prominent music websites since its inception in 1995. It's well known for its album reviews and annual lists of top albums. While Pitchfork became popular for its coverage of indie rock, Boomkat is the leading online store for underground electronic music, particularly of the experimental variety, and similarly publishes an annual top album list.

Aggro-gator creates webpages that enable users to listen to the albums on these annual lists using Spotify in one place without having to search for them individually on Spotify.

## Mechanics

Aggro-gator is currently a collection of scripts that scrape the Pitchfork or Boomkat top album webpages and creates a webpage that provides an abbreviated version of the reviews from the respective sites along with an embedded Spotify player for each album.

### 1. Scrape top album webpage
pitchfork.py
boomkat.py

### 2. Create embeddable Spotify player
spotify.py

### 3. Create webpage using scraped album info and Spotify player
html_table_creator.py