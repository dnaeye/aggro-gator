# Search for Spotify ID for given album and create HTML code for embedded player
# Started 2020-12-29
# Updated 2020-12-29

# Import libraries
import pandas as pd
import requests
import json
from spotify_secrets import *  # Simple .py file declaring client_id and client_secret variables

# Authorization
token_endpoint = "https://accounts.spotify.com/api/token"

auth_response = requests.post(token_endpoint, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
})

auth_response_data = auth_response.json()

token = auth_response_data['access_token']

# Search
endpoint = "https://api.spotify.com/v1/search"

# Import data
class import_data:
    def __init__(self):
        self.site = input("Enter site code (Pitchfork=p, Boomkat=b): ")
        self.year = input("Enter year: ")

def get_input():
    return import_data()

user_input = get_input()

if user_input.site == 'p':
    site = 'pitchfork'
elif user_input.site  == 'b':
    site = 'boomkat'
else:
    print('Enter appropriate code.')
year = user_input.year

filename = site + "_" + year + ".csv"

df = pd.read_csv(filename)

html = []

for i in range(len(df)):
    artist = df.iloc[i]['artist'].replace(" / ", ", ")
    if 'various' in artist.lower():
        artist_param = ''
    else:
        artist_param = ' artist:' + artist
    album = df.iloc[i]['album']
    query = 'album:' + album + artist_param

    headers = {'Authorization': 'Bearer {token}'.format(token=token)}
    params = {'q': query, 'type': 'album', 'market': 'US'}

    data = requests.get(
        endpoint,
        headers=headers,
        params=params
    )

    print('artist:', artist, 'album', album, data.status_code)

    if data.status_code == 200:
        if len(data.json()['albums']['items']) > 0:
            album_data = data.json()
            album_id = album_data['albums']['items'][0]['id']

            # Create embeddable player HTML code
            # See https://developer.spotify.com/documentation/widgets/generate/embed/
            width = '"300"'
            height = '"80"'
            base = '<iframe src="https://open.spotify.com/embed/album/'
            frame_border = '"0"'
            allow_transparency = '"true"'
            allow = '"encrypted-media'
            code = base + album_id + '"' + ' width=' + width + ' height=' + height + ' frameborder=' + frame_border \
                + ' allowtransparency=' + allow_transparency + ' allow=' + allow + '"></iframe>'
        else:
            code = "Not available"
    else:
        code = 'Not available'

    html.append(code)

df['html'] = pd.Series(html)

df.to_csv(site + "_" + year + "_html.csv", index=False)