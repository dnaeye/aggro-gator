# Create HTML table from CSV file
# Started 2021-01-01
# Updated 2021-01-01

# Import libraries
import pandas as pd

# Config to show all dataframe columns
pd.set_option('display.max_columns', None)

# Get user input
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

filename = site + "_" + year + "_album-ids.csv"

# Import album data
df = pd.read_csv("data/" + filename)
try:
    df = df.drop(columns='genre')
except:
    pass

# Create hyperlink to album review
df['album'] = "<a href='" + df['review_url'] + "' target='_blank'>" + df['album'] + "</a>"

df = df.drop(columns='review_url')

# Create webpage header and footer content
html_head = '''
<html>
    <head>
        <title>''' + site.title() + ''''s Top Albums of ''' + year + '''</title>
    </head>
    <link rel="stylesheet" href="css/style.css"/>
    
    <body>
        <div class="container">
            <div class="centered">
                <h1>''' + site.title() + ''''s Top Albums of ''' + year + '''</h1>
            </div>
        </div>
    
    <script type="text/javascript">
    function getSpotfiyPlayer(album_id) {
        var player_prefix = "<iframe src=\\\'https://open.spotify.com/embed/album/";
        var player_suffix = "\\\' width=\\\"300\\\" height=\\\"80\\\" frameborder=\\\"0\\\" allowtransparency=\\\"true\\\" allow=\\\"encrypted-media\\\"></iframe>";
        document.getElementById("player").innerHTML = player_prefix.concat(album_id, player_suffix);
    }
    </script>
'''

html_end = '''
    </body>
    <footer>
        <p id="player"></p>
    </footer>
</html>
'''

# Output HTML code to file
outfile = site + "-" + year + ".html"

with open("html/" + outfile, 'w', encoding="utf-8-sig") as f:
    f.write(html_head)
    f.write('<table class="center">')
    f.write('<col style = "width:5%">')
    f.write('<col style = "width:15%">')
    f.write('<col style = "width:15%">')
    f.write('<col style = "width:30%">')
    f.write('<col style = "width:10%">')
    f.write('<thead>')
    f.write('<tr>')
    for header in df.columns:
        if header == 'album_id':
            f.write('<th>' + "Play Album" + '</th>')
        else:
            f.write('<th>' + str(header).title() + '</th>')
    f.write('</tr>')
    f.write('</thead>')

    for i in range(len(df)):
        f.write('<tr>')
        for col in df.columns:
            value = df.iloc[i][col]
            if col == 'rank':
                f.write('<td align="center">' + str(value) + '</td>')
            elif col == 'album_id':
                if value == 'Not available':
                    f.write('<td align="center">' + str(value) + '</td>')
                else:
                    f.write('<td align="center"><button onclick="getSpotfiyPlayer(\'' \
                            + value + '\')">Load Player</button></td>')
            else:
                f.write('<td>' + str(value) + '</td>')
        f.write('\t\t</tr>')
    f.write('\t</table>')
    f.write(html_end)




